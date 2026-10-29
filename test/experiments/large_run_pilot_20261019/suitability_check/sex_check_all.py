"""X/Y-gene sex check (suitability.check_sex) on every aligned matrix of the large run.

Run (repository root):  python test/experiments/large_run_pilot_20261019/suitability_check/sex_check_all.py
"""

import glob
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

import pandas as pd

from tools import suitability as su

HERE = Path(__file__).resolve().parent
ORGANISM = {"9606": "Human", "10090": "Mouse", "10116": "Rat"}
rows = []
for matrix in sorted(glob.glob(str(HERE.parent / "runs_claude/*/*/aligned/aligned_matrix.csv"))):
    case_dir = Path(matrix).parents[1]
    meta_path = case_dir / "aligned/aligned_metadata.csv"
    if not meta_path.exists():
        continue
    meta = pd.read_csv(meta_path, index_col=0)
    taxid = str(meta["taxid_ch1"].iloc[0]) if "taxid_ch1" in meta else ""
    run = case_dir.parent.name
    sx = su.check_sex(matrix, meta, organism=ORGANISM.get(taxid, "Mouse"), out_dir=HERE / "sex" / run)
    rows.append({"run": run, "case": case_dir.name, "organism": ORGANISM.get(taxid, "?"), "status": sx["status"],
                 "metadata_sex_column": sx.get("metadata_sex_column", ""),
                 "predicted": sx.get("predicted", {}), "mismatched": ";".join(sx.get("mismatched", [])),
                 "summary": sx.get("summary", "")})
pd.DataFrame(rows).to_csv(HERE / "sex_check_all.csv", index=False)
print(pd.DataFrame(rows).drop(columns=["summary"]).to_string())
