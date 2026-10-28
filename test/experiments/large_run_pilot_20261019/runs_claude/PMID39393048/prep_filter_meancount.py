"""Apply the paper's gene filter (S2.12.6.p1) to the deposited GEO count matrix.

"Genes with a mean across all samples of 10 reads per million (RPM) or fewer reads
were removed (63%) ... leaving a total of 14,979 for analysis."

Input : data/GSE267512/GSE267512_GeneCounts_RAW_DATA.csv.gz (Ensembl rows, SYMBOL column, 57 samples)
Output: <run_dir>/prep/GSE267512_counts_rowmean_ge10.csv (same layout, filtered rows)
The text says "10 RPM" but the authors code (github.com/DaniHiam/TESTO_RNAseq, "TESTO_RNAseq Analysis_Github.R")
filters rowMeans(raw counts) >= 10; that rule is applied here over the 57 deposited samples.
"""
import sys
from pathlib import Path

import pandas as pd

src = Path(sys.argv[1])
out = Path(sys.argv[2])
df = pd.read_csv(src, index_col=0)
annot = [c for c in df.columns if not pd.api.types.is_numeric_dtype(df[c])]
counts = df.drop(columns=annot)

keep = counts.mean(axis=1) >= 10  # authors code: rowMeans(xx) >= 10
out.parent.mkdir(parents=True, exist_ok=True)
df.loc[keep].to_csv(out)
print(f"annotation={annot} samples={counts.shape[1]} genes_in={len(df)} kept={int(keep.sum())} "
      f"removed_frac={1 - keep.mean():.3f}")
