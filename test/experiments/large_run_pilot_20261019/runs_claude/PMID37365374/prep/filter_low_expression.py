"""Filter low-expression genes from the deposited GSE230002 moderated log2CPM matrix.

Decision (agent): keep genes with log2CPM >= 0 (CPM >= ~1) in at least 6 samples
(6 = the smallest arm, Diet-ONLY), the classic edgeR CPM>1 rule, standing in for the
unstated filter of the paper's edgeR route. No values are changed; rows are only dropped.
Usage: python filter_low_expression.py <in.csv> <out.csv>
"""
import sys
import pandas as pd

src, dst = sys.argv[1], sys.argv[2]
d = pd.read_csv(src, index_col=0)
keep = (d >= 0).sum(axis=1) >= 6
out = d.loc[keep]
out.to_csv(dst)
print(f"kept {int(keep.sum())} of {len(d)} rows; duplicated ids after filter: {int(out.index.duplicated().sum())}")
