"""Restrict the GSE87748 read-coverage matrix to the 6,242 genes the authors tested.

The paper (S2.3.p1) kept genes with > 2.5 RPKM in >= 5 samples. Exon lengths are not
deposited, so RPKM cannot be recomputed; the authors' own tested-gene list
(GSE87748_RNAseq_stats.txt.gz, 6,242 rows = "6,242 genes detected", S3.1.p1) is used as
the gene universe instead. Counts are not changed.
"""
import sys
import pandas as pd

data, out = sys.argv[1], sys.argv[2]
m = pd.read_csv(f"{data}/GSE87748/GSE87748_RNAseq_Readcoverage_v3.txt.gz", sep="\t", index_col=0)
s = pd.read_csv(f"{data}/GSE87748/GSE87748_RNAseq_stats.txt.gz", sep="\t", index_col=0)
keep = [g for g in s.index if g in m.index]
print(f"matrix {m.shape}, tested genes {len(s)}, found in matrix {len(keep)}")
m.loc[keep].to_csv(out)
