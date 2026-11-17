"""Merge GSE226005_RAW.tar per-sample DESeq2-normalized tables into one gene x GSM matrix.

Each member is tab-delimited with a one-field title line (e.g. "IMR90 Senescenct rep1")
followed by gene<TAB>value rows. tools/geo_tar.py sniffs the title line as space-delimited
and skips all 12 members, so this script reads them with sep='\t', skiprows=1.
Usage: python prep_merge_tar.py <RAW.tar> <out.csv>
"""
import sys
import tarfile

import pandas as pd

tar_path, out_path = sys.argv[1], sys.argv[2]
cols = {}
with tarfile.open(tar_path) as tf:
    for m in tf.getmembers():
        if not m.isfile():
            continue
        gsm = m.name.split("_")[0]
        with tf.extractfile(m) as fh:
            df = pd.read_csv(fh, sep="\t", skiprows=1, header=None, names=["gene", gsm],
                             compression="gzip")
        if df["gene"].duplicated().any():
            raise SystemExit(f"duplicated gene ids in {m.name}")
        cols[gsm] = df.set_index("gene")[gsm]
merged = pd.concat(cols, axis=1, join="outer")
merged.index.name = "gene"
merged.to_csv(out_path)
print(f"{merged.shape[0]} genes x {merged.shape[1]} samples; missing={int(merged.isna().sum().sum())}")
