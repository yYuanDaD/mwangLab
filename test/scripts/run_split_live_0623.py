"""Live keyword cohort to light up the [#split] step end-to-end: a real keyword -> GSE279359
(4-timepoint design) -> the cohort phase-3 [#split] block auto-splits it into per-condition study
records + runs all-pairwise DESeq2. Confirms the integration fires in a fresh run (not just the
standalone demo).

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/scripts/run_split_live_0623.py
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

LABEL = "split_live_0623"
COHORT = os.path.join("output", f"agentA_cohort_{LABEL}")

print("=" * 78)
print("LIVE COHORT to light up [#split]  keyword='treadmill exercise mouse skeletal muscle RNA sequencing'")
print("=" * 78)

report = run_agent_a_cohort(
    keyword="treadmill exercise mouse skeletal muscle RNA sequencing",
    max_papers=1, organism="Mouse", with_analysis=True,
    treatment_keywords=["exercise", "training", "trained", "post", "run", "acute", "endurance"],
    control_keywords=["pre", "control", "sedentary", "rest", "baseline", "sham"],
    raw_da_method="all", require_pdf=True, search_pool=25,
    run_label=LABEL, output_base="./output", max_chars=24000, extract_findings=True,
)
print("\n----- report (head) -----")
print((report or "").splitlines()[0] if report else "(no report)")

# manifest: the two new [#split] columns
man = os.path.join(COHORT, "papers.csv")
if os.path.isfile(man):
    m = pd.read_csv(man).iloc[0]
    print(f"\nchosen_gse={m.get('chosen_gse')} analyzed={m.get('analyzed')} "
          f"split_studies={m.get('split_studies')} pairwise_comparisons={m.get('pairwise_comparisons')}")

# the [#split] log line
log = os.path.join(COHORT, "cohort.log")
if os.path.isfile(log):
    for ln in open(log, encoding="utf-8"):
        if "[#split]" in ln:
            print("  LOG:", ln.strip())

# the split artifacts
sd = glob.glob(os.path.join(COHORT, "studies", "*_study_split"))
if sd:
    d = sd[0]
    print(f"\n----- {os.path.relpath(d)} -----")
    ssv = os.path.join(d, "study_split.csv")
    csv = os.path.join(d, "cross_study_comparisons.csv")
    if os.path.isfile(ssv):
        s = pd.read_csv(ssv)
        print(f"\nsplit studies ({len(s)}):")
        print(s[["study_id", "source_gse", "study_name"]].to_string(index=False))
    if os.path.isfile(csv):
        c = pd.read_csv(csv)
        print(f"\ncross-study comparisons ({len(c)}):")
        print(c[["contrast_label", "treatment_study", "control_study", "n_deg", "status"]].to_string(index=False))
        inter = c[~c["contrast_label"].str.contains("pre-exercise|vs pre", regex=True, na=False)]
        print(f"\n{c['n_deg'].notna().sum()}/{len(c)} ran; {len(inter)} inter-condition pairs.")
else:
    print("\n[#split] produced no study_split dir — check cohort.log (maybe single-condition / no own-GSE)")
print("\nDONE.")
