"""Scan all downloaded GEO metadata CSVs for a stratification axis (time/duration/dose)
to find a real validation target for requirement #8. Zero cost (pandas only)."""

import os
import sys
import glob
import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))

TIME_HINTS = ("time", "timepoint", "duration", "week", "wk", "day", "hour", "hr",
              "month", "dose", "age", "post", "stage")
DESIGN_HINTS = ("characteristics", "title", "source", "treatment", "group",
                "condition", "phenotype", "genotype", "agent", "exercise")


def looks_timelike(values):
    """True if the column's distinct values look like a graded time/dose axis."""
    joined = " ".join(str(v).lower() for v in values)
    return any(h in joined for h in ("week", "wk", " day", "days", "hour", " hr",
                                     "month", "min", "timepoint", "h post", "dose"))


for mpath in sorted(glob.glob(os.path.join("data", "*", "*metadata*.csv"))):
    acc = os.path.basename(os.path.dirname(mpath))
    try:
        df = pd.read_csv(mpath, index_col=0)
    except Exception as e:
        continue
    time_cols, design_cols = [], []
    for col in df.columns:
        cl = str(col).lower()
        vals = df[col].dropna().astype(str)
        uniq = vals.unique().tolist()
        if not (2 <= len(uniq) <= 10):
            continue
        name_time = any(h in cl for h in TIME_HINTS)
        val_time = looks_timelike(uniq)
        if name_time or val_time:
            time_cols.append((col, uniq))
        if any(h in cl for h in DESIGN_HINTS):
            design_cols.append((col, uniq))
    if time_cols and design_cols:
        print(f"\n=== {acc}  ({df.shape[0]} samples) ===")
        print("  TIME-LIKE columns:")
        for col, uniq in time_cols[:4]:
            print(f"    [{col}] -> {uniq[:8]}")
        print("  DESIGN columns:")
        for col, uniq in design_cols[:4]:
            print(f"    [{col}] -> {uniq[:8]}")
