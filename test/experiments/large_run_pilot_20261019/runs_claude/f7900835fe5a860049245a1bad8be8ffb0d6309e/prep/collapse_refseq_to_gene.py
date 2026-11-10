"""Collapse GSE128078 Cufflinks isoform FPKM (RefSeq NM_/NR_ tracking ids) to gene-level FPKM.

Gene FPKM = sum of its RefSeq transcript FPKMs (Cufflinks gene-level FPKM is the sum of isoform FPKMs).
Mapping: MyGene.info, scopes=refseq, species=human, top-scored hit per accession. Unmapped ids dropped.
Usage: python collapse_refseq_to_gene.py <isoform_fpkm.txt.gz> <out_gene_fpkm.csv> <out_mapping.csv>
"""
import sys
import pandas as pd
import mygene

src, out, map_out = sys.argv[1:4]
x = pd.read_csv(src, sep="\t", index_col=0)
ids = x.index.astype(str).str.split(".").str[0]
x.index = ids
mg = mygene.MyGeneInfo()
hits = mg.querymany(list(dict.fromkeys(ids)), scopes="refseq", fields="symbol", species="human",
                    verbose=False, returnall=False)
best = {}
for h in hits:
    q = h.get("query")
    if h.get("notfound") or "symbol" not in h:
        continue
    sc = h.get("_score", 0)
    if q not in best or sc > best[q][1]:
        best[q] = (h["symbol"], sc)
mapping = pd.Series({k: v[0] for k, v in best.items()}, name="symbol")
mapping.index.name = "refseq"
mapping.to_csv(map_out)
sym = pd.Series(x.index.map(lambda i: mapping.get(i)), index=x.index)
keep = sym.notna()
g = x.loc[keep].groupby(sym[keep].values).sum()
g.index.name = "gene"
g.to_csv(out)
print(f"transcripts={len(x)} mapped={int(keep.sum())} unmapped={int((~keep).sum())} genes={len(g)} samples={g.shape[1]}")
