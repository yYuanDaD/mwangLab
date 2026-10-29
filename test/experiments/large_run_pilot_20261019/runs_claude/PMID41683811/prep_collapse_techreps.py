"""Collapse GSE315228 technical sequencing replicates (rep1-3) into one library per biopsy.

Each biopsy (patient x time point) was sequenced up to three times (paper FIG3 legend;
GEO titles "..., patient N, repK"). Technical replicates of one biopsy are not independent
biological samples, so their counts are summed (DESeq2 collapseReplicates convention).
Libraries with < 10,000 assigned reads are failed runs and are dropped before summing.

Writes, next to this script:
  GSE315228_counts_by_biopsy.csv     genes x 24 biopsies (summed raw counts)
  GSE315228_metadata_by_biopsy.csv   one row per biopsy (subject, grp, time, source GSMs)
  GSE315228_metadata_reps.csv        GEO metadata + barcode key (for the replicate-level case)
"""
import os
import re
import sys

import pandas as pd

DATA = sys.argv[1] if len(sys.argv) > 1 else "E:/agent/mwangLab_pdf/data/GSE315228"
OUT = os.path.dirname(os.path.abspath(__file__))
MIN_READS = 10_000

meta = pd.read_csv(os.path.join(DATA, "GSE315228_metadata.csv"), index_col=0)
counts = pd.read_csv(os.path.join(DATA, "GSE315228_raw_counts_all_samples.csv.gz"), index_col=0)

meta["barcode"] = meta["description"].str.extract(r"Library name: (barcode\d+)", expand=False)
assert meta["barcode"].notna().all() and set(meta["barcode"]) == set(counts.columns)
meta["subject"] = "P" + meta["characteristics_ch1.4.patient no"].astype(str)
meta["grp"] = meta["characteristics_ch1.2.treatment"].map({"control": "ctr", "experiment": "exp"})
meta["time"] = meta["characteristics_ch1.1.condition"].map({"0 day": "d0", "1 day": "d1", "12 days": "d12"})
meta["rep"] = meta["title"].str.extract(r"rep(\d)", expand=False)
assert meta[["grp", "time", "rep"]].notna().all().all()
# title must agree with the characteristics columns
t_time = meta["title"].map(lambda s: "d0" if "before" in s else ("d1" if "1d after" in s else "d12"))
t_subj = "P" + meta["title"].str.extract(r"patient (\d+)", expand=False)
assert (t_time == meta["time"]).all() and (t_subj == meta["subject"]).all()

libsize = counts.sum()
meta["library_size"] = meta["barcode"].map(libsize)
meta["failed_library"] = meta["library_size"] < MIN_READS
meta.to_csv(os.path.join(OUT, "GSE315228_metadata_reps.csv"))

keep = meta[~meta["failed_library"]]
meta["biopsy"] = meta["subject"] + "_" + meta["time"]
keep = meta[~meta["failed_library"]]
summed = {}
rows = []
for biopsy, g in keep.groupby("biopsy", sort=True):
    summed[biopsy] = counts[g["barcode"].tolist()].sum(axis=1)
    rows.append({"biopsy": biopsy, "subject": g["subject"].iloc[0], "grp": g["grp"].iloc[0],
                 "time": g["time"].iloc[0], "n_tech_reps": len(g),
                 "source_gsm": ";".join(g.index), "source_barcodes": ";".join(g["barcode"]),
                 "library_size": int(g["library_size"].sum())})
by_biopsy = pd.DataFrame(summed)
by_biopsy.index.name = counts.index.name or "gene_id"
by_biopsy.to_csv(os.path.join(OUT, "GSE315228_counts_by_biopsy.csv"))
md = pd.DataFrame(rows).set_index("biopsy")
md.to_csv(os.path.join(OUT, "GSE315228_metadata_by_biopsy.csv"))
print(md.to_string())
print("dropped failed libraries:", meta.loc[meta["failed_library"], ["barcode", "library_size"]].to_dict("index"))
