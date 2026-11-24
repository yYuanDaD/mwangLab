"""Reconstruct integer read counts from GSE144109_normalized_counts.tsv.gz.

The deposited file holds DESeq2-style normalized counts (GEO data_processing:
"gene coverages in units of normalized read counts"; featureCounts -> DESeq2).
Each column equals integer counts / size factor. Multiplying each column by
1 / (smallest positive value in that column) returns exact integers for every
gene in every sample (max deviation from an integer 0.0 at 1e-6), so this is an
exact inversion, not rounding. A per-sample constant scale does not change
DESeq2 results because DESeq2 re-estimates size factors. The result is rounded
only to remove floating-point noise (checked < 1e-6 before rounding).
Usage: python -I prep_counts.py <normalized.tsv.gz> <out.csv>
"""
import sys
import numpy as np
import pandas as pd

x = pd.read_csv(sys.argv[1], index_col=0)
inv_sf = 1.0 / x.apply(lambda c: c[c > 0].min())
raw = x * inv_sf
dev = float((raw - raw.round()).abs().to_numpy().max())
assert dev < 1e-6, f"not an exact integer inversion (max dev {dev})"
raw = raw.round().astype(np.int64)
raw.index.name = "gene_id"
raw.to_csv(sys.argv[2])
print("max_dev", dev)
print("size_factors(1/inv)", (1 / inv_sf).round(6).to_dict())
print("library_sizes", raw.sum().to_dict())
