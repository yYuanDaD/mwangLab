"""Sum the two sequencing lanes (L001/L002, same library) of each GSE178262 sample into one GSM column.
Lane columns are paired by the sample number 'S<n>' that GEO's per-sample description also carries."""
import re, sys
import pandas as pd
src, meta, out = sys.argv[1:4]
x = pd.read_csv(src, sep=None, engine="python", index_col=0)
m = pd.read_csv(meta, index_col=0)
lane = {}
for c in x.columns:
    k = re.search(r"_S(\d+)_L00([12])$", c)
    lane.setdefault(int(k.group(1)), []).append(c)
res = {}
for gsm, d in m["description"].items():
    sn = {int(re.search(r"_S(\d+)_L00[12]$", p.strip()).group(1)) for p in d.split(",")[1:]}
    assert len(sn) == 1, (gsm, sn)
    cols = lane[sn.pop()]
    assert len(cols) == 2, (gsm, cols)
    res[gsm] = x[cols].sum(axis=1)
y = pd.DataFrame(res)
y.index.name = "entrez_id"
y.to_csv(out)
print(y.shape, y.sum().min(), y.sum().max())
