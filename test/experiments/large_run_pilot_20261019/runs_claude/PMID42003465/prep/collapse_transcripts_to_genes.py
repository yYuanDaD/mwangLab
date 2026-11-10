"""GSE315915's deposited matrix is keyed by ENSMUST transcript IDs, one row per transcript,
under a column named GeneID. The paper reports genes. This sums each gene's transcript counts
using Ensembl release 102 (GRCm38, the assembly named in the GEO processing notes) and writes
a gene-level integer count matrix plus the mapping record.

Usage: collapse_transcripts_to_genes.py <gtf.gz> <counts.txt.gz> <out_dir>
"""
import gzip
import re
import sys
from pathlib import Path

import pandas as pd

gtf, counts_path, out_dir = sys.argv[1], sys.argv[2], Path(sys.argv[3])
rows = []
with gzip.open(gtf, "rt") as handle:
    for line in handle:
        if line.startswith("#"):
            continue
        fields = line.rstrip("\n").split("\t")
        if fields[2] != "transcript":
            continue
        attrs = dict(re.findall(r'(\w+) "([^"]*)"', fields[8]))
        rows.append((attrs["transcript_id"], attrs["gene_id"], attrs.get("gene_name"),
                     attrs.get("gene_biotype"), attrs.get("transcript_biotype"), fields[0]))
tx2gene = pd.DataFrame(rows, columns=["transcript", "gene_id", "symbol", "gene_biotype",
                                      "transcript_biotype", "chrom"]).set_index("transcript")
counts = pd.read_csv(counts_path, sep="\t", index_col=0)
mapping = tx2gene.reindex(counts.index)
mapping.insert(0, "total_count", counts.sum(axis=1))
mapping.to_csv(out_dir / "transcript_gene_mapping.csv")

mapped = mapping["gene_id"].notna()
print("transcripts", len(counts), "mapped", int(mapped.sum()), "unmapped", int((~mapped).sum()))
print("share of counts unmapped", round(counts[~mapped].sum().sum() / counts.sum().sum(), 5))
print("transcript biotypes\n", mapping["transcript_biotype"].value_counts().head(8).to_string())
print("chrom MT share", round(counts[mapping["chrom"] == "MT"].sum().sum() / counts.sum().sum(), 4))

gene = counts[mapped].groupby(mapping.loc[mapped, "gene_id"]).sum()
gene.index.name = "gene_id"
gene.to_csv(out_dir / "GSE315915_gene_level_counts.csv")
symbols = mapping.loc[mapped].drop_duplicates("gene_id").set_index("gene_id")["symbol"]
symbols.to_csv(out_dir / "gene_symbols.csv")
print("genes", gene.shape, "nonzero", int((gene.sum(axis=1) > 0).sum()))
print("per gene transcripts", mapping.loc[mapped].groupby("gene_id").size().describe().round(2).to_dict())
