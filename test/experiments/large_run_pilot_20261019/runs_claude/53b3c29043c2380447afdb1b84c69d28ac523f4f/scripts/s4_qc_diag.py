import sys, os, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT)); os.chdir(ROOT)
import numpy as np, pandas as pd
CD = pathlib.Path(__file__).resolve().parents[1] / "case_01"
x = pd.read_csv(CD / "aligned" / "aligned_matrix.csv", index_col=0)
x = x[~x.index.duplicated()]
m = pd.read_csv(CD / "aligned" / "design_metadata.csv", index_col=0)
cpm = np.log2(x / x.sum() * 1e6 + 1)
lab = m["grp"] + "_" + m["description"].str.extract(r"(\d+)$")[0]
genes = ["Arntl", "Dbp", "Per1", "Per2", "Nr1d1", "Nr4a3", "Nr4a1", "Fos", "Egr1", "Atf3", "Ppargc1a", "Hk2"]
tab = cpm.loc[[g for g in genes if g in cpm.index]].T.round(2)
tab.index = lab[tab.index]
print(tab.sort_index().to_string())
expr = cpm[(x > 10).sum(axis=1) >= 5]
top = expr.loc[expr.var(axis=1).sort_values().index[-2000:]]
z = top.sub(top.mean(axis=1), axis=0)
u, s, vt = np.linalg.svd(z.values, full_matrices=False)
pcs = pd.DataFrame(vt[:3].T * s[:3], index=lab[z.columns], columns=["PC1", "PC2", "PC3"]).round(1)
print("var explained", (s[:5] ** 2 / (s ** 2).sum()).round(3))
print(pcs.sort_index().to_string())
corr = expr.corr(method="spearman")
corr.index = lab[corr.index]; corr.columns = lab[corr.columns]
print("min corr per sample:\n", corr.where(~np.eye(len(corr), dtype=bool)).mean().sort_values().head(5).round(4))
out = {"marker_log2cpm": tab.sort_index().to_dict(), "pca": pcs.sort_index().to_dict()}
json.dump(out, open(CD / "results" / "qc_diagnostics.json", "w", encoding="utf-8"), indent=1)
