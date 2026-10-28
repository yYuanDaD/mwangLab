"""Transpose GSE324100's deposited DESeq2-normalized matrix (samples x genes, with
annotation columns) into genes x samples, keyed by library name (e.g. P1_S25).

Checks that the file's own Group/Sex labels agree with GEO metadata (title) for
each library before writing.
"""
import re
import sys
from pathlib import Path

import pandas as pd

root = Path(__file__).resolve().parents[5]
src = root / "data/GSE324100/GSE324100_C26_PoWeR_Prevention_Gastroc_RNA-seq_Normalized_counts.txt.gz"
meta_p = root / "data/GSE324100/GSE324100_metadata.csv"
out = Path(__file__).resolve().parent / "GSE324100_normalized_counts_genes_x_samples.csv"

x = pd.read_csv(src, sep="\t")
ann = ["Sample name", "Group", "Sex", "Group (Sex-Independent)"]
labels = x[ann].set_index("Sample name")
m = pd.read_csv(meta_p, index_col=0)
m["lib"] = m["description"].str.extract(r"Library name: (P\d+_S\d+)")[0]
mm = m.set_index("lib")
bad = []
for lib, row in labels.iterrows():
    title = re.sub(r"\d+$", "", mm.loc[lib, "title"])
    if title != row["Group"] or mm.loc[lib, "characteristics_ch1.2.Sex"] != row["Sex"]:
        bad.append((lib, row["Group"], title))
if bad or set(labels.index) != set(mm.index):
    sys.exit(f"label mismatch: {bad}; libs file-only={set(labels.index)-set(mm.index)} meta-only={set(mm.index)-set(labels.index)}")

g = x.drop(columns=ann[1:]).set_index("Sample name").T
g.index.name = "gene_id"
g = g[sorted(g.columns, key=lambda s: int(s.split("_")[0][1:]))]
g.to_csv(out)
print(f"wrote {out} shape={g.shape}; labels agree with GEO metadata for all {len(labels)} libraries")
