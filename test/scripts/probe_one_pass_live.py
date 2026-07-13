"""LIVE proof for req #3 one-pass extraction: run the merged lean call on the REAL cached
GSE208615 paper + GEO metadata, and show that (a) it is ONE LLM call and (b) that single call
returns BOTH the descriptive tables AND the paper's reported findings (#5) — i.e. findings are
extracted in the same pass, no separate #5 call.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/scripts/probe_one_pass_live.py
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

from tools.seacdm_tools import extract_tables_from_text

PAPER = "data/papers/ce74938ff6bc79920a89e84c09b0c0300e7c634f.txt"   # GSE208615 (Acvr1c/Bdnf)
META = "data/GSE208615/GSE208615_metadata.csv"

text = open(PAPER, encoding="utf-8", errors="ignore").read()[:24000]   # cohort's max_chars
report, usage = {}, []
tables = extract_tables_from_text("GSE208615", text, "Mouse",
                                  report=report, metadata_csv=META, usage=usage)

print(f"extraction_mode : {report.get('extraction_mode')}")
print(f"LLM calls       : {len(usage)}  ({[u['call'] for u in usage]})")
print(f"input tokens    : {sum((u.get('input_tokens') or 0) for u in usage)}")
findings = report.get("reported_findings") or []
print(f"reported_findings extracted in that SAME call: {len(findings)}")
fv = report.get("findings_verify") or {}
if fv:
    print(f"  verbatim-verified: {fv.get('n_verified')}/{fv.get('n_total')} "
          f"({fv.get('n_unverified')} flagged, {fv.get('n_snapped')} snapped)")
for f in findings[:5]:
    print(f"    - {f['entity']} ({f['entity_type']}) {f['direction']}  src={f['source'][:60]!r}")
print(f"structural rows : experiment={len(tables['experiment'])} sample={len(tables['sample'])} "
      f"groups={len(tables['groups'])} material={len(tables['material'])}")

assert report.get("extraction_mode") == "lean(1-call)"
assert len(usage) == 1, f"expected ONE merged call, got {len(usage)}"
print("\nPROVEN: one lean call returned descriptive tables + reported findings together (req #3).")
