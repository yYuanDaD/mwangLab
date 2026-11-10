import sys, pathlib, json; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6]))
from tools import native
native.enable_native_mode()
R = pathlib.Path(__file__).resolve().parents[1]
tmp = R / "_explore"
cols = [f"UPL25.{x}_dedup.bam" for x in []]
d = native.derive_columns("data/GSE308674/GSE308674_metadata.csv", tmp / "derived.csv",
    aliases={"batch": "characteristics_ch1.4.batch"},
    patterns={"count_col": ("description", r"Column name in gene_counts\.csv: (\S+)$"),
              "grp": ("characteristics_ch1.3.treatment", r"^(.+)$")},
    recode={"grp": {"PBS injection": "C", "Lactate administration": "L", "HIIT": "H",
                    "MCT1/2 inhibitor": "M", "HIIT+MCT1/2 inhibitor": "HM"}})
print(json.dumps(d["levels"], indent=1))
a = native.align_to_metadata("data/GSE308674/GSE308674_gene_counts.csv.gz", tmp / "derived.csv", tmp / "aligned", key_column="count_col")
print({k: v for k, v in a.items() if k != "outputs"})
p = native.profile_matrix(tmp / "aligned" / "aligned_matrix.csv")
print(json.dumps(p, indent=1))
print(json.dumps(native.design_check(tmp/"aligned"/"aligned_metadata.csv", ["grp","batch"]), indent=1))
print(json.dumps(native.confounding_report(tmp/"aligned"/"aligned_metadata.csv", "grp", ["batch"]), indent=1))
import pandas as pd
m = pd.read_csv(tmp/"aligned"/"aligned_metadata.csv", index_col=0)
for t in ["L","H","M","HM"]:
    s = m.index[m.grp.isin(["C",t])]
    terms = ["grp","batch"] if m.loc[s,"batch"].nunique()>1 else ["grp"]
    print(t, native.design_check(m, terms, samples=list(s))["residual_df"], terms)
c = pd.read_csv(tmp/"aligned"/"aligned_matrix.csv", index_col=0)
print(c.sum().describe()); print((c.sum(axis=1)>0).sum())
