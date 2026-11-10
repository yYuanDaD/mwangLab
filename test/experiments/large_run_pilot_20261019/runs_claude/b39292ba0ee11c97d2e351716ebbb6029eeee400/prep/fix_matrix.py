"""Repair GSE97718_FPKM_cufflinks_all_samples.txt.gz before analysis.

1. Excel turned March*/Sept*/Sep15 gene names into date serials (e.g. 36951 = 2001-03-01 = "Mar1").
   Serial -> date; month Mar -> MarchfN, Sep -> SeptinN, except Sep15 (selenoprotein 15) -> Selenof.
   N = year - 2000. Current MGI symbols are used so enrichment can map them.
2. Cufflinks emits one row per locus; 262 gene names occur on several loci. Rows with the same
   name are summed (FPKM is additive over the transcripts/loci of a gene) to give one gene-level row.
Usage: python fix_matrix.py <in.txt.gz> <out.csv>
"""
import sys
from datetime import date, timedelta
import pandas as pd

src, out = sys.argv[1], sys.argv[2]
df = pd.read_csv(src, sep="\t")
ids = df["gene_id"].astype(str)
fixed = {}
for v in sorted(set(i for i in ids if i.isdigit())):
    d = date(1899, 12, 30) + timedelta(days=int(v))
    n = d.year - 2000
    if d.day != 1 or d.month not in (3, 9) or not 1 <= n <= 15:
        raise SystemExit(f"unexpected serial {v} -> {d}")
    if d.month == 3:
        fixed[v] = f"Marchf{n}"
    else:
        fixed[v] = "Selenof" if n == 15 else f"Septin{n}"
clash = set(fixed.values()) & set(ids)
if clash:
    raise SystemExit(f"restored names already present: {clash}")
df["gene_id"] = ids.map(lambda i: fixed.get(i, i))
n_rows = len(df)
n_dup_names = int(df["gene_id"].duplicated(keep=False).groupby(df["gene_id"]).any().sum())
g = df.groupby("gene_id", sort=False).sum(numeric_only=True)
g.index.name = "gene_id"
g.to_csv(out)
print({"serials_restored": fixed, "rows_in": n_rows, "genes_out": len(g), "names_on_several_loci": n_dup_names})
