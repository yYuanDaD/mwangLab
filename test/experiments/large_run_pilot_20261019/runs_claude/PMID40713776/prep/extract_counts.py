"""Extract the per-sample CLC 'Expression values' (total read counts) columns from the
GSE283853 CLC export and rename them to the GEO library names (m1..c3)."""
import sys
import pandas as pd

src, out = sys.argv[1], sys.argv[2]
d = pd.read_csv(src, index_col=0)
cols = [c for c in d.columns if c.endswith(" - Expression values")]
e = d[cols].copy()
e.columns = [c.split(" - ")[0] for c in cols]
e.index.name = "gene"
assert e.shape[1] == 12, e.shape
e.to_csv(out)
print(e.shape)
