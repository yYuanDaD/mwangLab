"""Repair GSE245594_fpkm_mRNA.xls.gz for the case runner.

The deposited file is a gzipped tab-separated text table (not an Excel workbook) with a
.xls extension, so the runner's file scan skips it. Its columns are Sed_1..Sed_4 and
SW_1..SW_4; the GEO titles are "Sedentary, bio rep N" / "Swimming, bio rep N".
This script renames each column to the GSM whose title has the same arm word and the
same replicate number (label match, never column order), and writes a CSV.
Values are not changed.
"""
import re, sys
from pathlib import Path
import pandas as pd

src, meta, out = map(Path, sys.argv[1:4])
m = pd.read_csv(meta, index_col=0)
lookup = {}
for gsm, title in m["title"].items():
    arm, rep = re.fullmatch(r"(Swimming|Sedentary), bio rep(\d+)", title).groups()
    lookup[{"Swimming": "SW", "Sedentary": "Sed"}[arm] + "_" + rep] = gsm
x = pd.read_csv(src, sep="\t", index_col=0, compression="gzip")
assert x.index.is_unique, "duplicated transcript ids"
assert set(x.columns) == set(lookup), (sorted(x.columns), sorted(lookup))
x = x.rename(columns=lookup)
x.index.name = "transcript_id"
out.parent.mkdir(parents=True, exist_ok=True)
x.to_csv(out)
print({"rows": x.shape[0], "cols": x.shape[1], "map": lookup})
