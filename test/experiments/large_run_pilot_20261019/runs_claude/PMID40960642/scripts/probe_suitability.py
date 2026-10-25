"""Scratch probe: comparison names from the suitability enumerator (no run records)."""
import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import pandas as pd
from tools import suitability as su

m = pd.read_csv("data/GSE292369/GSE292369_metadata.csv", index_col=0)
d = pd.DataFrame({"cond": m["characteristics_ch1.2.treatment"].map({"placebo": "PLA", "ketone ester": "KME"}),
                  "time": m["characteristics_ch1.1.treatment"].map({"rest": "PRE", "exercised": "POST"}),
                  "subject": m["characteristics_ch1.3.subject id"]}, index=m.index)
for c in su.enumerate_comparisons(d, ["cond", "time"], references={"cond": "PLA", "time": "PRE"}):
    print(c["name"], c["kind"], c.get("analyzable"), [x["cell"] for x in c["cells"]])
