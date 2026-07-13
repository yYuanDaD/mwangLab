"""Zero-LLM loader for the pathway<->exercise chain tables (sea_cdm_schema `pathway` / `enrichment`,
plus the contrast columns on `analysis`). Re-houses facts that already live in the GSEA result CSVs
into schema-conformant rows, so the chain becomes a relational JOIN instead of a file parse.

Nothing here is computed or extracted — it is a pure re-shaping of existing `*_GSEA_*.csv` output:
  - one `enrichment` row per significant pathway (FDR q < cutoff) per analysis (the EDGE),
  - one deduped `pathway` row per distinct gene-set (the NODE, SHARED across studies),
  - one `analysis` row carrying the contrast as treatment/control group FKs + a label,
  - two `groups` rows (the contrast's two arms), derived from the GSEA filename's '<treat> vs <ctrl>'.

So this module is deterministic and offline. `collection_version` is the only asserted metadatum
(passed in per study); everything else is read from the GSEA CSV. `pathway.n_genes` and
`enrichment.paper_named` are left empty in this v1 (would need the GMT / a text pass).

Run the minimal unit:  PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/unit/test_enrichment_loader.py
"""

import os
import pandas as pd

from tools.sea_cdm_schema import csv_columns, SEA_TABLES
from tools.pathway_chain_tools import _parse_gsea_rows, _parse_gsea_contrast


def _row(table: str, **kw) -> dict:
    """A dict reindexed to the EXACT csv_columns(table) order — gaps left None (schema-conformant)."""
    return {c: kw.get(c) for c in csv_columns(table)}


def _collection_for_species(species: str):
    """(category, dbver, collection_version) for the MSigDB Hallmark GMT — mirrors enrichment_tools:
    mouse uses the mouse-symbol 'mh.all' GMT, human uses 'h.all'."""
    if str(species).strip().lower().startswith("mouse"):
        cat, ver = "mh.all", "2024.1.Mm"
    else:
        cat, ver = "h.all", "2024.1.Hs"
    return cat, ver, f"{cat}@{ver}"


def load_hallmark_gmt_sizes(species: str) -> dict:
    """{pathway_id -> gene-set size} from the same MSigDB Hallmark GMT the GSEA used, for
    pathway.n_genes. Needs network (MSigDB) + lxml; returns {} on ANY failure so the loader
    degrades to empty n_genes rather than blocking the cohort."""
    cat, ver, _ = _collection_for_species(species)
    try:
        from tools.enrichment_tools import _get_hallmark_gmt   # shares the process GMT cache
        gmt = _get_hallmark_gmt(cat, ver)
        return {name: len(genes) for name, genes in (gmt or {}).items()}
    except Exception:
        return {}


def _rows_for_gsea(study_id: str, gsea_csv: str, collection_version: str,
                   analysis_n: int, fdr_cutoff: float,
                   groups_lookup: dict = None, gmt_sizes: dict = None):
    """The analysis / groups / pathway / enrichment rows for ONE GSEA result file.

    groups_lookup ({arm label -> real group_id}): cohort mode — point the contrast at the REAL
    phase-2 group rows (matched by subject_group label) and DON'T synthesize groups. None: standalone
    mode — synthesize the two arm rows so the tables are self-contained.
    gmt_sizes ({pathway_id -> size}): fills pathway.n_genes when provided."""
    contrast = _parse_gsea_contrast(gsea_csv)                  # '<treat> vs <ctrl>'
    treat, ctrl = ([s.strip() for s in contrast.split(" vs ", 1)] + [""])[:2]
    aid = f"{study_id}_gsea{analysis_n}"

    if groups_lookup is not None:
        # cohort: resolve to existing group_ids; an unmatched arm -> None FK (fail-soft, still emits
        # the edge + contrast_label so the pathway side is never lost to a vocabulary miss).
        gt, gc = groups_lookup.get(treat), groups_lookup.get(ctrl)
        groups = []
    else:
        gt, gc = f"{study_id}_grp{analysis_n}a", f"{study_id}_grp{analysis_n}b"
        groups = [
            _row("groups", group_id=gt, study_id=study_id, subject_group=treat,
                 subject_group_source="derived from GSEA-file contrast"),
            _row("groups", group_id=gc, study_id=study_id, subject_group=ctrl,
                 subject_group_source="derived from GSEA-file contrast"),
        ]
    analysis = _row("analysis", analysis_id=aid, study_id=study_id,
                    treatment_group_id=gt, control_group_id=gc, contrast_label=contrast,
                    analysis_name="GSEA Hallmark (preranked)", da_method="gsea")

    sizes = gmt_sizes or {}
    pathway, enrichment = {}, []
    for i, g in enumerate(_parse_gsea_rows(gsea_csv, fdr_cutoff=fdr_cutoff, max_lead=60), 1):
        pid = g["pathway_id"]
        pathway[pid] = _row("pathway", pathway_id=pid, pathway_name=g["pathway"],
                            library="MSigDB Hallmark", collection_version=collection_version,
                            n_genes=sizes.get(pid))
        enrichment.append(_row("enrichment", enrichment_id=f"{aid}_enr{i}", analysis_id=aid,
                               pathway_id=pid, direction=g["direction"], nes=g["nes"], fdr=g["fdr"],
                               leading_edge_genes=";".join(g["lead"]), gsea_source=gsea_csv))
    return analysis, groups, pathway, enrichment


