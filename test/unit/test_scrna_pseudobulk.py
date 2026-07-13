"""Mostly-zero-cost test of #2 pseudobulk scRNA support (synthetic data, no network unless run_gsea).

Builds a synthetic scRNA dataset with a KNOWN differential signal, then checks:
  - aggregation sums are EXACT (pseudobulk = sum of that group's cells)
  - low-cell (sample x celltype) groups are dropped at min_cells
  - dense-CSV and .h5ad loaders produce the SAME pseudobulk manifest
  - per-cell-type DESeq2 recovers the planted signal: TypeA (DE planted) >> TypeB (no signal),
    TypeC skipped (treatment has too few cells -> no 2-group contrast)

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/unit/test_scrna_pseudobulk.py
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

import numpy as np
import pandas as pd
from tools.scrna_tools import aggregate_pseudobulk, run_scrna_pseudobulk_da

TMP = os.path.join("test", "output", "test_scrna")
os.makedirs(TMP, exist_ok=True)
rng = np.random.default_rng(0)

GENES = [f"Gene{i:03d}" for i in range(200)]
SIGNAL = set(GENES[:20])               # 20 genes get a 4x boost in TypeA treatment
samples = {f"ctrl{i}": "control" for i in range(1, 5)}
samples.update({f"treat{i}": "treatment" for i in range(1, 5)})
celltypes = ["TypeA", "TypeB", "TypeC"]

cell_rows, mat_cols, cell_ids = [], [], []
for samp, cond in samples.items():
    for ct in celltypes:
        # TypeC: only 3 cells in treatment samples (-> dropped -> TypeC has no treatment arm -> skipped)
        n = 3 if (ct == "TypeC" and cond == "treatment") else 40
        for k in range(n):
            cid = f"{samp}_{ct}_{k}"
            lam = rng.uniform(2, 8, size=len(GENES))
            if ct == "TypeA" and cond == "treatment":
                for gi, g in enumerate(GENES):
                    if g in SIGNAL:
                        lam[gi] *= 4.0          # planted up-regulation
            counts = rng.poisson(lam)
            mat_cols.append(counts)
            cell_ids.append(cid)
            cell_rows.append({"cell": cid, "sample": samp, "celltype": ct, "condition": cond})

X = np.array(mat_cols).T                         # genes x cells
mat = pd.DataFrame(X, index=GENES, columns=cell_ids)
mat.index.name = "gene"
matrix_csv = os.path.join(TMP, "synth_counts.csv")
meta_csv = os.path.join(TMP, "synth_cellmeta.csv")
mat.to_csv(matrix_csv)
pd.DataFrame(cell_rows).set_index("cell").to_csv(meta_csv)
print(f"synthetic: {X.shape[0]} genes x {X.shape[1]} cells, {len(samples)} samples, {len(celltypes)} cell types")

# --- 1. aggregation correctness + drop logic --------------------------------------------
rep = {}
manifest = aggregate_pseudobulk(matrix_csv, "sample", "celltype", condition_col="condition",
                                cell_metadata_path=meta_csv, min_cells=10,
                                output_dir=os.path.join(TMP, "pb_dense"), report=rep)
print("manifest cell types:", list(manifest.keys()), "| dropped groups:", len(rep["dropped"]))
# exact-sum check: TypeA / ctrl1 pseudobulk == manual sum of those cells
a_counts = pd.read_csv(manifest["TypeA"]["counts_csv"], index_col=0)
mask = (pd.DataFrame(cell_rows).set_index("cell")["sample"] == "ctrl1") & \
       (pd.DataFrame(cell_rows).set_index("cell")["celltype"] == "TypeA")
manual = mat.loc[:, mask[mask].index].sum(axis=1)
assert (a_counts["ctrl1"].values == manual.values).all(), "pseudobulk sum != manual group sum"
print("  exact-sum check OK (TypeA/ctrl1)")
# TypeC treatment cells (3 < 10) were dropped
assert any(d["celltype"] == "TypeC" and d["sample"].startswith("treat") for d in rep["dropped"]), \
    "TypeC treatment groups should have been dropped"
print("  low-cell drop OK (TypeC treatment groups dropped)")

# --- 2. .h5ad loader parity --------------------------------------------------------------
import anndata
import scipy.sparse as sp
obs = pd.DataFrame(cell_rows).set_index("cell")
ad = anndata.AnnData(X=sp.csr_matrix(X.T.astype(np.float32)),     # cells x genes
                     obs=obs, var=pd.DataFrame(index=GENES))
h5_path = os.path.join(TMP, "synth.h5ad")
ad.write_h5ad(h5_path)
rep2 = {}
manifest2 = aggregate_pseudobulk(h5_path, "sample", "celltype", condition_col="condition",
                                 min_cells=10, output_dir=os.path.join(TMP, "pb_h5ad"), report=rep2)
a2 = pd.read_csv(manifest2["TypeA"]["counts_csv"], index_col=0)
assert (a2["ctrl1"].values == a_counts["ctrl1"].values).all(), "h5ad vs dense pseudobulk mismatch"
assert set(manifest.keys()) == set(manifest2.keys()), "h5ad vs dense manifest mismatch"
print("  .h5ad loader parity OK")

# --- 3. per-cell-type DESeq2 recovers the signal (offline: run_gsea=False) ---------------
print("\nrunning pseudobulk DESeq2 per cell type...")
msg = run_scrna_pseudobulk_da.invoke({
    "matrix_path": matrix_csv, "cell_metadata_path": meta_csv,
    "sample_col": "sample", "celltype_col": "celltype", "condition_col": "condition",
    "control_group": "control", "treatment_group": "treatment",
    "organism": "Mouse", "da_method": "deseq2", "min_cells": 10,
    "run_gsea": False, "output_dir": os.path.join(TMP, "da"),
})
print(msg)
summ = pd.read_csv(os.path.join(TMP, "da", "scrna_pseudobulk_summary.csv"))
by_ct = {r["celltype"]: r for _, r in summ.iterrows()}
print("\nsummary:", {k: (v["status"], v["n_deg"]) for k, v in by_ct.items()})
assert by_ct["TypeA"]["n_deg"] >= 10, f"TypeA should recover planted signal, got {by_ct['TypeA']['n_deg']}"
assert by_ct["TypeB"]["n_deg"] <= 5, f"TypeB (no signal) should be ~0, got {by_ct['TypeB']['n_deg']}"
assert str(by_ct["TypeC"]["status"]).startswith("skipped"), f"TypeC should be skipped, got {by_ct['TypeC']['status']}"

# the planted genes should dominate TypeA's hits
deg_a = pd.read_csv(os.path.join(TMP, "da", "TypeA", "DEG_results_treatment_vs_control.csv"), index_col=0)
sig_a = deg_a[deg_a["padj"] < 0.05]
recovered = SIGNAL & set(sig_a.index)
print(f"TypeA: {len(sig_a)} DEG, {len(recovered)}/20 planted genes recovered")
assert len(recovered) >= 15, f"expected >=15 of 20 planted genes, got {len(recovered)}"

print("\nPASS — #2 pseudobulk: exact aggregation, low-cell drop, h5ad/dense parity, per-cell-type "
      "DESeq2 recovers planted signal (TypeA), null cell type clean (TypeB), too-few-samples skipped (TypeC).")
