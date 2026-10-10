import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from langchain_core.tools import tool


_METADATA_SIGNATURE_COLUMNS = {
    "geo_accession", "title", "source_name_ch1", "organism_ch1",
    "submission_date", "platform_id", "library_strategy",
}


def _looks_like_metadata(df: pd.DataFrame) -> list:
    """Return the list of metadata-signature columns present in df, if any.
    A non-empty result means the file is almost certainly a GEO metadata
    table, not a counts/expression matrix."""
    return [c for c in df.columns if c in _METADATA_SIGNATURE_COLUMNS]


def _load_expression_matrix(path: str) -> pd.DataFrame:
    """Load an expression CSV (rows = genes, columns = samples) as numeric.

    Drops columns that are entirely non-numeric (e.g. gene annotation columns
    like 'gene_name', 'gene_biotype' that some GEO files mix in alongside
    sample counts).
    """
    df = pd.read_csv(path, index_col=0, sep=None, engine="python")
    coerced = df.apply(pd.to_numeric, errors="coerce")
    non_numeric = coerced.columns[coerced.isna().all(axis=0)].tolist()
    if non_numeric:
        print(f"   Dropping {len(non_numeric)} non-numeric columns (likely annotations): {non_numeric}")
        coerced = coerced.drop(columns=non_numeric)
    return coerced.fillna(0)


def _reject_if_metadata(path: str) -> str:
    """Return an error message if the CSV at `path` looks like GEO metadata,
    or empty string if it looks like a counts/expression matrix."""
    try:
        head = pd.read_csv(path, index_col=0, nrows=5, sep=None, engine="python")
    except Exception:
        return ""
    sig = _looks_like_metadata(head)
    if sig:
        return (f"This file looks like GEO sample metadata, not a counts/expression matrix "
                f"(it has metadata columns {sig}). "
                f"Pass the raw counts file (e.g. *_raw_data.csv or *_Counts.csv) instead. "
                f"If you need to inspect the metadata file's groupings, use inspect_metadata.")
    return ""


def _align_metadata(expr_df: pd.DataFrame, metadata_df: pd.DataFrame) -> tuple:
    """Intersect samples between expression columns and metadata index, with
    smart alignment fallback (substring + token-overlap + LLM) when names diverge."""
    # pandas infers all-numeric sample labels as integers on one side and
    # strings on the other (common for Salmon/Kallisto exports).  Sample IDs
    # are identifiers, so compare them in a single representation before
    # invoking the semantic fallback.
    expr_df = expr_df.copy()
    expr_df.columns = expr_df.columns.astype(str)
    metadata_df = metadata_df.copy()
    metadata_df.index = metadata_df.index.astype(str)
    common = expr_df.columns.intersection(metadata_df.index)
    if len(common) == 0:
        from tools.llm_helpers import align_samples_with_llm_fallback
        mapping, _ = align_samples_with_llm_fallback(expr_df.columns.tolist(), metadata_df)
        if mapping:
            metadata_df = metadata_df.rename(index=mapping)
            metadata_df = metadata_df[~metadata_df.index.duplicated(keep="first")]
            common = expr_df.columns.intersection(metadata_df.index)
    return expr_df.loc[:, common], metadata_df.loc[common]


def _restrict_to_metadata_samples(expr_df: pd.DataFrame, metadata_csv: str) -> tuple:
    """If metadata_csv is given, filter expr_df columns to those that match
    a sample in the metadata. Returns (filtered_expr, dropped_columns)."""
    if not metadata_csv:
        return expr_df, []
    metadata = pd.read_csv(metadata_csv, index_col=0)
    aligned, _ = _align_metadata(expr_df, metadata)
    dropped = [c for c in expr_df.columns if c not in aligned.columns]
    return aligned, dropped


