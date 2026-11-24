"""Rename the deposited matrix column 'Exe_KO_reap4' to 'Exe_KO_rep4' (GEO title of GSM8606529).

The deposited GSE280845_RAWCountMatrix.csv.gz has one typo in a column name; every other
column equals a GEO sample title exactly. Values are not touched.
Usage: python -I fix_column_typo.py <in.csv.gz> <out.csv.gz>
"""
import sys
import pandas as pd

src, dst = sys.argv[1], sys.argv[2]
df = pd.read_csv(src, index_col=0)
assert "Exe_KO_reap4" in df.columns and "Exe_KO_rep4" not in df.columns
df = df.rename(columns={"Exe_KO_reap4": "Exe_KO_rep4"})
df.to_csv(dst)
print(df.shape, list(df.columns))
