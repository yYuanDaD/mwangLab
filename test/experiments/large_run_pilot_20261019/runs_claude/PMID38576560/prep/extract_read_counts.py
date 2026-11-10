"""Extract the HTSeq read-count columns of GSE256152_Gene_exp_with_symbol.txt.gz and
rename them to the GEO sample titles by name (never by position).

Matrix column  -> GEO title
  Tnm<r>:read count        -> Tnm-<r>
  Tnm_swim<r>:read count   -> Tnm-swim-<r>
  Tnm_cur<r>:read count    -> Tnm-cur-<r>
  Tnm_union<r>:read count  -> Tnm+union-<r>
The FPKM columns and annotation columns are dropped.
"""
import re, sys
import pandas as pd

src, out = sys.argv[1], sys.argv[2]
df = pd.read_csv(src, sep="\t", index_col=0)
sep = {"": "Tnm-", "swim": "Tnm-swim-", "cur": "Tnm-cur-", "union": "Tnm+union-"}
rename = {}
for c in df.columns:
    m = re.fullmatch(r"Tnm(?:_(swim|cur|union))?(\d+):read count", str(c))
    if m:
        rename[c] = sep[m.group(1) or ""] + m.group(2)
assert len(rename) == 12 and len(set(rename.values())) == 12, rename
counts = df[list(rename)].rename(columns=rename)
assert counts.isna().sum().sum() == 0, "missing read counts"
assert (counts.round() == counts).all().all(), "non-integer read counts"
assert not counts.index.duplicated().any()
counts = counts.astype(int)
counts.index.name = "gene_id"
counts.to_csv(out)
print(counts.shape, rename)
