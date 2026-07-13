"""Validate that build_pipeline_rows maps an 'all'-mode batch study into correct SEA-CDM
analysis/results rows. Zero cost — reads the artifacts already on disk from the demo run.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/validation/validate_all_rows.py
"""
import os
import sys
import json

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

import pandas as pd
from tools.cohort_tools import build_pipeline_rows

COHORT = os.path.join("output", "cohort_demo_all_0612")
ACC = "GSE279359"
STUDY = ACC

summary_row = pd.read_csv(os.path.join(COHORT, "summary.csv")).iloc[0].to_dict()
summary_row = {k: (None if (isinstance(v, float) and pd.isna(v)) else v) for k, v in summary_row.items()}

rows = build_pipeline_rows(STUDY, summary_row, os.path.join(COHORT, ACC))

print("=== analysis row ===")
print(json.dumps(rows["analysis"][0], indent=2, ensure_ascii=False))

print(f"\n=== results rows ({len(rows['results'])}) ===")
for r in rows["results"]:
    print(f"  {r['results_id']:18s} | {r['analysis_type']:62s} | {os.path.basename(str(r['file_access']))}")

# ---- assertions ----
a = rows["analysis"][0]
assert a["da_method"] == "all (deseq2+edger+limma-voom)", a["da_method"]
assert a["n_deg"] == summary_row["n_deg"], (a["n_deg"], summary_row["n_deg"])
assert "consensus" in a["analysis_name"].lower(), a["analysis_name"]
assert a["input_data"], "input_data should not be None for 'all' mode"

types = [r["analysis_type"] for r in rows["results"]]
per_method = [t for t in types if t.startswith("differential expression (")]
compares = [t for t in types if t.startswith("multi-method DA comparison")]
gseas = [t for t in types if t.startswith("GSEA")]
# 3 contrasts x 3 methods = 9 per-method DEG rows; 3 comparison tables; GSEA failed -> 0 GSEA rows
assert len(per_method) == 9, f"expected 9 per-method DEG rows, got {len(per_method)}: {per_method}"
assert len(compares) == 3, f"expected 3 comparison rows, got {len(compares)}"
# each per-method row names a real method
for t in per_method:
    m = t[len("differential expression ("):-1]
    assert m in ("deseq2", "edger", "limma-voom"), m
# every file_access exists on disk
for r in rows["results"]:
    assert os.path.isfile(str(r["file_access"])), f"missing file: {r['file_access']}"
# results ids unique
ids = [r["results_id"] for r in rows["results"]]
assert len(ids) == len(set(ids)), "duplicate results_id"

print(f"\nper-method DEG rows: {len(per_method)} | comparison rows: {len(compares)} | GSEA rows: {len(gseas)}")
print("ALL ASSERTIONS PASSED — 'all'-mode batch maps cleanly into SEA-CDM analysis/results.")
