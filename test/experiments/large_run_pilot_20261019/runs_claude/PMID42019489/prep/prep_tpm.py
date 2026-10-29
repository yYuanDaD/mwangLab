"""Prepare GSE312393 TPM matrices for the case runner.

Repairs: the 6-week file carries a row-number index plus gene_id/gene_name
annotation columns; re-index it by Ensembl gene_id and drop the annotation.
Both files: strip whitespace from sample names, check unique Ensembl IDs.

Label-blind expression filter (declared in the method gate): keep genes with
TPM >= 1 in at least 3 samples of that file (the smallest arm size), so limma's
variance moderation is not dominated by tens of thousands of near-zero genes.
The unfiltered re-indexed matrices are also written for reference.
"""
from pathlib import Path
import sys

import pandas as pd

data = Path(sys.argv[1])  # data/GSE312393
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)


def finish(df: pd.DataFrame, stem: str) -> None:
    df.columns = [str(c).strip() for c in df.columns]
    df.index = df.index.astype(str).str.strip().str.replace(r"\.\d+$", "", regex=True)
    assert not df.index.duplicated().any(), f"{stem}: duplicated gene IDs"
    df = df.apply(pd.to_numeric, errors="raise")
    df.index.name = "gene_id"
    df.to_csv(out / f"{stem}_tpm_unfiltered.csv")
    keep = (df >= 1).sum(axis=1) >= 3
    df.loc[keep].to_csv(out / f"{stem}_tpm_filtered.csv")
    print(stem, "all", df.shape, "kept", int(keep.sum()))


h24 = pd.read_csv(data / "GSE312393_human_gene_24H_exercise_tpm.tsv.gz", sep="\t", index_col=0)
finish(h24, "h24")

w6 = pd.read_csv(data / "GSE312393_human_gene_6weeks_tpm.tsv.gz", sep="\t")
w6 = w6.set_index("gene_id").drop(columns=[c for c in w6.columns if c in ("gene_name",) or str(c).startswith("Unnamed")], errors="ignore")
finish(w6, "w6")
