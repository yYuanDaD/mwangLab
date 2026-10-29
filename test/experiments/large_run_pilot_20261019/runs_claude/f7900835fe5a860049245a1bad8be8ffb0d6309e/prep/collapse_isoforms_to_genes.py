"""Collapse GSE128078 RefSeq isoform FPKM to gene-level FPKM.

The deposited matrix (GSE128078_FES_isoforms_FPKM.txt.gz) is Cufflinks isoform FPKM
keyed by unversioned RefSeq transcript accessions (NM_/NR_). The paper analysed
gene-level expression and reports gene symbols. Cufflinks defines gene FPKM as the
sum of its isoform FPKMs, so isoforms are mapped to HGNC symbols (MyGene.info,
scope refseq, human) and summed per symbol. Transcripts without a symbol are
dropped (counted in the mapping report). Genes that are zero in every sample are
dropped (no information; no value is changed).

Usage: python collapse_isoforms_to_genes.py <isoform_fpkm.txt.gz> <out_dir>
"""
import json
import sys
from pathlib import Path

import mygene
import pandas as pd

src, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
out_dir.mkdir(parents=True, exist_ok=True)
iso = pd.read_csv(src, sep="\t", index_col=0)
iso.index = iso.index.astype(str)

map_path = out_dir / "refseq_to_symbol.csv"
if map_path.exists():
    mapping = pd.read_csv(map_path, index_col=0)["symbol"].dropna().to_dict()
else:
    mg = mygene.MyGeneInfo()
    hits = mg.querymany(list(iso.index), scopes="refseq", fields="symbol", species="human",
                        as_dataframe=False, returnall=False, verbose=False)
    mapping = {}
    for h in hits:
        if h.get("notfound") or "symbol" not in h:
            continue
        q = h["query"]
        if q not in mapping:  # first hit (MyGene orders by score)
            mapping[q] = h["symbol"]
    pd.Series(mapping, name="symbol").rename_axis("refseq").to_csv(map_path)

sym = pd.Series({t: mapping.get(t) for t in iso.index})
mapped = iso.loc[sym.notna()]
gene = mapped.groupby(sym.dropna()).sum()
gene.index.name = "gene"
nonzero = gene.loc[(gene > 0).any(axis=1)]
out = out_dir / "GSE128078_gene_FPKM.csv"
nonzero.to_csv(out)
report = {
    "input": str(src), "output": str(out),
    "n_transcripts": int(len(iso)), "n_transcripts_mapped": int(sym.notna().sum()),
    "n_transcripts_unmapped": int(sym.isna().sum()),
    "n_genes": int(len(gene)), "n_genes_all_zero_dropped": int(len(gene) - len(nonzero)),
    "n_genes_written": int(len(nonzero)),
    "rule": "sum of isoform FPKM per HGNC symbol (Cufflinks gene FPKM definition)",
    "mapping_source": "MyGene.info querymany scopes=refseq species=human, first hit",
}
(out_dir / "collapse_report.json").write_text(json.dumps(report, indent=1))
print(json.dumps(report, indent=1))
