"""Third live keyword-cohort test: keyword 'exercise RNA-seq', EXPANDED paper count.
Same scope as test2 (text + analysis) but max_papers 3 -> 8 and search_pool 30 -> 50,
to exercise the pipeline on a wider set of ranked hits.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/scripts/run_cohort_test3.py
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)
sys.path.insert(0, _ROOT)

from tools.cohort_tools import run_agent_a_cohort

if __name__ == "__main__":
    report = run_agent_a_cohort(
        keyword="exercise RNA-seq",
        max_papers=8,                      # expanded from test2's 3
        search_pool=50,                    # wider candidate pool (was default 30)
        organism="",                       # auto hint; batch defaults to Mouse for analysis
        with_analysis=True,                # full scope: download + DESeq2/limma + GSEA on own-GSEs
        treatment_keywords=["exercise", "trained", "training", "post", "run",
                             "aerobic", "endurance", "resistance"],
        control_keywords=["sedentary", "control", "rest", "pre", "untrained",
                           "baseline", "sham"],
        raw_da_method="auto",              # exercise the LLM method picker + da_method_reason
        run_label="test3_exercise_rnaseq",
    )
    print("\n" + "=" * 78)
    print(report)
    print("=" * 78)
