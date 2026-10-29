import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os
ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())
os.chdir(ROOT)
import numpy as np, pandas as pd

tx = pd.read_csv("data/GSE292369/GSE292369_Partek_KE_recovery_transcript_counts.txt.gz", sep="\t")
print(tx.shape, tx.columns[:6].tolist())
samp = [c for c in tx.columns if c.startswith("GC-DO")]
v = tx[samp].to_numpy()
print("min", v.min(), "max", v.max(), "int frac", np.mean(np.isclose(v, np.round(v))), "NaN", np.isnan(v).sum())
print("genes", tx["Gene"].nunique(), "null gene", tx["Gene"].isna().sum())
g = tx.groupby("Gene")[samp].sum()
print("gene matrix", g.shape, "lib sizes (M)", (g.sum() / 1e6).round(1).describe())

nm = pd.read_csv("data/GSE292369/GSE292369_Partek_KE_recovery_Normalization_Outliers_Removed_Deseq2.txt.gz", sep="\t", index_col=0)
print("normalized", nm.shape)
print(nm.iloc[:, :4])
print("missing samples:", sorted(set(samp) - set(nm.index)))
genes_n = nm.columns[4:]
print("n genes normalized", len(genes_n), "in gene matrix", len(set(genes_n) & set(g.index)))
common = [s for s in nm.index]
gg = g.loc[[x for x in genes_n if x in g.index], common]
nn = nm.loc[common, gg.index].T.astype(float)
ratio = (gg / nn).replace([np.inf, -np.inf], np.nan)
print("per-sample ratio (raw/normalized) median and IQR spread:")
med = ratio.median()
spread = (ratio.quantile(0.9) - ratio.quantile(0.1)) / med
print(pd.DataFrame({"sf": med.round(4), "rel_spread_10_90": spread.round(4)}).head(40))
