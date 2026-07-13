"""req #6 — annotate whether our COMPUTED differential expression agrees with the paper's OWN
REPORTED findings.

Two result sources now coexist for an analyzed study (see [[project_seacdm_determinism]]):
  - text-mined findings (#5): {entity, entity_type, direction, comparison, source} from the paper
  - computational DEG (#1/#8/'all'): per-contrast gene log2FoldChange + padj (and, in 'all' mode,
    a per-gene multi-method comparison table with a >=2-method consensus flag)

This module joins them gene-by-gene and emits a per-finding verdict so a reviewer can see, finding
by finding, whether our recomputation backs up what the paper claims:
  confirmed         our data: significant, SAME direction as the paper
  contradicted      our data: significant, OPPOSITE direction
  direction_only    our data: same direction sign but NOT significant (sub-threshold agreement)
  not_detected      measured but no significant change (paper says it changed, we don't see it)
  not_in_results    checkable gene/protein but absent from our matrix / could not map its ID
  not_checkable     entity is a pathway/phenotype/multiword description, not a single gene symbol

Honest scope: gene-level only. Pathway/GSEA-level agreement is left for when GSEA succeeds (the
demo study has integer gene IDs that break GSEA). Direction is sign-of-log2FC; magnitude is not
threshold-matched (papers and our pipeline use different cohorts/cutoffs).
"""

import os
import re
import glob
import pandas as pd

from tools.enrichment_tools import _ensembl_to_symbol_map

# gene-level Ensembl (ENSG…, ENSMUSG…), version suffix optional
_ENS_GENE_RE = re.compile(r"^ENS[A-Z]*G\d{6,}", re.I)

AGREEMENT_COLUMNS = [
    "entity", "entity_type", "direction", "comparison",
    "our_symbol", "our_contrast", "our_log2fc", "our_padj", "our_significant",
    "agreement", "note", "source",
]


def _entity_candidates(entity: str) -> list[str]:
    """Uppercase candidate gene-symbol forms for a paper entity, or [] if it isn't a single symbol.

    Handles the species prefix authors use ('mSirt2' -> mouse Sirt2, 'hDDX17' -> human DDX17) by
    also offering the de-prefixed form. Multi-word / descriptive entities ('RNA-binding proteins
    (RBPs)', 'exon-skipping events') are NOT gene symbols -> return [] so they fall to not_checkable.
    """
    e = (entity or "").strip()
    if not e or " " in e or "(" in e or "-" in e and len(e) > 12:
        return []
    cands = [e.upper()]
    # species-prefixed mouse/human symbol: lowercase m/h followed by a capitalised symbol
    if re.match(r"^[mh][A-Z0-9]", e):
        cands.append(e[1:].upper())
    # de-dupe, keep order
    seen, out = set(), []
    for c in cands:
        if c and c not in seen:
            seen.add(c)
            out.append(c)
    return out


def _index_is_integer(values) -> bool:
    s = [str(v) for v in list(values)[:200]]
    if not s:
        return False
    hits = sum(1 for v in s if v.isdigit())
    return hits / len(s) > 0.8


