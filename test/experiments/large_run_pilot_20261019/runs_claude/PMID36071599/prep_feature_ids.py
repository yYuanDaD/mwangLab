"""GSE211204 RSEM gene matrix: rows are 'ENSG...version|SYMBOL'. Write a copy indexed by gene
symbol (unique symbols) or unversioned Ensembl ID (symbols shared by several genes), values unchanged.

usage: python -I prep_feature_ids.py <in RawCountFile_RSEM_genes.txt.gz> <out.csv>
"""
import sys

import pandas as pd

src, dst = sys.argv[1], sys.argv[2]
m = pd.read_csv(src, sep="\t", index_col=0)
ens = m.index.str.split("|").str[0].str.replace(r"\.\d+$", "", regex=True)
sym = m.index.str.split("|").str[1]
dup = pd.Series(sym).duplicated(keep=False).values
new = [e if (d or not isinstance(s, str) or not s) else s for e, s, d in zip(ens, sym, dup)]
m.index = new
m.index.name = "gene"
assert not m.index.has_duplicates, m.index[m.index.duplicated()][:5].tolist()
m.to_csv(dst)
print(f"{m.shape[0]} genes x {m.shape[1]} samples; {int(dup.sum())} rows kept as Ensembl IDs (shared symbols)")
