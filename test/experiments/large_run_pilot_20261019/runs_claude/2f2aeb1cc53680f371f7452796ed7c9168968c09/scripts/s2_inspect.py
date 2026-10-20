import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6]))
from tools import native
native.enable_native_mode()
import pandas as pd
r = native.merge_raw_tar("data/GSE179302")
print({k: v for k, v in r.items() if k != "samples"}); print(r["samples"][:3])
t = native.read_table(r["output"]); print(t.shape, t.iloc[:3,:3])
x = pd.read_csv("data/GSE179302/GSE179302_raw_counts.csv.gz", index_col=0)
print("cols:", sorted(set(c.rsplit('_',1)[1] for c in x.columns)))
p1 = [c for c in x.columns if c.endswith("_P1")]; p2=[c for c in x.columns if c.endswith("_P2")]
print(len(p1), len(p2), x.columns[x.columns.str.contains('_P[^12]')].tolist()[:20])
m = pd.read_csv("data/GSE179302/GSE179302_metadata.csv", index_col=0)
titles = set(m.title)
print("titles with P1:", sum(t+'_P1' in x.columns for t in titles), "with P2:", sum(t+'_P2' in x.columns for t in titles))
print("tail rows tar:", t.index[-5:].tolist(), "csv:", x.index[-5:].tolist())
# compare first GSM with csv cols
desc = m.set_index("description")
g0 = t.columns[0]; print("tar col0", g0)
common = t.index.intersection(x.index); print("common genes", len(common))
for gsm in t.columns[:3]:
    ttl = m.loc[gsm, "title"] if gsm in m.index else None
    for suf in ["_P1","_P2"]:
        c = f"{ttl}{suf}"
        if c in x.columns:
            a = t.loc[common, gsm]; b = x.loc[common, c]
            print(gsm, c, "equal frac", (a.values==b.values).mean(), "sums", a.sum(), b.sum())
print("csv colsums P1 med", x[p1].sum().median(), "P2 med", x[p2].sum().median(), "tar med", t.sum().median())
