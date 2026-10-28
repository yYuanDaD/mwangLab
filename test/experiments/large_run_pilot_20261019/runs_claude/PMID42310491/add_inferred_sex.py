"""Add the X/Y-inferred sex (suitability sex check) to the GEO metadata.

GEO GSE324036 does not record sex, although the paper used male and female mice
(S1.1.p1). The case runner's suitability sex check (Xist vs chrY genes, all
calls high confidence) is copied into a column `sex` so a sensitivity model can
adjust for it. Inputs and output are given as arguments.

usage: python add_inferred_sex.py <metadata.csv> <sex_check.tsv> <out.csv>
"""
import sys

import pandas as pd

meta_path, sex_path, out_path = sys.argv[1:4]
meta = pd.read_csv(meta_path, index_col=0)
sex = pd.read_csv(sex_path, sep="\t", index_col=0)
assert set(sex.index) == set(meta.index), "sex table and metadata samples differ"
assert (sex["confidence"] == "high").all(), "uncertain sex call"
meta["sex"] = sex.loc[meta.index, "predicted_sex"]
meta.to_csv(out_path)
print(meta["sex"].value_counts().to_dict())
