"""Prepare GSE205907 inputs for the case runner.

1. Matrix: drop the 27 rows whose gene IDs were mangled into dates by Excel
   (2019-03-xx = Marchf genes, 2019-09-xx = Septin genes; two duplicated;
   which date maps to which gene cannot be recovered, so they are removed).
2. Sample sheet: the deposited FPKM matrix columns (e.g. E26Nigra, M6Stria,
   S1Cortex) carry the animal ID, treatment group and brain region, but GEO
   sample titles only carry "<region>,<treatment>,rep<k>". There is no
   non-positional key from matrix columns to GSM IDs, so the sample sheet is
   derived from the column names themselves:
     prefix E -> MPTP+exercise (EX), M -> MPTP, S -> Saline (SAL)
     suffix Cereb / Corte|Cortex / Nigra / Stria -> region
   The derived counts (4 animals x 3 groups x 4 regions) are checked against
   the GEO metadata's treatment x tissue table.

Usage: python prep_GSE205907.py <data_dir> <out_dir>
"""
import re
import sys
from pathlib import Path

import pandas as pd

data_dir, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
out_dir.mkdir(parents=True, exist_ok=True)

mat = pd.read_csv(data_dir / "GSE205907_fpkm.csv", index_col=0)
bad = [i for i in mat.index if re.fullmatch(r"\d{4}-\d{2}-\d{2}.*", str(i))]
mat = mat.drop(index=bad)
assert not mat.index.duplicated().any()
mat.index.name = "gene"
mat.to_csv(out_dir / "GSE205907_fpkm_clean.csv")

grp_map = {"E": "EX", "M": "MPTP", "S": "SAL"}
reg_map = {"Cereb": "Cereb", "Corte": "Cortex", "Cortex": "Cortex", "Nigra": "Nigra", "Stria": "Stria"}
rows = []
for col in mat.columns:
    m = re.fullmatch(r"([EMS])(\d+)(Cereb|Cortex|Corte|Nigra|Stria)", col)
    assert m, col
    rows.append({"sample": col, "grp": grp_map[m.group(1)], "animal": f"{m.group(1)}{m.group(2)}",
                 "tissue": reg_map[m.group(3)]})
sheet = pd.DataFrame(rows).set_index("sample")
sheet.to_csv(out_dir / "GSE205907_sample_sheet.csv")

geo = pd.read_csv(data_dir / "GSE205907_metadata.csv", index_col=0)
geo_tab = pd.crosstab(geo["characteristics_ch1.1.treatment"].map(
    {"MPTP+exercise": "EX", "MPTP": "MPTP", "Saline": "SAL"}),
    geo["characteristics_ch1.0.tissue"].map(
    {"cerebellum": "Cereb", "cortex": "Cortex", "nigra": "Nigra", "striatum": "Stria"}))
our_tab = pd.crosstab(sheet["grp"], sheet["tissue"])
assert geo_tab.equals(our_tab.loc[geo_tab.index, geo_tab.columns]), (geo_tab, our_tab)
print("dropped rows:", bad)
print(our_tab)
print("each animal has 4 regions:", sheet.groupby("animal").size().eq(4).all())
