"""req #7 — build the exercise -> pathway -> gene MECHANISM CHAIN for an analysed study.

The point of the chain is to answer the mentor's question in one table: "exercise acts through
WHICH pathway, and moves WHICH genes?" It joins the two evidence sources we already produce:

  computational (GSEA Hallmark)  — each significant pathway carries an NES (direction + strength),
                                   an FDR, the experimental CONTRAST it came from (= the exercise
                                   contrast in an exercise study), and its LEADING-EDGE genes (the
                                   members that actually drive the enrichment).
  text-mined (#5 findings)       — pathways/genes the paper itself reports as changed with exercise,
                                   each with the verbatim source sentence and the comparison.

Each computational row is cross-linked back to the paper two ways:
  - cross_support      : did the paper TEXT also name this pathway?  (pathway-level paper-vs-ours)
  - genes_paper_reported : which of the pathway's leading-edge genes does the paper ALSO report as
                           exercise-changed?  (this is the real payload — it ties a computational
                           pathway to a driver gene to a paper claim to the exercise stimulus, all
                           in one cell).

Text-mined pathways the paper claims but our GSEA did NOT surface are emitted too (source='text',
cross_support = whether our GSEA detected them) so the table doubles as a gap analysis.

PROVENANCE — every value in a row is traceable to its origin (mirrors tools/sea_cdm_schema.py's
`Sourced` convention). Machine-derived GSEA facts (pathway/nes/fdr/member_genes) trace to the
`gsea_source` result FILE they all came from; anything FILTERED from paper text carries an explicit
source: `genes_paper_reported_source` holds the verbatim sentence(s) the confirmed driver gene was
read from, and `text_source` holds the verbatim sentence behind a text-mined row's pathway claim.
So no text-filtered value is ever shown without the sentence it was taken from.

Honest scope: pathway membership is GSEA leading-edge (computational) only — we do not invent
member genes for text-only pathways. Direction is sign-of-NES / the paper's stated direction;
magnitudes are not threshold-matched across cohorts. Pathway name matching is token-overlap, so a
rare paraphrase can be missed (logged, never silently dropped).
"""

import os
import re
import glob
import pandas as pd

from tools.agreement_tools import _entity_candidates

# Columns follow the docs/assets/struct.png mechanism spine — NODE -> EDGE -> NODE -> EDGE —
# so the table reads left-to-right as  Exercise --regulates--> Pathway --has-member--> Gene.
# Each text-filtered value sits next to its own `_source`; the GSEA facts share one `gsea_source`.
CHAIN_COLUMNS = [
    # -- keys / which evidence class produced this row --
    "chain_id", "study_id", "source",
    # -- NODE: Exercise (the stimulus / contrast) --
    "contrast",
    # -- EDGE: Exercise --regulates--> Pathway  (direction / strength / significance) --
    "direction", "nes", "fdr",
    # -- NODE: Pathway --
    "pathway", "pathway_id",
    # -- EDGE: Pathway --has-member--> Gene   (+ the Gene node itself) --
    "n_member_genes", "member_genes",
    # -- NODE: Regulated Gene (text-confirmed driver) — TEXT-FILTERED, carries its own source --
    "genes_paper_reported", "genes_paper_reported_source",
    # -- cross-link verdict (pathway-level paper agreement / gap analysis) --
    "cross_support",
    # -- PROVENANCE: file behind the computational facts / verbatim sentence behind text facts --
    "gsea_source", "text_source",
]

# generic words that carry no pathway identity — dropped before token-overlap matching
_PATHWAY_STOPWORDS = {
    "hallmark", "of", "the", "and", "or", "to", "in", "a", "an", "via", "by", "with",
    "pathway", "pathways", "signaling", "signalling", "response", "regulation", "process",
    "processes", "system", "activity", "metabolism", "metabolic", "function", "related",
}


def _readable_pathway(term: str) -> str:
    """'HALLMARK_OXIDATIVE_PHOSPHORYLATION' -> 'Oxidative Phosphorylation'."""
    t = re.sub(r"^HALLMARK_", "", str(term), flags=re.I)
    t = t.replace("_", " ").strip()
    return t.title() if t else str(term)


def _pathway_tokens(name: str) -> set:
    """Distinctive lowercase tokens of a pathway name (drop generic stopwords / short tokens)."""
    toks = re.findall(r"[A-Za-z0-9]+", str(name).lower())
    return {t for t in toks if len(t) >= 4 and t not in _PATHWAY_STOPWORDS}


def _name_match(gsea_tokens: set, text_blob: str) -> bool:
    """True if the paper text plausibly names this GSEA pathway: a majority of its distinctive
    tokens appear in the blob, with at least one length>=5 token (avoids spurious 1-short-word hits)."""
    if not gsea_tokens:
        return False
    present = {t for t in gsea_tokens if re.search(r"\b" + re.escape(t) + r"\b", text_blob)}
    if not present:
        return False
    has_strong = any(len(t) >= 5 for t in present)
    return has_strong and (len(present) / len(gsea_tokens)) >= 0.6


