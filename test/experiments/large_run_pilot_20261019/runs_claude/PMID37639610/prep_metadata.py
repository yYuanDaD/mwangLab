"""Build a sample sheet keyed by the matrix column names of GSE233485.

The deposited TPM matrix uses animal IDs (WT_1, MCK_3874, MKO_SO_23, ...) that do not
appear anywhere in the GEO sample records (descriptions are WT_3mo_1, mTG_24mo_3, ...), so
a GSM-level mapping is not determinable. Group membership is encoded in the column prefix:
  WT_*      -> WT, 3 mo        WSO_*    -> WT, 24 mo
  MCK_*     -> mTG, 3 mo       MCK_SO_* -> mTG, 24 mo   (MCK = muscle creatine kinase promoter transgene)
  MKO_*     -> mKO, 3 mo       MKO_SO_* -> mKO, 24 mo
The script checks the per-group counts against the GEO metadata and fails if they differ.
No sample is mapped to a GSM id; position is never used.
"""
import re, sys
import pandas as pd

matrix, geo_meta, out = sys.argv[1:4]
cols = pd.read_csv(matrix, sep="\t", index_col=0, nrows=1).columns.astype(str)
rules = [(r"^WSO_\d+$", "WT", "24mo"), (r"^MCK_SO_\d+$", "mTG", "24mo"), (r"^MKO_SO_\d+$", "mKO", "24mo"),
         (r"^WT_\d+$", "WT", "3mo"), (r"^MCK_\d+$", "mTG", "3mo"), (r"^MKO_\d+$", "mKO", "3mo")]
rows = []
for c in cols:
    hits = [(g, a) for p, g, a in rules if re.match(p, c)]
    if len(hits) != 1:
        raise SystemExit(f"column {c} matched {len(hits)} rules")
    rows.append({"sample": c, "genotype": hits[0][0], "age": hits[0][1]})
sheet = pd.DataFrame(rows).set_index("sample")
geo = pd.read_csv(geo_meta, index_col=0)
gmap = {"WT": "WT", "PGC-1{alpha} transgenic": "mTG", "PGC-1{alpha} knockout": "mKO"}
amap = {"3 months old": "3mo", "24 months old": "24mo"}
geo_counts = pd.Series(list(zip(geo["characteristics_ch1.2.genotype"].map(gmap),
                                geo["characteristics_ch1.3.age"].map(amap)))).value_counts().sort_index()
ours = pd.Series(list(zip(sheet.genotype, sheet.age))).value_counts().sort_index()
if not geo_counts.equals(ours):
    raise SystemExit(f"group counts differ\nGEO:\n{geo_counts}\nmatrix:\n{ours}")
sheet["tissue"] = "gastrocnemius"
sheet["sex"] = "male"
sheet.to_csv(out)
print(ours.to_string())
