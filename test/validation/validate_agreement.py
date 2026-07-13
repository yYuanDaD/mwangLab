"""#6 validation: annotate the GSE279359 cohort run's text-mined findings against our computed
multi-method DEG, finding by finding. Zero LLM cost (MyGene network for ID->symbol only).

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/validation/validate_agreement.py
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

import pandas as pd
from tools.agreement_tools import build_agreement_report

COHORT = os.path.join("output", "agentA_cohort_demo_full3_0612")
STUDY = "GSE279359"
findings_csv = os.path.join(COHORT, "studies", f"{STUDY}_reported_findings.csv")
deg_dir = os.path.join(COHORT, "cohort_analysis", STUDY)
counts = os.path.join("data", STUDY, "GSE279359_processed_counts.txt.gz")
out_csv = os.path.join(COHORT, "studies", f"{STUDY}_agreement.csv")

rep = {}
rows = build_agreement_report(STUDY, findings_csv, deg_dir, counts_path=counts,
                             species="Mouse", out_csv=out_csv, report=rep)

print(f"findings: {rep.get('n_findings')} | symbols mapped from matrix: {rep.get('n_symbols_mapped')} "
      f"| contrasts: {rep.get('n_contrasts')}")
print(f"summary: {rep.get('summary')}\n")

df = pd.DataFrame(rows)
show = ["entity", "entity_type", "direction", "our_symbol", "our_contrast",
        "our_log2fc", "our_padj", "our_significant", "agreement", "note"]
with pd.option_context("display.max_colwidth", 26, "display.width", 240):
    print(df[show].to_string())

print(f"\nagreement CSV: {out_csv}")
# sanity: every finding got a verdict
assert df["agreement"].notna().all(), "some findings have no verdict"
assert len(df) == rep["n_findings"]
print("\nPASS — every reported finding carries an agreement annotation.")