def _parse_gsea_contrast(path: str) -> str:
    """'DEG_results_<treat>_vs_<ctrl>_GSEA_Hallmark.csv' -> '<treat> vs <ctrl>'.

    In raw_da_method='all' runs the DEG file carries a '__<method>' suffix
    (e.g. '..._vs_pre-exercise__deseq2_GSEA_Hallmark.csv'). That suffix must be stripped here,
    else it leaks into the control arm ('pre-exercise  deseq2') and breaks the enrichment->groups
    FK resolution downstream. The DA method stays recoverable from gsea_source (the file path)."""
    b = os.path.basename(path)[:-4]
    b = re.sub(r"_GSEA_.*$", "", b)          # drop the _GSEA_<lib> suffix
    b = re.sub(r"__(deseq2|edger|limma[-_]voom|limma)$", "", b, flags=re.I)  # drop the DA-method tag
    if b.startswith("DEG_results_"):
        b = b[len("DEG_results_"):]
    return b.replace("_vs_", " vs ").replace("_", " ")


def _paper_gene_symbols(findings: list) -> set:
    """UPPERCASE candidate symbols the paper reports as changed (gene/protein findings only)."""
    out = set()
    for f in findings:
        if (f.get("entity_type") or "").strip().lower() in ("gene", "protein"):
            out.update(_entity_candidates(f.get("entity", "")))
    return out


def _paper_gene_sources(findings: list) -> dict:
    """{UPPERCASE candidate symbol -> verbatim paper sentence(s) it was reported in}.

    The source twin of `_paper_gene_symbols`: keeps each gene's #5 `source` quote so a confirmed
    leading-edge gene can be shown alongside the exact text it was filtered from (provenance)."""
    out = {}
    for f in findings:
        if (f.get("entity_type") or "").strip().lower() not in ("gene", "protein"):
            continue
        src = (f.get("source") or "").strip()
        for cand in _entity_candidates(f.get("entity", "")):
            if not cand:
                continue
            if cand not in out:
                out[cand] = src
            elif src and src not in out[cand]:
                out[cand] = out[cand] + " | " + src
    return out


def _parse_gsea_rows(gsea_csv: str, fdr_cutoff: float, max_lead: int) -> list:
    """One dict per significant Hallmark pathway in a GSEA result CSV."""
    df = pd.read_csv(gsea_csv)
    term_col = "Term" if "Term" in df.columns else ("Name" if "Name" in df.columns else None)
    if term_col is None or "NES" not in df.columns:
        return []
    fdr_col = next((c for c in ("FDR q-val", "FDR", "fdr") if c in df.columns), None)
    lead_col = next((c for c in ("Lead_genes", "Lead_Genes", "ledge_genes") if c in df.columns), None)
    contrast = _parse_gsea_contrast(gsea_csv)
    rows = []
    for _, r in df.iterrows():
        fdr = float(r[fdr_col]) if fdr_col and pd.notna(r[fdr_col]) else None
        if fdr is not None and fdr >= fdr_cutoff:
            continue
        nes = float(r["NES"]) if pd.notna(r["NES"]) else None
        if nes is None:
            continue
        lead = []
        if lead_col and pd.notna(r[lead_col]):
            lead = [g.strip() for g in str(r[lead_col]).replace(",", ";").split(";") if g.strip()]
        rows.append({
            "contrast": contrast,
            "pathway": _readable_pathway(r[term_col]),
            "pathway_id": str(r[term_col]),
            "direction": "up" if nes > 0 else "down",
            "nes": round(nes, 3),
            "fdr": (round(fdr, 4) if fdr is not None else None),
            "lead": lead[:max_lead],
            "n_lead_total": len(lead),
        })
    return rows


