"""Keep the 120 muscle long-RNA libraries of GSE209880 and add a `key` column equal to the
matrix column names of GSE209880_muscle_long_counts.txt.gz (e.g. muscle_longRNA_PH010_w0pre -> PH010_pre).

The series metadata mixes four library types (muscle long/short, serum EV long/short) whose
titles map to the same subject_time key, so a key derived from all rows would not be unique."""
import re
import sys
from pathlib import Path

import pandas as pd

src, out = Path(sys.argv[1]), Path(sys.argv[2])
meta = pd.read_csv(src, index_col=0)
keep = meta[meta["title"].str.startswith("muscle_longRNA_")].copy()
keys = keep["title"].str.extract(r"^muscle_longRNA_(PH\d+)_w0(pre|h3|h24)$")
if keys.isna().any().any():
    raise SystemExit(f"unparsed titles: {keep.loc[keys.isna().any(axis=1), 'title'].tolist()}")
keep["key"] = keys[0] + "_" + keys[1]
assert keep["key"].is_unique and len(keep) == 120, (len(keep), keep["key"].duplicated().sum())
out.parent.mkdir(parents=True, exist_ok=True)
keep.to_csv(out)
print(f"wrote {out}: {len(keep)} samples")
