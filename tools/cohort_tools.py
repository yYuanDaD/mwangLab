"""Agent A cohort orchestrator (Phase 3).

Turns a single KEYWORD into 13 SEA-CDM CSVs populated from the top hits:

    search_papers(keyword)
      -> for each ranked hit:
           fetch_paper_text(search_index=N)         # handle-based, no PMCID typo
           classify each GSE own-vs-cited            # pick the paper's OWN data
           extract_sea_cdm_tables(study_id, text)    # 9 text tables, per-field source
           append rows to the shared SEA-CDM cohort CSVs
      -> (optional) run_batch_geo_pipeline(own_GSEs) # fills analysis/results rows

One paper spans MULTIPLE rows; FK columns (study_id / experiment_id / group_id ...)
link rows across the CSVs. Deterministic Python control flow (not agent-prompt
driven) so the cohort run is reproducible, cheap, and re-runnable — matching the
project's "programmatic guardrails" philosophy. The interactive single-paper path
still goes through the agent + the @tool wrappers.

study_id rule (the PK every row hangs off):
    - the paper's OWN GEO accession when one is clearly stated ("...are deposited...")
    - else the PMCID  (so a paper with no downloadable GSE STILL contributes its
      9 text tables — the demo is "info from keyword-found papers", not only papers
      that happen to have a re-analyzable matrix).
Analysis (DESeq2/limma/GSEA) is run ONLY for strictly-own GSEs, and only when
with_analysis=True (default off — text tables first, fast and stable).
"""

import csv
import glob
import json
import os
import re
from dataclasses import asdict, dataclass
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv

# Also supports standalone and test invocation outside main.py.
load_dotenv()

import tools.paper_tools as pt
from tools.paper_tools import (
    search_papers, fetch_paper_text,
    _extract_accessions, _context_for, _normalize_pmcid,
)
from tools.seacdm_tools import (
    extract_tables_from_text, append_tables_to_csvs, build_reported_findings,
    build_reconciliation_rows,
)
from tools.sea_cdm_schema import SEA_TABLES, csv_columns
from tools.geo_tools import download_geo_data


_VALID_ORGANISMS = {"": "", "human": "Human", "mouse": "Mouse"}
_VALID_RAW_DA_METHODS = {"deseq2", "edger", "limma-voom", "auto", "auto-llm", "all"}


@dataclass(frozen=True)
class AgentACohortRequest:
    """Normalized, deterministic input consumed by the cohort orchestrator.

    The interactive agent supplies user intent once. Python owns defaults, bounds, label
    generation and keyword cleanup so later stages never depend on the model remembering or
    reformatting intermediate values.
    """

    keyword: str
    max_papers: int
    organism: str
    with_analysis: bool
    treatment_keywords: list[str]
    control_keywords: list[str]
    raw_da_method: str
    require_pdf: bool
    min_year: int
    search_pool: int
    run_label: str
    output_base: str
    max_chars: int
    extract_findings: bool
    require_exercise_relevance: bool


def _clean_keywords(values) -> list[str]:
    """Return non-empty, case-insensitively unique keywords in stable input order."""
    out, seen = [], set()
    for value in values or []:
        text = str(value).strip()
        key = text.casefold()
        if text and key not in seen:
            seen.add(key)
            out.append(text)
    return out


def normalize_agent_a_request(**kwargs) -> AgentACohortRequest:
    """Validate and normalize all model-facing arguments before any network or file work."""
    keyword = str(kwargs.get("keyword") or "").strip()
    if not keyword:
        raise ValueError("keyword must be a non-empty search query")

    organism_raw = str(kwargs.get("organism") or "").strip().casefold()
    if organism_raw not in _VALID_ORGANISMS:
        raise ValueError("organism must be 'Human', 'Mouse', or empty")

    method = str(kwargs.get("raw_da_method") or "deseq2").strip().lower()
    if method not in _VALID_RAW_DA_METHODS:
        allowed = ", ".join(sorted(_VALID_RAW_DA_METHODS))
        raise ValueError(f"raw_da_method must be one of: {allowed}")

    treatment = _clean_keywords(kwargs.get("treatment_keywords"))
    control = _clean_keywords(kwargs.get("control_keywords"))
    overlap = {x.casefold() for x in treatment} & {x.casefold() for x in control}
    if overlap:
        raise ValueError(f"treatment/control keywords overlap: {sorted(overlap)}")

    raw_label = str(kwargs.get("run_label") or keyword).strip()
    label = re.sub(r"_+", "_", re.sub(r"[^A-Za-z0-9.-]+", "_", raw_label)).strip("_.-")[:40]
    if not label:
        label = "agent_a"

    max_papers = max(1, min(int(kwargs.get("max_papers", 5)), 50))
    search_pool = max(max_papers, min(int(kwargs.get("search_pool", 30)), 100))
    max_chars = max(5000, min(int(kwargs.get("max_chars", 100000)), 500000))
    min_year = max(0, int(kwargs.get("min_year", 0)))

    return AgentACohortRequest(
        keyword=keyword,
        max_papers=max_papers,
        organism=_VALID_ORGANISMS[organism_raw],
        with_analysis=bool(kwargs.get("with_analysis", False)),
        treatment_keywords=treatment,
        control_keywords=control,
        raw_da_method=method,
        require_pdf=bool(kwargs.get("require_pdf", True)),
        min_year=min_year,
        search_pool=search_pool,
        run_label=label,
        output_base=str(kwargs.get("output_base") or "./output"),
        max_chars=max_chars,
        extract_findings=bool(kwargs.get("extract_findings", True)),
        require_exercise_relevance=bool(kwargs.get("require_exercise_relevance", True)),
    )


