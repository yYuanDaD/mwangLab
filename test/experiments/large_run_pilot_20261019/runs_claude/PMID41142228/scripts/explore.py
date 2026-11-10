import sys, pathlib, json, gzip, tarfile; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os; os.chdir(ROOT)
import pandas as pd
from tools import native
native.enable_native_mode()
R = pathlib.Path(__file__).resolve().parents[1]
tmp = R / "_explore"; tmp.mkdir(exist_ok=True)
try:
    r = native.merge_raw_tar("data/GSE308626")
    print({k: v for k, v in r.items() if k != "samples"}); print(r["samples"])
except Exception as e:
    print("merge_raw_tar failed:", e)
# inspect one of each member type
with tarfile.open("data/GSE308626/GSE308626_RAW.tar") as t:
    for n in t.getnames()[:2]:
        with gzip.open(t.extractfile(n), "rt") as f:
            print(n); [print("  ", f.readline().rstrip()) for _ in range(8)]
