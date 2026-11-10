"""Merge GSE229755 per-sample FPKM files (from _RAW.tar) into one gene x GSM matrix.

Each GSM*_<title>.txt.gz holds st_gene_id, gene_id (Entrez), gene_symbol, fpkm_<title>.
Rows are indexed by gene_symbol; duplicated symbols are resolved by keeping the row
with the highest mean FPKM. Columns are named by GSM id (taken from the file name).
"""
import glob
import os
import sys

import pandas as pd

data_dir = sys.argv[1] if len(sys.argv) > 1 else "E:/agent/mwangLab_pdf/data/GSE229755"
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(data_dir, "GSE229755_fpkm_merged.csv")

cols = {}
ids = None
for f in sorted(glob.glob(os.path.join(data_dir, "_unpacked", "GSM*.txt.gz"))):
    gsm = os.path.basename(f).split("_")[0]
    d = pd.read_csv(f, sep="\t")
    fcol = [c for c in d.columns if c.startswith("fpkm_")]
    assert len(fcol) == 1, (f, d.columns)
    d = d.set_index("gene_id")
    if ids is None:
        ids = d[["gene_symbol"]]
    cols[gsm] = d[fcol[0]]

m = pd.DataFrame(cols)
m = m.join(ids)
m["gene_symbol"] = m["gene_symbol"].fillna(m.index.to_series().astype(str))
m["_mean"] = m.drop(columns="gene_symbol").mean(axis=1)
m = m.sort_values("_mean", ascending=False).drop_duplicates("gene_symbol")
m = m.set_index("gene_symbol").drop(columns="_mean")
m.index.name = "gene_symbol"
assert m.notna().all().all()
m.to_csv(out)
print(f"wrote {out}: {m.shape[0]} genes x {m.shape[1]} samples")
