"""Sensitivity input: keep genes with FPKM >= 1 in at least 4 samples (the size of one group),
approximating Cuffdiff's exclusion of loci with too few reads to test. Input is the repaired
gene-level matrix from fix_matrix.py. Usage: python filter_expressed.py <in.csv> <out.csv>"""
import sys
import pandas as pd
df = pd.read_csv(sys.argv[1], index_col=0)
keep = (df >= 1).sum(axis=1) >= 4
df.loc[keep].to_csv(sys.argv[2])
print({"genes_in": len(df), "genes_kept": int(keep.sum())})