def _build_id_to_symbol(gene_ids, counts_path: str, species: str) -> dict:
    """Map the DEG index values to UPPERCASE gene symbols.

    - symbols already -> identity (uppercased)
    - Ensembl gene IDs -> MyGene
    - integer/opaque IDs + a counts file that carries an Ensembl-gene column -> ID->Ensembl (by
      CONTENT, not by header name: TALON/long-read annotation columns are often mis-labelled) ->
      MyGene. Returns {} (=> everything not_in_results) if no bridge is available.
    """
    ids = [str(g) for g in gene_ids]
    if not ids:
        return {}

    # Already symbols? (alpha, not Ensembl, not pure-int)
    sample = ids[:200]
    n_ens = sum(1 for v in sample if _ENS_GENE_RE.match(v))
    n_int = sum(1 for v in sample if v.isdigit())
    if n_ens == 0 and n_int == 0:
        return {g: g.upper() for g in ids}

    # Ensembl directly
    if n_ens / len(sample) > 0.5:
        ens_to_sym = _ensembl_to_symbol_map(ids, species)
        return {g: ens_to_sym[g.split(".")[0]].upper()
                for g in ids if g.split(".")[0] in ens_to_sym}

    # Integer/opaque IDs -> bridge through the counts file. Read it with index_col=0 so the frame's
    # INDEX matches exactly how DESeq2/edgeR/limma indexed the matrix (these tools read the counts
    # the same way). Crucial for TALON / long-read files that carry an UNNAMED leading index column
    # (the DEG ends up keyed by that opaque integer, not by gene_ID — keying on gene_ID maps ~5%).
    if not counts_path or not os.path.isfile(counts_path):
        return {}
    try:
        ann = pd.read_csv(counts_path, sep=None, engine="python", index_col=0)
    except Exception:
        return {}
    if ann.shape[1] < 1:
        return {}
    ann.index = ann.index.astype(str)
    id_set = set(ids)
    if len(id_set & set(ann.index)) == 0:
        return {}  # the matrix index isn't what we keyed DA on; nothing to bridge

    def _is_symbol(v):
        return bool(re.match(r"^[A-Za-z][A-Za-z0-9._-]*$", v)) and not _ENS_GENE_RE.match(v) and not v.isdigit()

    # Prefer a DIRECT gene-symbol column (no MyGene needed). Bias toward a column whose NAME hints
    # at gene names/symbols (annot_gene_name, gene_name, symbol); else the first symbol-looking col.
    sym_col = None
    name_pref = [c for c in ann.columns if any(h in str(c).lower() for h in ("gene_name", "symbol", "genename"))]
    for c in name_pref + [c for c in ann.columns if c not in name_pref]:
        vals = ann[c].dropna().astype(str).head(200)
        if len(vals) and sum(1 for v in vals if _is_symbol(v)) / len(vals) > 0.7:
            sym_col = c
            break
    if sym_col is not None:
        return {i: s.upper() for i, s in zip(ann.index, ann[sym_col].astype(str))
                if s and s.lower() != "nan"}

    # No symbol column -> fall back to an Ensembl-gene column + MyGene.
    ens_col = None
    for c in ann.columns:
        vals = ann[c].dropna().astype(str).head(50)
        if len(vals) and sum(1 for v in vals if _ENS_GENE_RE.match(v)) / len(vals) > 0.5:
            ens_col = c
            break
    if ens_col is None:
        return {}
    id_to_ens = {k: v.split(".")[0] for k, v in zip(ann.index, ann[ens_col].astype(str))
                 if _ENS_GENE_RE.match(v)}
    ens_to_sym = _ensembl_to_symbol_map(list(set(id_to_ens.values())), species)
    return {k: ens_to_sym[e].upper() for k, e in id_to_ens.items() if e in ens_to_sym}


def _contrast_label(path: str) -> str:
    """'DEG_results_<treat>_vs_<ctrl>[__method|__DA_compare].csv' -> '<treat> vs <ctrl>'."""
    b = os.path.basename(path)[:-4]
    if b.startswith("DEG_results_"):
        b = b[len("DEG_results_"):]
    for suf in ("__DA_compare",):
        if b.endswith(suf):
            b = b[: -len(suf)]
    if "__" in b:  # strip a trailing __<method>
        b = b.rsplit("__", 1)[0]
    return b.replace("_vs_", " vs ").replace("_", " ")


