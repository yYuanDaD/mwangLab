"""Prep GSE269016_raw_counts.txt.gz: keep the RSEM read_count_* columns (drop fpkm_*), index by gene_symbol
(unique, no missing), and strip the read_count_ prefix so columns are the sample codes S1..S6/E1..E6 used in GEO titles."""
import sys
import pandas as pd
src, out = sys.argv[1], sys.argv[2]
d = pd.read_csv(src, sep="\t")
assert d.gene_symbol.notna().all() and not d.gene_symbol.duplicated().any()
cols = [c for c in d.columns if c.startswith("read_count_")]
m = d.set_index("gene_symbol")[cols]
m.columns = [c.replace("read_count_", "") for c in cols]
m.index.name = "gene_symbol"
m.to_csv(out)
print(m.shape)
