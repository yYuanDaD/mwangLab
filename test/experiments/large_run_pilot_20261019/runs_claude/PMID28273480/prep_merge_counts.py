"""Merge the two GSE97084 count files (two sequencing batches) into one matrix.

Both files share the same 57,773 Ensembl gene rows (GeneID unique). Annotation
columns (Chr, GeneName, Start, Stop, CodingLength) and the empty trailing column
are dropped; sample columns 's_10B-180_GeneCount' are renamed to the sample code
('10B') used in the GEO titles (upper-cased: the deposit has 's_18a-180').
"""
import re
import sys
from pathlib import Path

import pandas as pd

data = Path(sys.argv[1] if len(sys.argv) > 1 else "data/GSE97084")
out = Path(sys.argv[2] if len(sys.argv) > 2 else data / "GSE97084_merged_counts.csv")

frames = []
for f in ["GSE97084_GeneCount_raw.tsv.gz", "GSE97084_GeneCount_raw_2.tsv.gz"]:
    d = pd.read_csv(data / f, sep="\t")
    d = d.set_index("GeneID")
    cols = [c for c in d.columns if c.startswith("s_") and c.endswith("_GeneCount")]
    d = d[cols]
    d.columns = [re.match(r"^s_(\w+)-180_GeneCount$", c).group(1).upper() for c in cols]
    frames.append(d)

assert frames[0].index.equals(frames[1].index), "gene rows differ between files"
m = pd.concat(frames, axis=1)
assert not m.columns.duplicated().any()
m.index.name = "GeneID"
m.to_csv(out)
print(out, m.shape)
