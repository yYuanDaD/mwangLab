"""End-to-end Agent A cohort demo, max_papers=1, multi-method 'all'.
Exercises the WHOLE chain: search -> fetch -> own-GSE -> 13-table extract -> reported findings (#5)
-> with_analysis multi-method consensus ('all'). max_chars kept small to dodge the 30k tok/min cap.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/scripts/run_full_cohort_demo.py
"""
import os
import sys
import glob

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

import pandas as pd
from tools.cohort_tools import run_agent_a_cohort

LABEL = "demo_full3_0612"
COHORT = os.path.join("output", f"agentA_cohort_{LABEL}")

print("=" * 80)
print("FULL COHORT DEMO  max_papers=1  raw_da_method='all'  with_analysis=True")
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
    max_chars=24000,          # keep each of the 3 extraction calls small (rate-limit guard)
    extract_findings=True,    # #5
)

print("\n----- run_agent_a_cohort report -----")
print(report)

# ---- manifest ----
man = os.path.join(COHORT, "papers.csv")
print("\n----- papers.csv (manifest) -----")
if os.path.isfile(man):
    m = pd.read_csv(man)
    with pd.option_context("display.max_colwidth", 50, "display.width", 220):
        print(m.T)

# ---- 13-CSV row counts ----
csv_dir = os.path.join(COHORT, "csv")
print("\n----- 13 SEA-CDM CSVs (row counts) -----")
for p in sorted(glob.glob(os.path.join(csv_dir, "*.csv"))):
    n = max(0, sum(1 for _ in open(p, encoding="utf-8")) - 1)
    if n:
        print(f"   {os.path.basename(p):24s}  {n} rows")

# ---- analysis + results rows (where 'all' lands) ----
for name in ("analysis", "results"):
    p = os.path.join(csv_dir, f"{name}.csv")
    if os.path.isfile(p):
        df = pd.read_csv(p)
        print(f"\n----- {name}.csv ({len(df)} rows) -----")
        if name == "analysis":
            for _, arow in df.iterrows():
                print(f"   - da_method={arow.get('da_method')} | n_deg={arow.get('n_deg')}")
                print(f"     name: {arow.get('analysis_name')}")
        else:
            if "analysis_type" in df.columns:
                print(df["analysis_type"].value_counts().to_string())

print("\nDONE.")
