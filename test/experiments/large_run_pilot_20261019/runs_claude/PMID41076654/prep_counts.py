"""Repair GSE303983_genes.counts.csv.gz for the case runner.

1. Column names "3X-01_POST_S9.counts" -> "3X-01_POST" (= GEO title; the S-number is the
   sequencer sample sheet index and is not in the GEO metadata).
2. Feature IDs " ENSG00000004059.11|ARF5" -> gene symbol (leading space stripped); a symbol
   shared by several Ensembl genes keeps "SYMBOL|ENSG" so no rows are summed.
3. Paper's low-count filter (S2.6.2.1.p1; GEO data_processing): keep genes with >= 10 counts
   in at least 15 samples, irrespective of group. Paper reports 17,466 genes kept.

Usage: python prep_counts.py <in.csv.gz> <out.csv>
"""
import re
import sys

import pandas as pd

src, dst = sys.argv[1], sys.argv[2]
df = pd.read_csv(src, index_col=0)
df.columns = [re.sub(r"_S\d+\.counts$", "", c.strip()) for c in df.columns]
assert df.columns.is_unique, "duplicate sample columns after renaming"
ids = pd.Series(df.index.astype(str).str.strip())
ens = ids.str.split("|").str[0]
sym = ids.str.split("|").str[1].fillna(ens)
sym = sym.where(sym.str.len() > 0, ens)
keep = (df >= 10).sum(axis=1) >= 15
df = df.loc[keep.values]
ens, sym = ens[keep.values], sym[keep.values]
dup = sym.duplicated(keep=False)
df.index = [f"{s}|{e}" if d else s for s, e, d in zip(sym, ens, dup)]
df.index.name = "gene"
assert df.index.is_unique
df.to_csv(dst)
print(f"kept {df.shape[0]} genes x {df.shape[1]} samples; {int(dup.sum())} rows with shared symbols")
