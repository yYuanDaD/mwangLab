"""Repair GSE302911 TPM matrix for alignment.

The deposited file is whitespace-separated with a quoted header that has one
fewer field than the data rows (gene symbol is the row index). Column names
(e.g. Untrained_0h1) differ from the GEO library names (Untrained_0h_1) only by
the underscore before the replicate digit. This script reads the file, inserts
that underscore by a name rule (no positional mapping), checks every renamed
column is a GEO library name, and writes a CSV. Values are unchanged.
"""
import re
import sys
import pandas as pd

src, meta_csv, out = sys.argv[1:4]
d = pd.read_csv(src, sep=r"\s+")
d.index.name = "gene_symbol"
new = {c: re.sub(r"^(.*?)(\d)$", r"\1_\2", c) for c in d.columns}
meta = pd.read_csv(meta_csv, index_col=0)
libs = set(meta["description"].str.extract(r"Library name: (\S+?),RNASeq", expand=False))
missing = sorted(set(new.values()) - libs)
if missing or len(set(new.values())) != len(new):
    raise SystemExit(f"rename check failed: {missing}")
d = d.rename(columns=new)
d.to_csv(out)
print(d.shape, list(d.columns))
