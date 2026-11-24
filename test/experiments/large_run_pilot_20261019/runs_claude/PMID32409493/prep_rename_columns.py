"""Rename GSE137631 raw-count columns to GSM ids by an explicit name rule (not by position).

Matrix column            -> GEO sample title             -> GSM
RYGB.<k>.<PRE|POST9>     -> "RYGB_<k> <PRE|POST9>"
WD.RYGB.ET.<k>.<T>       -> "RYGB + exercise training_<k> <T>"
WD.lean.control.<k>      -> "lean control_<k>"
Usage: python prep_rename_columns.py <raw_counts.txt.gz> <metadata.csv> <out.csv>
"""
import re
import sys

import pandas as pd

raw, meta_path, out = sys.argv[1:4]
counts = pd.read_csv(raw, sep=None, engine="python", index_col=0)
meta = pd.read_csv(meta_path, index_col=0)
title_to_gsm = {t: g for g, t in meta["title"].items()}

def to_title(col: str) -> str:
    if m := re.fullmatch(r"RYGB\.(\d+)\.(PRE|POST9)", col):
        return f"RYGB_{m[1]} {m[2]}"
    if m := re.fullmatch(r"WD\.RYGB\.ET\.(\d+)\.(PRE|POST9)", col):
        return f"RYGB + exercise training_{m[1]} {m[2]}"
    if m := re.fullmatch(r"WD\.lean\.control\.(\d+)", col):
        return f"lean control_{m[1]}"
    raise SystemExit(f"unmapped column {col}")

rename = {c: title_to_gsm[to_title(c)] for c in counts.columns}
assert len(set(rename.values())) == len(rename) == 30
counts = counts.rename(columns=rename)
counts.index.name = "gene_id"
counts.to_csv(out)
pd.Series(rename, name="gsm").to_csv(out.replace(".csv", "_column_map.csv"), header=True)
print(counts.shape)
