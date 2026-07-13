"""Deterministic DEG -> SEA-CDM gene table loader.

`gene.csv` used to be populated from paper-reported findings. The current rule is stricter:
paper text is only used for reported gene-phenotype claims / reconciliation evidence, while
the `gene` table itself is populated from computed DEG result files.
"""

import glob
import os
import re

import pandas as pd

from tools.sea_cdm_schema import csv_columns


_DERIVED_RESULT_TOKENS = ("_GSEA_", "_GO_", "_KEGG_", "_Reactome_", "_MSigDB_", "__DA_compare")


def _row(table: str, **kw) -> dict:
    return {c: kw.get(c) for c in csv_columns(table)}


def _safe_symbol(value) -> str:
    s = str(value or "").strip()
    if not s or s.lower() in {"nan", "none"}:
        return ""
    return s


def _contrast_from_deg(path: str) -> str:
    base = os.path.basename(path)
    stem = base[:-4] if base.lower().endswith(".csv") else base
    if stem.startswith("DEG_results_"):
        stem = stem[len("DEG_results_"):]
    if "__" in stem:
        stem = stem.split("__", 1)[0]
    return stem.replace("_vs_", " vs ").replace("_", " ")


def _direction(log2fc) -> str:
    try:
        return "up" if float(log2fc) > 0 else "down" if float(log2fc) < 0 else "unchanged"
    except Exception:
        return "n/a"


def discover_deg_csvs(study_batch_dir: str) -> list[str]:
    """Find primary DEG result CSVs in a batch study directory."""
    paths = sorted(glob.glob(os.path.join(study_batch_dir, "DEG_results_*.csv")))
    return [
        p for p in paths
        if not any(tok in os.path.basename(p) for tok in _DERIVED_RESULT_TOKENS)
    ]


def gene_rows_from_deg_files(
    study_id: str,
    deg_csvs,
    organism: str = "",
    padj_cutoff: float = 0.05,
    log2fc_cutoff: float = 0.0,
    max_genes_per_file: int = 250,
) -> list[dict]:
    """Build schema-conformant gene rows from computed DEG CSVs.

    Rows are significant genes from the computed result, sorted by adjusted p-value. Sourced
    columns keep the DEG CSV path as computational provenance rather than a paper quote.
    """
    rows = []
    seen = set()
    n = 0
    for deg_csv in deg_csvs or []:
        try:
            df = pd.read_csv(deg_csv, index_col=0)
        except Exception:
            continue
        if "padj" not in df.columns or "log2FoldChange" not in df.columns:
            continue
        work = df.copy()
        work.index = work.index.astype(str)
        work["padj"] = pd.to_numeric(work["padj"], errors="coerce")
        work["log2FoldChange"] = pd.to_numeric(work["log2FoldChange"], errors="coerce")
        sig = work[(work["padj"] < padj_cutoff) & (work["log2FoldChange"].abs() >= log2fc_cutoff)]
        if sig.empty:
            continue
        sig = sig.sort_values(["padj", "log2FoldChange"], ascending=[True, False]).head(max_genes_per_file)
        contrast = _contrast_from_deg(deg_csv)
        source = os.path.normpath(deg_csv)
        for gene_id, r in sig.iterrows():
            symbol = _safe_symbol(gene_id)
            if not symbol:
                continue
            key = (symbol.lower(), contrast.lower(), source.lower())
            if key in seen:
                continue
            seen.add(key)
            n += 1
            lfc = r.get("log2FoldChange")
            padj = r.get("padj")
            magnitude = f"log2FC={float(lfc):.4g}; padj={float(padj):.3g}"
            rows.append(_row(
                "gene",
                gene_id=f"{study_id}_deg_gene{n}",
                study_id=study_id,
                experiment_id=f"{study_id}_exp1",
                gene_symbol=symbol,
                gene_symbol_source=source,
                organism=organism or None,
                comparison=contrast,
                comparison_source=source,
                regulation_direction=_direction(lfc),
                magnitude=magnitude,
                magnitude_source=source,
                relationship_to_exercise="is_regulated_by",
                reference_source="computed_deg",
                reference_source_id=study_id,
            ))
    return rows


def gene_rows_for_study_batch(
    study_id: str,
    study_batch_dir: str,
    organism: str = "",
    padj_cutoff: float = 0.05,
    log2fc_cutoff: float = 0.0,
    max_genes_per_file: int = 250,
) -> list[dict]:
    return gene_rows_from_deg_files(
        study_id,
        discover_deg_csvs(study_batch_dir),
        organism=organism,
        padj_cutoff=padj_cutoff,
        log2fc_cutoff=log2fc_cutoff,
        max_genes_per_file=max_genes_per_file,
    )