def enrichment_rows_for_study(study_id: str, gsea_csvs, species: str,
                              groups_lookup: dict = None, gmt_sizes: dict = None,
                              fdr_cutoff: float = 0.25) -> dict:
    """Cohort entry point: pathway (node) + enrichment (edge) + one GSEA-analysis row per GSEA file
    for ONE study, referencing the REAL phase-2 groups via groups_lookup. Returns
    {'analysis','groups','pathway','enrichment'} (groups empty when groups_lookup is given)."""
    _, _, version = _collection_for_species(species)
    analysis, groups, pathway, enrichment = [], [], {}, []
    for k, gsea in enumerate(sorted(gsea_csvs), 1):
        a, g, p, e = _rows_for_gsea(study_id, gsea, version, k, fdr_cutoff,
                                    groups_lookup=groups_lookup, gmt_sizes=gmt_sizes)
        analysis.append(a)
        groups.extend(g)
        enrichment.extend(e)
        for pid, prow in p.items():
            pathway.setdefault(pid, prow)
    return {"analysis": analysis, "groups": groups, "pathway": pathway, "enrichment": enrichment}


def load_enrichment_tables(studies, out_dir: str, fdr_cutoff: float = 0.25,
                           gmt_sizes: dict = None, report: dict = None):
    """Populate pathway / enrichment / analysis / groups CSVs from GSEA results.

    Args:
        studies: list of (study_id, gsea_csv, collection_version). Multiple GSEA files for the same
                 study_id get distinct analysis ids (auto-incremented per study).
        out_dir: directory to write the 4 CSVs into.
        fdr_cutoff: keep pathways with FDR q < this (default 0.25).
    Returns the four row collections; also writes the CSVs in csv_columns order."""
    os.makedirs(out_dir, exist_ok=True)
    analysis_rows, groups_rows, enrich_rows = [], [], []
    pathway_dim = {}                                 # pathway_id -> row (deduped = SHARED node)
    per_study = {}                                   # study_id -> running analysis count

    for study_id, gsea_csv, version in studies:
        per_study[study_id] = per_study.get(study_id, 0) + 1
        a, g, p, e = _rows_for_gsea(study_id, gsea_csv, version, per_study[study_id], fdr_cutoff,
                                    gmt_sizes=gmt_sizes)
        analysis_rows.append(a)
        groups_rows.extend(g)
        enrich_rows.extend(e)
        for pid, prow in p.items():
            pathway_dim.setdefault(pid, prow)        # first writer wins; shared across studies

    written = {"analysis": analysis_rows, "groups": groups_rows,
               "pathway": list(pathway_dim.values()), "enrichment": enrich_rows}
    for table, rows in written.items():
        path = os.path.join(out_dir, SEA_TABLES[table]["csv"])
        pd.DataFrame(rows, columns=csv_columns(table)).to_csv(path, index=False)

    if report is not None:
        report.update({t: len(r) for t, r in written.items()})
        report["out_dir"] = out_dir
    return written


def _study_of(child_id) -> str:
    """'{study}_exp1_samp3' / '{study}_exp1' -> '{study}' (every child PK is study-prefixed)."""
    return str(child_id).split("_exp")[0] if "_exp" in str(child_id) else str(child_id)


