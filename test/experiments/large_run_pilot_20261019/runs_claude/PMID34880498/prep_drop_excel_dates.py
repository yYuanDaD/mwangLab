"""Drop Excel-mangled gene IDs (e.g. '2019-03-01', from 1-Mar / March1 or Marc1) from the
deposited GSE164401 hippocampal count tables. The original symbol cannot be recovered
unambiguously (March1/Marc1, March2/Marc2 collide), so the rows are removed.
Usage: python prep_drop_excel_dates.py <in.csv> <out.csv>
"""
import re
import sys

import pandas as pd

src, dst = sys.argv[1], sys.argv[2]
df = pd.read_csv(src, index_col=0)
bad = [i for i in df.index.astype(str) if re.match(r"^\d{4}-\d{2}-\d{2}", i)]
df = df.drop(index=bad)
assert not df.index.duplicated().any()
df.to_csv(dst)
print(f"{src}: dropped {len(bad)} rows {bad}; {df.shape[0]} genes x {df.shape[1]} samples -> {dst}")
