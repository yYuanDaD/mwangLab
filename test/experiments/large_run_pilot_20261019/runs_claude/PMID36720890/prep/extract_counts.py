"""Extract the integer `count.*` columns from the two GSE214542 deposited files.

File 1 labels one count column `count.MPTP1_M`; its log-count profile correlates
best with `FPKM.MPTP_M_rep1`, and every other count column follows the
`<title>` naming, so it is renamed to `MPTP_M_rep1`. Column names become the
GEO sample titles. Gene IDs (Ensembl) stay as the index; gene_name is kept as
an annotation column.
"""
import sys
import pandas as pd

data_dir, out_dir = sys.argv[1], sys.argv[2]
for k in ("1", "2"):
    d = pd.read_csv(f"{data_dir}/GSE214542_{k}_genes_fpkm_expression.txt.gz", sep="\t", index_col=0)
    c = [x for x in d.columns if x.startswith("count.")]
    out = d[c].rename(columns=lambda x: x[len("count."):]).rename(columns={"MPTP1_M": "MPTP_M_rep1"})
    out = out.astype(int)
    out.index.name = "gene_id"
    out.to_csv(f"{out_dir}/GSE214542_{k}_counts.csv")
    print(k, out.shape, list(out.columns))
