"""Repair GSE222163_exp_all.csv.gz before the case runner reads it.

1. Matrix column names use 'Ctrl' while GEO 'description' uses 'ctrl' (BAT_Ctrl1 vs BAT_ctrl1);
   the case is the only difference, so the columns are lower-cased on that token to match
   the metadata description exactly (one-to-one, checked below).
2. Two Excel-mangled symbols ('1-Mar', '2-Mar') each occur twice (March1/Mtarc1 and
   March2/Mtarc2 collapsed by Excel). Their identity cannot be recovered, so the four rows
   are dropped.
Values are not changed.
"""
import sys
from pathlib import Path

import pandas as pd

src = Path(sys.argv[1])
meta = Path(sys.argv[2])
out = Path(sys.argv[3])

x = pd.read_csv(src, index_col=0)
m = pd.read_csv(meta, index_col=0)
x.columns = [c.replace("_Ctrl", "_ctrl") for c in x.columns]
desc = set(m["description"].astype(str))
assert set(x.columns) == desc and len(x.columns) == len(desc), "column/description mismatch"
dup = x.index[x.index.duplicated(keep=False)]
print("dropping duplicated symbols:", sorted(set(dup)), "rows:", len(dup))
x = x.loc[~x.index.duplicated(keep=False)]
out.parent.mkdir(parents=True, exist_ok=True)
x.to_csv(out)
print("wrote", out, x.shape)
