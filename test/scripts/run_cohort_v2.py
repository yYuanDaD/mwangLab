"""Real-cohort smoke test for the A+B LLM fallback. Picks 5 Exercise-related
GSEs that exercise both fallbacks:

  - GSE297707: previously deg_gsea_ok — control for A's confirm path
  - GSE297515: previously preprocess_ok_no_design — A's override/refuse target
  - GSE326587: known abbreviation mismatch (HC_F1_TL_S54_L003) — B target
  - GSE283691, GSE282641: fresh studies for general validation

Run from project root:
    python test/scripts/run_cohort_v2.py
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, _ROOT)
os.chdir(_ROOT)

from tools.batch_tools import run_batch_geo_pipeline  # noqa: E402


if __name__ == "__main__":
    accessions = [
        "GSE297707",
        "GSE297515",
        "GSE326587",
        "GSE283691",
        "GSE282641",
    ]
    out = run_batch_geo_pipeline.invoke({
        "accessions": accessions,
        "organism": "Mouse",
        "treatment_keywords": ["exercise", "training", "HIIT", "HIE", "exe",
                               "run", "treadmill", "swimming", "wheel", "AEX",
                               "aerobic"],
        "control_keywords": ["sedentary", "control", "sham", "sed",
                             "untreated", "vehicle", "PBS", "rest", "resting",
                             "home cage", "homecage"],
        "run_label": "Exercise_v2_llm_fallback",
        "source_search_csv": "output/search_Exercise.csv",
    })
    print("\n" + "=" * 60)
    print("RUN RETURN VALUE")
    print("=" * 60)
    print(out)
