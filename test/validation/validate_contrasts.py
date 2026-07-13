"""Stage-1 validation for req #8: show _auto_detect_contrasts output on real metadata.
Zero cost (pandas only)."""
import os
import sys
import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

from tools.batch_tools import _auto_detect_contrasts, _auto_detect_design

TK = ["exercise", "trained", "training", "post", "run", "aerobic", "endurance", "resistance"]
CK = ["sedentary", "control", "rest", "pre", "untrained", "baseline", "sham"]

CASES = ["GSE242358", "GSE279359", "GSE250122", "GSE202295", "GSE151066",
         "GSE117161", "GSE163356", "GSE208615", "GSE266241"]

for acc in CASES:
    mpath = os.path.join("data", acc, f"{acc}_metadata.csv")
    if not os.path.exists(mpath):
        print(f"\n{acc}: (no local metadata)")
        continue
    contrasts = _auto_detect_contrasts(mpath, TK, CK)
    single = _auto_detect_design(mpath, TK, CK)
    df = pd.read_csv(mpath, index_col=0)
    print(f"\n=== {acc} ({df.shape[0]} samples) -> {len(contrasts)} contrast(s) ===")
    for col, ctrl, treat in contrasts:
        cn = int((df[col] == ctrl).sum())
        tn = int((df[col] == treat).sum())
        print(f"    [{col}]  {ctrl!r}(n={cn})  vs  {treat!r}(n={tn})")
    print(f"    (backward-compat _auto_detect_design first pick: {single})")
