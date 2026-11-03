"""Apply the paper's gene filter (S2.12.6.p1): drop genes whose mean across all samples is <= 10 reads."""
import sys
import pandas as pd
src, dst = sys.argv[1], sys.argv[2]
x = pd.read_csv(src, index_col=0)
num = x.drop(columns="SYMBOL")
keep = num.mean(axis=1) > 10
print("genes before", len(x), "after", int(keep.sum()))
x[keep].to_csv(dst)
