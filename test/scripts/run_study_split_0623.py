"""End-to-end demo of the per-condition STUDY SPLIT via the reusable study_split.split_and_compare:
split GSE279359 by timepoint -> 4 study records (descriptive fields INHERITED from the parent GSE
study row) + run a REAL DESeq2 for every pairwise comparison (incl. the inter-timepoint pairs the
baseline-only pipeline never runs). Zero LLM.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/scripts/run_study_split_0623.py
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

import pandas as pd
from tools.study_split import split_and_compare

GSE = "GSE279359"
ALIGNED = f"output/agentA_cohort_rerun_0622/cohort_analysis/{GSE}/{GSE}_metadata_aligned.csv"
COUNTS = f"data/{GSE}/{GSE}_processed_counts.txt.gz"
PARENT_STUDY = f"output/agentA_cohort_rerun_0622/csv/study.csv"   # inherit descriptive fields from here
OUT = f"output/_study_split_demo/{GSE}"
CK = ["pre", "control", "sedentary", "rest", "baseline"]

# parent GSE study row (for inheritance)
parent_row = None
if os.path.isfile(PARENT_STUDY):
    pdf = pd.read_csv(PARENT_STUDY)
    pr = pdf[pdf["study_id"] == GSE]
    parent_row = pr.iloc[0].to_dict() if len(pr) else None

rep = {}
plan = split_and_compare(GSE, COUNTS, ALIGNED, OUT, parent_study_row=parent_row,
                         control_keywords=CK, pairing="all", report=rep)
print("report:", rep)

print("\n===== study_split.csv (split studies, descriptive fields inherited from parent) =====")
sdf = pd.read_csv(os.path.join(OUT, "study_split.csv"))
nonempty = [c for c in sdf.columns if sdf[c].notna().any()]
print("filled columns:", nonempty)
print(sdf[["study_id", "source_gse", "study_name"]].to_string(index=False))
inh = [c for c in ("study_description", "study_type", "study_focus", "study_keywords") if c in sdf.columns]
print("inherited descriptive values:", {c: (sdf[c].dropna().unique().tolist()[:1] or ["(parent empty)"]) for c in inh})

print("\n===== cross_study_comparisons.csv =====")
cdf = pd.read_csv(os.path.join(OUT, "cross_study_comparisons.csv"))
print(cdf[["contrast_label", "treatment_study", "control_study", "n_deg", "status"]].to_string(index=False))
inter = cdf[~cdf["contrast_label"].str.contains("pre-exercise")]
print(f"\n{rep.get('n_ok')}/{rep.get('n_comparisons')} comparisons ran; "
      f"{len(inter)} inter-timepoint pairs the baseline-only pipeline never runs.")
