"""Build a clean CPM matrix and a combined sample sheet for GSE325957.

The deposited CPM file (GSE325957_CPM_and_Pairwise_DESEq2_Results.csv, converted from
the GEO xlsx) has a spurious first header row ("Unnamed: N") and a gene_symbol column.
Its 15 sample columns mix 9 exercised samples deposited in GSE325957 (NPE_*, HPE_*) with
6 sedentary samples reused from GSE120958 (NP_*, HP_*; GSM ids listed in the series'
own GSE325957_reanalysis_samples.csv). GSE325957 metadata covers only the 9 exercised
samples, so this script writes a combined sheet indexed by matrix column name.
Values are copied unchanged; no filtering or transformation.
"""
import sys
from pathlib import Path

import pandas as pd

data = Path(sys.argv[1])  # data/GSE325957
out = Path(sys.argv[2])   # run dir
out.mkdir(parents=True, exist_ok=True)

raw = pd.read_csv(data / "GSE325957_CPM_and_Pairwise_DESEq2_Results.csv", header=1)
raw = raw.set_index("gene_id")
cpm = raw.drop(columns=["gene_symbol"])
cpm = cpm[~cpm.index.isna()]
cpm.to_csv(out / "GSE325957_CPM_clean.csv")

meta = pd.read_csv(data / "GSE325957_metadata.csv", index_col=0)
rows = []
for gsm, r in meta.iterrows():
    sid = str(r["description"]).split(",")[-1].strip()  # "Library name: ...,NPE_1" -> NPE_1
    rows.append({"sample": sid, "gsm": gsm, "series": "GSE325957",
                 "sample_group": r["characteristics_ch1.1.sample group"],
                 "diet": "NP" if sid.startswith("NP") else "HP", "activity": "E"})
re = pd.read_csv(data / "GSE325957_reanalysis_samples.csv")
for _, r in re.iterrows():
    sid = r["Processed Data Column Header"]
    rows.append({"sample": sid, "gsm": r["GSM Number"], "series": r["GSE Number"],
                 "sample_group": ("Normal" if sid.startswith("NP") else "High") + " Phosphate Sedentary (GSE120958)",
                 "diet": "NP" if sid.startswith("NP") else "HP", "activity": "S"})
sheet = pd.DataFrame(rows).set_index("sample")
missing = set(cpm.columns) ^ set(sheet.index)
assert not missing, missing
sheet.loc[list(cpm.columns)].to_csv(out / "GSE325957_combined_samples.csv")
print(cpm.shape, sheet.shape, int(cpm.isna().sum().sum()))
