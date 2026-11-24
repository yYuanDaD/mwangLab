"""Rename the deposited matrix column prefix 'cont_' to 'Control_' so the columns
match the GEO titles (e.g. 'Control synovium rep1') after key normalization.
Values are not changed."""
import sys, pandas as pd
src, dst = sys.argv[1], sys.argv[2]
x = pd.read_csv(src, index_col=0)
x.columns = [c.replace("cont_", "Control_", 1) if c.startswith("cont_") else c for c in x.columns]
x.to_csv(dst)
print(dst, x.shape)
