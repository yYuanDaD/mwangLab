"""Split GSE235174_counts_allsamples.txt.gz into its three side-by-side blocks.

The deposited file holds three tables pasted column-wise in one TSV:
  cols 0-8   : gene_id_mRNA + 8 HTSeq integer counts (20,030 rows)
  cols 9-17  : lncRNA_id + 8 lncRNA quantities (non-integer; 52,355 rows)
  col  18    : Chrom (lncRNA annotation)
  cols 19-27 : id_circRNA + 8 CIRI back-splice junction read counts (11,526 rows)
Rows of the shorter blocks are padded with empty cells. Each block is written
as its own CSV (feature id index, columns aPR_1..4, bPR_1..4). Duplicated mRNA
symbols (2 symbols) are summed.
"""
import sys
from pathlib import Path

import pandas as pd

src = Path(sys.argv[1])
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)

raw = pd.read_csv(src, sep="\t", header=None, dtype=str)
header = raw.iloc[0].tolist()
d = raw.iloc[1:]
samples = header[1:9]
assert samples == header[10:18] == header[20:28], header

blocks = {"mRNA": (0, list(range(1, 9))), "lncRNA": (9, list(range(10, 18))), "circRNA": (19, list(range(20, 28)))}
for name, (idcol, cols) in blocks.items():
    b = d[[idcol] + cols].dropna(subset=[idcol])
    b.columns = ["feature_id"] + samples
    vals = b[samples].astype(float)
    assert not vals.isna().any().any(), name
    vals.index = b["feature_id"].values
    n_dup = int(vals.index.duplicated().sum())
    vals = vals.groupby(level=0, sort=False).sum()
    vals.index.name = "feature_id"
    vals.to_csv(out / f"GSE235174_{name}_counts.csv")
    print(name, vals.shape, "duplicated ids summed:", n_dup)
