"""Rename GSE310858_Read_counts.txt.gz sample columns to GSM ids.

Matrix columns look like ``<subject>-<time>-<tissue>_S<n>.sorted.bam`` (time 0 = before,
1 = after bed rest; s = soleus, v = vastus lateralis). The ``_S<n>`` lane suffix repeats
every 8 columns, so it is not a key. Each column is mapped by NAME to the metadata row with
the same individual, time point and tissue (never by position); the script fails if any
column is unmatched or matched twice. Counts are copied unchanged.

usage: python -I rename_columns.py <counts.txt.gz> <metadata.csv> <out.csv.gz>
"""
import re
import sys

import pandas as pd

counts_path, meta_path, out_path = sys.argv[1:4]
counts = pd.read_csv(counts_path, sep="\t", index_col=0)
meta = pd.read_csv(meta_path, index_col=0)

time_map = {"0": "before treatment", "1": "after treatment"}
tissue_map = {"s": "musculus soleus", "v": "musculus vastus lateralis"}
lookup = {}
for gsm, row in meta.iterrows():
    key = (str(row["characteristics_ch1.2.individual"]), row["characteristics_ch1.5.time point"],
           row["characteristics_ch1.0.tissue"])
    assert key not in lookup, key
    lookup[key] = gsm

rename = {}
for col in counts.columns:
    m = re.fullmatch(r"(\d+)-([01])-([sv])_S\d+\.sorted\.bam", col)
    if m is None:
        if col in ("gene_name", "gene_biotype"):
            continue
        raise SystemExit(f"unparsed column {col}")
    key = (m.group(1), time_map[m.group(2)], tissue_map[m.group(3)])
    if key not in lookup:
        raise SystemExit(f"no metadata row for {col} {key}")
    rename[col] = lookup[key]
if len(set(rename.values())) != len(rename) or len(rename) != len(meta):
    raise SystemExit("mapping is not one-to-one")
out = counts.rename(columns=rename)
out.index.name = "gene_id"
out.to_csv(out_path)
print(f"wrote {out_path}: {out.shape}; mapped {len(rename)} columns")
