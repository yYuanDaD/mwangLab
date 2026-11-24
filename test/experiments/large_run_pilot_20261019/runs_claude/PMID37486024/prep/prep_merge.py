"""Merge the two GSE224900 count files (sequencing runs 19565R, 20063R) and add a
subject key to the metadata.

Subject key: GEO has no participant ID. Each participant's biopsies were numbered
consecutively in blocks (PREbc, PREac, Day1, POSTbc, [POSTac], 7d) within a run; a new
block starts at each PREbc sample. Age and sex are constant within every block
(checked below), which supports the block = participant reading.
"""
import sys, pandas as pd
data, out = sys.argv[1], sys.argv[2]
a = pd.read_csv(f"{data}/GSE224900/GSE224900_19565R_counts.txt.gz", sep="\t", index_col=0)
b = pd.read_csv(f"{data}/GSE224900/GSE224900_20063R_counts.txt.gz", sep="\t", index_col=0)
assert a.index.equals(b.index) or set(a.index) == set(b.index)
m = pd.concat([a, b.loc[a.index]], axis=1)
assert not m.columns.duplicated().any()
m.index.name = "gene_id"
m.to_csv(f"{out}/GSE224900_merged_counts.csv.gz")

md = pd.read_csv(f"{data}/GSE224900/GSE224900_metadata.csv", index_col=0)
md["key"] = md.title.str.split().str[0]
md["run"] = md.key.str[:5]
md["num"] = md.key.str.extract(r"X(\d+)$")[0].astype(int)
md = md.sort_values(["run", "num"])
subj, cur = [], None
for _, r in md.iterrows():
    if r.title.split()[1].startswith("PREbc"):
        cur = f"{r.run}_S{r.num:03d}"
    subj.append(cur)
md["subject"] = subj
chk = md.groupby("subject").agg(age=("characteristics_ch1.2.age", "nunique"),
                                sex=("characteristics_ch1.4.Sex", "nunique"),
                                trt=("characteristics_ch1.1.treatment", "nunique"), n=("key", "size"))
assert (chk[["age", "sex", "trt"]] == 1).all().all(), chk
print(chk.to_string())
md = md.drop(columns=["num"])
# sex from GEO, corrected where XIST/chrY expression contradicts it for a whole, internally
# consistent block (19565_S084: all 6 biopsies XIST-high, chrY-absent -> female; GEO says M).
md["sex"] = md["characteristics_ch1.4.Sex"]
md.loc[md.subject == "19565_S084", "sex"] = "F"
md = md.rename(columns={"characteristics_ch1.4.Sex": "sex_geo_reported"})
md.to_csv(f"{out}/GSE224900_metadata_subject.csv")
print(m.shape)
