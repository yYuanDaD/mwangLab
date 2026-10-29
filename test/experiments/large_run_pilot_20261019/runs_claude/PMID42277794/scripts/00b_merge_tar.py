import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json; os.chdir(ROOT)
import pandas as pd
from tools import native
native.enable_native_mode()
res = native.merge_raw_tar("data/GSE263186")
print(json.dumps({k: v for k, v in res.items()}, indent=1))
m = native.read_table(res["output"])
print(m.head(8)); print(m.tail(6)); print(m.sum().round(0))
meta = pd.read_csv("data/GSE263186/GSE263186_metadata.csv", index_col=0)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 120)
for c in meta.columns:
    vals = meta[c].astype(str).unique()
    print(c, "|", len(vals), "|", list(vals)[:12])
