"""Verify the two reporting-explanation fixes (audit gaps 2 & 3):

Gap 2 — every matched-gene agreement verdict now carries an explanatory `note` (previously
        confirmed/contradicted/direction_only/not_detected/confirmed_change had note=None).
Gap 3 — DA/GSEA decision-log steps now carry a prose `reason` (deseq2/edger/limma-voom/gsea/
        da_method_comparison previously stored only structured details).

Gap-2 is checked both synthetically (all 5 verdict branches) and on the REAL GSE279359 agreement
(regenerated zero-network from the cohort's existing DEG + findings). Gap-3 is checked by reading
the source so the reason strings are present at every DA/GSEA record call site.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/unit/test_report_explanations.py
"""
import os
import sys
import glob

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

import pandas as pd
from tools.agreement_tools import _verdict_note, build_agreement_report

# ---------- Gap 2a: _verdict_note covers every verdict, never blank ----------
cases = [
    ("confirmed", "Sirt1", "up", 1.2, 0.01, True),
    ("contradicted", "Sirt1", "down", 1.2, 0.01, True),
    ("direction_only", "Sirt1", "up", 0.4, None, False),
    ("not_detected", "Sirt1", "up", 0.1, None, False),
    ("confirmed_change", "Sirt1", "down", -1.5, 0.02, True),
]
for v, sym, pdir, lfc, padj, sig in cases:
    note = _verdict_note(v, sym, pdir, lfc, padj, sig)
    assert note and sym in note, (v, note)
    assert "padj" in note or "p-value" in note, (v, note)
print("[2a] _verdict_note: all 5 verdict branches produce a non-empty explanation  OK")
# the key one: not_detected explicitly says the gene WAS measured but not significant
nd = _verdict_note("not_detected", "mSirt2", "up", 0.1, None, False)
assert "IS in our DEG matrix" in nd and "not significant" in nd, nd
print(f"[2b] not_detected note explains it: \"{nd}\"  OK")

# ---------- Gap 2c: regenerate the REAL GSE279359 agreement -> not_detected rows get notes ----------
D = "output/agentA_cohort_rerun_0622"
findings = os.path.join(D, "studies", "GSE279359_reported_findings.csv")
deg_dir = os.path.join(D, "cohort_analysis", "GSE279359")
counts = glob.glob("data/GSE279359/GSE279359_processed_counts*.gz")
if os.path.isfile(findings) and os.path.isdir(deg_dir) and counts:
    out = os.path.join("test", "output", "test_report_explanations_agreement.csv")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    rows = build_agreement_report("GSE279359", findings, deg_dir, counts[0], "Mouse", out)
    df = pd.DataFrame(rows)
    nd_rows = df[df["agreement"] == "not_detected"]
    assert len(nd_rows) > 0, "expected some not_detected verdicts in GSE279359"
    assert nd_rows["note"].notna().all() and (nd_rows["note"].str.len() > 0).all(), \
        "every not_detected row must now carry a note"
    print(f"[2c] real GSE279359: {len(nd_rows)} not_detected rows, ALL now have a note, e.g.:")
    print("       " + str(nd_rows.iloc[0]["note"]))
else:
    print("[2c] SKIP (GSE279359 artifacts not present) — synthetic checks above still cover the logic")

# ---------- Gap 3: every DA/GSEA decision record call now passes a reason= ----------
src = open("tools/batch_tools.py", encoding="utf-8").read()
import re
# the 4 DA/GSEA 'ok' record sites we added reasons to
checks = [
    ('dlog.record("gsea", "ok"', 'preranked GSEA of contrast'),
    ('dlog.record(m, "ok"', 'differential expression on contrast'),
    ('dlog.record("da_method_comparison", "ok"', 'cross-checked'),
    ('dlog.record(method, "ok"', 'differential expression on contrast'),
]
for call, phrase in checks:
    i = src.find(call)
    assert i != -1, f"record call not found: {call}"
    window = src[i:i + 400]
    assert "reason=" in window and phrase in window, f"missing reason for {call}"
print("[3] all 4 DA/GSEA decision-log steps (gsea / per-method / comparison / single) now pass reason=  OK")

print("\nPASS — report explanations: every agreement verdict carries an explanatory note (incl. "
      "not_detected), and every DA/GSEA decision-log step now records a prose reason.")
