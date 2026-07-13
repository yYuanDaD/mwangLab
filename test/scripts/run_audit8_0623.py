"""Short-keyword cohort run for the 8-requirement REPORTING audit.

Keyword kept deliberately short. After it lands, we audit whether EACH meeting requirement is not
just done but EXPLAINED in the output (reason / provenance / note), per the user's ask:
"重点关注 agent 对于每一项报告有没有解释".

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/scripts/run_audit8_0623.py
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

from dotenv import load_dotenv
load_dotenv()

from tools.cohort_tools import run_agent_a_cohort

LABEL = "audit8_0623"
report = run_agent_a_cohort(
    keyword="acute exercise muscle RNA-seq",
    max_papers=1, organism="Mouse", with_analysis=True,
    treatment_keywords=["exercise", "training", "trained", "post", "run", "acute", "endurance"],
    control_keywords=["sedentary", "control", "pre", "rest", "sham", "baseline"],
    raw_da_method="all", require_pdf=True, search_pool=25,
    run_label=LABEL, output_base="./output/_kw_robustness",
    max_chars=24000, extract_findings=True,
)
print("\n===== REPORT =====")
print(report)
print("\nDONE.  cohort dir: output/_kw_robustness/agentA_cohort_" + LABEL)
