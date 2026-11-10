"""Merge GSE237736 per-sample StringTie gene_abundance files into one FPKM matrix.

GEO deposits only StringTie gene_abundance tables (FPKM/TPM/Coverage; no read counts).
Columns become GSM ids (prefix of each member name). The FPKM column is used, as the
series data_processing states ("tab-delimited text files include FPKM values").
Gene IDs that appear on several loci (152 rows per sample) are summed per gene ID
(FPKM is additive across the loci/transcripts of one gene within a sample).

Usage: python -I merge_stringtie_fpkm.py <unpacked_dir> <out_csv>
"""
import glob
import os
import re
import sys

import pandas as pd


def main(src_dir: str, out_csv: str) -> None:
    files = sorted(glob.glob(os.path.join(src_dir, "GSM*_StringTie.gene_abundance.tab.gz")))
    if len(files) != 16:
        raise SystemExit(f"expected 16 files, found {len(files)}")
    cols = {}
    for f in files:
        gsm = re.match(r"(GSM\d+)_", os.path.basename(f)).group(1)
        d = pd.read_csv(f, sep="\t")
        cols[gsm] = d.groupby("Gene ID")["FPKM"].sum()
    m = pd.DataFrame(cols).fillna(0.0)
    m.index.name = "gene_id"
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    m.to_csv(out_csv)
    print(f"wrote {out_csv}: {m.shape[0]} genes x {m.shape[1]} samples")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
