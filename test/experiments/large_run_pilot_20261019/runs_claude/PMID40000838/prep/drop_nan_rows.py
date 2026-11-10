"""Drop the 57 all-NaN gene rows from the GSE280656 RSEM gene-count matrices (values otherwise unchanged)."""
import sys
import pandas as pd

src, dst = sys.argv[1], sys.argv[2]
d = pd.read_csv(src, sep="\t", index_col=0)
na = d.isna()
partial = na.any(axis=1) & ~na.all(axis=1)
assert not partial.any(), f"{int(partial.sum())} rows are only partly NaN"
out = d.loc[~na.all(axis=1)]
print(f"{src}: {d.shape} -> {out.shape} (dropped {int(na.all(axis=1).sum())} all-NaN rows)")
out.to_csv(dst)
