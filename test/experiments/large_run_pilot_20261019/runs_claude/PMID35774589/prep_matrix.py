"""Re-index the deposited GSE198652 Partek count matrix by gene symbol.

The deposited file's first column is `Chromosome` (not a gene ID), followed by
annotation columns; `Gene Symbol` is unique (checked below). Output keeps only
the 34 sample columns, values unchanged (non-integer estimated counts).
"""
import sys
from pathlib import Path

import pandas as pd

src = Path(sys.argv[1])
out = Path(sys.argv[2])
d = pd.read_csv(src, sep="\t")
ann = ["Chromosome", "Start", "Stop", "Strand", "Gene Symbol", "gene_biotype", "gene_name", "gene_source"]
assert d["Gene Symbol"].notna().all() and not d["Gene Symbol"].duplicated().any()
m = d.set_index("Gene Symbol").drop(columns=[c for c in ann if c != "Gene Symbol"])
m.index.name = "gene"
assert m.shape == (23011, 34), m.shape
out.parent.mkdir(parents=True, exist_ok=True)
m.to_csv(out)
print(out, m.shape)
