"""Read-only exploration of GSE243060 files (no decisions recorded)."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, re; os.chdir(ROOT)
import pandas as pd, numpy as np
raw = pd.read_csv("data/GSE243060/GSE243060_RED-S_mouse_tissue_expression_raw_counts_v1.csv.gz", index_col=0)
norm = pd.read_csv("data/GSE243060/GSE243060_RED-S_mouse_tissue_expression_normalized_counts_v1.csv.gz", index_col=0)
meta = pd.read_csv("data/GSE243060/GSE243060_metadata.csv", index_col=0)
print("raw", raw.shape, "norm", norm.shape)
print("raw index dup", raw.index.duplicated().sum(), "norm index dup", norm.index.duplicated().sum())
print("raw cols[:3]", list(raw.columns[:4]), "norm cols[:3]", list(norm.columns[:4]))
num = raw.drop(columns=["Symbol"])
print("non-numeric?", [c for c in num.columns if not pd.api.types.is_numeric_dtype(num[c])][:5])
v = num.values
print("NaN", np.isnan(v).sum(), "neg", (v<0).sum(), "intfrac", np.mean(v == np.round(v)))
lib = meta["description"].str.split(",").str[0]
key = "X" + lib
print("lib unique", lib.is_unique, "matched", key.isin(num.columns).sum(), "of", len(meta), "matrix cols", num.shape[1])
print("unmatched matrix cols", [c for c in num.columns if c not in set(key)][:20])
print("unmatched meta", list(lib[~key.isin(num.columns)])[:20])
# norm cols
ncols = [c for c in norm.columns if c != "Symbol"]
print("norm cols same set as raw?", set(ncols) == set(num.columns), len(ncols))
# parse lib name structure
pat = re.compile(r"^(\d+)_([FM])_(\d+)(?:_5)?([LH])_([A-Za-z]+)_S\d+$")
bad = [l for l in lib if not pat.match(l)]
print("lib names not matching pattern", len(bad), bad[:20])
meta["lib"] = lib
meta["tissue"] = meta["characteristics_ch1.1.tissue"]
tab = meta.groupby(["tissue", "characteristics_ch1.2.Sex", "characteristics_ch1.3.treatment", "characteristics_ch1.4.zeitgeber time"]).size().unstack([1,2,3]).fillna(0).astype(int)
pd.set_option("display.width", 250); print(tab)
# consistency of lib code with characteristics
m = lib.str.extract(r"^(\d+)_([FM])_(\d+)(?:_5)?([LH])_([A-Za-z]+)_S\d+$")
m.columns = ["mouse", "sex", "zt", "wl", "tcode"]
meta = meta.join(m)
print(pd.crosstab(meta["sex"], meta["characteristics_ch1.2.Sex"]))
print(pd.crosstab(meta["wl"], meta["characteristics_ch1.3.treatment"]))
print(pd.crosstab(meta["zt"], meta["characteristics_ch1.4.zeitgeber time"]))
print(pd.crosstab(meta["tcode"], meta["tissue"]).T)
# mouse consistency: same mouse id -> same sex/treatment/zt
g = meta.groupby("mouse")[["characteristics_ch1.2.Sex", "characteristics_ch1.3.treatment", "characteristics_ch1.4.zeitgeber time"]].nunique()
print("mice", len(g), "inconsistent", int((g > 1).any(axis=1).sum()))
# per tissue duplicates of mouse
d = meta.groupby(["tissue", "mouse"]).size()
print("tissue x mouse dup", int((d > 1).sum()))
# norm: per-tissue normalized? check per-sample column sums
print("norm values sample", norm.drop(columns=["Symbol"]).iloc[:3, :4])
print("norm NaN frac", float(norm.drop(columns=["Symbol"]).isna().mean().mean()))
