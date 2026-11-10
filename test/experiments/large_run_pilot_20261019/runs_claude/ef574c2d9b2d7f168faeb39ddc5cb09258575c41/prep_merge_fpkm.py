"""Merge GSE60833 per-sample Cufflinks genes.fpkm_tracking files into one gene x sample FPKM matrix.

Each GSM*_<id>.fpkm.txt.gz in GSE60833_RAW.tar is a Cufflinks gene-level FPKM table
(tracking_id = Ensembl gene, ENSEMBL v71). Cufflinks reports some genes on several
loci (duplicated tracking_id); their FPKM rows are summed per gene (FPKM is additive
over disjoint loci of one gene to a first approximation). Columns are named by GSM id.

Usage: python prep_merge_fpkm.py <RAW.tar> <out.csv>
"""
import sys
import tarfile
import io
import re

import pandas as pd


def main(tar_path: str, out_csv: str) -> None:
    cols = {}
    n_dup = {}
    with tarfile.open(tar_path) as tf:
        for m in sorted(tf.getmembers(), key=lambda x: x.name):
            mt = re.match(r"(GSM\d+)_.*\.fpkm\.txt\.gz$", m.name)
            if not mt:
                continue
            raw = tf.extractfile(m).read()
            df = pd.read_csv(io.BytesIO(raw), sep="\t", compression="gzip",
                             usecols=["tracking_id", "FPKM"])
            n_dup[mt.group(1)] = int(df["tracking_id"].duplicated().sum())
            cols[mt.group(1)] = df.groupby("tracking_id")["FPKM"].sum()
    mat = pd.DataFrame(cols).fillna(0.0)
    mat.index.name = "gene_id"
    mat.to_csv(out_csv)
    print(f"merged {mat.shape[0]} genes x {mat.shape[1]} samples -> {out_csv}")
    print(f"duplicated tracking_id rows summed per sample: min={min(n_dup.values())} max={max(n_dup.values())}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