@tool
def run_pca(
    expression_csv: str,
    metadata_csv: str,
    group_column: str,
    output_dir: str = "./output",
    n_components: int = 2,
) -> str:
    """
    Run PCA on a normalized expression matrix and save a scatter plot colored by group.

    Args:
        expression_csv: Path to a normalized expression CSV (rows = genes, columns = samples).
            Use the *_normalized.csv produced by preprocess_counts for best results.
        metadata_csv: Path to the metadata CSV (rows = samples).
        group_column: Column in the metadata used to color the points.
        output_dir: Directory to save the PCA plot and component scores.
        n_components: Number of principal components to compute (>=2).
    """
    os.makedirs(output_dir, exist_ok=True)
    try:
        expr = _load_expression_matrix(expression_csv)
        metadata = pd.read_csv(metadata_csv, index_col=0)
        expr, metadata = _align_metadata(expr, metadata)
        if expr.shape[1] < 2:
            return "PCA failed: fewer than 2 samples after aligning expression and metadata."
        if group_column not in metadata.columns:
            return f"PCA failed: column '{group_column}' not in metadata. Available: {list(metadata.columns)}"

        # PCA expects samples as rows
        X = expr.T.values
        n_components = max(2, min(n_components, min(X.shape) - 1))
        pca = PCA(n_components=n_components)
        scores = pca.fit_transform(X)
        var_ratio = pca.explained_variance_ratio_ * 100

        scores_df = pd.DataFrame(
            scores,
            index=expr.columns,
            columns=[f"PC{i+1}" for i in range(n_components)],
        )
        scores_df[group_column] = metadata[group_column].values

        base = os.path.splitext(os.path.basename(expression_csv))[0]
        scores_path = os.path.join(output_dir, f"{base}_pca_scores.csv")
        plot_path = os.path.join(output_dir, f"{base}_pca.png")
        scores_df.to_csv(scores_path)

        fig, ax = plt.subplots(figsize=(7, 6))
        groups = scores_df[group_column].astype(str).unique()
        cmap = plt.get_cmap("tab10")
        for i, g in enumerate(groups):
            sub = scores_df[scores_df[group_column].astype(str) == g]
            ax.scatter(sub["PC1"], sub["PC2"], label=g, s=80, color=cmap(i % 10), edgecolor="black")
        for sample, row in scores_df.iterrows():
            ax.annotate(str(sample), (row["PC1"], row["PC2"]), fontsize=7, alpha=0.7)
        ax.set_xlabel(f"PC1 ({var_ratio[0]:.1f}%)")
        ax.set_ylabel(f"PC2 ({var_ratio[1]:.1f}%)")
        ax.set_title(f"PCA — colored by {group_column}")
        ax.legend(loc="best", fontsize=9)
        ax.grid(alpha=0.3)
        fig.tight_layout()
        fig.savefig(plot_path, dpi=150)
        plt.close(fig)

        return (f"PCA completed.\n"
                f"- Samples: {expr.shape[1]}, components: {n_components}\n"
                f"- Variance explained: " +
                ", ".join(f"PC{i+1}={v:.1f}%" for i, v in enumerate(var_ratio)) + "\n"
                f"- Scores saved to: {scores_path}\n"
                f"- Plot saved to: {plot_path}")
    except Exception as e:
        return f"PCA failed. Error: {str(e)}"


