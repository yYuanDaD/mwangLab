"""Merge the DRAGEN/Salmon-format *.quant.genes.sf.gz files in GSE289091_RAW.tar into one
estimated-count matrix (NumReads column), columns named by GSM id.

Gene IDs: GENCODE v37 versioned Ensembl ids; the version suffix is stripped and the
_PAR_Y copies are dropped (they duplicate the X-linked id). Usage:
    python -I prep_merge_quant.py <RAW.tar> <out.csv>
"""
import gzip
import io
import sys
import tarfile

import pandas as pd

tar_path, out_path = sys.argv[1], sys.argv[2]
cols = {}
with tarfile.open(tar_path) as tar:
    for member in tar.getmembers():
        if not member.name.endswith(".quant.genes.sf.gz"):
            continue
        gsm = member.name.split("_")[0]
        raw = gzip.decompress(tar.extractfile(member).read())
        table = pd.read_csv(io.BytesIO(raw), sep="\t", index_col=0)
        cols[gsm] = table["NumReads"]
matrix = pd.DataFrame(cols)
before = len(matrix)
matrix = matrix[~matrix.index.str.endswith("_PAR_Y")]
matrix.index = matrix.index.str.split(".").str[0]
assert not matrix.index.has_duplicates, "duplicate Ensembl ids after stripping versions"
matrix.index.name = "gene_id"
matrix.to_csv(out_path)
print(f"{matrix.shape[0]} genes ({before - len(matrix)} PAR_Y rows dropped) x {matrix.shape[1]} samples -> {out_path}")
