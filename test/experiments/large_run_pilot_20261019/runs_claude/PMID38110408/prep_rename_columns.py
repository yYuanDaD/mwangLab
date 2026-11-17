"""Rename GSE239729 matrix columns (A,B,C,A1,B1,C1) to GSM ids.

The deposited FPKM file has no column key present in the GEO metadata. Group membership
is assigned from evidence, not file order: Cdo1 (ENSMUSG00000033022) FPKM is ~3-4x lower
in A1/B1/C1 (243-272) than in A/B/C (822-1072), as expected for the hepatocyte Cdo1
knockout, and samples cluster A/B/C vs A1/B1/C1 on log2 correlation. Within each genotype
the replicate order (A->1, B->2, C->3) is an ASSUMPTION; no analysis in this run depends
on within-group sample identity (the case is refused at design).
"""
import sys
import pandas as pd

src, out = sys.argv[1], sys.argv[2]
d = pd.read_csv(src, sep="\t", index_col=0)
cdo1 = d.loc["ENSMUSG00000033022"]
assert cdo1[["A1", "B1", "C1"]].max() < cdo1[["A", "B", "C"]].min(), "Cdo1 marker does not separate groups"
mapping = {"A": "GSM7670607", "B": "GSM7670608", "C": "GSM7670609",      # WT 1-3
           "A1": "GSM7670610", "B1": "GSM7670611", "C1": "GSM7670612"}   # Cdo1-LKO 1-3
d = d.rename(columns=mapping)
d.index.name = "gene_id"
d.to_csv(out)
print(cdo1.to_dict())
