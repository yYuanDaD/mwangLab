"""Prepare the GSE293221 count matrix for the case runner.

Input: data/GSE293221/GSE293221_merged_from_tar.csv (per-sample HTSeq counts merged by gene symbol).
Changes (no value is altered):
  1. Column names GSM8878836_Sample_DP_MT_013_Genes_ReadCount -> GSM8878836 (metadata index).
  2. Rows put in a fixed pseudo-random order (seed 0). Reason: tools/native.py:620 classifies feature IDs
     from the first 2000 rows only and the gene_symbol pattern (native.py:601) rejects digit-leading mouse
     symbols (0610005C13Rik ...). In the alphabetical file the head is Riken-heavy, so the IDs are called
     'other' (54.6%) and enrichment is skipped, although 93.5% of all IDs are gene symbols.
Usage: python prep_matrix.py <input_csv> <output_csv>
"""
import re
import sys

import pandas as pd

src, dst = sys.argv[1], sys.argv[2]
x = pd.read_csv(src, index_col=0)
x.columns = [re.match(r"^(GSM\d+)_", c).group(1) for c in x.columns]
assert x.columns.is_unique and not x.index.duplicated().any()
x = x.sample(frac=1.0, random_state=0)
x.index.name = "gene_id"
x.to_csv(dst)
print(x.shape)