def _load_contrast_table(path: str, id_to_symbol: dict) -> pd.DataFrame:
    """Return a frame indexed by UPPERCASE symbol with columns log2fc / padj / sig.

    Consensus table (..__DA_compare.csv): log2fc = mean of the per-method *_log2FC, sig =
    consensus_ge2 (>=2 methods). Single DEG table: log2fc/padj direct, sig = padj<0.05.
    """
    df = pd.read_csv(path, index_col=0)
    is_compare = any(c.endswith("_log2FC") for c in df.columns)
    out = pd.DataFrame(index=df.index)
    if is_compare:
        lfc_cols = [c for c in df.columns if c.endswith("_log2FC")]
        padj_cols = [c for c in df.columns if c.endswith("_padj")]
        out["log2fc"] = df[lfc_cols].mean(axis=1)
        out["padj"] = df[padj_cols].min(axis=1) if padj_cols else pd.NA
        if "consensus_ge2" in df.columns:
            out["sig"] = df["consensus_ge2"].astype(str).str.lower().isin(("true", "1"))
        else:
            out["sig"] = out["padj"] < 0.05
    else:
        if "log2FoldChange" not in df.columns:
            return pd.DataFrame(columns=["log2fc", "padj", "sig"])
        out["log2fc"] = df["log2FoldChange"]
        out["padj"] = df.get("padj")
        out["sig"] = (df["padj"] < 0.05) if "padj" in df.columns else False
    out.index = [str(i) for i in out.index]
    out["symbol"] = [id_to_symbol.get(i) for i in out.index]
    out = out.dropna(subset=["symbol"])
    # one row per symbol — keep the most significant
    out = out.sort_values("padj", na_position="last").drop_duplicates("symbol", keep="first")
    return out.set_index("symbol")


def _verdict_note(verdict: str, sym: str, paper_dir: str, our_log2fc: float,
                  our_padj, our_sig: bool) -> str:
    """A human-readable reason for EACH matched-gene verdict, so a reviewer never sees a bare
    label (e.g. 'not_detected') with no explanation. Built from the actual numbers we computed."""
    our_dir = "up" if (our_log2fc or 0) > 0 else "down"
    pj = f"padj={our_padj}" if our_padj is not None else "padj=NA (filtered / no adj p-value)"
    pd_ = paper_dir or "n/a"
    if verdict == "confirmed":
        return f"{sym} significant in our DEG ({our_dir}, {pj}) and matches the paper's '{pd_}'"
    if verdict == "contradicted":
        return f"{sym} significant in our DEG ({our_dir}, {pj}) but OPPOSITE to the paper's '{pd_}'"
    if verdict == "direction_only":
        return f"{sym} trends the same way as the paper ('{pd_}') but is NOT significant in our DEG ({pj})"
    if verdict == "not_detected":
        return (f"{sym} IS in our DEG matrix but not significant ({pj} >= 0.05); "
                f"the paper reports it '{pd_}'")
    if verdict == "confirmed_change":
        return f"{sym} significant in our DEG ({our_dir}, {pj}); the paper reports a change (no direction given)"
    return ""


def _verdict(text_dir: str, our_sig: bool, our_log2fc: float) -> str:
    our_dir = "up" if (our_log2fc or 0) > 0 else "down"
    td = (text_dir or "").strip().lower()
    if td in ("up", "down"):
        if our_sig and our_dir == td:
            return "confirmed"
        if our_sig and our_dir != td:
            return "contradicted"
        if not our_sig and our_dir == td:
            return "direction_only"
        return "not_detected"
    if td == "unchanged":
        return "contradicted" if our_sig else "confirmed"
    # 'changed' / 'n/a' / other
    return "confirmed_change" if our_sig else "not_detected"


