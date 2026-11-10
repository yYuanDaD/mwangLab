"""Build the GSE217155 read-count matrix (9 samples) from the deposited per-sample files.

GSM6705777_musNASH5.txt.gz holds fpkm/tpm/read_count columns for all nine samples; the
other eight files hold one sample each. The tar merger kept the rightmost column per file
and dropped NASH5. This script takes read_count_<title> columns, checks the eight single-sample
files agree with the combined file, renames columns to GSM ids, and maps Entrez IDs to mouse
gene symbols (MyGene.info); unmapped or duplicated symbols keep the Entrez ID.
Usage: python build_counts.py <unpacked_dir> <metadata_csv> <out_csv>
"""
import sys, glob, os
import pandas as pd

unpacked, meta_csv, out_csv = sys.argv[1:4]
meta = pd.read_csv(meta_csv, index_col=0)
title2gsm = dict(zip(meta["title"], meta.index))
combined = pd.read_csv(os.path.join(unpacked, "GSM6705777_musNASH5.txt.gz"), sep="\t", index_col=0)
rc = combined[[c for c in combined.columns if c.startswith("read_count_")]].copy()
rc.columns = [c[len("read_count_"):] for c in rc.columns]
# consistency with single-sample files
for f in glob.glob(os.path.join(unpacked, "*.txt.gz")):
    if "NASH5" in f:
        continue
    s = pd.read_csv(f, sep="\t", index_col=0)
    col = [c for c in s.columns if c.startswith("read_count_")][0]
    t = col[len("read_count_"):]
    diff = (s[col].reindex(rc.index) - rc[t]).abs().max()
    print(f"{t}: max abs diff vs combined = {diff}")
    assert diff < 1e-6, t
rc = rc[[t for t in meta["title"]]]
rc.columns = [title2gsm[t] for t in rc.columns]
rc.index = rc.index.astype(str)
# Entrez -> symbol
import mygene
mg = mygene.MyGeneInfo()
res = mg.querymany(list(rc.index), scopes="entrezgene", fields="symbol", species="mouse", as_dataframe=False, verbose=False)
m = {}
for r in res:
    if "symbol" in r and not r.get("notfound"):
        m.setdefault(str(r["query"]), r["symbol"])
sym = pd.Series([m.get(i, i) for i in rc.index], index=rc.index)
dup = sym.duplicated(keep=False)
sym[dup] = sym.index[dup]
print(f"mapped {sum(i in m for i in rc.index)}/{len(rc)}; duplicated symbols kept as Entrez: {int(dup.sum())}")
rc.index = sym.values
rc.index.name = "gene"
rc.to_csv(out_csv)
print(rc.shape)