def build_pathway_chain(study_id: str, gsea_csvs: list, findings_csv: str = "",
                        out_csv: str = "", fdr_cutoff: float = 0.25, max_lead: int = 60,
                        report: dict = None) -> list:
    """Join computational GSEA pathways with the paper's text-mined findings into one chain table.

    Args:
        study_id: SEA-CDM study id (paper-keyed) for the chain_id / study_id columns.
        gsea_csvs: list of '*_GSEA_*.csv' paths for this study (one per contrast).
        findings_csv: '<study>_reported_findings.csv' from #5 (optional — text side / cross-link).
        out_csv: where to write the chain CSV (optional).
        fdr_cutoff: keep GSEA pathways with FDR q < this. Default 0.25 (standard GSEA threshold).
        max_lead: cap leading-edge genes stored per pathway (the full count is kept in a column).
        report: optional dict; receives summary counts.
    Returns the chain rows (list of dicts)."""
    findings = []
    if findings_csv and os.path.isfile(findings_csv):
        findings = pd.read_csv(findings_csv).fillna("").to_dict("records")
    paper_genes = _paper_gene_symbols(findings)
    paper_gene_src = _paper_gene_sources(findings)   # SYMBOL -> verbatim paper sentence(s)
    # one lowercase blob of paper entity + source text, for pathway-name cross-matching
    text_blob = " ".join(
        f"{f.get('entity', '')} {f.get('source', '')}".lower() for f in findings
    )
    # paper-claimed pathways (text side): pathway-type findings, plus 'other' findings that read
    # like a pathway/process rather than a single token
    text_pathways = []
    for f in findings:
        et = (f.get("entity_type") or "").strip().lower()
        ent = (f.get("entity") or "").strip()
        if et == "pathway" or (et == "other" and " " in ent and len(ent) > 6):
            text_pathways.append(f)

    rows = []
    matched_gsea_terms = set()           # gsea pathway_ids the paper text also named
    n_chain_links = 0                    # gsea rows that have >=1 paper-reported leading-edge gene

    cid = 0
    for gsea_csv in sorted(gsea_csvs):
        for g in _parse_gsea_rows(gsea_csv, fdr_cutoff, max_lead):
            cid += 1
            toks = _pathway_tokens(g["pathway_id"])
            paper_named = _name_match(toks, text_blob)
            if paper_named:
                matched_gsea_terms.add(g["pathway_id"])
            lead_upper = {x.upper() for x in g["lead"]}
            confirmed = sorted(lead_upper & paper_genes)
            # provenance for the text-filtered driver genes: 'GENE: <verbatim paper sentence>'
            gp_source = " || ".join(
                f"{gene}: {paper_gene_src[gene]}" if paper_gene_src.get(gene) else gene
                for gene in confirmed
            )
            if confirmed:
                n_chain_links += 1
            n_total = g["n_lead_total"]
            member = ";".join(g["lead"])
            if n_total > len(g["lead"]):
                member += f" (+{n_total - len(g['lead'])} more)"
            rows.append({
                "chain_id": f"{study_id}_chain{cid}",
                "study_id": study_id,
                "source": "computational (GSEA Hallmark)",
                "contrast": g["contrast"],
                "direction": g["direction"],
                "nes": g["nes"],
                "fdr": g["fdr"],
                "pathway": g["pathway"],
                "pathway_id": g["pathway_id"],
                "n_member_genes": n_total,
                "member_genes": member,
                "genes_paper_reported": ";".join(confirmed),
                "genes_paper_reported_source": gp_source,
                "cross_support": "paper text names this pathway" if paper_named else "",
                "gsea_source": gsea_csv,                 # the result file these facts came from
                "text_source": "",
            })

    # text-claimed pathways the paper asserts — emit as their own rows, flagging whether our GSEA
    # detected them (gap analysis). cross_support carries the GSEA detection verdict.
    gsea_token_sets = [(_pathway_tokens(r["pathway_id"]), r["pathway"])
                       for r in rows if r["source"].startswith("computational")]
    n_text_only = 0
    for f in text_pathways:
        cid += 1
        ent = (f.get("entity") or "").strip()
        toks = _pathway_tokens(ent)
        # did any kept GSEA pathway match this text pathway by token overlap?
        gsea_hit = ""
        for gt, gname in gsea_token_sets:
            if toks and gt and len(toks & gt) >= 1 and any(len(t) >= 5 for t in (toks & gt)):
                gsea_hit = gname
                break
        if not gsea_hit:
            n_text_only += 1
        rows.append({
            "chain_id": f"{study_id}_chain{cid}",
            "study_id": study_id,
            "source": "text-mined (paper)",
            "contrast": f.get("comparison") or "",
            "direction": f.get("direction") or "",
            "nes": None,
            "fdr": None,
            "pathway": ent,
            "pathway_id": "",
            "n_member_genes": None,
            "member_genes": "",
            "genes_paper_reported": "",
            "genes_paper_reported_source": "",
            "cross_support": (f"our GSEA detected: {gsea_hit}" if gsea_hit
                              else "not detected by our GSEA"),
            "gsea_source": "",
            "text_source": f.get("source") or "",     # verbatim sentence behind this text claim
        })

    if out_csv:
        os.makedirs(os.path.dirname(out_csv), exist_ok=True)
        pd.DataFrame(rows, columns=CHAIN_COLUMNS).to_csv(out_csv, index=False)
    if report is not None:
        report["n_rows"] = len(rows)
        report["n_gsea_pathways"] = sum(1 for r in rows if r["source"].startswith("computational"))
        report["n_text_pathways"] = sum(1 for r in rows if r["source"].startswith("text"))
        report["n_pathways_paper_confirmed"] = len(matched_gsea_terms)
        report["n_chain_links_gene"] = n_chain_links   # gsea pathways with a paper-reported driver gene
        report["n_text_only_pathways"] = n_text_only
        report["out_csv"] = out_csv
    return rows
