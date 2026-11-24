"""Add the suitability report's X/Y-inferred sex to a copy of the GEO metadata.

GEO GSE277819 deposits no sex field; the paper enrolled older men and women.
Inputs: the GEOparse metadata CSV and suitability/aligned_matrix_sex_check.tsv
(from the first case_runner execute). Refuses if any subject's three biopsies
disagree or any call is not high confidence.
"""
import sys
import pandas as pd

meta_csv, sex_tsv, out_csv = sys.argv[1:4]
meta = pd.read_csv(meta_csv, index_col=0)
sex = pd.read_csv(sex_tsv, sep="\t", index_col=0)
if set(sex.index) != set(meta.index):
    sys.exit("sex table and metadata sample sets differ")
if (sex["confidence"] != "high").any():
    sys.exit("non-high-confidence sex calls present")
meta["inferred_sex"] = sex.loc[meta.index, "predicted_sex"]
pid = meta["characteristics_ch1.1.participant id"]
per_subject = meta.groupby(pid)["inferred_sex"].nunique()
if (per_subject > 1).any():
    sys.exit(f"subjects with discordant sex calls: {list(per_subject[per_subject > 1].index)}")
meta.to_csv(out_csv)
print(meta.groupby("inferred_sex")[pid.name].nunique().to_dict())