def compare_findings_to_deg(findings: list, contrast_tables: dict) -> tuple:
    """findings: list of dicts (#5). contrast_tables: {contrast_label: df indexed by symbol}.
    Returns (annotated_rows, summary_counts)."""
    rows, summary = [], {}
    for f in findings:
        entity = f.get("entity", "")
        etype = (f.get("entity_type") or "").strip().lower()
        row = {
            "entity": entity, "entity_type": f.get("entity_type"),
            "direction": f.get("direction"), "comparison": f.get("comparison"),
            "our_symbol": None, "our_contrast": None, "our_log2fc": None,
            "our_padj": None, "our_significant": None, "agreement": None,
            "note": None, "source": f.get("source"),
        }
        cands = _entity_candidates(entity) if etype in ("gene", "protein") else []
        if not cands:
            row["agreement"] = "not_checkable"
            row["note"] = ("not a single gene symbol" if etype in ("gene", "protein")
                           else f"entity_type={etype or 'n/a'} (not gene-level)")
            rows.append(row)
            summary["not_checkable"] = summary.get("not_checkable", 0) + 1
            continue
        # search every contrast for any candidate symbol; keep the most significant hit
        best = None  # (padj, contrast, sym, log2fc, sig)
        for label, tbl in contrast_tables.items():
            for sym in cands:
                if sym in tbl.index:
                    r = tbl.loc[sym]
                    padj = r["padj"]
                    key = padj if pd.notna(padj) else 1.0
                    if best is None or key < best[0]:
                        best = (key, label, sym, float(r["log2fc"]), bool(r["sig"]))
        if best is None:
            row["agreement"] = "not_in_results"
            row["note"] = "gene not found in our matrix / ID unmapped"
            rows.append(row)
            summary["not_in_results"] = summary.get("not_in_results", 0) + 1
            continue
        _, label, sym, log2fc, sig = best
        verdict = _verdict(f.get("direction"), sig, log2fc)
        our_padj = round(best[0], 4) if best[0] < 1.0 else None
        row.update({
            "our_symbol": sym, "our_contrast": label,
            "our_log2fc": round(log2fc, 3),
            "our_padj": our_padj,
            "our_significant": sig, "agreement": verdict,
            "note": _verdict_note(verdict, sym, f.get("direction"), log2fc, our_padj, sig),
        })
        rows.append(row)
        summary[verdict] = summary.get(verdict, 0) + 1
    return rows, summary


def build_agreement_report(study_id: str, findings_csv: str, deg_dir: str,
                           counts_path: str = "", species: str = "Mouse",
                           out_csv: str = "", report: dict = None) -> list:
    """Join #5 findings (findings_csv) with the study's DEG tables in deg_dir, write a per-finding
    agreement CSV, and return the annotated rows. `report` (if given) gets the summary counts."""
    if not os.path.isfile(findings_csv):
        if report is not None:
            report["error"] = "no findings csv"
        return []
    findings = pd.read_csv(findings_csv).to_dict("records")

    _DERIVED = ("_GSEA_", "_GO_", "_KEGG_", "_Reactome_", "_MSigDB_")
    all_deg = sorted(p for p in glob.glob(os.path.join(deg_dir, "DEG_results_*.csv"))
                     if not any(tok in os.path.basename(p) for tok in _DERIVED))
    compare = [p for p in all_deg if "__DA_compare" in os.path.basename(p)]
    # prefer consensus comparison tables; else fall back to single/per-method DEG files
    deg_files = compare if compare else [p for p in all_deg if "__DA_compare" not in os.path.basename(p)]
    if not deg_files:
        if report is not None:
            report["error"] = "no DEG files"
        return []

    # build the ID->symbol bridge once from the union of gene IDs across tables
    gene_ids = set()
    for p in deg_files:
        try:
            gene_ids.update(pd.read_csv(p, index_col=0, usecols=[0]).index.astype(str))
        except Exception:
            gene_ids.update(pd.read_csv(p, index_col=0).index.astype(str))
    id_to_symbol = _build_id_to_symbol(sorted(gene_ids), counts_path, species)

    contrast_tables = {}
    for p in deg_files:
        lbl = _contrast_label(p)
        tbl = _load_contrast_table(p, id_to_symbol)
        if len(tbl):
            contrast_tables[lbl] = tbl

    rows, summary = compare_findings_to_deg(findings, contrast_tables)

    if out_csv:
        os.makedirs(os.path.dirname(out_csv), exist_ok=True)
        pd.DataFrame(rows, columns=AGREEMENT_COLUMNS).to_csv(out_csv, index=False)
    if report is not None:
        report["summary"] = summary
        report["n_findings"] = len(rows)
        report["n_symbols_mapped"] = len(id_to_symbol)
        report["n_contrasts"] = len(contrast_tables)
        report["out_csv"] = out_csv
    return rows