@tool
def sample_correlation_heatmap(
    expression_csv: str,
    output_dir: str = "./output",
    method: str = "pearson",
    metadata_csv: str = "",
) -> str:
    """
    Compute a sample-sample correlation matrix and save a heatmap.

    Args:
        expression_csv: Path to a normalized expression CSV (rows = genes, columns = samples).
        output_dir: Directory to save the correlation matrix and heatmap.
        method: 'pearson' or 'spearman'.
        metadata_csv: Optional. If provided, restrict columns to samples present
            in the metadata index — useful when the CSV mixes annotation columns
            (e.g. gene_chr, gene_start) with sample counts.
    """
    os.makedirs(output_dir, exist_ok=True)
    try:
        reject = _reject_if_metadata(expression_csv)
        if reject:
            return f"Sample correlation aborted: {reject}"
        expr = _load_expression_matrix(expression_csv)
        expr, dropped = _restrict_to_metadata_samples(expr, metadata_csv)
        if dropped:
            print(f"   Restricted to metadata samples; dropped {len(dropped)} non-sample columns: {dropped}")
        if expr.shape[1] < 2:
            return (f"Correlation failed: only {expr.shape[1]} sample column(s) remain after filtering. "
                    f"Check that '{expression_csv}' is an expression matrix and that metadata_csv (if given) matches it.")
        if method not in ("pearson", "spearman"):
            return f"Correlation failed: method must be 'pearson' or 'spearman', got '{method}'."

        corr = expr.corr(method=method)
        if corr.empty or len(corr) < 2:
            return "Correlation failed: correlation matrix is empty after filtering."
        base = os.path.splitext(os.path.basename(expression_csv))[0]
        matrix_path = os.path.join(output_dir, f"{base}_corr_{method}.csv")
        plot_path = os.path.join(output_dir, f"{base}_corr_{method}.png")
        corr.to_csv(matrix_path)

        fig, ax = plt.subplots(figsize=(max(6, 0.4 * len(corr) + 4), max(5, 0.4 * len(corr) + 3)))
        im = ax.imshow(corr.values, cmap="viridis", vmin=corr.values.min(), vmax=1.0)
        ax.set_xticks(range(len(corr)))
        ax.set_yticks(range(len(corr)))
        ax.set_xticklabels(corr.columns, rotation=90, fontsize=8)
        ax.set_yticklabels(corr.index, fontsize=8)
        ax.set_title(f"Sample-sample {method} correlation")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        fig.tight_layout()
        fig.savefig(plot_path, dpi=150)
        plt.close(fig)

        # Flag unusually low correlations (potential outliers); guard against empty stack
        off_diag = corr.where(~np.eye(len(corr), dtype=bool))
        stacked = off_diag.stack().dropna()
        if len(stacked) == 0:
            extreme_line = "- Lowest pairwise correlation: n/a (no off-diagonal entries)"
        else:
            worst_pair = stacked.idxmin()
            extreme_line = (f"- Lowest pairwise correlation: {stacked.min():.3f} "
                            f"between {worst_pair[0]} and {worst_pair[1]}")

        return (f"Sample correlation ({method}) completed.\n"
                f"- Matrix saved to: {matrix_path}\n"
                f"- Heatmap saved to: {plot_path}\n"
                f"{extreme_line}")
    except Exception as e:
        return f"Sample correlation failed. Error: {str(e)}"


# Sex-marker genes. Y-linked genes are expressed only when a Y chromosome is
# present (male); Xist coats the inactive X and is expressed only with two X
# chromosomes (female). Matching is case-insensitive so the same set covers
# mouse/rat (Ddx3y) and human (DDX3Y) symbols; Rps4y1 is human-specific but
# harmless to include.
_SEX_Y_MARKERS = ("Ddx3y", "Uty", "Eif2s3y", "Kdm5d", "Rps4y1")
_SEX_XIST_MARKER = "Xist"


def _normalize_sex_value(v) -> str:
    """Map a free-text metadata sex value to 'male'/'female'/'' (unknown).
    Checks 'female' before 'male' because 'female' contains the substring 'male'."""
    s = str(v).strip().lower()
    if not s or s in ("nan", "na", "none", "unknown", "n/a"):
        return ""
    if "female" in s or s in ("f", "女", "雌"):
        return "female"
    if "male" in s or s in ("m", "男", "雄"):
        return "male"
    return ""


def _detect_sex_column(metadata: pd.DataFrame) -> str:
    """Find the metadata column most likely to hold sample sex. Prefers columns
    named like sex/gender whose values actually look like sex labels."""
    for col in metadata.columns:
        if "sex" in col.lower() or "gender" in col.lower():
            vals = metadata[col].dropna().map(_normalize_sex_value)
            if (vals != "").any():
                return col
    return ""


def _match_sex_markers(expr_df: pd.DataFrame, organism: str) -> dict:
    """Map each sex-marker symbol to its row label in expr_df. Tries
    case-insensitive symbol match first, then Ensembl IDs via mygene for the
    species when the matrix is indexed by Ensembl gene IDs."""
    index = list(expr_df.index)
    lower_map = {}
    for g in index:
        lower_map.setdefault(str(g).lower(), g)
    wanted = {m.lower(): m for m in (_SEX_Y_MARKERS + (_SEX_XIST_MARKER,))}
    found = {sym: lower_map[low] for low, sym in wanted.items() if low in lower_map}
    if found:
        return found

    # Ensembl fallback: only the handful of marker symbols need conversion.
    if not any(str(g).upper().startswith("ENS") for g in index[:20]):
        return found
    ens_index = {}
    for g in index:
        ens_index.setdefault(str(g).split(".")[0], g)
    try:
        import mygene
        res = mygene.MyGeneInfo().querymany(
            list(wanted.values()), scopes="symbol", fields="ensembl.gene",
            species=organism.lower(), as_dataframe=False, verbose=False,
        )
        for r in res:
            sym, ens = r.get("query"), r.get("ensembl")
            ids = []
            if isinstance(ens, dict):
                ids = [ens.get("gene")]
            elif isinstance(ens, list):
                ids = [e.get("gene") for e in ens if isinstance(e, dict)]
            for eid in ids:
                if eid in ens_index:
                    found[sym] = ens_index[eid]
    except Exception as e:
        print(f"   mygene Ensembl marker lookup failed: {e}")
    return found


