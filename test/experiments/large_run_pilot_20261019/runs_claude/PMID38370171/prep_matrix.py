"""Prep GSE240131_raw_counts.txt.gz: index by gene symbol, drop ID annotation columns.

The deposited file carries st_gene_id, an integer Entrez gene_id column and gene_symbol
before the 12 sample columns. The integer gene_id column is otherwise read as a sample.
Three symbols are duplicated (Excel-mangled 1-Mar/2-Mar and Plin2); those rows get the
st_gene_id appended so no row is lost or summed.
"""
import sys
import pandas as pd

src, out = sys.argv[1], sys.argv[2]
d = pd.read_csv(src, sep="\t")
dup = d["gene_symbol"].duplicated(keep=False)
d.loc[dup, "gene_symbol"] = d.loc[dup, "gene_symbol"] + "__" + d.loc[dup, "st_gene_id"]
d = d.drop(columns=["st_gene_id", "gene_id"]).set_index("gene_symbol")
d.index.name = "gene"
assert d.index.is_unique and d.shape == (17397, 12)
d.to_csv(out)
print(d.shape, int(dup.sum()), "duplicated-symbol rows suffixed")
