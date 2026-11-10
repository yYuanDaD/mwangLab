"""Paper's low-count rule (PMC13619381 S2.7.p1): DESeq2 median-of-ratios size factors on the
complete unfiltered matrix, then keep miRNAs with >= 10 normalized counts in >= 3 samples.
Writes the raw (unnormalized) counts of the kept miRNAs; values are not changed.

usage: python paper_filter.py <counts.csv.gz> <out.csv>
"""
import sys

import numpy as np
import pandas as pd

src, out = sys.argv[1], sys.argv[2]
counts = pd.read_csv(src, index_col=0, sep=None, engine="python")
log = np.log(counts.replace(0, np.nan))
zero_free = log.notna().all(axis=1)
geo_mean = log[zero_free].mean(axis=1)
size_factors = np.exp(log[zero_free].sub(geo_mean, axis=0).median(axis=0))
normalized = counts / size_factors
keep = (normalized >= 10).sum(axis=1) >= 3
counts.loc[keep].to_csv(out)
print(f"zero-free genes {int(zero_free.sum())}; kept {int(keep.sum())}/{len(keep)}; "
      f"zero-free genes all kept: {bool(keep[zero_free].all())}")