@tool
def infer_sex_from_expression(
    counts_csv: str,
    metadata_csv: str = "",
    organism: str = "Mouse",
    output_dir: str = "./output",
) -> str:
    """
    Infer each sample's biological sex from sex-marker gene expression and, when a
    metadata sex column is available, cross-check it to catch sample swaps/mislabels.

    Method: Y-linked genes (Ddx3y/Uty/Eif2s3y/Kdm5d, human RPS4Y1) are expressed
    only in males; Xist is expressed only in females. The call is a within-sample
    relative comparison, so it works on raw counts OR normalized (FPKM/TPM/log) data.

    Args:
        counts_csv: Path to an expression matrix (rows = genes, columns = samples).
        metadata_csv: Optional metadata CSV; if it has a sex/gender column, predicted
            sex is compared against it and disagreements are flagged.
        organism: 'Mouse', 'Human', or 'Rat'. Only used for the Ensembl-ID fallback.
        output_dir: Directory where the per-sample sex-check table is written.
    """
    os.makedirs(output_dir, exist_ok=True)
    try:
        reject = _reject_if_metadata(counts_csv)
        if reject:
            return f"Sex inference aborted: {reject}"
        expr = _load_expression_matrix(counts_csv)
        expr, dropped = _restrict_to_metadata_samples(expr, metadata_csv)
        if dropped:
            print(f"   Restricted to metadata samples; dropped {len(dropped)} non-sample columns: {dropped}")
        if expr.shape[1] == 0:
            return ("Sex inference failed: no sample columns remain after filtering. "
                    f"Check that '{counts_csv}' is an expression matrix (rows=genes, columns=samples).")

        found = _match_sex_markers(expr, organism)
        y_found = [s for s in _SEX_Y_MARKERS if s in found]
        xist_found = _SEX_XIST_MARKER in found
        if not y_found and not xist_found:
            return (f"Sex inference failed: none of the sex-marker genes "
                    f"({', '.join(_SEX_Y_MARKERS)}, {_SEX_XIST_MARKER}) were found in the matrix index. "
                    f"The matrix may use IDs that don't map (check organism='{organism}') or lack sex chromosomes.")

        # Put markers on a comparable per-sample log scale. Negative values mean the
        # matrix is already log-transformed; otherwise CPM-normalize then log2.
        has_neg = bool((expr.values < 0).any())
        if has_neg:
            signal = expr
        else:
            libsize = expr.sum(axis=0).replace(0, np.nan)
            signal = np.log2(expr.div(libsize, axis=1) * 1e6 + 1)

        y_signal = (signal.loc[[found[s] for s in y_found]].mean(axis=0)
                    if y_found else pd.Series(0.0, index=expr.columns))
        xist_signal = (signal.loc[found[_SEX_XIST_MARKER]]
                       if xist_found else pd.Series(0.0, index=expr.columns))
        maleness = y_signal - xist_signal

        margin = 1.0  # log2 units; the male/female marker contrast is normally several units
        def _call(m):
            if m > margin:
                return "male"
            if m < -margin:
                return "female"
            return "unknown"

        result = pd.DataFrame({
            "y_signal": y_signal.round(3),
            "xist_signal": xist_signal.round(3),
            "maleness_score": maleness.round(3),
            "predicted_sex": maleness.map(_call),
            "confidence": maleness.abs().map(lambda m: "high" if m >= 2 * margin else ("low" if m >= margin else "ambiguous")),
        })

        # Cross-check against metadata-reported sex, if available.
        n_mismatch = 0
        sex_col = ""
        if metadata_csv:
            metadata = pd.read_csv(metadata_csv, index_col=0)
            _, metadata = _align_metadata(expr, metadata)
            sex_col = _detect_sex_column(metadata)
            if sex_col:
                reported = metadata[sex_col].map(_normalize_sex_value)
                result["reported_sex"] = [reported.get(s, "") for s in result.index]
                def _agree(row):
                    if not row["reported_sex"] or row["predicted_sex"] == "unknown":
                        return "n/a"
                    return "ok" if row["predicted_sex"] == row["reported_sex"] else "MISMATCH"
                result["agreement"] = result.apply(_agree, axis=1)
                n_mismatch = int((result["agreement"] == "MISMATCH").sum())

        base = os.path.splitext(os.path.basename(counts_csv))[0]
        out_path = os.path.join(output_dir, f"{base}_sex_check.tsv")
        result.to_csv(out_path, sep="\t")

        n_male = int((result["predicted_sex"] == "male").sum())
        n_female = int((result["predicted_sex"] == "female").sum())
        n_unknown = int((result["predicted_sex"] == "unknown").sum())
        lines = [
            f"Sex inference completed on {expr.shape[1]} samples.",
            f"- Markers found: Y={y_found or 'none'}, Xist={'yes' if xist_found else 'no'}",
            f"- Predicted: {n_male} male, {n_female} female, {n_unknown} unknown/ambiguous",
        ]
        if sex_col:
            lines.append(f"- Metadata sex column: '{sex_col}'")
            if n_mismatch:
                bad = result.index[result["agreement"] == "MISMATCH"].tolist()
                lines.append(f"- WARNING: {n_mismatch} sample(s) disagree with metadata "
                             f"(possible swap/mislabel): {bad}")
            else:
                lines.append("- All confidently-predicted samples agree with metadata.")
        elif metadata_csv:
            lines.append("- No sex/gender column detected in metadata; skipped cross-check.")
        lines.append(f"- Per-sample sex-check table saved to: {out_path}")
        return "\n".join(lines)
    except Exception as e:
        return f"Sex inference failed. Error: {type(e).__name__}: {e}"


