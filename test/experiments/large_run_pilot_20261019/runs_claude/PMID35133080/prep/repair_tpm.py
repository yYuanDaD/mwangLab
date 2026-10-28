"""Repair GSE186045_tpm_table.csv (Excel export) into a gene x sample TPM matrix.

Deposited layout: row 1 is a sheet title, row 2 the real header
(ensembl Gene ID, Gene Name, 1A-PRE, ...), last row a column SUM (= 1e6).
Repairs (no value is changed):
  1. use row 2 as header; drop the trailing SUM row;
  2. index by gene symbol (unique after checking), keep Ensembl ID out;
  3. rename sample columns '<subject>-PRE/POST' -> '<subject>-pre/post' so they
     equal the key derived from the GEO 'title' field (exact, name-based, not positional).
Then the paper's expression filter (S2.5.p1: "Protein-coding genes with a TPM > 0.1")
is applied as mean TPM across all 26 libraries > 0.1 and written as a separate file.
Usage: python repair_tpm.py <in_csv> <out_dir>
"""
import sys
from pathlib import Path
import pandas as pd

src, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
out_dir.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(src, header=1)
df = df[df["Gene Name"] != "SUM"]
assert df["Gene Name"].notna().all(), "missing gene names"
dup = df["Gene Name"].duplicated(keep=False)
print("duplicated symbols:", int(dup.sum()), df.loc[dup, "Gene Name"].tolist()[:10])
if dup.any():
    # keep Ensembl ID for duplicated symbols to stay unique; do not merge values
    df.loc[dup, "Gene Name"] = df.loc[dup, "Gene Name"] + "|" + df.loc[dup, "ensembl Gene ID"]
df = df.drop(columns=["ensembl Gene ID"]).set_index("Gene Name")
df.index.name = "gene"
df.columns = [c.replace("-PRE", "-pre").replace("-POST", "-post") for c in df.columns]
df = df.apply(pd.to_numeric, errors="raise")
print("shape", df.shape, "NaN", int(df.isna().sum().sum()), "colsum range",
      float(df.sum().min()), float(df.sum().max()))
df.to_csv(out_dir / "GSE186045_tpm_repaired.csv")
keep = df.mean(axis=1) > 0.1
filt = df.loc[keep]
print("filter mean TPM > 0.1:", int(keep.sum()), "of", len(df))
filt.to_csv(out_dir / "GSE186045_tpm_meanTPMgt0.1.csv")
