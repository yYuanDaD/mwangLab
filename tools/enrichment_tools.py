"""GO and KEGG enrichment analysis on a DESeq2 DEG result file.

Uses gseapy.enrichr (queries the Enrichr API, no local DB needed). Ensembl
gene IDs are converted to gene symbols via mygene before submission.
"""

import os
import re

import pandas as pd
import gseapy as gp
import mygene


_ORGANISM_GENE_SETS = {
    "Mouse": [
        "GO_Biological_Process_2023",
        "GO_Molecular_Function_2023",
        "GO_Cellular_Component_2023",
        "KEGG_2019_Mouse",
    ],
    "Human": [
        "GO_Biological_Process_2023",
        "GO_Molecular_Function_2023",
        "GO_Cellular_Component_2023",
        "KEGG_2021_Human",
    ],
}

_ENSEMBL_PATTERN = re.compile(r"^ENS[A-Z]*G\d+(\.\d+)?$")


def _looks_ensembl(ids: list[str]) -> bool:
    sample = [str(x) for x in ids[:20]]
    if not sample:
        return False
    return sum(1 for x in sample if _ENSEMBL_PATTERN.match(x)) >= len(sample) * 0.8


_NUMERIC_ID_PATTERN = re.compile(r"^\d+$")


def _looks_numeric_ids(ids: list[str]) -> bool:
    """True if the index is mostly bare integers (e.g. TALON gene_IDs / row ids).
    Such IDs are neither Ensembl nor gene symbols, so GSEA against a symbol-keyed
    Hallmark library would find zero overlap — they must be mapped to symbols first."""
    sample = [str(x) for x in ids[:50]]
    if not sample:
        return False
    return sum(1 for x in sample if _NUMERIC_ID_PATTERN.match(x)) >= len(sample) * 0.8


def _load_id_symbol_map(map_csv: str) -> dict:
    """Load an id->symbol sidecar (written by preprocess_counts) as {str(id): symbol}.
    The sidecar has the matrix row id as index (col 0) and a 'symbol' column."""
    try:
        m = pd.read_csv(map_csv, index_col=0)
        col = "symbol" if "symbol" in m.columns else m.columns[0]
        out = {}
        for k, v in m[col].items():
            s = str(v).strip()
            if s and s.lower() != "nan":
                out[str(k)] = s
        return out
    except Exception:
        return {}


def _discover_id_symbol_map(deg_csv: str) -> str:
    """Find an *_id2symbol.csv sidecar in the DEG file's directory (one matrix per
    study dir, so the first match is unambiguous). Returns '' if none."""
    import glob as _glob
    d = os.path.dirname(os.path.abspath(deg_csv))
    hits = sorted(_glob.glob(os.path.join(d, "*_id2symbol.csv")))
    return hits[0] if hits else ""


# ---- cost caches: GMT + Ensembl->symbol are deterministic & re-queried across a cohort. ----

_GMT_CACHE: dict = {}                  # (category, dbver) -> {set_name: [genes]}


def _get_hallmark_gmt(category: str, dbver: str) -> dict:
    """MSigDB Hallmark GMT, cached per (category, dbver) for the process. The collection is
    version-pinned/immutable, so N same-species GSEA runs in a cohort fetch it ONCE, not N times.
    Empty/failed fetches are NOT cached (so a transient network failure can retry)."""
    key = (category, dbver)
    cached = _GMT_CACHE.get(key)
    if cached:
        return cached
    gmt = gp.Msigdb().get_gmt(category=category, dbver=dbver)
    if gmt:
        _GMT_CACHE[key] = gmt
    return gmt


_SYMBOL_CACHE: dict = {}               # (ensembl_no_version, species_lower) -> symbol or None


def _query_symbols(cleaned: list[str], species: str) -> dict:
    """{version-stripped Ensembl id -> symbol} via MyGene, cached per (id, species). Only the
    IDs not already cached are sent to MyGene; misses are cached as None so notfound IDs aren't
    re-queried. Deterministic mapping -> safe to memoize across studies in a cohort."""
    sp = species.lower()
    miss = [c for c in dict.fromkeys(cleaned) if (c, sp) not in _SYMBOL_CACHE]
    if miss:
        res = mygene.MyGeneInfo().querymany(
            miss, scopes="ensembl.gene", fields="symbol", species=sp,
            as_dataframe=False, verbose=False)
        got = {}
        for r in res:
            q, sym = r.get("query"), r.get("symbol")
            if q is not None and sym:
                got[q] = sym               # last-wins on duplicate hits (matches prior behavior)
        for c in miss:
            _SYMBOL_CACHE[(c, sp)] = got.get(c)
    return {c: _SYMBOL_CACHE[(c, sp)] for c in cleaned if _SYMBOL_CACHE.get((c, sp))}


