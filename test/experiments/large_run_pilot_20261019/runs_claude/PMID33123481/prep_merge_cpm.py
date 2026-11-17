"""Merge GSE150620 per-sample CPM files (GSE150620_RAW.tar members) into one matrix.

Why a prep script: the generic tar merge (tools/geo_tar.py:127) keeps the first row of every
duplicated gene symbol without reporting it. The deposited files hold 52,640 rows with 106
duplicated symbols (110 surplus rows), including Excel-mangled dates (1-Mar, 2-Mar, ...).
Rule applied here, recorded in the case spec:
  * duplicated Excel-date IDs (e.g. "1-Mar" = Marchf1 and Mtarc1) are ambiguous -> dropped;
  * other duplicated symbols -> keep the row with the highest mean CPM across all 22 samples
    (summing would add the CPM floor of 1 twice);
  * columns are renamed to GSM accessions (metadata index).
Values are left on the deposited linear CPM scale (floored at 1); the log2(x+1) transform is
applied by the case runner as the method decision.

Usage: python prep_merge_cpm.py <unpacked_dir> <out_csv>
"""
import re
import sys
from pathlib import Path

import pandas as pd

unpacked, out = Path(sys.argv[1]), Path(sys.argv[2])
date_re = re.compile(r"^\d{1,2}-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)$")

cols = {}
for f in sorted(unpacked.glob("GSM*.txt.gz")):
    gsm = f.name.split("_")[0]
    t = pd.read_csv(f, sep="\t")
    assert t.shape[1] == 2, f
    t.columns = ["gene", "cpm"]
    cols[gsm] = t
genes0 = cols[next(iter(cols))]["gene"].tolist()
for gsm, t in cols.items():
    assert t["gene"].tolist() == genes0, f"row order differs in {gsm}"
m = pd.DataFrame({g: t["cpm"].values for g, t in cols.items()})
m.insert(0, "gene_id", genes0)

dup = m["gene_id"].duplicated(keep=False)
is_date = m["gene_id"].astype(str).str.match(date_re)
n_rows = len(m)
drop_date = dup & is_date
m = m[~drop_date]
m["_mean"] = m.drop(columns="gene_id").mean(axis=1)
m = m.sort_values("_mean", ascending=False).drop_duplicates("gene_id", keep="first")
m = m.drop(columns="_mean").set_index("gene_id").sort_index()
m.to_csv(out)
print(f"rows in: {n_rows}; duplicated-date rows dropped: {int(drop_date.sum())}; "
      f"genes out: {m.shape[0]} x {m.shape[1]} samples -> {out}")
