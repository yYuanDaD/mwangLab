"""Collapse GSE315915 transcript-level (ENSMUST) raw counts to gene-level counts.

The deposited matrix is indexed by Ensembl mouse transcript IDs, but the paper
(S2.2.p1, FIG2) reports gene-level DESeq2 results. Each transcript is mapped to its
Ensembl gene (and symbol) with MyGene.info (scope ensembl.transcript); counts of
transcripts from one gene are summed (tools.omics_semantics.aggregate_transcripts_to_genes).
Unmapped transcripts are dropped and listed in the mapping file.

Usage: python prep/collapse_transcripts.py <matrix.txt.gz> <out_dir>
"""
import sys
from pathlib import Path

import pandas as pd
import mygene

sys.path.insert(0, str(Path(__file__).resolve().parents[6]))
from tools.omics_semantics import aggregate_transcripts_to_genes  # noqa: E402

src, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
out_dir.mkdir(parents=True, exist_ok=True)
counts = pd.read_csv(src, sep="\t", index_col=0)
ids = counts.index.astype(str).str.split(".").str[0]

map_csv = out_dir / "tx2gene_mygene.csv"
if map_csv.exists():
    mp = pd.read_csv(map_csv, index_col=0)
else:
    mg = mygene.MyGeneInfo()
    res = mg.querymany(list(ids.unique()), scopes="ensembl.transcript",
                       fields="ensembl.gene,symbol", species="mouse",
                       as_dataframe=False, returnall=True, verbose=False)
    rows = {}
    for hit in res["out"]:
        q = hit["query"]
        if hit.get("notfound") or q in rows:
            continue
        ens = hit.get("ensembl")
        genes = sorted({e["gene"] for e in (ens if isinstance(ens, list) else [ens]) if e and "gene" in e})
        rows[q] = {"gene_id": genes[0] if len(genes) == 1 else None,
                   "symbol": hit.get("symbol"), "n_gene_hits": len(genes)}
    mp = pd.DataFrame.from_dict(rows, orient="index").reindex(ids.unique())
    mp.index.name = "transcript_id"
    mp.to_csv(map_csv)

gene = pd.Series(mp.reindex(ids)["gene_id"].to_numpy(), index=counts.index)
genes = aggregate_transcripts_to_genes(counts, gene, method="sum").astype("int64")
genes.index.name = "gene_id"
genes.to_csv(out_dir / "GSE315915_gene_counts_from_transcripts.csv")

mapped = gene.notna()
print(f"transcripts={len(counts)} mapped={int(mapped.sum())} unmapped={int((~mapped).sum())}")
print(f"counts retained={counts[mapped.to_numpy()].to_numpy().sum() / counts.to_numpy().sum():.4f}")
print(f"genes={genes.shape[0]} samples={genes.shape[1]}")
