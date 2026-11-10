"""Reproduce the paper's low-count filter (S2.8.p1): keep genes with at least 10 reads on average
across all deposited samples. Values are not changed; the SYMBOL annotation column is kept.
Usage: python filter_mean10.py <in.csv.gz> <out.csv.gz>"""
import sys
import pandas as pd

src, dst = sys.argv[1], sys.argv[2]
d = pd.read_csv(src, index_col=0)
x = d.drop(columns=["SYMBOL"])
keep = x.mean(axis=1) >= 10
out = d.loc[keep]
out.to_csv(dst)
print(f"kept {int(keep.sum())} of {len(d)} genes (mean count >= 10 over {x.shape[1]} samples)")
print(f"strict > 10 would keep {int((x.mean(axis=1) > 10).sum())}")
