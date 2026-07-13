"""req #2 — single-cell RNA-seq support via PSEUDOBULK aggregation.

Why pseudobulk (the data-level reason): a scRNA matrix is genes x CELLS (thousands–millions of
cells), with per-cell metadata saying which biological SAMPLE (animal/donor) and which CELL TYPE
each cell is. You cannot run DESeq2/edgeR per-cell: cells from one animal are pseudoreplicates, so
treating n=10,000 cells as n=10,000 samples inflates significance massively (the well-known
single-cell DE false-discovery problem, Squair et al. 2021). The robust, consensus best-practice is
to SUM raw counts within each (sample x cell-type) group -> a handful of "pseudobulk samples", one
expression profile per animal per cell type. That collapses back to a genes x sample matrix with
TRUE biological replicates, which our existing bulk DA machinery (DESeq2/edgeR/limma-voom + GSEA)
consumes unchanged, run once PER CELL TYPE.

Scope (mirrors the proteomics decision — DA layer only): matrix + per-cell annotation IN, pseudobulk
DA OUT. We do NOT do cell calling, QC filtering, clustering, or cell-type annotation (those are
upstream scanpy/Seurat steps); we assume the deposited per-cell cell-type labels, which authors
almost always provide. Pseudobulk SUMS are integer counts -> DESeq2/edgeR/limma-voom are all valid
(matrix_type='raw_counts'); 'all' gives the multi-method consensus exactly as for bulk.

Inputs supported: .h5ad (AnnData, X = cells x genes), a 10x MTX directory (matrix.mtx[.gz] +
barcodes + features), or a dense genes x cells CSV/TSV. Per-cell metadata comes from adata.obs
(.h5ad) or a separate CSV keyed by cell barcode.

Fail-loud: (sample x cell-type) groups with too few cells are DROPPED with an explicit reason (a
pseudobulk profile from 3 cells is noise); cell types without >=min_samples_per_group pseudobulk
samples in BOTH conditions are SKIPPED for DE (can't form a 2-group contrast) — both are logged,
never silently absorbed.
"""

import os
import gzip
import glob

import numpy as np
import pandas as pd


def _safe_name(s: str) -> str:
    return "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in str(s)).strip("_") or "x"


def _read_mtx_dir(mtx_dir: str):
    """10x triple -> (X cells x genes csr, gene_names list, barcodes list). 10x stores genes x cells."""
    import scipy.io
    import scipy.sparse as sp

    def _find(*names):
        for n in names:
            for cand in (os.path.join(mtx_dir, n), os.path.join(mtx_dir, n + ".gz")):
                if os.path.isfile(cand):
                    return cand
        return None

    mtx = _find("matrix.mtx")
    feats = _find("features.tsv", "genes.tsv")
    bc = _find("barcodes.tsv")
    if not (mtx and feats and bc):
        raise FileNotFoundError(f"10x triple incomplete in {mtx_dir} (need matrix.mtx + features/genes.tsv + barcodes.tsv)")
    op = (lambda p: gzip.open(p, "rt")) if mtx.endswith(".gz") else (lambda p: open(p))
    with op(mtx) as fh:
        m = scipy.io.mmread(fh)                  # genes x cells
    gene_names = [ln.split("\t")[1] if "\t" in ln else ln.strip()
                  for ln in (gzip.open(feats, "rt") if feats.endswith(".gz") else open(feats))]
    barcodes = [ln.strip().split("\t")[0]
                for ln in (gzip.open(bc, "rt") if bc.endswith(".gz") else open(bc))]
    X = sp.csr_matrix(m).T.tocsr()               # -> cells x genes
    return X, [g.strip() for g in gene_names], barcodes


