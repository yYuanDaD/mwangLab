"""Drop the 23 ERCC spike-in rows (NaN in samples whose count table lacked them) and the
GeneSymbol/GeneBiotype annotation columns from the GSE129962 featureCounts matrix.
Gene rows and counts are unchanged. Usage: python prep_counts.py <in.txt.gz> <out.csv>"""
import sys
import pandas as pd

src, dst = sys.argv[1], sys.argv[2]
d = pd.read_csv(src, sep="\t", index_col=0)
ercc = d.index.astype(str).str.startswith("ERCC-")
counts = d.loc[~ercc].drop(columns=["GeneSymbol", "GeneBiotype"])
assert not counts.isna().any().any(), "NaN outside ERCC rows"
counts = counts.astype(int)
counts.index.name = "GeneID"
counts.to_csv(dst)
print(f"dropped {int(ercc.sum())} ERCC rows; wrote {counts.shape[0]} genes x {counts.shape[1]} samples to {dst}")
