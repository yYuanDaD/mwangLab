import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6]))
import os; os.chdir(pathlib.Path(__file__).resolve().parents[6])
from tools import native
native.enable_native_mode()
print(native.call_tool("tools.geo_tools:download_geo_data", geo_accession="GSE297318"))
print(native.call_tool("tools.geo_tools:download_supplementary_files", geo_accession="GSE297318"))
import pandas as pd
m = pd.read_csv("data/GSE297318/GSE297318_metadata.csv", index_col=0)
print(m.shape)
for c in m.columns:
    v = m[c].astype(str).unique()
    if len(v) > 1: print(c, len(v), list(v)[:24])
for p in sorted(pathlib.Path("data/GSE297318").iterdir()): print(p.name, p.stat().st_size)