def _load_scrna(matrix_path: str, cell_metadata_path: str = ""):
    """Return (X cells x genes [sparse or ndarray], gene_names list, obs DataFrame indexed by cell)."""
    ext = os.path.splitext(matrix_path)[1].lower()
    if ext == ".h5ad":
        import anndata
        ad = anndata.read_h5ad(matrix_path)
        X = ad.X                                  # cells x genes
        gene_names = [str(g) for g in ad.var_names]
        obs = ad.obs.copy()
        obs.index = [str(i) for i in obs.index]
        if cell_metadata_path and os.path.isfile(cell_metadata_path):
            extra = pd.read_csv(cell_metadata_path, index_col=0)
            extra.index = [str(i) for i in extra.index]
            for c in extra.columns:               # external metadata columns win / augment obs
                obs[c] = extra[c].reindex(obs.index)
        return X, gene_names, obs
    if os.path.isdir(matrix_path):
        X, gene_names, barcodes = _read_mtx_dir(matrix_path)
        if not cell_metadata_path or not os.path.isfile(cell_metadata_path):
            raise ValueError("10x MTX input requires a separate cell_metadata_path (barcode-indexed).")
        obs = pd.read_csv(cell_metadata_path, index_col=0)
        obs.index = [str(i) for i in obs.index]
        obs = obs.reindex([str(b) for b in barcodes])
        return X, gene_names, obs
    # dense genes x cells CSV/TSV
    df = pd.read_csv(matrix_path, sep=None, engine="python", index_col=0)
    gene_names = [str(g) for g in df.index]
    X = df.T.to_numpy()                            # cells x genes
    if not cell_metadata_path or not os.path.isfile(cell_metadata_path):
        raise ValueError("dense-matrix input requires a separate cell_metadata_path (cell-indexed).")
    obs = pd.read_csv(cell_metadata_path, index_col=0)
    obs.index = [str(i) for i in obs.index]
    obs = obs.reindex([str(c) for c in df.columns])
    return X, gene_names, obs


def _row_sum(X, positions):
    """Sum the given integer row positions of X (sparse or ndarray) -> 1D gene vector."""
    sub = X[positions]
    s = sub.sum(axis=0)
    return np.asarray(s).ravel()


def aggregate_pseudobulk(matrix_path: str, sample_col: str, celltype_col: str,
                         condition_col: str = "", cell_metadata_path: str = "",
                         min_cells: int = 10, output_dir: str = "./output/scrna",
                         report: dict = None) -> dict:
    """Sum raw counts within each (sample x cell-type) group into pseudobulk profiles.

    Writes, per cell type, a `<celltype>_pseudobulk_counts.csv` (genes x pseudobulk-samples) and a
    `<celltype>_pseudobulk_metadata.csv` (pseudobulk-sample -> sample/celltype/condition/n_cells).
    Returns a manifest dict {celltype: {counts_csv, metadata_csv, n_pb_samples, n_cells, conditions}}.
    Groups with < min_cells cells are dropped (logged in report['dropped'])."""
    X, gene_names, obs = _load_scrna(matrix_path, cell_metadata_path)
    for col in (sample_col, celltype_col):
        if col not in obs.columns:
            raise KeyError(f"cell metadata has no column '{col}'. Available: {list(obs.columns)[:30]}")
    # obs is returned ALREADY aligned to X rows (h5ad: anndata guarantees it; mtx/dense: reindexed to
    # barcodes/columns). Capture cell-id -> X-row position BEFORE dropna so positions stay valid.
    full_pos = {cid: i for i, cid in enumerate(obs.index)}
    obs = obs.dropna(subset=[sample_col, celltype_col])

    # The pseudobulk replicate unit is (sample x condition), NOT sample alone: in PAIRED designs the
    # same donor/animal contributes cells under BOTH conditions (e.g. Kang: each patient has ctrl AND
    # stim cells). Grouping by sample alone would merge them into one ambiguous profile. We group by
    # (sample, condition) when a condition col is given; the pb id only gains a '__<condition>' suffix
    # for samples that actually span >1 condition, so the common single-condition case (and existing
    # callers) keep their plain sample-named columns.
    have_cond = bool(condition_col) and condition_col in obs.columns
    multi_cond_samples = set()
    if have_cond:
        nuniq = obs.groupby(sample_col)[condition_col].nunique()
        multi_cond_samples = set(nuniq[nuniq > 1].index)
    group_cols = [sample_col, condition_col] if have_cond else [sample_col]

    os.makedirs(output_dir, exist_ok=True)
    manifest, dropped = {}, []
    for ct, ct_obs in obs.groupby(celltype_col, sort=True):
        cols, meta_rows = {}, []
        for keys, s_obs in ct_obs.groupby(group_cols, sort=True):
            samp, cond = (keys if have_cond else (keys, ""))
            samp, cond = str(samp), str(cond)
            ncells = len(s_obs)
            if ncells < min_cells:
                dropped.append({"celltype": str(ct), "sample": samp, "condition": cond,
                                "n_cells": ncells, "reason": f"< min_cells ({min_cells})"})
                continue
            positions = [full_pos[c] for c in s_obs.index if c in full_pos]
            if not positions:
                continue
            vec = _row_sum(X, positions)
            pb_id = _safe_name(samp)
            if samp in multi_cond_samples:
                pb_id = f"{_safe_name(samp)}__{_safe_name(cond)}"
            cols[pb_id] = np.rint(vec).astype(np.int64)
            meta_rows.append({"pb_sample": pb_id, "sample": samp, "celltype": str(ct),
                              "condition": cond, "n_cells": ncells})
        if not cols:
            continue
        ct_safe = _safe_name(ct)
        counts_df = pd.DataFrame(cols, index=gene_names)
        counts_df.index.name = "gene"
        meta_df = pd.DataFrame(meta_rows).set_index("pb_sample")
        counts_csv = os.path.join(output_dir, f"{ct_safe}_pseudobulk_counts.csv")
        meta_csv = os.path.join(output_dir, f"{ct_safe}_pseudobulk_metadata.csv")
        counts_df.to_csv(counts_csv)
        meta_df.to_csv(meta_csv)
        manifest[str(ct)] = {
            "counts_csv": counts_csv, "metadata_csv": meta_csv,
            "n_pb_samples": len(meta_df), "n_cells": int(ct_obs.shape[0]),
            "conditions": meta_df["condition"].value_counts().to_dict() if condition_col else {},
            "celltype_safe": ct_safe,
        }
    if report is not None:
        report["dropped"] = dropped
        report["n_celltypes"] = len(manifest)
        report["genes"] = len(gene_names)
        report["cells"] = int(obs.shape[0])
    return manifest


