"""Minimal live cohort to light up req #2 (reconciliation row in the CDM result layer) end-to-end.

Keyword lands on the proven own-GSE GSE279359 (cached raw counts). with_analysis=True so:
  download -> DESeq2 -> #5 findings (now one-pass via lean) -> #6 agreement -> #2 reconciliation row.
Single-method deseq2 + modest max_chars keeps it fast and under the 30k-input-tok/min limit.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/scripts/run_recon_min_cohort_0626.py
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

from tools.cohort_tools import run_agent_a_cohort

report = run_agent_a_cohort(
    keyword="treadmill exercise mouse skeletal muscle RNA sequencing",
    max_papers=1,
    organism="Mouse",
    with_analysis=True,
    treatment_keywords=["immediately", "post", "1h", "24h", "exercise", "trained", "treadmill"],
    control_keywords=["pre", "sedentary", "baseline", "rest", "control", "sed"],
    raw_da_method="deseq2",
    max_chars=40000,
    run_label="recon_min_0626",
)
print("\n========== COHORT REPORT ==========")
print(report)
