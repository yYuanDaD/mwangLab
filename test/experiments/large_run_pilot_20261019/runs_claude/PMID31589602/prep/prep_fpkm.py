"""Drop Excel date-mangled gene names from GSE123878_FpkmValues_AllSamples.csv.

The deposited xlsx converted Sept*/March* (and possibly Marc*) gene symbols into
dates (e.g. '2018-09-15 00:00:00'); '2018-03-02' occurs twice (two different
genes), so the original symbols cannot be recovered unambiguously. All
date-like IDs are dropped (21 rows); no other values are changed.
Usage: python -I prep_fpkm.py <in_csv> <out_csv>
"""
import sys
import pandas as pd

src, out = sys.argv[1], sys.argv[2]
df = pd.read_csv(src)
ids = df["GeneName"].astype(str)
bad = ids.str.match(r"^\d{4}-\d{2}-\d{2}")
print(f"dropping {int(bad.sum())} date-mangled IDs: {sorted(set(ids[bad]))}")
clean = df.loc[~bad].copy()
assert not clean["GeneName"].duplicated().any(), "duplicate gene IDs remain"
clean.to_csv(out, index=False)
print(f"wrote {out}: {clean.shape[0]} genes x {clean.shape[1]-1} samples")
