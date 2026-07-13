"""Real cohort run to validate the limma branch end-to-end through batch_tools.

3 mouse studies, all previously skipped by the old _find_raw_counts_file:
  - GSE283691: fpkm_or_tpm (exercises log2 transform + limma)
  - GSE315104: log_transformed (exercises limma direct, only batch column → likely no_design)
  - GSE317978: log_transformed (exercises limma direct, multi-group sample-group column)

Exits with the batch tool's text report. Inspect output/cohort_limma_validation/summary.csv afterwards.
"""
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)

from dotenv import load_dotenv
load_dotenv(".env", override=True)

from tools.batch_tools import run_batch_geo_pipeline


def main():
    result = run_batch_geo_pipeline.invoke({
        "accessions": ["GSE283691", "GSE315104", "GSE317978"],
        "organism": "Mouse",
        "treatment_keywords": ["HFD", "high-fat", "treated", "KO", "knockout", "REG3B", "BcBKO", "disease"],
        "control_keywords": ["SD", "standard", "normal", "chow", "control", "WT", "wild-type", "flox", "PBS", "GFP"],
        "run_label": "limma_validation",
    })
    print("\n=== FINAL REPORT ===")
    print(result)


if __name__ == "__main__":
    main()