def _ensembl_to_symbol(ensembl_ids: list[str], species: str) -> list[str]:
    """Strip version suffix, query MyGene.info (cached), return unique symbols in input order."""
    cleaned = [eid.split(".")[0] for eid in ensembl_ids]
    m = _query_symbols(cleaned, species)
    symbols = []
    for c in cleaned:
        sym = m.get(c)
        if sym and sym not in symbols:
            symbols.append(sym)
    return symbols


from langchain_core.tools import tool


@tool
def run_enrichment_analysis(
    deg_csv: str,
    organism: str = "Mouse",
    padj_cutoff: float = 0.05,
    log2fc_cutoff: float = 1.0,
    direction: str = "all",
    top_n: int = 10,
    output_dir: str = "./output",
) -> str:
    """
    Run GO (BP/MF/CC) and KEGG enrichment on a DEG result file produced by run_deseq2_analysis.

    Args:
        deg_csv: Path to a DEG CSV file (must have 'padj' and 'log2FoldChange' columns; index = gene IDs).
        organism: 'Mouse' or 'Human'. Determines which KEGG library is queried and which species is used for ID conversion.
        padj_cutoff: Maximum adjusted p-value for a gene to be considered significant. Default 0.05.
        log2fc_cutoff: Minimum |log2 fold change| for a gene to be considered significant. Default 1.0.
        direction: 'up', 'down', or 'all'. Which DEGs to submit for enrichment.
        top_n: Number of top enriched terms per library to include in the returned summary.
        output_dir: Directory where per-library result CSVs are written.
    """
    try:
        if organism not in _ORGANISM_GENE_SETS:
            return f"Error: organism must be 'Mouse' or 'Human', got '{organism}'."
        if direction not in ("up", "down", "all"):
            return f"Error: direction must be 'up', 'down', or 'all', got '{direction}'."

        df = pd.read_csv(deg_csv, index_col=0)
        for col in ("padj", "log2FoldChange"):
            if col not in df.columns:
                return f"Error: DEG file is missing required column '{col}'."

        sig = df.dropna(subset=["padj", "log2FoldChange"])
        sig = sig[sig["padj"] < padj_cutoff]
        if direction == "up":
            sig = sig[sig["log2FoldChange"] > log2fc_cutoff]
        elif direction == "down":
            sig = sig[sig["log2FoldChange"] < -log2fc_cutoff]
        else:
            sig = sig[sig["log2FoldChange"].abs() > log2fc_cutoff]

        if sig.empty:
            return (f"No significant DEGs found with padj < {padj_cutoff} and "
                    f"|log2FC| > {log2fc_cutoff} (direction={direction}). "
                    f"Cannot run enrichment.")

        gene_ids = sig.index.astype(str).tolist()

        if _looks_ensembl(gene_ids):
            print(f"Detected Ensembl IDs ({len(gene_ids)} genes), converting to symbols via MyGene.info...")
            gene_list = _ensembl_to_symbol(gene_ids, species=organism)
            if not gene_list:
                return "Error: failed to convert any Ensembl IDs to gene symbols. Check organism setting."
            print(f"Converted to {len(gene_list)} unique symbols.")
        else:
            gene_list = list(dict.fromkeys(gene_ids))
            print(f"Using {len(gene_list)} gene IDs as-is (do not look like Ensembl).")

        if len(gene_list) < 5:
            return (f"Only {len(gene_list)} valid genes after filtering / ID conversion. "
                    f"Enrichment requires at least ~5 genes for meaningful results.")

        os.makedirs(output_dir, exist_ok=True)
        base = os.path.splitext(os.path.basename(deg_csv))[0]
        gene_sets = _ORGANISM_GENE_SETS[organism]

        print(f"Running Enrichr against {len(gene_sets)} libraries for {len(gene_list)} {organism} genes...")
        enr = gp.enrichr(
            gene_list=gene_list,
            gene_sets=gene_sets,
            organism=organism.lower(),
            outdir=None,
            no_plot=True,
        )

        results = enr.results
        if results is None or results.empty:
            return "Enrichr returned no results. Possible network issue or no enriched terms."

        summary_lines = [
            f"Enrichment analysis complete for {len(gene_list)} {organism} genes "
            f"(direction={direction}, padj<{padj_cutoff}, |log2FC|>{log2fc_cutoff}).",
            "",
        ]
        saved_files = []
        for lib in gene_sets:
            lib_df = results[results["Gene_set"] == lib].copy()
            if lib_df.empty:
                summary_lines.append(f"### {lib}: no terms returned.")
                continue
            lib_df = lib_df.sort_values("Adjusted P-value")
            out_path = os.path.join(output_dir, f"{base}_{lib}.csv")
            lib_df.to_csv(out_path, index=False)
            saved_files.append(out_path)

            summary_lines.append(f"### {lib} — top {min(top_n, len(lib_df))} terms (sorted by adjusted p):")
            top = lib_df.head(top_n)[["Term", "Adjusted P-value", "Overlap", "Genes"]]
            for _, row in top.iterrows():
                summary_lines.append(
                    f"- {row['Term']} | padj={row['Adjusted P-value']:.2e} | "
                    f"overlap={row['Overlap']} | genes={row['Genes'][:80]}"
                )
            summary_lines.append("")

        summary_lines.append(f"Saved {len(saved_files)} per-library CSVs to {output_dir}/.")
        return "\n".join(summary_lines)

    except Exception as e:
        return f"Enrichment analysis failed. Error: {type(e).__name__}: {e}"


