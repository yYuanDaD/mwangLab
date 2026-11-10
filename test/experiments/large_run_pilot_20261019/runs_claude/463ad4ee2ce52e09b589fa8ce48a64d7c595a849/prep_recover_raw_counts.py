"""Recover integer raw counts from GSE207992_DESeq2_normcounts.csv.

The deposited file holds DESeq2-normalized counts (raw / size factor). In every
sample the smallest non-zero value corresponds to a raw count of 1, so
raw = norm / min_nonzero(norm). The script checks that the recovered values are
integers (tolerance 1e-3) for every entry and fails otherwise.

Columns are renamed to the sample label (AH1..AH16), which equals the GEO
metadata `description` field. Gene IDs lose their Ensembl version suffix
(checked unique). Annotation columns are dropped; a symbol map is written beside it.
"""
import re
import sys

import numpy as np
import pandas as pd

src, out, sym_out = sys.argv[1], sys.argv[2], sys.argv[3]
m = pd.read_csv(src, index_col=0)
annot = ["Chromosome", "Start", "End", "Strand", "Gene_ID"]
counts = m.drop(columns=annot)
raw = {}
report = []
for col in counts.columns:
    v = counts[col].to_numpy(dtype=float)
    mn = v[v > 0].min()
    r = v / mn
    dev = np.abs(r - np.round(r)).max()
    if dev > 1e-3:
        raise SystemExit(f"{col}: recovered values not integer (max deviation {dev})")
    label = re.search(r"\b(AH\d+)\b", col).group(1)
    raw[label] = np.round(r).astype(int)
    report.append((col, label, 1.0 / mn, int(np.round(r).sum()), dev))
df = pd.DataFrame(raw, index=[i.split(".")[0] for i in counts.index])
if df.index.duplicated().any():
    raise SystemExit("duplicated Ensembl IDs after stripping versions")
df.index.name = "gene_id"
df.to_csv(out)
pd.Series(m["Gene_ID"].values, index=df.index, name="symbol").to_csv(sym_out)
for col, label, sf, total, dev in report:
    print(f"{col} -> {label}: size_factor={sf:.4f} library={total} max_dev={dev:.2e}")
print(df.shape)
