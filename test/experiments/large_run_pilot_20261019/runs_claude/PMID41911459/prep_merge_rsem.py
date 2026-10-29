"""Merge GSE325919 RSEM *.genes.results.gz members into one expected_count matrix.

The repository tar merger (tools/geo_tar.py:59-60) only accepts .txt/.tsv/.csv/.tab members,
so the RSEM `.genes.results.gz` files are skipped. This script reads the `expected_count`
column (RSEM expected counts, the paper's stated input, S2.24.p2) from every member and
writes one gene x GSM matrix. Values are left unrounded.

Usage: python -I prep_merge_rsem.py <RAW.tar> <out.csv.gz>
"""
import re
import sys
import tarfile

import pandas as pd

tar_path, out_path = sys.argv[1], sys.argv[2]
cols = {}
with tarfile.open(tar_path) as tf:
    for m in tf.getmembers():
        if not m.name.endswith(".genes.results.gz"):
            continue
        gsm = re.match(r"(GSM\d+)_", m.name).group(1)
        df = pd.read_csv(tf.extractfile(m), sep="\t", compression="gzip", index_col="gene_id")
        cols[gsm] = df["expected_count"]
mat = pd.DataFrame(cols).sort_index(axis=1)
mat.index.name = "gene_id"
assert mat.notna().all().all(), "gene sets differ between members"
mat.to_csv(out_path)
print(f"wrote {out_path}: {mat.shape[0]} genes x {mat.shape[1]} samples; "
      f"non-integer fraction {(mat.values % 1 != 0).mean():.3f}")
