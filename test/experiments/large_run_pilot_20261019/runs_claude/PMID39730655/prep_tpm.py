"""Extract the per-sample TPM block from GSE280324_FPKM.txt.gz.

The deposited file holds FPKM, TPM, read-count and group-average columns side
by side. The paper (S3.p1) used TPM -> log2(TPM+1) -> limma, so keep only the
six tpm_* columns, index by gene_symbol (unique, no NA), and rename the columns
to the sample tag (C_48, ..., E_71) that GEO 'description' carries as fpkm_<tag>.
"""
import sys
from pathlib import Path

import pandas as pd

src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/GSE280324/GSE280324_FPKM.txt.gz")
out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).with_name("GSE280324_TPM.csv")

d = pd.read_csv(src, sep="\t")
assert not d["gene_symbol"].duplicated().any() and d["gene_symbol"].notna().all()
tpm_cols = [c for c in d.columns if c.startswith("tpm_")]
assert len(tpm_cols) == 6, tpm_cols
m = d.set_index("gene_symbol")[tpm_cols]
m.columns = [c[len("tpm_"):] for c in tpm_cols]
m.index.name = "gene"
m.to_csv(out)
print(out, m.shape, m.sum().round(1).to_dict())