from langchain_core.tools import tool


@tool
def run_scrna_pseudobulk_da(
    matrix_path: str,
    sample_col: str,
    celltype_col: str,
    condition_col: str,
    control_group: str,
    treatment_group: str,
    cell_metadata_path: str = "",
    organism: str = "Mouse",
    da_method: str = "deseq2",
    min_cells: int = 10,
    min_samples_per_group: int = 2,
    run_gsea: bool = True,
    output_dir: str = "./output/scrna",
) -> str:
    """Run pseudobulk differential expression on a single-cell RNA-seq dataset, ONE contrast PER CELL TYPE.

    Aggregates raw counts within each (sample x cell-type) group into pseudobulk profiles, then runs
    the bulk DA machinery (DESeq2/edgeR/limma-voom, or 'all' for the multi-method consensus) + GSEA
    per cell type. This is the robust way to do scRNA DE — per-cell tests inflate significance via
    pseudoreplication.

    Args:
        matrix_path: .h5ad file, a 10x MTX directory, or a dense genes x cells CSV/TSV.
        sample_col: per-cell metadata column naming the biological sample/donor (the replicate unit).
        celltype_col: per-cell metadata column naming the cell type (one DE run per value).
        condition_col: per-cell metadata column carrying the experimental condition.
        control_group / treatment_group: the two values in condition_col to contrast.
        cell_metadata_path: CSV (cell-barcode indexed) for MTX/dense input; ignored for .h5ad with obs.
        organism: 'Mouse' or 'Human' (for GSEA Hallmark species).
        da_method: 'deseq2' (default) | 'edger' | 'limma-voom' | 'all' (run all three + consensus).
        min_cells: drop a (sample x cell-type) group with fewer cells (unreliable pseudobulk profile).
        min_samples_per_group: a cell type needs at least this many pseudobulk samples in BOTH the
            control and treatment groups, else it is skipped for DE (can't form a 2-group contrast).
        run_gsea: also run preranked GSEA (Hallmark) on each cell type's DEG result.
        output_dir: where pseudobulk matrices + per-cell-type DEG/GSEA artifacts are written.
    """
    try:
        from tools.batch_tools import (_DecisionLog, _ALL_RAW_METHODS, _invoke_da_method,
                                        _gsea_for_deg, _run_contrast_multi)
        from tools.deseq2_tools import deg_filename

        os.makedirs(output_dir, exist_ok=True)
        agg_dir = os.path.join(output_dir, "pseudobulk")
        prep: dict = {}
        manifest = aggregate_pseudobulk(matrix_path, sample_col, celltype_col,
                                        condition_col=condition_col, cell_metadata_path=cell_metadata_path,
                                        min_cells=min_cells, output_dir=agg_dir, report=prep)
        if not manifest:
            return ("No pseudobulk profiles produced (every (sample x cell-type) group had "
                    f"< {min_cells} cells, or the metadata columns were empty). "
                    f"dropped={len(prep.get('dropped', []))}.")

        methods = list(_ALL_RAW_METHODS) if da_method == "all" else [da_method]
        multi = len(methods) > 1
        fail_log = os.path.join(output_dir, "failures.log")
        dlog = _DecisionLog(os.path.basename(matrix_path))
        dlog.record("pseudobulk", "ok", n_celltypes=prep["n_celltypes"], genes=prep["genes"],
                    cells=prep["cells"], n_dropped_groups=len(prep.get("dropped", [])),
                    min_cells=min_cells)

        rows, n_de_run = [], 0
        for ct, info in manifest.items():
            ct_out = os.path.join(output_dir, info["celltype_safe"])
            os.makedirs(ct_out, exist_ok=True)
            meta = pd.read_csv(info["metadata_csv"], index_col=0)
            nctrl = int((meta["condition"] == control_group).sum())
            ntreat = int((meta["condition"] == treatment_group).sum())
            base_row = {"celltype": ct, "n_pb_samples": info["n_pb_samples"],
                        "n_cells": info["n_cells"], "n_control": nctrl, "n_treatment": ntreat,
                        "da_method": da_method}
            if nctrl < min_samples_per_group or ntreat < min_samples_per_group:
                base_row["status"] = "skipped_too_few_samples"
                base_row["n_deg"] = None
                rows.append(base_row)
                dlog.record("contrast", "skipped", reason="too few pseudobulk samples per group",
                            celltype=ct, n_control=nctrl, n_treatment=ntreat,
                            min_samples_per_group=min_samples_per_group)
                continue

            counts_path = info["counts_csv"]
            meta_path = info["metadata_csv"]
            n_de_run += 1
            try:
                if multi:
                    res = _run_contrast_multi(methods, counts_path, counts_path, meta_path,
                                              "condition", control_group, treatment_group, ct_out,
                                              organism, "raw_counts", dlog, fail_log,
                                              info["celltype_safe"])
                    base_row["n_deg"] = res.get("n_deg")
                    base_row["per_method_deg"] = str(res.get("per_method"))
                    base_row["logfc_pairwise_r"] = str(res.get("pairwise_r"))
                    base_row["status"] = res.get("status")
                else:
                    canon = os.path.join(ct_out, deg_filename(treatment_group, control_group))
                    if os.path.exists(canon):
                        os.remove(canon)
                    print(_invoke_da_method(da_method, counts_path, counts_path, meta_path,
                                            "condition", control_group, treatment_group, ct_out)[:200])
                    if not os.path.exists(canon):
                        base_row["status"] = "deg_failed"
                        base_row["n_deg"] = None
                        rows.append(base_row)
                        continue
                    deg = pd.read_csv(canon, index_col=0)
                    base_row["n_deg"] = int((deg["padj"] < 0.05).sum()) if "padj" in deg.columns else None
                    base_row["status"] = "deg_ok"
                    if run_gsea:
                        nsig, gstatus = _gsea_for_deg(canon, organism, ct_out, dlog, fail_log,
                                                      info["celltype_safe"], f"{ct} {treatment_group} vs {control_group}")
                        base_row["n_gsea_sig"] = nsig
                        base_row["status"] = gstatus
            except Exception as e:
                base_row["status"] = f"error: {type(e).__name__}: {e}"
                base_row["n_deg"] = None
                with open(fail_log, "a", encoding="utf-8") as f:
                    f.write(f"{ct} | {type(e).__name__}: {e}\n")
            rows.append(base_row)

        summary_csv = os.path.join(output_dir, "scrna_pseudobulk_summary.csv")
        pd.DataFrame(rows).to_csv(summary_csv, index=False)
        dlog.save(os.path.join(output_dir, "decisions.json"), status="ok")

        lines = [
            f"scRNA pseudobulk DA complete: {prep['cells']} cells x {prep['genes']} genes "
            f"-> {prep['n_celltypes']} cell types ({len(prep.get('dropped', []))} low-cell groups dropped).",
            f"DA: {da_method}  |  contrast: {treatment_group} vs {control_group}  |  organism: {organism}",
            "",
        ]
        for r in rows:
            deg = r.get("n_deg")
            extra = f" [per-method {r.get('per_method_deg')}]" if multi and r.get("per_method_deg") else ""
            lines.append(f"- {r['celltype']:24s} | pb_samples={r['n_pb_samples']} "
                         f"(ctrl={r['n_control']}/treat={r['n_treatment']}) | "
                         f"{'DEG=' + str(deg) if deg is not None else r['status']}{extra}")
        lines += ["", f"summary: {summary_csv}", f"pseudobulk matrices: {agg_dir}/",
                  f"per-cell-type DEG/GSEA: {output_dir}/<celltype>/"]
        return "\n".join(lines)
    except Exception as e:
        return f"scRNA pseudobulk DA failed. Error: {type(e).__name__}: {e}"