def _exercise_descriptors(out_dir: str) -> dict:
    """{study_id -> self-describing exercise string} built from the OTHER SEA-CDM tables, so a
    study-local contrast like '14-0-0 vs 0-0-0' reads as e.g. 'Mus musculus hippocampus, voluntary
    wheel running 14 days'. Each part is independent + fail-soft (missing table/column is skipped):
      species  <- subject.species          (metadata-derived, deterministic)
      tissue   <- sample.biosample_type     (metadata-derived, deterministic)
      modality <- interventions.material     (LLM text; absent until a cohort run extracts it)
      duration <- interventions.intervention_time (+ time_unit)
    """
    parts = {}                                       # study_id -> {species,tissue,modality,duration}

    def _collect(fname, idcol, valcol, key):
        f = os.path.join(out_dir, fname)
        if not os.path.isfile(f):
            return
        try:
            d = pd.read_csv(f)
        except Exception:
            return
        if idcol not in d.columns or valcol not in d.columns:
            return
        for _, r in d.iterrows():
            v = r.get(valcol)
            if pd.notna(v) and str(v).strip():
                parts.setdefault(_study_of(r[idcol]), {}).setdefault(key, set()).add(str(v).strip())

    _collect("subject.csv", "subject_id", "species", "species")
    _collect("sample.csv", "sample_id", "biosample_type", "tissue")
    _collect("interventions.csv", "intervention_id", "material", "modality")
    _collect("interventions.csv", "intervention_id", "intervention_time", "duration")
    _collect("interventions.csv", "intervention_id", "time_unit", "unit")

    out = {}
    for sid, p in parts.items():
        seg = []
        if p.get("species"):  seg.append("/".join(sorted(p["species"])))
        if p.get("tissue"):   seg.append("/".join(sorted(p["tissue"])))
        bio = ", ".join(seg)
        ex = []
        if p.get("modality"): ex.append("/".join(sorted(p["modality"])))
        if p.get("duration"):
            dur = "/".join(sorted(p["duration"]))
            unit = ("/".join(sorted(p["unit"]))) if p.get("unit") else ""
            ex.append(f"{dur} {unit}".strip())
        exercise = " ".join(ex)
        desc = "; ".join(s for s in (bio, exercise) if s)
        if desc:
            out[sid] = desc
    return out


def write_chain_view(out_dir: str, out_csv: str = None, fdr_cutoff: float = 0.25) -> pd.DataFrame:
    """Materialize the normalized pathway/enrichment/analysis tables into ONE denormalized,
    human-readable chain VIEW — one row per chain (enrichment edge) — so 'which chains exist' is
    visible at a glance without writing a JOIN. The `chain` column renders each row as a single
    readable string: 'exercise[<contrast>] --<dir>--> <pathway>'. Writes <out_dir>/chain_view.csv."""
    A = pd.read_csv(os.path.join(out_dir, "analysis.csv"))
    P = pd.read_csv(os.path.join(out_dir, "pathway.csv"))
    E = pd.read_csv(os.path.join(out_dir, "enrichment.csv"))
    v = (E.merge(P, on="pathway_id", how="left")
          .merge(A[["analysis_id", "study_id", "contrast_label"]], on="analysis_id", how="left"))
    v = v[v["fdr"] < fdr_cutoff].copy()
    # a contrast like '14-0-0 vs 0-0-0' is a STUDY-LOCAL encoding, meaningless on its own. The
    # `exercise` column resolves it to a self-describing descriptor (species/tissue/modality/duration
    # from subject/sample/interventions); the chain string prepends study + that descriptor so each
    # row is interpretable AND cross-study comparable. Fail-soft to study+contrast when absent.
    desc = _exercise_descriptors(out_dir)
    v["exercise"] = v["study_id"].map(lambda s: desc.get(s, ""))
    v["chain"] = (v["study_id"].astype(str)
                  + v["exercise"].map(lambda e: f" ({e})" if e else "")
                  + " | exercise[" + v["contrast_label"].astype(str) + "] --"
                  + v["direction"].astype(str) + "--> " + v["pathway_name"].astype(str)
                  + " (NES " + v["nes"].astype(str) + ", FDR " + v["fdr"].astype(str) + ")")
    cols = ["chain", "study_id", "exercise", "contrast_label", "pathway_name", "pathway_id", "n_genes",
            "direction", "nes", "fdr", "leading_edge_genes", "gsea_source"]
    v = v[[c for c in cols if c in v.columns]].sort_values(["study_id", "fdr"]).reset_index(drop=True)
    out_csv = out_csv or os.path.join(out_dir, "chain_view.csv")
    v.to_csv(out_csv, index=False)
    return v


def query_chain(out_dir: str, study_id: str = None, fdr_cutoff: float = 0.25) -> pd.DataFrame:
    """The pathway<->exercise chain as a JOIN over the 4 CSVs: enrichment ⋈ pathway ⋈ analysis ⋈
    groups(×2 arms). Returns one row per (pathway, contrast) with NES/FDR/direction + the two arms."""
    A = pd.read_csv(os.path.join(out_dir, "analysis.csv"))
    G = pd.read_csv(os.path.join(out_dir, "groups.csv"))
    P = pd.read_csv(os.path.join(out_dir, "pathway.csv"))
    E = pd.read_csv(os.path.join(out_dir, "enrichment.csv"))
    j = (E.merge(P, on="pathway_id")
           .merge(A, on="analysis_id")
           .merge(G.add_prefix("t_"), left_on="treatment_group_id", right_on="t_group_id")
           .merge(G.add_prefix("c_"), left_on="control_group_id", right_on="c_group_id"))
    j = j[j["fdr"] < fdr_cutoff]
    if study_id is not None:
        j = j[j["study_id"] == study_id]
    return j[["study_id", "pathway_name", "direction", "nes", "fdr",
              "t_subject_group", "c_subject_group", "contrast_label"]]
