"""Prepare GSE299413 normalized-count matrices for the case runner.

The deposited Partek Flow files carry 20 annotation columns (Chromosome,
Start, Stop, Length, ... transl_table) before the sample columns; Start/Stop/
Length are numeric and would be read as samples. This script keeps only the
gene symbol (unique in both files) as the index and the RNA230912TZ_* sample
columns, without changing any value. One output file per tissue.
"""
import sys
from pathlib import Path

import pandas as pd

src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/GSE299413")
out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).parent / "prep"
out.mkdir(parents=True, exist_ok=True)
for tissue in ("Tibialis", "Tumor"):
    d = pd.read_csv(src / f"GSE299413_{tissue}_Normalized_counts.txt.gz", sep="\t")
    assert not d["Gene Symbol"].duplicated().any()
    samples = [c for c in d.columns if c.startswith("RNA230912TZ_")]
    m = d.set_index("Gene Symbol")[samples]
    m.index.name = "gene"
    m.to_csv(out / f"GSE299413_{tissue}_normalized_clean.csv")
    print(tissue, m.shape)
