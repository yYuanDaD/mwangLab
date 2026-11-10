"""Exploration only (no decisions): check raw/normcounts consistency and the paper's filter yield."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, re; os.chdir(ROOT)
import numpy as np, pandas as pd
from pydeseq2.preprocessing import deseq2_norm

raw = pd.read_csv("data/GSE220280/GSE220280_silver_hmt_raw.csv.gz", index_col=0)
norm = pd.read_csv("data/GSE220280/GSE220280_2022-10-09_humanmito_normcounts.csv.gz", index_col=0)
def key(c):
    m = re.match(r"^\s*hmt[ab][-.](\d{2})[-.](\d)(?:[-.]\d)?_S\d+_L001\.tdf?\s*$", c)
    return f"hmt-{m.group(1)}-{m.group(2)}"
raw.columns = [key(c) for c in raw.columns]; norm.columns = [key(c) for c in norm.columns]
norm = norm.loc[raw.index, raw.columns]
print("raw NaN <-> norm 0:", ((raw.isna()) == (norm == 0)).values.mean())
sf_auth = (raw.fillna(0) / norm.replace(0, np.nan)).median()
print("author size factors (raw/norm):", sf_auth.round(3).to_dict())
c = raw.fillna(0).astype(int)
normed, sf = deseq2_norm(c.T)
print("pydeseq2 sf:", np.round(sf, 3).tolist())
keep = normed.sum(axis=0) >= 10
print("mito: nonzero", int((c.sum(axis=1) > 0).sum()), "pass norm-sum>=10:", int(keep.sum()), " author-norm sum>=10:", int((norm.sum(axis=1) >= 10).sum()))

m = pd.read_csv("data/GSE276889/GSE276889_Human_skm_total_RNA_RAW_ENSEMBL.csv.gz", index_col=0)
normed, sf = deseq2_norm(m.T)
print("mRNA genes", m.shape, "pass norm-sum>=10:", int((normed.sum(axis=0) >= 10).sum()), "dup ids", m.index.has_duplicates)
