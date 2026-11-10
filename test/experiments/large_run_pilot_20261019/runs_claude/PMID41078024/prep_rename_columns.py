"""Rename GSE302532 TPM matrix columns to the GEO library names (437P, ...).

The deposited columns read "Sedentary - 437P_S7 (GE) - TPM"; GEO metadata stores the
library name in `description` ("Library name: 437P"). Values are copied unchanged;
the Ensembl `Identifier` annotation column is dropped (gene `Name` stays the index).
"""
import re
import sys
from pathlib import Path

import pandas as pd

src = Path(sys.argv[1])
out = Path(sys.argv[2])
df = pd.read_csv(src, index_col=0)
df = df.drop(columns=["Identifier"])
mapping = {}
for c in df.columns:
    m = re.search(r" - (\d+P)_S\d+ \(GE\) - TPM$", c)
    if not m:
        raise SystemExit(f"unexpected column: {c}")
    mapping[c] = m.group(1)
assert len(set(mapping.values())) == len(mapping)
df = df.rename(columns=mapping)
df.index.name = "gene"
out.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(out)
print(mapping)
print(df.shape)
