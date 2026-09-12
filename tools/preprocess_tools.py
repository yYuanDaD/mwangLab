import os
import re
import pandas as pd
import numpy as np
from langchain_core.tools import tool


# Column names that commonly hold a gene SYMBOL in GEO/TALON supplementary matrices.
# Matched case-insensitively against the non-numeric columns we are about to drop, so the
# id->symbol mapping is captured before it's lost — GSEA needs symbols, not feature IDs.
_SYMBOL_COL_PATTERNS = [
    "annot_gene_name", "gene_name", "gene_symbol", "genesymbol", "external_gene_name",
    "hgnc_symbol", "mgi_symbol", "gene symbol", "gene name", "symbol",
]


def _looks_like_symbols(series: pd.Series) -> bool:
    """True if the column is mostly non-numeric strings (real gene symbols, not IDs)."""
    vals = [str(v).strip() for v in series.dropna().head(50) if str(v).strip()]
    if not vals:
        return False
    non_numeric = sum(1 for v in vals if not re.match(r"^[\d.]+$", v))
    return non_numeric >= len(vals) * 0.8


def _pick_symbol_column(df: pd.DataFrame, dropped_cols: list) -> str:
    """Among the columns being dropped as non-numeric, pick the one that holds gene symbols.
    Prefer an exact known name; fall back to any dropped column that looks symbol-like."""
    lower = {c.lower(): c for c in dropped_cols}
    for pat in _SYMBOL_COL_PATTERNS:
        if pat in lower and _looks_like_symbols(df[lower[pat]]):
            return lower[pat]
    for c in dropped_cols:
        if _looks_like_symbols(df[c]):
            return c
    return ""


@tool
def preprocess_counts(
    counts_csv: str,
    output_dir: str = "./output",
    min_count: int = 10,
    min_samples: int = 3,
    transcript_to_gene_csv: str = "",
) -> str:
    """
    Filter low-expression genes and produce a log2(CPM+1) normalized expression matrix.

    Args:
        counts_csv: Path to the raw counts CSV (rows = genes, columns = samples).
        output_dir: Directory to save the filtered and normalized matrices.
        min_count: Minimum count a gene must reach in at least `min_samples` samples.
        min_samples: Number of samples that must satisfy the count threshold.
        transcript_to_gene_csv: Optional two-column transcript-to-gene mapping. When
            supplied, transcript rows are aggregated to gene rows before filtering.

    Returns:
        A summary of how many genes were kept and the paths to the output files.
    """
    os.makedirs(output_dir, exist_ok=True)
    try:
        print(f"Loading counts from {counts_csv} ...")
        # sep=None lets csv.Sniffer auto-detect comma vs tab — GEO supplementary
        # files are often .tsv/.txt and would otherwise read as a single column.
        counts_df = pd.read_csv(counts_csv, index_col=0, sep=None, engine="python")
        raw_df = counts_df  # keep the string columns before numeric coercion drops them

        base = os.path.splitext(os.path.basename(counts_csv))[0]

        # Drop columns that are entirely non-numeric — GEO counts files sometimes
        # mix gene-annotation columns (gene_name, gene_biotype) in with sample counts.
        counts_df = counts_df.apply(pd.to_numeric, errors="coerce")
        non_numeric = counts_df.columns[counts_df.isna().all(axis=0)].tolist()
        if non_numeric:
            print(f"   Dropping {len(non_numeric)} non-numeric columns (likely annotations): {non_numeric}")
            # Before discarding them, salvage a gene-symbol column into an id->symbol sidecar so
            # downstream GSEA can map the integer/feature-ID index back to symbols (TALON etc).
            sym_col = _pick_symbol_column(raw_df, non_numeric)
            if sym_col:
                id2sym = raw_df[sym_col].astype(str)
                id2sym.index = id2sym.index.astype(str)
                id2sym = id2sym[id2sym.str.strip().ne("") & id2sym.str.lower().ne("nan")]
                if len(id2sym):
                    map_path = os.path.join(output_dir, f"{base}_id2symbol.csv")
                    id2sym.rename("symbol").to_csv(map_path)
                    print(f"   Saved id->symbol map ({len(id2sym)} genes, from '{sym_col}') to {map_path}")
            counts_df = counts_df.drop(columns=non_numeric)
        counts_df = counts_df.fillna(0)

        if transcript_to_gene_csv:
            from tools.omics_semantics import aggregate_transcripts_to_genes
            mapping = pd.read_csv(transcript_to_gene_csv, sep=None, engine="python")
            if mapping.shape[1] < 2:
                raise ValueError("transcript_to_gene_csv must contain at least two columns")
            transcript_col, gene_col = mapping.columns[:2]
            tx_to_gene = dict(zip(mapping[transcript_col].astype(str), mapping[gene_col].astype(str)))
            counts_df = aggregate_transcripts_to_genes(counts_df, tx_to_gene, method="sum")
            print(f"   Aggregated transcript rows to {counts_df.shape[0]} gene rows")

        n_genes_in = counts_df.shape[0]
        n_samples = counts_df.shape[1]
        print(f"   Input: {n_genes_in} genes x {n_samples} samples")

        keep_mask = (counts_df >= min_count).sum(axis=1) >= min_samples
        filtered = counts_df.loc[keep_mask]
        n_genes_kept = filtered.shape[0]
        print(f"   After filtering: {n_genes_kept} genes kept "
              f"({n_genes_in - n_genes_kept} dropped)")

        lib_size = filtered.sum(axis=0).replace(0, np.nan)
        cpm = filtered.divide(lib_size, axis=1) * 1e6
        normalized = np.log2(cpm + 1)
        normalized = normalized.fillna(0)

        filtered_path = os.path.join(output_dir, f"{base}_filtered.csv")
        normalized_path = os.path.join(output_dir, f"{base}_normalized.csv")
        filtered.to_csv(filtered_path)
        normalized.to_csv(normalized_path)

        return (f"Preprocessing completed.\n"
                f"- Genes in: {n_genes_in}, kept: {n_genes_kept}, dropped: {n_genes_in - n_genes_kept}\n"
                f"- Filter rule: count >= {min_count} in at least {min_samples} samples\n"
                f"- Normalization: log2(CPM + 1)\n"
                f"- Filtered counts saved to: {filtered_path}\n"
                f"- Normalized matrix saved to: {normalized_path}")
    except Exception as e:
        return f"Preprocessing failed. Error: {str(e)}"