def _ensembl_to_symbol_map(ensembl_ids: list[str], species: str) -> dict[str, str]:
    """Map version-stripped Ensembl IDs to gene symbols (cached; keeps the per-ID mapping
    instead of collapsing to a unique list like _ensembl_to_symbol)."""
    cleaned = [eid.split(".")[0] for eid in ensembl_ids]
    return _query_symbols(cleaned, species)


@tool
def run_gsea_analysis(
    deg_csv: str,
    organism: str = "Mouse",
    ranking_metric: str = "stat",
    top_n: int = 10,
    output_dir: str = "./output",
    id_symbol_map_csv: str = "",
) -> str:
    """
    Run GSEA (preranked) on a DESeq2 DEG result file against the MSigDB Hallmark gene sets.

    Unlike run_enrichment_analysis (ORA), GSEA uses the FULL ranked gene list — no padj or
    log2FC cutoff — and detects coordinated changes across pathway members. Run this in
    addition to ORA when you want to catch pathways with subtle but coherent shifts.

    Args:
        deg_csv: Path to a DEG CSV from run_deseq2_analysis (needs the ranking_metric column).
        organism: 'Mouse' or 'Human'. Selects the species-specific Hallmark library
            (mouse symbols vs. human symbols — no cross-species mapping needed).
        ranking_metric: Column to rank genes by. Default 'stat' (DESeq2 Wald statistic, recommended).
            Alternatives in the DEG file: 'log2FoldChange'.
        top_n: Number of top enriched terms per direction (up/down) to include in the summary.
        output_dir: Directory where the full results CSV is written.
        id_symbol_map_csv: Optional path to an id->symbol sidecar (preprocess_counts writes
            '<base>_id2symbol.csv' when the raw matrix carried a gene-name column). Needed when
            the DEG index is bare integer feature IDs (e.g. TALON gene_IDs) rather than symbols
            or Ensembl IDs. If left empty, an '*_id2symbol.csv' in the DEG file's directory is
            auto-discovered.
    """
    try:
        if organism not in ("Mouse", "Human"):
            return f"Error: organism must be 'Mouse' or 'Human', got '{organism}'."

        df = pd.read_csv(deg_csv, index_col=0)
        if ranking_metric not in df.columns:
            return (f"Error: ranking column '{ranking_metric}' not in DEG file. "
                    f"Available columns: {list(df.columns)}")

        ranked = df[[ranking_metric]].dropna().copy()
        ranked.index = ranked.index.astype(str)

        gene_ids = ranked.index.tolist()
        if _looks_ensembl(gene_ids):
            print(f"Detected Ensembl IDs ({len(gene_ids)} genes), converting to symbols via MyGene.info...")
            ens_to_sym = _ensembl_to_symbol_map(gene_ids, species=organism)
            if not ens_to_sym:
                return "Error: failed to convert any Ensembl IDs to gene symbols. Check organism setting."
            cleaned = [eid.split(".")[0] for eid in ranked.index]
            ranked["_symbol"] = [ens_to_sym.get(c) for c in cleaned]
            ranked = ranked.dropna(subset=["_symbol"])
            # On duplicate symbols (multiple Ensembl IDs -> one symbol), keep the row
            # with the largest |metric| so the strongest signal wins.
            ranked["_abs"] = ranked[ranking_metric].abs()
            ranked = ranked.sort_values("_abs", ascending=False).drop_duplicates("_symbol")
            ranked = ranked.set_index("_symbol")[[ranking_metric]]
            print(f"Converted to {len(ranked)} unique gene symbols.")
        elif _looks_numeric_ids(gene_ids):
            # Bare integer feature IDs (e.g. TALON gene_IDs) — neither symbols nor Ensembl.
            # Map them to symbols via the sidecar preprocess_counts dropped them into.
            map_csv = id_symbol_map_csv or _discover_id_symbol_map(deg_csv)
            if not map_csv:
                return ("Error: DEG index looks like bare integer feature IDs (e.g. TALON "
                        "gene_IDs), not gene symbols or Ensembl IDs, and no id->symbol sidecar "
                        "('*_id2symbol.csv') was found next to the DEG file. GSEA cannot map "
                        "these to the symbol-keyed Hallmark library. Re-run preprocess_counts on "
                        "a matrix that includes a gene-name column, or pass id_symbol_map_csv.")
            id2sym = _load_id_symbol_map(map_csv)
            if not id2sym:
                return f"Error: id->symbol sidecar '{map_csv}' was empty or unreadable."
            print(f"Detected integer feature IDs ({len(gene_ids)} genes); mapping to symbols "
                  f"via {os.path.basename(map_csv)} ...")
            ranked["_symbol"] = [id2sym.get(i) for i in ranked.index]
            ranked = ranked.dropna(subset=["_symbol"])
            # Same dedup rule as the Ensembl path: on duplicate symbols keep the strongest |metric|.
            ranked["_abs"] = ranked[ranking_metric].abs()
            ranked = ranked.sort_values("_abs", ascending=False).drop_duplicates("_symbol")
            ranked = ranked.set_index("_symbol")[[ranking_metric]]
            print(f"Mapped to {len(ranked)} unique gene symbols.")
        elif ranked.index.duplicated().any():
            ranked["_abs"] = ranked[ranking_metric].abs()
            ranked = ranked.sort_values("_abs", ascending=False)
            ranked = ranked[~ranked.index.duplicated(keep="first")][[ranking_metric]]

        if len(ranked) < 100:
            return (f"Only {len(ranked)} valid genes after filtering / ID conversion. "
                    f"GSEA needs at least a few thousand ranked genes for meaningful results.")

        ranked = ranked.sort_values(ranking_metric, ascending=False)
        rnk = ranked.reset_index()
        rnk.columns = ["gene", "score"]

        # Mouse hallmark is 'mh.all' (mouse-symbol GMT); human is 'h.all'.
        # dbver names follow MSigDB releases (see Msigdb().list_dbver()).
        if organism == "Mouse":
            category, dbver = "mh.all", "2024.1.Mm"
        else:
            category, dbver = "h.all", "2024.1.Hs"
        print(f"Fetching MSigDB Hallmark library ({category}, {dbver})...")
        try:
            hallmark = _get_hallmark_gmt(category, dbver)
        except Exception as e:
            return f"Failed to fetch MSigDB Hallmark library ({category}, {dbver}): {type(e).__name__}: {e}"
        if not hallmark:
            return f"MSigDB Hallmark library ({category}, {dbver}) returned no gene sets."

        print(f"Running GSEA prerank: {len(ranked)} ranked genes vs. {len(hallmark)} Hallmark sets...")
        pre_res = gp.prerank(
            rnk=rnk,
            gene_sets=hallmark,
            min_size=15,
            max_size=500,
            permutation_num=1000,
            outdir=None,
            seed=42,
            verbose=False,
        )

        results = pre_res.res2d
        if results is None or results.empty:
            return "GSEA returned no results (possibly too few overlapping genes with Hallmark sets)."

        os.makedirs(output_dir, exist_ok=True)
        base = os.path.splitext(os.path.basename(deg_csv))[0]
        out_path = os.path.join(output_dir, f"{base}_GSEA_Hallmark.csv")
        results_sorted = results.sort_values("NES", ascending=False)
        results_sorted.to_csv(out_path, index=False)

        up = results_sorted[results_sorted["NES"] > 0].head(top_n)
        down = results_sorted[results_sorted["NES"] < 0].sort_values("NES").head(top_n)
        sig_count = int((results_sorted["FDR q-val"] < 0.25).sum())

        lines = [
            f"GSEA complete on {len(ranked)} {organism} genes ranked by '{ranking_metric}'.",
            f"{len(hallmark)} Hallmark sets tested, {sig_count} significant at FDR q < 0.25.",
            "",
            f"### Top {len(up)} UP (NES > 0, enriched in treatment):",
        ]
        for _, row in up.iterrows():
            lines.append(
                f"- {row['Term']} | NES={row['NES']:.2f} | "
                f"NOM p={row['NOM p-val']:.2e} | FDR q={row['FDR q-val']:.2e}"
            )
        lines.append("")
        lines.append(f"### Top {len(down)} DOWN (NES < 0, depleted in treatment):")
        for _, row in down.iterrows():
            lines.append(
                f"- {row['Term']} | NES={row['NES']:.2f} | "
                f"NOM p={row['NOM p-val']:.2e} | FDR q={row['FDR q-val']:.2e}"
            )
        lines.append("")
        lines.append(f"Full results saved to: {out_path}")
        return "\n".join(lines)

    except Exception as e:
        return f"GSEA analysis failed. Error: {type(e).__name__}: {e}"
