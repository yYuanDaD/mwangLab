"""Post-hoc look (not a decision): PCA and correlation of the 10 RW samples, to understand the HFS_vs_CS gap."""
import pathlib, numpy as np, pandas as pd
RUN = pathlib.Path(__file__).resolve().parents[1]
m = pd.read_csv(RUN / "GSE232510/aligned/aligned_matrix.csv", index_col=0)
meta = pd.read_csv(RUN / "GSE232510/aligned/design_metadata.csv", index_col=0)
keep = (m >= 10).sum(axis=1) >= 3
cpm = np.log2(m[keep] / m.sum() * 1e6 + 1)
top = cpm.loc[cpm.var(axis=1).sort_values(ascending=False).index[:1000]]
x = (top.T - top.T.mean()).values
u, s, vt = np.linalg.svd(x, full_matrices=False)
ve = s**2 / (s**2).sum()
pcs = pd.DataFrame(u[:, :3] * s[:3], index=top.columns, columns=["PC1", "PC2", "PC3"])
pcs["grp"] = meta.loc[pcs.index, "grp"]; pcs["rep"] = meta.loc[pcs.index, "rep_label"]
print("var explained", np.round(ve[:4], 3)); print(pcs.round(1))
c = cpm.corr(method="spearman").round(3); c.index = [f"{meta.loc[i,'rep_label']}" for i in c.index]; c.columns = c.index
print(c)
out = RUN / "GSE232510" / "results" / "posthoc_pca.csv"; pcs.to_csv(out); print(out)
