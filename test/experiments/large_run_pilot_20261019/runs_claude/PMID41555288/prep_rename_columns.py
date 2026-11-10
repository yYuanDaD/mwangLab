"""Rename GSE310294 matrix columns sampleN_FPKM -> Sample_N so they match the
metadata 'description' field ('Library name: Sample N') via alignment.key_patterns.
Values are unchanged (integer raw fragment counts; the '_FPKM' suffix is a mislabel:
column sums 14-18 M, all integers, GEO data_processing says 'raw fragment counts')."""
import re, sys
from pathlib import Path
import pandas as pd

src = Path(sys.argv[1]); out = Path(sys.argv[2])
df = pd.read_csv(src, index_col=0)
mapping = {}
for c in df.columns:
    m = re.fullmatch(r"sample(\d+)_FPKM", c)
    if not m:
        raise SystemExit(f"unexpected column {c}")
    mapping[c] = f"Sample_{m.group(1)}"
df = df.rename(columns=mapping)
out.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(out)
print(mapping, df.shape)