@tool
def sample_qc_summary(
    counts_csv: str,
    output_dir: str = "./output",
    detection_threshold: int = 1,
    metadata_csv: str = "",
) -> str:
    """
    Compute per-sample QC: library size, number of detected genes, and basic stats.

    Args:
        counts_csv: Path to the raw counts CSV (rows = genes, columns = samples).
        output_dir: Directory to save the per-sample QC table.
        detection_threshold: A gene is considered detected if its count is >= this value.
        metadata_csv: Optional. If provided, restrict columns to samples present
            in the metadata index — useful when the CSV mixes annotation columns
            (e.g. gene_chr, gene_start) with sample counts.
    """
    os.makedirs(output_dir, exist_ok=True)
    try:
        reject = _reject_if_metadata(counts_csv)
        if reject:
            return f"Sample QC aborted: {reject}"
        counts = _load_expression_matrix(counts_csv)
        counts, dropped = _restrict_to_metadata_samples(counts, metadata_csv)
        if dropped:
            print(f"   Restricted to metadata samples; dropped {len(dropped)} non-sample columns: {dropped}")
        if counts.shape[1] == 0:
            return ("Sample QC failed: no sample columns remain after filtering. "
                    f"Check that '{counts_csv}' is a counts matrix (rows=genes, columns=samples).")
        lib_size = counts.sum(axis=0)
        detected = (counts >= detection_threshold).sum(axis=0)
        median_count = counts.median(axis=0)
        max_count = counts.max(axis=0)

        qc = pd.DataFrame({
            "library_size": lib_size,
            "detected_genes": detected,
            "median_count": median_count,
            "max_count": max_count,
        })
        qc["pct_detected"] = (qc["detected_genes"] / counts.shape[0] * 100).round(2)

        base = os.path.splitext(os.path.basename(counts_csv))[0]
        qc_path = os.path.join(output_dir, f"{base}_sample_qc.tsv")
        qc.to_csv(qc_path, sep="\t")

        median_lib = lib_size.median()
        low = qc[qc["library_size"] < 0.5 * median_lib].index.tolist()
        outlier_msg = (f"- WARNING: low-library-size samples (<50% of median): {low}"
                       if low else "- No obvious library-size outliers.")

        return (f"Sample QC completed.\n"
                f"- Samples: {counts.shape[1]}, genes: {counts.shape[0]}\n"
                f"- Median library size: {median_lib:.0f}\n"
                f"- Median detected genes per sample: {detected.median():.0f}\n"
                f"{outlier_msg}\n"
                f"- Per-sample QC saved to: {qc_path}")
    except Exception as e:
        return f"Sample QC failed. Error: {str(e)}"
