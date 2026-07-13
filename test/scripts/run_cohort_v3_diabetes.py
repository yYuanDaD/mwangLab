"""Run the Diabetes 5-top + 5-random cohort with A+B LLM fallbacks active.

Selection done by test/scripts/pick_cohort.py from output/geo_search_Diabetes.csv
(seed=42, reproducible). See pick_cohort output for accession-to-title mapping.

Run from project root:
    python test/scripts/run_cohort_v3_diabetes.py
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, _ROOT)
sys.path.insert(0, _HERE)
os.chdir(_ROOT)

from tools.batch_tools import run_batch_geo_pipeline  # noqa: E402
from pick_cohort import pick_cohort  # noqa: E402


if __name__ == "__main__":
    search_csv = "output/geo_search_Diabetes.csv"
    accessions = pick_cohort(search_csv, n_top=5, n_random=5, seed=42)
    print(f"Cohort ({len(accessions)} accessions): {accessions}")

    out = run_batch_geo_pipeline.invoke({
        "accessions": accessions,
        "organism": "Mouse",
        # Diabetes model conventions:
        # diabetic / db (db/db mice) / ob (ob/ob mice) / STZ (streptozotocin) /
        # HFD (high-fat diet) / T2D (type 2 diabetes) / hyperglycemia
        "treatment_keywords": [
            "diabetic", "diabetes", "db", "ob", "STZ", "streptozotocin",
            "HFD", "high fat", "high-fat", "T2D", "T1D", "type 2", "type 1",
            "hyperglycemia", "hyperglycemic", "obese", "obesity",
        ],
        # Diabetes control conventions:
        # WT/wildtype / lean / chow diet / normal diet / LFD (low-fat) /
        # ND (normal diet) / vehicle / untreated
        "control_keywords": [
            "control", "wildtype", "WT", "wild type", "wild-type",
            "lean", "chow", "normal", "ND", "LFD", "low fat", "low-fat",
            "vehicle", "untreated", "saline", "PBS", "non-diabetic",
            "nondiabetic", "healthy",
        ],
        "run_label": "Diabetes_top5_random5",
        "source_search_csv": search_csv,
    })
    print("\n" + "=" * 60)
    print("RUN RETURN VALUE")
    print("=" * 60)
    print(out)
