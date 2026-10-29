"""Collapse GSE315915 transcript-level (ENSMUST) raw counts to gene-level counts.

The deposited matrix is indexed by Ensembl mouse transcript IDs, but the paper
(S2.2.p1, FIG2) reports gene-level DESeq2 results. Each transcript is mapped to its
parent Ensembl gene with the Ensembl REST API (POST /lookup/id, field "Parent").
Counts of transcripts from one gene are summed
(tools.omics_semantics.aggregate_transcripts_to_genes). Transcripts that the current
Ensembl release no longer resolves (retired since GRCm38) are dropped and listed in the
mapping file with an empty gene_id.

Usage: python prep/collapse_transcripts.py <matrix.txt.gz> <out_dir>
"""
import sys
import time
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[6]))
from tools.omics_semantics import aggregate_transcripts_to_genes  # noqa: E402

src, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
out_dir.mkdir(parents=True, exist_ok=True)
counts = pd.read_csv(src, sep="\t", index_col=0)
ids = counts.index.astype(str).str.split(".").str[0]

map_csv = out_dir / "tx2gene_ensembl_rest.csv"
if map_csv.exists():
    mp = pd.read_csv(map_csv, index_col=0)
else:
    uniq = list(ids.unique())
    rows = {}
    for i in range(0, len(uniq), 1000):
        batch = uniq[i:i + 1000]
        for attempt in range(5):
            r = requests.post("https://rest.ensembl.org/lookup/id", json={"ids": batch},
                              headers={"Content-Type": "application/json",
                                       "Accept": "application/json"}, timeout=180)
            if r.ok:
                break
            time.sleep(5 * (attempt + 1))
        r.raise_for_status()
        for k, v in r.json().items():
            v = v or {}
            rows[k] = {"gene_id": v.get("Parent"), "biotype": v.get("biotype")}
    mp = pd.DataFrame.from_dict(rows, orient="index").reindex(uniq)
    mp.index.name = "transcript_id"
    mp.to_csv(map_csv)

gene = pd.Series(mp.reindex(ids)["gene_id"].to_numpy(), index=counts.index)
genes = aggregate_transcripts_to_genes(counts, gene, method="sum").astype("int64")
genes.index.name = "gene_id"
genes.to_csv(out_dir / "GSE315915_gene_counts_from_transcripts.csv")

mapped = gene.notna().to_numpy()
print(f"transcripts={len(counts)} mapped={int(mapped.sum())} unmapped={int((~mapped).sum())}")
print(f"counts retained={counts[mapped].to_numpy().sum() / counts.to_numpy().sum():.4f}")
print(f"genes={genes.shape[0]} samples={genes.shape[1]}")