def _write_workflow_state(cohort_dir: str, request: AgentACohortRequest, state: str, **details) -> str:
    """Persist one machine-readable checkpoint; Python, not the agent, carries workflow state."""
    os.makedirs(cohort_dir, exist_ok=True)
    path = os.path.join(cohort_dir, "workflow_state.json")
    payload = {
        "state": state,
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        "request": asdict(request),
        "details": details,
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
    return path


# ---- own-vs-cited GSE classification --------------------------------------------------
# The regex finds every GSE in a paper; only some are the paper's OWN deposited data.
# We score the text window around each accession for deposition vs reuse language.
# Deliberately exclude "accession number" / "under accession" / "raw data": those phrases
# occur in BOTH deposition AND citation sentences ("downloaded from ... accession numbers ...")
# so they don't discriminate. Keep only deposition verbs and "this study" ownership markers.
_OWN_SIGNALS = (
    "deposited", "have been deposited", "are deposited", "was deposited", "were deposited",
    "deposited in", "deposited at", "deposited to", "deposited under", "submitted to",
    "we deposited", "we have deposited", "data are available", "data have been deposited",
    "generated in this study", "generated for this study", "reported in this study",
    "of this study", "in the present study",
)
_CITED_SIGNALS = (
    "downloaded from", "obtained from", "publicly available", "publicly accessible",
    "previously published", "reanalyz", "re-analyz", "retrieved from", "we used data",
    "dataset from", "from a previous", "reused", "extracted from", "acquired from",
    "data from", "published dataset",
)

_EXERCISE_RELEVANCE_PATTERNS = tuple(
    re.compile(p, re.I)
    for p in (
        r"\bacute\s+exercise\b",
        r"\bchronic\s+exercise\b",
        r"\bexercise[-\s]+training\b",
        r"\bexercise[-\s]+intervention\b",
        r"\bexercise[-\s]+program\b",
        r"\bexercise[-\s]+protocol\b",
        r"\bexercise[-\s]+bout\b",
        r"\bexercise[-\s]+regimen\b",
        r"\bexercise[-\s]+induced\b",
        r"\bpre[-\s]+exercise\b",
        r"\bpost[-\s]+exercise\b",
        r"\btreadmill\b",
        r"\bwheel\s+running\b",
        r"\bvoluntary\s+wheel\b",
        r"\bendurance\s+(exercise|training)\b",
        r"\bresistance\s+(exercise|training)\b",
        r"\baerobic\s+(exercise|training)\b",
        r"\bsprint\s+(exercise|training)\b",
        r"\bhigh[-\s]+intensity\s+interval\b",
        r"\bhiit\b",
        r"\bswimming\s+exercise\b",
        r"\bforced\s+swim",
        r"\bcontractile\s+activity\b",
        r"\bsedentary\s+(control|controls|group|mice|rats|subjects|participants)\b",
        r"\b(exercised|trained)\s+(mice|rats|animals|subjects|participants|humans)\b",
    )
)


def _is_exercise_relevant_search_hit(row: dict) -> tuple[bool, str]:
    """Conservative paper-level gate for exercise cohorts.

    Search APIs can rank papers that only mention generic "training" (model training / training
    dataset) or "acute" (acute leukemia). Do not spend LLM extraction or populate exercise/gene
    tables unless title/abstract clearly describe an exercise intervention/exposure context.
    """
    title = row.get("title") or ""
    abstract = row.get("abstract") or ""
    hay = f"{title}\n{abstract}"
    for pat in _EXERCISE_RELEVANCE_PATTERNS:
        m = pat.search(hay)
        if m:
            return True, f"matched {m.group(0)!r}"
    return False, "no explicit exercise intervention/exposure phrase in title/abstract"


def classify_gse_ownership(text: str, gse: str, width: int = 170):
    """Return (ownership, score, snippet) for one GSE.

    ownership in {'own','cited','ambiguous'}. The snippet is recorded for human audit
    regardless — like the project's existing GSE snippet_verified cross-check."""
    snippet = _context_for(text, gse, width=width)
    low = snippet.lower()
    own = sum(low.count(s) for s in _OWN_SIGNALS)
    cited = sum(low.count(s) for s in _CITED_SIGNALS)
    if own > cited and own > 0:
        return "own", own, snippet
    if cited > own and cited > 0:
        return "cited", cited, snippet
    return "ambiguous", 0, snippet


def choose_own_gse(text: str):
    """Pick the paper's OWN GSE from its full text. Returns (chosen_gse, ownership_tag,
    classifications) where classifications is a list of dicts for every GSE found.

    ownership_tag: 'own' (clear deposition language), 'own_assumed_single' (the only GSE
    and not clearly a citation), or '' (no own GSE — caller keys rows by PMCID instead)."""
    accs = _extract_accessions(text)
    gses = accs.get("GEO_series", [])
    classifications = []
    for g in gses:
        own, score, snip = classify_gse_ownership(text, g)
        classifications.append({"gse": g, "ownership": own, "score": score, "snippet": snip})

    owned = [c for c in classifications if c["ownership"] == "own"]
    if owned:
        best = max(owned, key=lambda c: c["score"])
        return best["gse"], "own", classifications
    # No clearly-own GSE. If there is exactly ONE GSE and it isn't clearly a citation,
    # assume it is the paper's own (study_id only; analysis still gated on strict 'own').
    if len(classifications) == 1 and classifications[0]["ownership"] != "cited":
        return classifications[0]["gse"], "own_assumed_single", classifications
    return "", "", classifications


# ---- cohort CSV scaffolding -----------------------------------------------------------

def init_cohort_csvs(csv_dir: str) -> None:
    """(Re)create header-only CSVs for every SEA-CDM table so the demo shows the full
    schema even where a table ends up with 0 rows. Always truncates so re-running a cohort
    with the same run_label starts from a clean slate (no stale rows from a prior run).
    ontology is written as an explicit stub."""
    os.makedirs(csv_dir, exist_ok=True)
    for name, entry in SEA_TABLES.items():
        path = os.path.join(csv_dir, entry["csv"])
        cols = csv_columns(name)
        if not cols:
            # ontology — deferred to Agent B (ontology mapping). Leave a self-documenting stub.
            with open(path, "w", encoding="utf-8") as f:
                f.write("# ontology table is deferred to Agent B (ontology mapping); Agent A emits no rows\n")
            continue
        # always overwrite the header (truncate any prior run's rows)
        with open(path, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=cols).writeheader()


# ---- analysis / results rows from a batch run -----------------------------------------

_INPUT_DATA_DESC = {
    "deseq2": "Raw RNA-seq integer counts (per-gene, per-sample matrix)",
    "limma": "Log-scale expression matrix (log2 CPM / FPKM / TPM)",
    "limma-voom": "Raw RNA-seq integer counts (voom-transformed)",
    "edger": "Raw RNA-seq integer counts (edgeR NB GLM)",
}


def _order(table: str, row: dict) -> dict:
    return {c: row.get(c) for c in csv_columns(table)}


def build_pipeline_rows(study_id: str, summary_row: dict, batch_study_dir: str) -> dict:
    """Build {'analysis': [...], 'results': [...]} rows from one study's batch artifacts.

    Handles raw_da_method='all': per-method DEG files (DEG_results_<t>_vs_<c>__<method>.csv) each
    become a results row tagged with their method, the per-gene comparison table
    (..__DA_compare.csv) becomes its own row, and the analysis row records the consensus n_deg plus
    the per-method / log2FC-concordance summary in its name + input_data."""
    da_method = (summary_row or {}).get("da_method") or None
    is_all = bool(da_method and da_method.startswith("all"))
    gsea_csvs = sorted(glob.glob(os.path.join(batch_study_dir, "*_GSEA_*.csv")))
    # Exclude enrichment files whose names inherit the DEG prefix.
    _DERIVED = ("_GSEA_", "_GO_", "_KEGG_", "_Reactome_", "_MSigDB_")
    all_deg = sorted(p for p in glob.glob(os.path.join(batch_study_dir, "DEG_results_*.csv"))
                     if not any(tok in os.path.basename(p) for tok in _DERIVED))
    # In 'all' mode the dir also holds per-gene comparison tables (..__DA_compare.csv); split them
    # out so they aren't mislabelled as plain DEG outputs.
    compare_csvs = [p for p in all_deg if "__DA_compare" in os.path.basename(p)]
    deg_csvs = [p for p in all_deg if "__DA_compare" not in os.path.basename(p)]

    def _method_of(path):
        """The DA method a DEG file came from: the '__<method>' suffix in 'all' mode, else da_method."""
        base = os.path.basename(path)[:-4]  # strip '.csv'
        if "__" in base:
            return base.rsplit("__", 1)[1]
        return da_method

    input_desc = _INPUT_DATA_DESC.get(da_method)
    if input_desc is None and is_all:
        input_desc = "Raw RNA-seq integer counts (analyzed by DESeq2 + edgeR + limma-voom)"
    name = "Differential expression analysis"
    if is_all:
        per = (summary_row or {}).get("da_per_method_deg")
        r = (summary_row or {}).get("da_logfc_r")
        name = ("Differential expression — multi-method consensus (DESeq2 + edgeR + limma-voom; "
                "n_deg = genes significant in >=2 methods"
                + (f"; per-method {per}" if per else "")
                + (f"; mean log2FC r={r}" if r is not None else "") + ")")
    if gsea_csvs:
        name += " + GSEA (Hallmark)"

    analysis = _order("analysis", {
        "analysis_id": f"{study_id}_analysis1",
        "study_id": study_id,
        "group_id": None,
        "documentation_id": None,
        "input_data": input_desc,
        "input_data_id": study_id,
        "file_access": f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={study_id}",
        "analysis_name": name,
        "da_method": da_method,
        "n_deg": (summary_row or {}).get("n_deg"),
        "reference_source": "GEO",
        "reference_source_id": study_id,
    })

    results = []
    n = 0
    for p in deg_csvs:
        n += 1
        m = _method_of(p)
        results.append(_order("results", {
            "results_id": f"{study_id}_res{n}",
            "experiment_id": f"{study_id}_exp1",
            "analysis_type": f"differential expression ({m})" if m else "differential expression",
            "original_assay_type": "experimental assay",
            "datatype": "Spreadsheet",
            "file_access": p,
            "file_type": "csv",
        }))
    for p in compare_csvs:
        n += 1
        results.append(_order("results", {
            "results_id": f"{study_id}_res{n}",
            "experiment_id": f"{study_id}_exp1",
            "analysis_type": "multi-method DA comparison (per-gene log2FC/padj + >=2-method consensus)",
            "original_assay_type": "experimental assay",
            "datatype": "Spreadsheet",
            "file_access": p,
            "file_type": "csv",
        }))
    for p in gsea_csvs:
        n += 1
        results.append(_order("results", {
            "results_id": f"{study_id}_res{n}",
            "experiment_id": f"{study_id}_exp1",
            "analysis_type": "GSEA (Hallmark)",
            "original_assay_type": "experimental assay",
            "datatype": "Spreadsheet",
            "file_access": p,
            "file_type": "csv",
        }))
    return {"analysis": [analysis], "results": results}


# ---- the orchestrator -----------------------------------------------------------------

def run_agent_a_cohort(
    keyword: str,
    max_papers: int = 5,
    organism: str = "",
    with_analysis: bool = False,
    treatment_keywords: list[str] | None = None,
    control_keywords: list[str] | None = None,
    raw_da_method: str = "deseq2",
    require_pdf: bool = True,
    min_year: int = 0,
    search_pool: int = 30,
    run_label: str = "",
    output_base: str = "./output",
    max_chars: int = 100000,
    extract_findings: bool = True,
    require_exercise_relevance: bool = True,
) -> str:
    """Run the full keyword -> 13-CSV Agent A (SEA-CDM v1) cohort pipeline in ONE call. Returns a
    text report; all artifacts land under output_base/agentA_cohort_{run_label}/.

    This replaces the Legacy manual paper-first sequence. It runs, per top hit:
    own-vs-cited GSE disambiguation; the 9 SEA-CDM text tables with per-field provenance; subject/
    sample/groups/assay derived deterministically from the GEO metadata CSV (byte-identical
    across re-runs); the paper's text-mined reported findings (#5); the computed-vs-reported agreement
    annotation (#6, when with_analysis); and the pathway->gene->exercise mechanism chain (#7). With
    with_analysis=True it also runs run_batch_geo_pipeline on strictly-own GSEs (DESeq2/edgeR/
    limma-voom + GSEA), splitting each design column into one contrast per treatment level (#8).

    Args:
        keyword: search query (e.g. 'exercise skeletal muscle transcriptome').
        max_papers: how many of the ranked hits to actually extract.
        organism: 'Mouse'/'Human' hint passed to extraction + analysis.
        with_analysis: if True, run run_batch_geo_pipeline on strictly-own GSEs to fill
            analysis/results rows (slow — downloads + DESeq2/GSEA). Default off.
        treatment_keywords / control_keywords: forwarded to the batch for auto-DEG.
        raw_da_method: DA method for raw-count studies — 'deseq2' (default) / 'edger' /
            'limma-voom' / 'auto' (deterministic DESeq2, no LLM) / 'auto-llm' (LLM picks per
            study) / 'all' (run DESeq2 + edgeR + limma-voom and report the >=2-method consensus,
            with per-method DEG files + a per-gene comparison table). Forwarded to
            run_batch_geo_pipeline; in 'all' mode analysis.da_method records the consensus and
            results rows include each per-method DEG + the comparison CSV.
        require_pdf / min_year / search_pool: search_papers knobs (search_pool = max_results).
        run_label: cohort dir label (defaults to a slug of the keyword).
        output_base: root under which agentA_cohort_{run_label}/ is created.
        max_chars: per-paper text truncation (cost guard).
        extract_findings: if True, mine paper-reported gene/pathway/phenotype findings.
        require_exercise_relevance: if True, skip search hits whose title/abstract do not clearly
            describe an exercise intervention/exposure context before fetching/extracting.
    """
    request = normalize_agent_a_request(
        keyword=keyword, max_papers=max_papers, organism=organism,
        with_analysis=with_analysis, treatment_keywords=treatment_keywords,
        control_keywords=control_keywords, raw_da_method=raw_da_method,
        require_pdf=require_pdf, min_year=min_year, search_pool=search_pool,
        run_label=run_label, output_base=output_base, max_chars=max_chars,
        extract_findings=extract_findings,
        require_exercise_relevance=require_exercise_relevance,
    )
    # From here onward every stage consumes the normalized values. This deliberately keeps
    # intermediate state out of the ReAct loop and preserves the existing public signature.
    keyword = request.keyword
    max_papers = request.max_papers
    organism = request.organism
    with_analysis = request.with_analysis
    treatment_keywords = request.treatment_keywords
    control_keywords = request.control_keywords
    raw_da_method = request.raw_da_method
    require_pdf = request.require_pdf
    min_year = request.min_year
    search_pool = request.search_pool
    output_base = request.output_base
    max_chars = request.max_chars
    extract_findings = request.extract_findings
    require_exercise_relevance = request.require_exercise_relevance
    label = request.run_label
    cohort_dir = os.path.join(output_base, f"agentA_cohort_{label}")
    csv_dir = os.path.join(cohort_dir, "csv")
    studies_dir = os.path.join(cohort_dir, "studies")
    os.makedirs(studies_dir, exist_ok=True)
    init_cohort_csvs(csv_dir)
    state_path = _write_workflow_state(cohort_dir, request, "INITIALIZED")
    log_lines = [f"# Agent A cohort run  keyword={keyword!r}  label={label}  with_analysis={with_analysis}"]

    def log(msg):
        print(msg)
        log_lines.append(msg)

    # Track wall time and LLM token cost per stage.
    from tools.cost_timing import RunProfiler
    prof = RunProfiler()

    # 1. Search.
    log(f"\n[1/3] search_papers(keyword={keyword!r}, require_pdf={require_pdf}, max_results={search_pool})")
    with prof.stage("search"):
        search_report = search_papers.invoke({
            "keyword": keyword, "require_pdf": require_pdf,
            "max_results": search_pool, "min_year": min_year,
        })
    rows = list(pt._LAST_SEARCH_ROWS)
    if not rows:
        log(search_report)
        _write_log(cohort_dir, log_lines)
        _write_workflow_state(cohort_dir, request, "NO_SEARCH_RESULTS", search_report=str(search_report))
        return f"No papers to process for {keyword!r}.\n{search_report}"
    _write_workflow_state(cohort_dir, request, "SEARCHED", n_search_results=len(rows))
    manifest = []

    def _base_manifest_row(row: dict, status: str = "", reason: str = "") -> dict:
        return {
            "idx": row.get("idx"), "paperId": row.get("paperId", ""),
            "pmcid": _normalize_pmcid(row.get("pmcid")),
            "title": (row.get("title") or "")[:70], "year": row.get("year"),
            "study_id": None, "chosen_gse": None, "ownership": "",
            "n_experiments": 0, "n_text_rows": 0, "analyzed": False,
            "da_method": None, "da_method_reason": None, "status": status, "text_path": None,
            "n_findings": 0, "findings_unverified": 0,
            "exercise_relevant": None if not reason else status != "skipped_not_exercise_relevant",
            "exercise_relevance_reason": reason or None,
        }

    skipped_relevance = []
    selected_rows = []
    if require_exercise_relevance:
        for row in rows:
            ok, reason = _is_exercise_relevant_search_hit(row)
            row["_exercise_relevance_reason"] = reason
            if ok:
                selected_rows.append(row)
                if len(selected_rows) >= max_papers:
                    break
            else:
                skipped_relevance.append(row)
                manifest.append(_base_manifest_row(row, status="skipped_not_exercise_relevant", reason=reason))
        log(f"  -> {len(rows)} ranked hits; exercise relevance gate selected "
            f"{len(selected_rows)} for extraction, skipped {len(skipped_relevance)}.")
    else:
        selected_rows = rows[:max_papers]
        log(f"  -> {len(rows)} ranked hits; processing top {min(max_papers, len(rows))}.")

    if not selected_rows:
        log("  -> no exercise-relevant papers selected for extraction.")
        man_path = os.path.join(cohort_dir, "papers.csv")
        pd.DataFrame(manifest).to_csv(man_path, index=False)
        _write_log(cohort_dir, log_lines)
        _write_workflow_state(
            cohort_dir, request, "NO_RELEVANT_PAPERS",
            papers_considered=len(manifest), manifest=man_path,
        )
        return (f"No exercise-relevant papers to process for {keyword!r}. "
                f"Skipped {len(skipped_relevance)} search hits. Manifest: {man_path}")

    # 2. Per-paper: fetch -> classify -> extract text tables -> append CSVs.
    own_gse_to_paper = {}  # strictly-own GSEs eligible for analysis
    log(f"\n[2/3] extracting {len(selected_rows)} exercise-relevant paper(s)")
    for row in selected_rows:
        idx = row["idx"]
        pmcid = _normalize_pmcid(row.get("pmcid"))
        paper_id = row.get("paperId", "")
        title = (row.get("title") or "")[:70]
        reason = row.get("_exercise_relevance_reason") or ""
        mrow = _base_manifest_row(row, reason=reason)
        log(f"\n  [#{idx}] {title} ({row.get('year')}) pmcid={pmcid or '∅'}")
        if require_exercise_relevance:
            log(f"      exercise relevance: {reason}")

        # fetch (handle-based, reuses Europe-PMC + PDF fallback + guards)
        with prof.stage("fetch"):
            fetch_report = fetch_paper_text.invoke({"search_index": idx})
        text_path = _locate_text(paper_id, pmcid)
        if not text_path:
            mrow["status"] = "fetch_failed"
            log(f"      fetch failed / no text saved. {fetch_report.splitlines()[0] if fetch_report else ''}")
            manifest.append(mrow)
            continue
        mrow["text_path"] = text_path
        with open(text_path, encoding="utf-8", errors="ignore") as f:
            full_text = f.read()

        # own-vs-cited — run on the FULL text. The paper's OWN GSE is declared in the Data
        # Availability / accession statement, which usually sits at the very END of the paper;
        # truncating to max_chars first (as we do for the LLM extraction below) can cut it off and
        # mis-key an own study as pmcid-keyed (observed: GSE279359's deposition is past a 24k cut,
        # so a small max_chars made with_analysis find "no own GSE"). Ownership detection is a
        # cheap regex pass — no reason to starve it of the tail.
        chosen_gse, ownership, classes = choose_own_gse(full_text)

        # truncate ONLY the LLM-extraction input (cost / rate-limit guard).
        text = full_text[:max_chars] if len(full_text) > max_chars else full_text
        study_id = chosen_gse or pmcid or paper_id
        mrow.update({"study_id": study_id, "chosen_gse": chosen_gse or None, "ownership": ownership})
        gse_summary = ", ".join(f"{c['gse']}:{c['ownership']}" for c in classes) or "none"
        log(f"      GSEs: {gse_summary} | study_id={study_id} ({ownership or 'pmcid-keyed'})")

        # Fetch metadata first so structural tables are deterministic.
        meta_csv = None
        if ownership == "own" and chosen_gse:
            meta_csv = os.path.join("data", chosen_gse, f"{chosen_gse}_metadata.csv")
            if not os.path.exists(meta_csv):
                try:
                    with prof.stage("download_metadata"):
                        download_geo_data.invoke({"geo_accession": chosen_gse})
                except Exception as e:
                    log(f"      metadata fetch for {chosen_gse} failed: {type(e).__name__}: {e}")
            meta_csv = meta_csv if os.path.exists(meta_csv) else None

        prov: dict = {}
        ext_usage: list = []
        try:
            with prof.stage("extraction"):
                tables = extract_tables_from_text(study_id, text, organism, report=prov,
                                                  metadata_csv=meta_csv, usage=ext_usage)
            prof.add_llm_usage("extraction", ext_usage)
        except Exception as e:
            mrow["status"] = f"extract_failed: {type(e).__name__}: {e}"
            log(f"      extraction failed: {type(e).__name__}: {e}")
            manifest.append(mrow)
            continue

        _write_study_json(studies_dir, study_id, tables)
        append_tables_to_csvs(tables, csv_dir)
        n_exp = len(tables["experiment"])
        n_rows = sum(len(v) for v in tables.values())
        n_unver = prov.get("n_unverified", 0)
        gerr = prov.get("group_errors") or {}
        meta_struct = bool(prov.get("metadata_structural"))
        mrow.update({
            "n_experiments": n_exp, "n_text_rows": n_rows,
            "status": "text_ok" if not gerr else "text_ok_partial",
            "prov_verified": prov.get("n_verified", 0), "prov_unverified": n_unver,
            "extract_group_errors": ";".join(sorted(gerr)) or None,
            "metadata_structural": meta_struct,
        })
        log(f"      extracted {n_exp} experiment(s), {n_rows} text rows -> CSVs"
            f" | provenance {prov.get('n_verified', 0)}/{prov.get('n_total', 0)} verbatim"
            + (f", {n_unver} flagged [UNVERIFIED]" if n_unver else "")
            + (" | subject/sample/groups/assay = deterministic (GEO metadata)" if meta_struct
               else " | subject/sample/groups/assay = LLM (no metadata)")
            + (f" | PARTIAL: group(s) {sorted(gerr)} failed -> empty" if gerr else ""))

        # Preserve paper findings even when computed analysis is unavailable.
        if extract_findings:
            try:
                frep: dict = {}
                findings_csv = os.path.join(studies_dir, f"{study_id}_reported_findings.csv")
                # Empty merged findings trigger the chunked fallback.
                prefetched_raw = prov.get("reported_findings")
                prefetched = prefetched_raw if prefetched_raw else None
                one_pass = prefetched is not None
                f5_usage: list = []
                with prof.stage("findings_#5"):
                    frows = build_reported_findings(study_id, text, findings_csv, organism,
                                                    report=frep, prefetched_findings=prefetched,
                                                    existing_tables=tables,
                                                    usage=f5_usage)
                prof.add_llm_usage("findings_#5", f5_usage)
                if frows.get("results"):
                    append_tables_to_csvs(frows, csv_dir)
                nf = frep.get("n_findings", 0)
                fu = frep.get("n_unverified", 0)
                mrow["n_findings"] = nf
                mrow["findings_unverified"] = fu
                mrow["findings_one_pass"] = one_pass
                log(f"      reported findings: {nf} mined from text"
                    + (" [one-pass: merged into lean call, no extra #5 call]" if one_pass
                       else " [standalone #5 call]")
                    + (f" ({fu} flagged [UNVERIFIED])" if fu else "")
                    + (f" -> {os.path.basename(findings_csv)} + results row" if nf else " (none)"))
            except Exception as e:
                log(f"      reported-findings extraction failed: {type(e).__name__}: {e}")

        if ownership == "own" and chosen_gse:
            own_gse_to_paper[chosen_gse] = study_id
        manifest.append(mrow)

    # 3. Optional analysis pass over strictly-own GSEs.
    analyzed_status = {}
    if with_analysis and own_gse_to_paper:
        gses = sorted(own_gse_to_paper)
        log(f"\n[3/3] with_analysis: run_batch_geo_pipeline on {len(gses)} own GSE(s): {gses}")
        from tools.batch_tools import run_batch_geo_pipeline
        # analysis_batch = download + DESeq2/edgeR/voom + GSEA (free CPU) + the gated contrast
        # validation / opt-in da-picker (small LLM, NOT token-captured here — see cost_timing.py).
        with prof.stage("analysis_batch(DA+GSEA)"):
            batch_report = run_batch_geo_pipeline.invoke({
                "accessions": gses, "organism": organism or "Mouse",
                "treatment_keywords": treatment_keywords, "control_keywords": control_keywords,
                "output_base": cohort_dir, "run_label": "analysis", "raw_da_method": raw_da_method,
            })
        log("  " + (batch_report or "").replace("\n", "\n  "))
        batch_dir = os.path.join(cohort_dir, "cohort_analysis")
        summary_path = os.path.join(batch_dir, "summary.csv")
        summ = {}
        if os.path.isfile(summary_path):
            df = pd.read_csv(summary_path)
            for _, r in df.iterrows():
                summ[str(r.get("accession"))] = {k: (None if pd.isna(v) else v) for k, v in r.to_dict().items()}
        from tools.agreement_tools import build_agreement_report
        from tools.pathway_chain_tools import build_pathway_chain
        from tools.batch_tools import _find_expression_file
        agreement_by_gse = {}
        chain_by_gse = {}
        enrich_by_gse = {}
        split_by_gse = {}          # per-condition study-split + cross-study pairwise comparisons
        _gmt_sizes = None          # MSigDB Hallmark set sizes for pathway.n_genes; fetched once, lazily
        for gse in gses:
            study_id = own_gse_to_paper[gse]
            study_batch_dir = os.path.join(batch_dir, gse)
            srow = summ.get(gse, {})
            analyzed_status[gse] = srow.get("status", "no_summary")
            prows = build_pipeline_rows(study_id, srow, study_batch_dir)
            append_tables_to_csvs(prows, csv_dir)

            # Rule #1: gene.csv is computed from DEG outputs, not filled from paper text.
            try:
                from tools.gene_loader import gene_rows_for_study_batch
                grows = gene_rows_for_study_batch(study_id, study_batch_dir, organism or "Mouse")
                if grows:
                    append_tables_to_csvs({"gene": grows}, csv_dir)
                log(f"      [#gene] DEG-derived gene table: {len(grows)} rows -> gene.csv")
            except Exception as e:
                log(f"      [#gene] DEG-derived gene load failed: {type(e).__name__}: {e}")

            # Compare computed DEG with paper-reported findings.
            findings_csv = os.path.join(studies_dir, f"{study_id}_reported_findings.csv")
            if os.path.isfile(findings_csv):
                try:
                    counts_path = ""
                    data_dir = os.path.join("data", gse)
                    if os.path.isdir(data_dir):
                        counts_path, _ = _find_expression_file(data_dir)
                    arep: dict = {}
                    agree_csv = os.path.join(studies_dir, f"{study_id}_agreement.csv")
                    with prof.stage("agreement_#6"):
                        build_agreement_report(study_id, findings_csv, study_batch_dir,
                                               counts_path=counts_path or "", species=organism or "Mouse",
                                               out_csv=agree_csv, report=arep)
                    agreement_by_gse[gse] = arep.get("summary", {})
                    summ_str = ", ".join(f"{k}={v}" for k, v in sorted((arep.get("summary") or {}).items()))
                    log(f"      [#6] agreement: {summ_str or 'none'} "
                        f"({arep.get('n_symbols_mapped', 0)} genes ID-mapped) -> {os.path.basename(agree_csv)}")
                    recon_rows = build_reconciliation_rows(
                        study_id, agree_csv, arep.get("summary") or {},
                        n_findings=arep.get("n_findings", 0))
                    if recon_rows.get("results"):
                        append_tables_to_csvs(recon_rows, csv_dir)
                        _su = arep.get("summary") or {}
                        _ndis = int(_su.get("contradicted", 0)) + int(_su.get("not_detected", 0))
                        log(f"      [#2] reconciliation -> results row {study_id}_res_recon1 "
                            f"(both paper claim + our DEG; {_ndis} disagreement(s) flagged)")
                except Exception as e:
                    log(f"      [#6] agreement annotation failed: {type(e).__name__}: {e}")

            # Build the exercise → pathway → gene chain.
            try:
                gsea_csvs = sorted(glob.glob(os.path.join(study_batch_dir, "*_GSEA_*.csv")))
                if gsea_csvs or os.path.isfile(findings_csv):
                    crep: dict = {}
                    chain_csv = os.path.join(studies_dir, f"{study_id}_pathway_chain.csv")
                    with prof.stage("chain_#7"):
                        build_pathway_chain(study_id, gsea_csvs,
                                            findings_csv=findings_csv if os.path.isfile(findings_csv) else "",
                                            out_csv=chain_csv, report=crep)
                    chain_by_gse[gse] = crep
                    log(f"      [#7] mechanism chain: {crep.get('n_gsea_pathways', 0)} GSEA + "
                        f"{crep.get('n_text_pathways', 0)} text pathways, "
                        f"{crep.get('n_chain_links_gene', 0)} with paper-reported driver gene, "
                        f"{crep.get('n_pathways_paper_confirmed', 0)} paper-named "
                        f"-> {os.path.basename(chain_csv)}")
            except Exception as e:
                log(f"      [#7] pathway chain failed: {type(e).__name__}: {e}")

            # Materialize pathway and enrichment rows from GSEA.
            try:
                if gsea_csvs:
                    from tools.enrichment_loader import enrichment_rows_for_study, load_hallmark_gmt_sizes
                    if _gmt_sizes is None:
                        _gmt_sizes = load_hallmark_gmt_sizes(organism or "Mouse")
                    gpath = os.path.join(csv_dir, "groups.csv")
                    glut = {}
                    if os.path.isfile(gpath):
                        gdf = pd.read_csv(gpath)
                        gsub = gdf[gdf["study_id"] == study_id] if "study_id" in gdf.columns else gdf
                        glut = {str(r["subject_group"]): str(r["group_id"]) for _, r in gsub.iterrows()
                                if pd.notna(r.get("subject_group")) and pd.notna(r.get("group_id"))}
                    with prof.stage("enrichment_#7b"):
                        erows = enrichment_rows_for_study(study_id, gsea_csvs, organism or "Mouse",
                                                          groups_lookup=glut, gmt_sizes=_gmt_sizes)
                    append_tables_to_csvs({"analysis": erows["analysis"],
                                           "pathway": list(erows["pathway"].values()),
                                           "enrichment": erows["enrichment"]}, csv_dir)
                    n_unres = sum(1 for a in erows["analysis"]
                                  if not a.get("treatment_group_id") or not a.get("control_group_id"))
                    enrich_by_gse[gse] = {"edges": len(erows["enrichment"]),
                                          "nodes": len(erows["pathway"]), "unresolved": n_unres}
                    log(f"      [#7b] enrichment tables: {len(erows['enrichment'])} edges, "
                        f"{len(erows['pathway'])} pathway nodes "
                        f"(n_genes {'filled' if _gmt_sizes else 'EMPTY: GMT fetch failed'}; "
                        f"{n_unres} contrast(s) with unresolved group FK) -> pathway.csv / enrichment.csv")
            except Exception as e:
                log(f"      [#7b] enrichment load failed: {type(e).__name__}: {e}")

            # Per-condition STUDY SPLIT + cross-study pairwise comparisons (user direction 2026-06-23):
            # turn a multi-condition own-GSE (0wk/2wk/… or post-exercise timepoints) into N per-condition
            # study records (descriptive fields INHERITED from the parent GSE study row; source_gse
            # back-link) and run a real DESeq2 for EVERY pairwise comparison — incl. the inter-condition
            # pairs the baseline-only contrast pass never runs. Supplementary per-study output; the main
            # 15 tables are untouched. Reuses the batch's aligned metadata + counts; zero LLM.
            try:
                from tools.study_split import split_and_compare
                aligned = os.path.join(study_batch_dir, f"{gse}_metadata_aligned.csv")
                counts_for_split = ""
                if os.path.isdir(os.path.join("data", gse)):
                    counts_for_split, _ = _find_expression_file(os.path.join("data", gse))
                if os.path.isfile(aligned) and counts_for_split:
                    parent_row = None
                    spath = os.path.join(csv_dir, "study.csv")
                    if os.path.isfile(spath):
                        sdf = pd.read_csv(spath)
                        pr = sdf[sdf["study_id"] == study_id]
                        parent_row = pr.iloc[0].to_dict() if len(pr) else None
                    split_dir = os.path.join(studies_dir, f"{study_id}_study_split")
                    srep: dict = {}
                    with prof.stage("split"):
                        split_and_compare(gse, counts_for_split, aligned, split_dir,
                                          parent_study_row=parent_row, control_keywords=control_keywords,
                                          pairing="all", max_pairs=15, report=srep)
                    if srep.get("n_studies"):
                        split_by_gse[gse] = srep
                        log(f"      [#split] {srep['n_studies']} per-condition studies, "
                            f"{srep.get('n_ok')}/{srep.get('n_comparisons')} pairwise DESeq2 "
                            f"-> studies/{os.path.basename(split_dir)}/")
            except Exception as e:
                log(f"      [#split] study split failed: {type(e).__name__}: {e}")

        # materialize the denormalized chain VIEW over the cohort's enrichment/pathway/analysis
        # tables — one readable row per chain, so 'which chains exist' is visible without a JOIN.
        try:
            if any(enrich_by_gse.values()):
                from tools.enrichment_loader import write_chain_view
                cv = write_chain_view(csv_dir)
                log(f"      [#7b] chain view: {len(cv)} chains -> chain_view.csv")
        except Exception as e:
            log(f"      [#7b] chain view failed: {type(e).__name__}: {e}")
        for m in manifest:
            gse = m["chosen_gse"]
            if gse in analyzed_status:
                m["analyzed"] = True
                m["status"] = f"text_ok+analysis:{analyzed_status[gse]}"
                srow = summ.get(gse, {})
                m["da_method"] = srow.get("da_method")
                m["da_method_reason"] = srow.get("da_method_reason")
                ag = agreement_by_gse.get(gse, {})
                m["agree_confirmed"] = ag.get("confirmed", 0) + ag.get("confirmed_change", 0)
                m["agree_contradicted"] = ag.get("contradicted", 0)
                m["agree_direction_only"] = ag.get("direction_only", 0)
                m["agree_not_detected"] = ag.get("not_detected", 0)
                m["agree_not_checkable"] = ag.get("not_checkable", 0) + ag.get("not_in_results", 0)
                ch = chain_by_gse.get(gse, {})
                m["chain_gsea_pathways"] = ch.get("n_gsea_pathways", 0)
                m["chain_gene_links"] = ch.get("n_chain_links_gene", 0)
                m["chain_paper_named"] = ch.get("n_pathways_paper_confirmed", 0)
                m["chain_text_only"] = ch.get("n_text_only_pathways", 0)
                en = enrich_by_gse.get(gse, {})
                m["enrichment_edges"] = en.get("edges", 0)
                m["pathway_nodes"] = en.get("nodes", 0)
                sp = split_by_gse.get(gse, {})
                m["split_studies"] = sp.get("n_studies", 0)
                m["pairwise_comparisons"] = sp.get("n_comparisons", 0)
    elif with_analysis:
        log("\n[3/3] with_analysis: no strictly-own GSE among the papers — nothing to analyze.")
    else:
        log("\n[3/3] with_analysis=False — skipped (run with with_analysis=True to fill analysis/results rows).")

    # Persist per-stage timing and estimated LLM cost.
    cost_csv = os.path.join(cohort_dir, "cost_timing.csv")
    prof.write_csv(cost_csv)
    log("\n[cost/timing] per-stage wall time + LLM token/$ (Sonnet 4.6 $3/$15 per Mtok):")
    for line in prof.summary_lines():
        log(line)
    log(f"  -> {os.path.basename(cost_csv)}  |  TOTAL ~${prof.total_usd():.4f}, {prof.total_wall():.0f}s wall")

    # manifest + log + report
    man_path = os.path.join(cohort_dir, "papers.csv")
    pd.DataFrame(manifest).to_csv(man_path, index=False)
    _write_log(cohort_dir, log_lines)

    n_skip = sum(1 for m in manifest if str(m["status"]).startswith("skipped_"))
    n_text = sum(1 for m in manifest if str(m["status"]).startswith("text_ok"))
    # a paper "failed" only if its TEXT extraction failed (fetch/extract) — an analysis
    # sub-step failing (e.g. 'deg_ok_gsea_failed') is NOT a paper-level failure.
    n_fail = sum(1 for m in manifest
                 if not str(m["status"]).startswith("text_ok")
                 and not str(m["status"]).startswith("skipped_"))
    n_anal = sum(1 for m in manifest if m["analyzed"])
    csv_counts = _count_csv_rows(csv_dir)
    _write_workflow_state(
        cohort_dir, request, "COMPLETED", papers_considered=len(manifest),
        papers_text_extracted=n_text, papers_failed=n_fail, papers_analyzed=n_anal,
        manifest=man_path, csv_dir=csv_dir,
    )
    report = [
        f"Agent A cohort complete: keyword={keyword!r}  ->  {cohort_dir}",
        f"- papers: {len(manifest)} considered | {n_skip} skipped_not_exercise | "
        f"{n_text} text-extracted | {n_fail} failed | {n_anal} analyzed",
        f"- {len(SEA_TABLES)} CSVs in {csv_dir} (rows): " + ", ".join(f"{t}={c}" for t, c in csv_counts.items() if c),
        f"- cost/timing: {cost_csv}  |  est ${prof.total_usd():.4f} LLM, {prof.total_wall():.0f}s wall "
        f"({prof.total_llm()} LLM calls, {prof.total_in()} in / {prof.total_out()} out tok)",
        f"- manifest: {man_path}",
        f"- workflow state: {state_path}",
        f"- per-study JSON: {studies_dir}/<study_id>/seacdm_tables.json",
        f"- log: {os.path.join(cohort_dir, 'cohort.log')}",
    ]
    return "\n".join(report)


# ---- small helpers --------------------------------------------------------------------

def _locate_text(paper_id: str, pmcid: str):
    """Find the .txt fetch_paper_text saved (it names by paperId, else normalized pmcid)."""
    for cand in (
        os.path.join("data", "papers", f"{paper_id}.txt") if paper_id else "",
        os.path.join("data", "papers", f"{_normalize_pmcid(pmcid)}.txt") if pmcid else "",
    ):
        if cand and os.path.isfile(cand) and os.path.getsize(cand) > 0:
            return cand
    return None


def _write_study_json(studies_dir: str, study_id: str, tables: dict):
    import json
    safe = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in study_id)
    d = os.path.join(studies_dir, safe)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "seacdm_tables.json"), "w", encoding="utf-8") as f:
        json.dump(tables, f, indent=2, ensure_ascii=False)


def _write_log(cohort_dir: str, lines: list):
    os.makedirs(cohort_dir, exist_ok=True)
    with open(os.path.join(cohort_dir, "cohort.log"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def _count_csv_rows(csv_dir: str) -> dict:
    counts = {}
    for name, entry in SEA_TABLES.items():
        path = os.path.join(csv_dir, entry["csv"])
        if not csv_columns(name) or not os.path.isfile(path):
            counts[name] = 0
            continue
        with open(path, encoding="utf-8") as f:
            counts[name] = max(0, sum(1 for _ in f) - 1)  # minus header
    return counts


# LangChain wrapper; scripts continue to call the plain function.
from langchain_core.tools import tool as _tool  # noqa: E402

run_agent_a_cohort_tool = _tool(run_agent_a_cohort)
