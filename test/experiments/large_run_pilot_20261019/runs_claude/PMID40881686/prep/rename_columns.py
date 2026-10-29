"""Rename GSE272928 matrix columns to a key derivable from the GEO sample titles.

Matrix columns are ALL02_BASELINE / CONT_51_BASELINE; GEO titles are "ALL02 BASELINE" /
"CONT 51 BASELINE". This inserts "_" between the group letters and the subject number
(ALL02_BASELINE -> ALL_02_BASELINE) so both sides read <GROUP>_<NN>_<TIME>. Name-based only;
values and row order are unchanged. The hgnc_symbol annotation column is kept.
"""
import re, sys
import pandas as pd

src, out = sys.argv[1], sys.argv[2]
df = pd.read_csv(src, index_col=0)
new = {}
for c in df.columns:
    m = re.fullmatch(r"(ALL|CONT)_?(\d+)_(BASELINE|PEAK)", c)
    new[c] = f"{m.group(1)}_{m.group(2)}_{m.group(3)}" if m else c
assert len(set(new.values())) == len(new)
df.rename(columns=new).to_csv(out)
print({k: v for k, v in new.items() if k != v})
