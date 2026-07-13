"""Re-run of the full Agent A cohort (SAME keyword as run_full_cohort_demo) on a fresh label,
to end-to-end re-validate this session's changes: the new pathway/enrichment schema tables +
chain_view (#7b wiring), the cost optimizations (skip-if-exists, GMT cache, contrast gate), and
#3/#4/#5/#6/#8 in a live run.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/scripts/rerun_cohort_0622.py
"""
import os
import sys
import glob

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from tools.cohort_tools import run_agent_a_cohort

LABEL = "rerun_0622"
COHORT = os.path.join("output", f"agentA_cohort_{LABEL}")

print("=" * 80)
print("COHORT RERUN  max_papers=1  raw_da_method='all'  with_analysis=True")
print("keyword: voluntary wheel running mouse skeletal muscle RNA sequencing")
print("=" * 80)

report = run_agent_a_cohort(
    keyword="voluntary wheel running mouse skeletal muscle RNA sequencing",
    max_papers=1,
    organism="Mouse",
    with_analysis=True,
    treatment_keywords=["exercise", "training", "trained", "post", "run", "HIIT", "endurance"],
    control_keywords=["sedentary", "control", "pre", "rest", "sham", "untrained"],
    raw_da_method="all",
    require_pdf=True,
    search_pool=25,
    run_label=LABEL,
    output_base="./output",
    max_chars=24000,
    extract_findings=True,
)

print("\n----- report -----")
print(report)

csv_dir = os.path.join(COHORT, "csv")
print("\n----- SEA-CDM CSVs (non-empty row counts) -----")
for p in sorted(glob.glob(os.path.join(csv_dir, "*.csv"))):
    try:
        n = max(0, sum(1 for _ in open(p, encoding="utf-8")) - 1)
    except Exception:
        n = -1
    if n:
        print(f"   {os.path.basename(p):26s}  {n} rows")

# new this session: pathway / enrichment / chain_view
print("\n----- #7b pathway<->exercise relational tables -----")
for name in ("analysis", "pathway", "enrichment"):
    p = os.path.join(csv_dir, f"{name}.csv")
    if os.path.isfile(p):
        df = pd.read_csv(p)
        print(f"   {name}.csv: {len(df)} rows")
cv = os.path.join(csv_dir, "chain_view.csv")
if os.path.isfile(cv):
    d = pd.read_csv(cv).fillna("")
    print(f"\n   chain_view.csv: {len(d)} chains")
    for s in d["chain"].head(25).tolist():
        print("     " + s)
else:
    print("   chain_view.csv: (not written — no GSEA enrichment for this study)")

print("\nDONE.")
