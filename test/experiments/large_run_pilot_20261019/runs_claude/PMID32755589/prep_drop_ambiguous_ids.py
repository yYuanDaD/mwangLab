"""Drop feature rows whose IDs are duplicated Excel-date conversions (1-Mar, 2-Mar).

In mouse, '1-Mar' can come from March1/Marchf1 or Marc1/Mtarc1 (same for 2-Mar), so the
two rows sharing each ID cannot be told apart. They are removed; all other rows are kept
unchanged (TPM values as deposited).
Usage: python prep_drop_ambiguous_ids.py <in.csv.gz> <out.csv>
"""
import sys
import pandas as pd

src, dst = sys.argv[1], sys.argv[2]
x = pd.read_csv(src, index_col=0)
dup = x.index.duplicated(keep=False)
print("dropping", sorted(set(x.index[dup])), int(dup.sum()), "rows")
x = x.loc[~dup]
x.index.name = "gene"
x.to_csv(dst)
print(x.shape)
