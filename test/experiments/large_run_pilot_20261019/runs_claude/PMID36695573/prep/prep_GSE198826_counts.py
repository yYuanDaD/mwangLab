"""Merge GSE198826 featureCounts files (Gas, Sol) into one matrix.

Skips the '#' featureCounts command line, renames BAM-path columns to the
library label (araki1, a1, ...) that GEO titles carry in brackets, and joins
Gas and Sol on Geneid. Usage: python prep_GSE198826_counts.py <data_dir> <out_csv>
"""
import re
import sys
import pandas as pd

data_dir, out_csv = sys.argv[1], sys.argv[2]
frames = []
for tissue in ("Gas", "Sol"):
    df = pd.read_csv(f"{data_dir}/GSE198826_counts_{tissue}.txt.gz", sep="\t", comment="#", index_col=0)
    df = df[[c for c in df.columns if c.endswith(".bam")]]
    df.columns = [re.match(r"^([^/]+)/", c).group(1) for c in df.columns]
    frames.append(df)
merged = frames[0].join(frames[1], how="inner")
merged.index.name = "Geneid"
merged.to_csv(out_csv)
print(merged.shape, list(merged.columns))
