"""Read-only: column-name formats and library-code consistency."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, re; os.chdir(ROOT)
import pandas as pd, numpy as np
raw = pd.read_csv("data/GSE243060/GSE243060_RED-S_mouse_tissue_expression_raw_counts_v1.csv.gz", index_col=0, nrows=5)
norm = pd.read_csv("data/GSE243060/GSE243060_RED-S_mouse_tissue_expression_normalized_counts_v1.csv.gz", index_col=0, nrows=5)
meta = pd.read_csv("data/GSE243060/GSE243060_metadata.csv", index_col=0)
rc = [c for c in raw.columns if c != "Symbol"]; nc = [c for c in norm.columns if c != "Symbol"]
print("raw-only", sorted(set(rc) - set(nc))[:10], len(set(rc) - set(nc)))
print("norm-only", sorted(set(nc) - set(rc))[:10])
lib = meta["description"].str.split(",").str[0]
rcs = set(rc)
key = [l if l in rcs else ("X" + l if "X" + l in rcs else None) for l in lib]
print("unresolved", sum(k is None for k in key), "both forms present", sum((l in rcs) and ("X" + l in rcs) for l in lib))
print("X-prefixed", sum(k.startswith("X") for k in key if k))
meta["lib"] = lib
def parse(l):
    t = l.split("_")
    mouse, sex = t[0], t[1]
    s = l
    wl = re.search(r"_(?:\d+(?:_5)?)?([LH])_", s) or re.search(r"_([LH])_ZT", s)
    zt = re.search(r"_ZT(\d+)_", s) or re.search(r"_(\d+)(?:_5)?[LH]_", s)
    return mouse, sex, wl.group(1) if wl else None, zt.group(1) if zt else None
P = pd.DataFrame([parse(l) for l in lib], index=meta.index, columns=["mouse", "sex", "wl", "zt"])
meta = meta.join(P)
print(P.isna().sum().to_dict())
print(pd.crosstab(meta["sex"], meta["characteristics_ch1.2.Sex"]))
print(pd.crosstab(meta["wl"], meta["characteristics_ch1.3.treatment"]))
print(pd.crosstab(meta["zt"], meta["characteristics_ch1.4.zeitgeber time"]))
g = meta.groupby("mouse")[["characteristics_ch1.2.Sex", "characteristics_ch1.3.treatment", "characteristics_ch1.4.zeitgeber time"]].nunique()
print("mice", len(g), "inconsistent", int((g > 1).any(axis=1).sum()))
print("tissue x mouse dup", int((meta.groupby(["characteristics_ch1.1.tissue", "mouse"]).size() > 1).sum()))
print(meta.groupby("characteristics_ch1.1.tissue")["lib"].apply(lambda s: sorted(set(re.sub(r"^\d+_[FM]_", "", x) for x in s))[:3]).to_string())
print(meta.groupby("characteristics_ch1.1.tissue").size().to_string())
