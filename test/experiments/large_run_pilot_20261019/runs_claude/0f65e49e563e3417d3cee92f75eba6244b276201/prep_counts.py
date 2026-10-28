"""Build a counts-only matrix for GSE236613.

The merged _RAW.tar matrix interleaves eXpress FPKM and counts columns per
sample (GSM*_SampleN_FPKM / GSM*_SampleN_counts). DESeq2 needs only the
integer counts columns; rename each to its GSM accession.
Usage: python prep_counts.py <merged_from_tar.csv> <out.csv>
"""
import re
import sys

import pandas as pd

src, out = sys.argv[1], sys.argv[2]
df = pd.read_csv(src, index_col=0)
cols = [c for c in df.columns if c.endswith("_counts")]
counts = df[cols].copy()
counts.columns = [re.match(r"^(GSM\d+)_", c).group(1) for c in cols]
assert counts.shape[1] == 9, counts.shape
assert (counts.values % 1 == 0).all(), "non-integer counts"
counts = counts.astype(int)
counts.index.name = "gene_id"
counts.to_csv(out)
print(counts.shape, counts.sum().to_dict())
