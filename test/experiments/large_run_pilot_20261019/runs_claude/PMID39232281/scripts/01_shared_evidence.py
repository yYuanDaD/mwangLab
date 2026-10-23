"""Shared evidence before any gate: matrix key per GEO sample, library-name codes, and
how the deposited normalized counts relate to the raw counts. No decisions recorded here."""
import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import os, re, json
from common import *
os.chdir(ROOT)
import numpy as np, pandas as pd

out = pathlib.Path(RUN) / "shared"
out.mkdir(parents=True, exist_ok=True)
raw = pd.read_csv(RAW, index_col=0)
norm = pd.read_csv(NORM, index_col=0)
meta = pd.read_csv(META, index_col=0)
rcols = set(c for c in raw.columns if c != "Symbol")
lib = meta["description"].str.split(",").str[0]
# The raw matrix names 326 libraries with an R make.names 'X' prefix and 93 without; the
# normalized matrix uses 'X' for all 419. Resolve each GEO library name to the one raw column
# that equals it exactly, with or without the prefix (never both, checked).
key, form = [], []
for l in lib:
    a, b = l in rcols, ("X" + l) in rcols
    assert a != b, l
    key.append(l if a else "X" + l)
    form.append("plain" if a else "X_prefixed")
meta["library_name"] = lib
meta["raw_matrix_column"] = key
meta["norm_matrix_column"] = "X" + lib
meta["raw_column_form"] = form

def parse(l):
    mouse, sex = l.split("_")[:2]
    wl = re.search(r"_(?:\d+(?:_5)?)?([LH])_", l)
    zt = re.search(r"_ZT(\d+)_", l) or re.search(r"_(\d+)(?:_5)?[LH]_", l)
    style = ("M_[LH]_ZTxx" if re.search(r"_[LH]_ZT\d+_", l) else
             "ZT_5[LH]_L003" if l.endswith("_L003") else
             "ZT_5[LH]" if re.search(r"_\d+_5[LH]_", l) else "ZT[LH]")
    return mouse, sex, wl.group(1), zt.group(1), style
P = pd.DataFrame([parse(l) for l in lib], index=meta.index, columns=["lib_mouse", "lib_sex", "lib_workload", "lib_zt", "lib_name_style"])
meta = meta.join(P)
checks = {
    "sex": pd.crosstab(meta["lib_sex"], meta["characteristics_ch1.2.Sex"]).to_dict(),
    "workload_vs_treatment": pd.crosstab(meta["lib_workload"], meta["characteristics_ch1.3.treatment"]).to_dict(),
    "zt": pd.crosstab(meta["lib_zt"], meta["characteristics_ch1.4.zeitgeber time"]).to_dict(),
    "n_mice": int(meta["lib_mouse"].nunique()),
    "mice_with_inconsistent_sex_treatment_zt": int((meta.groupby("lib_mouse")[["characteristics_ch1.2.Sex", "characteristics_ch1.3.treatment", "characteristics_ch1.4.zeitgeber time"]].nunique() > 1).any(axis=1).sum()),
    "tissue_x_mouse_duplicates": int((meta.groupby(["characteristics_ch1.1.tissue", "lib_mouse"]).size() > 1).sum()),
    "raw_column_forms": meta["raw_column_form"].value_counts().to_dict(),
}
meta.to_csv(out / "metadata_keyed.csv")

# Normalized counts: per-sample ratio raw/norm should be one constant (a size factor) if the
# deposited file is DESeq2 median-of-ratios normalization; compare with per-tissue median-of-ratios.
rows = []
nmat = norm.drop(columns=["Symbol"])
rmat = raw.drop(columns=["Symbol"])
for tissue, sub in meta.groupby("characteristics_ch1.1.tissue"):
    rc = rmat[sub["raw_matrix_column"]].to_numpy(float)
    nc = nmat[sub["norm_matrix_column"]].to_numpy(float)
    ok = (rc > 0).all(axis=1)
    logg = np.log(rc[ok]).mean(axis=1)
    sf_tissue = np.exp(np.median(np.log(rc[ok]) - logg[:, None], axis=0))
    for j, s in enumerate(sub.index):
        m = (rc[:, j] > 0) & (nc[:, j] > 0)
        ratio = rc[m, j] / nc[m, j]
        rows.append({"sample": s, "tissue": tissue, "deposited_sf": float(np.median(ratio)),
                     "ratio_cv": float(ratio.std() / ratio.mean()), "tissue_mor_sf": float(sf_tissue[j])})
sf = pd.DataFrame(rows)
sf["sf_rel_diff"] = (sf["deposited_sf"] - sf["tissue_mor_sf"]).abs() / sf["tissue_mor_sf"]
sf.to_csv(out / "normalized_vs_raw_size_factors.csv", index=False)
checks["normalized_counts"] = {"max_ratio_cv": float(sf["ratio_cv"].max()),
                               "median_rel_diff_vs_per_tissue_median_of_ratios": float(sf["sf_rel_diff"].median()),
                               "max_rel_diff": float(sf["sf_rel_diff"].max())}
# Expressed genes per tissue under the paper's rule (mean normalized count >= 10)
expr = {}
for tissue, sub in meta.groupby("characteristics_ch1.1.tissue"):
    expr[tissue] = int((nmat[sub["norm_matrix_column"]].mean(axis=1) >= 10).sum())
checks["expressed_genes_mean_norm_ge10"] = expr
checks["expressed_genes_mean_over_tissues"] = float(np.mean(list(expr.values())))
(out / "shared_checks.json").write_text(json.dumps(checks, indent=2, default=str), encoding="utf-8")
print(json.dumps(checks, indent=1, default=str))
