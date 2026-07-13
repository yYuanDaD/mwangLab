"""#5 validation: mine reported findings from a cached NO-DATA paper and confirm we get a
findings CSV + a non-empty results row. One LLM call.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/validation/validate_findings.py
"""
import os
import sys
import json

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)
sys.path.insert(0, _ROOT)

from tools.seacdm_tools import build_reported_findings

# PMC10913554 — "Swimming exercise reverses transcriptomic changes in aging mouse lens"
# (test3: ownership empty, NOT analyzed -> results would otherwise be empty).
PAPER = os.path.join("data", "papers", "fece27c2b0e906d7628a162d39a4589e153b63e7.txt")
STUDY = "PMC10913554"
OUT = os.path.join("output", "_findings_check")
os.makedirs(OUT, exist_ok=True)

with open(PAPER, encoding="utf-8", errors="ignore") as f:
    text = f.read()[:100000]

findings_csv = os.path.join(OUT, f"{STUDY}_reported_findings.csv")
rep = {}
rows = build_reported_findings(STUDY, text, findings_csv, organism="Mouse", report=rep)

print(f"study={STUDY}  chars={len(text)}")
print(f"findings mined : {rep.get('n_findings', 0)}  "
      f"(verbatim {rep.get('n_verified', 0)}/{rep.get('n_total', 0)}, "
      f"{rep.get('n_unverified', 0)} flagged [UNVERIFIED])")
print(f"analysis rows  : {len(rows['analysis'])}")
print(f"results rows   : {len(rows['results'])}")
if rows["results"]:
    print("\nresults row:")
    print(json.dumps(rows["results"][0], indent=2, ensure_ascii=False))
    print("\nanalysis row:")
    print(json.dumps(rows["analysis"][0], indent=2, ensure_ascii=False))

print(f"\nfindings CSV: {findings_csv}")
if os.path.exists(findings_csv):
    with open(findings_csv, encoding="utf-8") as f:
        lines = f.read().splitlines()
    print(f"  ({len(lines)-1} data rows). First 12:")
    for ln in lines[:13]:
        print("   ", ln[:160])
