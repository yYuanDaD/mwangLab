"""Stage-2 end-to-end validation for req #8: run the batch on GSE279359 (a pre/post
exercise time-course) and confirm it now produces ONE DEG + GSEA PER timepoint contrast
instead of a single pooled contrast.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/validation/validate_stage2.py
"""
import os
import sys
import glob

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)
sys.path.insert(0, _ROOT)

from tools.batch_tools import run_batch_geo_pipeline

OUT = os.path.join("output", "_stage2_check")

report = run_batch_geo_pipeline.invoke({
    "accessions": ["GSE279359"],
    "organism": "Human",
    "treatment_keywords": ["exercise", "post", "trained", "training", "run"],
    "control_keywords": ["pre", "baseline", "rest", "control", "sedentary"],
    "raw_da_method": "deseq2",
    "output_base": OUT,
    "run_label": "stage2",
})
print("\n" + "=" * 70)
print(report)

study_dir = os.path.join(OUT, "cohort_stage2", "GSE279359")
print("\nDEG files produced:")
for p in sorted(glob.glob(os.path.join(study_dir, "DEG_results_*.csv"))):
    print("   ", os.path.basename(p))
print("GSEA files produced:")
for p in sorted(glob.glob(os.path.join(study_dir, "*_GSEA_*.csv"))):
    print("   ", os.path.basename(p))
