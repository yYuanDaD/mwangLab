"""Descriptive QC (log2 CPM PCA + per-subject correlation) to look for the paper's unnamed excluded BFRT participant."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json; os.chdir(ROOT)
import numpy as np, pandas as pd
RUN = pathlib.Path("test/experiments/large_run_pilot_20261019/runs_claude/PMID41610852/GSE312780")
m = pd.read_csv(RUN / "aligned/aligned_matrix.csv", index_col=0)
d = pd.read_csv(RUN / "aligned/design_metadata.csv", index_col=0)
m = m[m.sum(axis=1) >= 10]
lib = m.sum()
print("library sizes (M):", (lib / 1e6).round(1).to_dict())
cpm = np.log2(m / lib * 1e6 + 1)
top = cpm.loc[cpm.var(axis=1).sort_values(ascending=False).index[:2000]]
x = (top.T - top.T.mean()).values
u, s, vt = np.linalg.svd(x, full_matrices=False)
pcs = pd.DataFrame(u[:, :4] * s[:4], index=top.columns, columns=["PC1", "PC2", "PC3", "PC4"])
var = (s ** 2 / (s ** 2).sum())[:4]
pcs = pcs.join(d[["title", "subject", "arm", "time"]])
print("var explained", var.round(3))
pcs["dist_z"] = ((pcs[["PC1", "PC2"]] - pcs[["PC1", "PC2"]].median()) / pcs[["PC1", "PC2"]].std()).pow(2).sum(axis=1).pow(0.5)
print(pcs.sort_values("dist_z", ascending=False).round(2).to_string())
corr = cpm.corr(method="pearson")
mean_corr = ((corr.sum() - 1) / (len(corr) - 1)).rename("mean_r")
print(mean_corr.to_frame().join(d[["title"]]).sort_values("mean_r").head(8).to_string())
out = RUN / "qc"; out.mkdir(exist_ok=True)
pcs.join(mean_corr).to_csv(out / "qc_pca_scores.csv")
json.dump({"var_explained": var.tolist(), "n_genes": int(len(m)), "top_var_genes": 2000,
           "transform": "log2(CPM+1) of genes with >=10 total counts"}, open(out / "qc_pca_summary.json", "w"), indent=1)
