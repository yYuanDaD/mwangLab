import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os, json
ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())
os.chdir(ROOT)
from tools import native, suitability as su
import pandas as pd
native.enable_native_mode()
R = pathlib.Path(__file__).resolve().parents[1]
tmp = R / "_explore"
d = native.derive_columns(tmp / "aligned" / "aligned_metadata.csv", tmp / "design.csv",
    aliases={"frail": "characteristics_ch1.1.frailty", "run": "characteristics_ch1.2.run"},
    patterns={"animal": ("title", r" (D\d+)$")},
    recode={"frail": {"robust": "low", "frail": "high"}, "run": {"control": "sed", "24h": "run"}})
print(d["levels"])
m = pd.read_csv(tmp / "design.csv", index_col=0)
rep = su.report(case_id="x", matrix_type="raw counts", metadata=m, factors=["frail", "run"],
                matrix_csv=tmp / "aligned" / "aligned_matrix.csv", organism="Mouse",
                references={"frail": "low", "run": "sed"}, out_dir=tmp / "suit")
print(rep["verdict"], rep["failed"], rep["warnings"])
for c in rep["comparisons"]:
    print(json.dumps(c, default=str))
print(json.dumps(rep["checks"]["sex"], default=str)[:1500])
