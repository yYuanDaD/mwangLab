"""Rename GSE245760 RSEM expected-count rows from '<ENSMUSG.ver>_<Symbol>' to the gene symbol.

Symbols that occur on more than one Ensembl gene keep '<Symbol>_<ENSMUSG>' (version stripped)
so distinct genes are never summed. Values are not changed (RSEM expected counts, non-integer).
Columns are kept as deposited ('A1.Aligned.toTranscriptome...'); the case spec strips the suffix.
"""
import sys
import pandas as pd

src, dst = sys.argv[1], sys.argv[2]
x = pd.read_csv(src, sep="\t", index_col=0)
ens = x.index.str.split("_", n=1).str[0].str.split(".").str[0]
sym = x.index.str.split("_", n=1).str[1]
dup = pd.Series(sym).duplicated(keep=False).values
new = [f"{s}_{e}" if d else s for s, e, d in zip(sym, ens, dup)]
x.index = pd.Index(new, name="gene")
assert x.index.is_unique
x.to_csv(dst)
print(x.shape, int(dup.sum()), "rows kept with Ensembl suffix")
