"""Pairing-key check for GSE278016: mouse = sample number (left) / number-60 (right)."""
import json, sys
import numpy as np, pandas as pd
sys.path.insert(0, ".")
from tools.pairing_check import check_pairing_key
d = "E:/agent/mwangLab_pdf/data/GSE278016/"
m = pd.read_csv(d + "GSE278016_metadata.csv", index_col=0).set_index("description")
x = pd.read_csv(d + "GSE278016_merged.counts.geo1.tsv.gz", sep="\t", index_col=0)
m = m[m["characteristics_ch1.3.treatm.diet"] == "CR"].copy()
num = m.index.str[-3:].astype(int)
m["mouse"] = np.where(m["characteristics_ch1.6.treatm.leg"] == "R", num - 60, num).astype(str)
m["immob"] = m["characteristics_ch1.4.treatm.immob"].astype(str)
m["cmpd"] = m["characteristics_ch1.5.treatm.compound"].astype(str)
x = x[m.index]
logcpm = np.log2(x / x.sum() * 1e6 + 1)
res = check_pairing_key(logcpm, m, key=["mouse"], across="immob", within=["cmpd"])
print(json.dumps(res, indent=1, default=str))
json.dump(res, open(sys.argv[1], "w"), indent=1, default=str)
print(m.groupby("mouse").size().value_counts().to_dict())
