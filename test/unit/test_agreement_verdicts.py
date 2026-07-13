"""Zero-cost unit test of the #6 verdict logic across ALL branches (the live GSE279359 study only
exercises not_detected/not_in_results/not_checkable). Synthetic DEG table + findings.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/unit/test_agreement_verdicts.py
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

import pandas as pd
from tools.agreement_tools import compare_findings_to_deg

# one synthetic contrast: symbol-indexed DEG with known log2fc / significance
deg = pd.DataFrame(
    {"log2fc": [2.0, -2.0, 0.4, 3.0, -1.5],
     "padj":   [0.001, 0.001, 0.30, 0.001, 0.20],
     "sig":    [True, True, False, True, False]},
    index=["PGC1A", "FOXO1", "MYOD1", "VEGFA", "IL6"],
)
tables = {"trained vs sedentary": deg}

findings = [
    {"entity": "PGC1A", "entity_type": "gene", "direction": "up", "source": "x"},      # confirmed
    {"entity": "FOXO1", "entity_type": "gene", "direction": "up", "source": "x"},      # contradicted (we say down)
    {"entity": "MYOD1", "entity_type": "gene", "direction": "up", "source": "x"},      # direction_only (up but n.s.)
    {"entity": "VEGFA", "entity_type": "gene", "direction": "down", "source": "x"},    # contradicted (we say up)
    {"entity": "IL6",   "entity_type": "gene", "direction": "down", "source": "x"},    # direction_only (down, n.s.)
    {"entity": "mPgc1a", "entity_type": "gene", "direction": "up", "source": "x"},     # confirmed (species prefix -> PGC1A)
    {"entity": "AKT1",  "entity_type": "gene", "direction": "up", "source": "x"},      # not_in_results
    {"entity": "AMPK signaling", "entity_type": "pathway", "direction": "up", "source": "x"},  # not_checkable
    {"entity": "VEGFA", "entity_type": "gene", "direction": "changed", "source": "x"}, # confirmed_change (sig)
]

rows, summary = compare_findings_to_deg(findings, tables)
got = [r["agreement"] for r in rows]
expect = ["confirmed", "contradicted", "direction_only", "contradicted", "direction_only",
          "confirmed", "not_in_results", "not_checkable", "confirmed_change"]

for f, g, e in zip(findings, got, expect):
    mark = "OK " if g == e else "XX "
    print(f"  {mark} {f['entity']:16s} text={f['direction']:8s} -> {g:16s} (expected {e})")

print("\nsummary:", summary)
assert got == expect, f"verdict mismatch:\n got={got}\n exp={expect}"
print("\nPASS — all verdict branches (confirmed/contradicted/direction_only/confirmed_change/"
      "not_in_results/not_checkable) behave correctly, incl. species-prefix matching.")
