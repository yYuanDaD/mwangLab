"""Cohort run on the GSEA-richest candidate keyword (acute + exhaustive + muscle + time course),
chosen to maximize significant Hallmark pathways. If it lands on an analyzed own-GSE study it also
exercises the just-shipped reporting fixes (agreement notes + DA decision reasons).

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/scripts/run_gsea_rich_0623.py
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

LABEL = "gsea_rich2_0623"
COHORT = os.path.join("output", "_kw_robustness", f"agentA_cohort_{LABEL}")

report = run_agent_a_cohort(
    keyword="acute exhaustive exercise mouse skeletal muscle RNA-seq time course",
    max_papers=3, organism="Mouse", with_analysis=True,
    treatment_keywords=["exercise", "training", "trained", "post", "run", "acute", "exhaustive",
                        "endurance", "exercised"],
    control_keywords=["sedentary", "control", "pre", "rest", "sham", "baseline", "untrained"],
    raw_da_method="all", require_pdf=True, search_pool=25,
    run_label=LABEL, output_base="./output/_kw_robustness",
    max_chars=24000, extract_findings=True,
)
print("\n===== REPORT =====")
print(report)

# GSEA richness + whether the reporting fixes show up
csv_dir = os.path.join(COHORT, "csv")
man = os.path.join(COHORT, "papers.csv")
if os.path.isfile(man):
    m = pd.read_csv(man).iloc[0]
    print(f"\nchosen_gse={m.get('chosen_gse')} ownership={m.get('ownership')} "
          f"analyzed={m.get('analyzed')} enrich_edges={m.get('enrichment_edges')} "
          f"chain_gsea={m.get('chain_gsea_pathways')}")
cv = os.path.join(csv_dir, "chain_view.csv")
if os.path.isfile(cv):
    d = pd.read_csv(cv)
    print(f"\nchain_view: {len(d)} chains; top by |NES|:")
    print(d.reindex(d["nes"].abs().sort_values(ascending=False).index)
          [["pathway_name", "direction", "nes", "fdr"]].head(8).to_string(index=False))
print("\nDONE.")
