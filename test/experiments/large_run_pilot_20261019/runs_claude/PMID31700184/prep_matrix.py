"""Rename GSE124799 count-matrix columns to match the GEO sample titles exactly.

Matrix columns are `Sed_1`, `Ex_1`, `ExSed_1`, ...; GEO titles are `Sed 1`, `Ex 1`,
`ExSed 1`, ... The only change is `_` -> ` ` in column names, checked against the
metadata titles by name (never by position). Values are untouched.
"""
import sys
from pathlib import Path

import pandas as pd

data = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("E:/agent/mwangLab_pdf/data")
out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).with_name("GSE124799_counts_titled.csv")

counts = pd.read_csv(data / "GSE124799" / "GSE124799_counts.txt.gz", sep="\t", index_col=0)
meta = pd.read_csv(data / "GSE124799" / "GSE124799_metadata.csv", index_col=0)
renamed = {c: c.replace("_", " ") for c in counts.columns}
titles = set(meta["title"].astype(str))
missing = sorted(set(renamed.values()) - titles)
if missing or len(set(renamed.values())) != len(renamed) or len(titles) != len(counts.columns):
    raise SystemExit(f"column/title mismatch: {missing}")
counts = counts.rename(columns=renamed)
counts.index.name = "gene_id"
counts.to_csv(out)
print(f"wrote {out} {counts.shape}")
