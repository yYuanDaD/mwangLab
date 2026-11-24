"""Transpose the GSE192982 deposited matrix (samples x genes, with 4 annotation
columns) into genes x samples. Values are unchanged (Partek log2(TMM+1))."""
import sys
import pandas as pd

src, out = sys.argv[1], sys.argv[2]
d = pd.read_csv(src, sep="\t", index_col=0)
d = d.drop(columns=["Treatment", "Sex", "Donor info", "Sex Stratified"])
t = d.T
t.index.name = "gene"
t.to_csv(out)
print(t.shape)
