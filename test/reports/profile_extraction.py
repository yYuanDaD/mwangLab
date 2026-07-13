"""req #4 — SEA-CDM extraction cost/time profiler + full-vs-lean comparison.

Measures the REAL per-call token usage (via with_structured_output include_raw), wall-clock time,
and $ cost of the SEA-CDM table extraction, for both modes:

  * FULL  (3 calls: study_level + design + methods) — the pre-#4 behavior; sends the full paper
    text THREE times.
  * LEAN  (1 merged call) — only available when a GEO metadata CSV supplies subject/sample/groups/
    assay (req #3); sends the full text ONCE.

Pricing: Claude Sonnet 4.6 = $3.00 / 1M input tokens, $15.00 / 1M output tokens (per the claude-api
skill, 2026-06). Prints a side-by-side table + the savings, and confirms the kept descriptive tables
are still populated and the metadata-derived structural tables are byte-identical between modes.

Run:  PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/reports/profile_extraction.py
Cost: 4 Sonnet calls on GSE208615 (3 full + 1 lean) ~= 100k input tokens; throttled by the 30k
      tok/min org limit (the SDK retries 429s), so expect a few minutes wall-clock.
"""

import os
import sys
import json
import time
import hashlib

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)
sys.path.insert(0, _ROOT)

from tools.seacdm_tools import extract_tables_from_text

PAPER_TXT = os.path.join("data", "papers", "ce74938ff6bc79920a89e84c09b0c0300e7c634f.txt")
STUDY_ID = "GSE208615"
ORGANISM = "Mouse"
MAX_CHARS = 100000
IN_PRICE = 3.00 / 1_000_000    # Sonnet 4.6 input $/token
OUT_PRICE = 15.00 / 1_000_000  # Sonnet 4.6 output $/token
OUT_DIR = os.path.join("output", "_extraction_profile")


def _cost(usage):
    ti = sum((u.get("input_tokens") or 0) for u in usage)
    to = sum((u.get("output_tokens") or 0) for u in usage)
    return ti, to, ti * IN_PRICE + to * OUT_PRICE


def _hash(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:10]


def _run(mode_lean):
    usage, rep = [], {}
    t0 = time.perf_counter()
    tables = extract_tables_from_text(STUDY_ID, TEXT, ORGANISM, report=rep,
                                      lean=mode_lean, usage=usage)
    secs = time.perf_counter() - t0
    ti, to, cost = _cost(usage)
    return {"tables": tables, "usage": usage, "report": rep, "secs": secs,
            "in_tok": ti, "out_tok": to, "cost": cost}


if not os.path.exists(PAPER_TXT):
    print(f"ERROR: cached paper text not found: {PAPER_TXT}")
    sys.exit(1)
with open(PAPER_TXT, encoding="utf-8", errors="ignore") as f:
    TEXT = f.read()[:MAX_CHARS]
os.makedirs(OUT_DIR, exist_ok=True)

print(f"Extraction profile: {STUDY_ID}  ({len(TEXT)} chars)  Sonnet 4.6 @ temp=0\n")

print("  running FULL (3-call) ...", flush=True)
full = _run(False)
print("  running LEAN (1-call) ...", flush=True)
lean = _run(True)

print("\n" + "=" * 72)
print(f"  mode   calls   in_tok   out_tok       $cost     secs   extraction_mode")
for name, r in (("FULL", full), ("LEAN", lean)):
    print(f"  {name:5s}  {len(r['usage']):5d}  {r['in_tok']:7d}  {r['out_tok']:8d}   "
          f"${r['cost']:.5f}  {r['secs']:7.1f}   {r['report'].get('extraction_mode')}")

if full["in_tok"] and lean["in_tok"]:
    din = 100 * (1 - lean["in_tok"] / full["in_tok"])
    dcost = 100 * (1 - lean["cost"] / full["cost"]) if full["cost"] else 0
    print(f"\n  LEAN vs FULL:  input tokens -{din:.1f}%   $cost -{dcost:.1f}%   "
          f"calls {len(full['usage'])} -> {len(lean['usage'])}")

# table row counts both modes
print("\n" + "=" * 72)
print("  per-table row counts (FULL vs LEAN)")
struct = ("subject", "sample", "groups", "assay")
kept = ("study", "experiment", "documentation", "material", "interventions")
for t in list(kept) + list(struct):
    fn, ln = len(full["tables"][t]), len(lean["tables"][t])
    tag = ""
    if t in struct:
        same = _hash(full["tables"][t]) == _hash(lean["tables"][t])
        tag = "  [structural: " + ("IDENTICAL" if same else "DIFFERS") + "]"
    print(f"  {t:14s} full={fn:<4d} lean={ln:<4d}{tag}")

# correctness guards: structural tables identical (both from metadata); kept tables non-empty in lean
struct_ok = all(_hash(full["tables"][t]) == _hash(lean["tables"][t]) for t in struct)
kept_ok = all(len(lean["tables"][t]) > 0 for t in ("study", "experiment", "material"))
print("\n  structural tables identical across modes :", struct_ok)
print("  lean kept study/experiment/material populated :", kept_ok)

with open(os.path.join(OUT_DIR, "profile.json"), "w", encoding="utf-8") as fh:
    json.dump({
        "study_id": STUDY_ID, "max_chars": MAX_CHARS,
        "pricing": {"in_per_mtok": 3.0, "out_per_mtok": 15.0, "model": "claude-sonnet-4-6"},
        "full": {k: full[k] for k in ("usage", "report", "secs", "in_tok", "out_tok", "cost")},
        "lean": {k: lean[k] for k in ("usage", "report", "secs", "in_tok", "out_tok", "cost")},
        "row_counts": {t: {"full": len(full["tables"][t]), "lean": len(lean["tables"][t])}
                       for t in full["tables"]},
        "structural_identical": struct_ok, "lean_kept_populated": kept_ok,
    }, fh, indent=2, ensure_ascii=False)
print(f"\nWritten {os.path.join(OUT_DIR, 'profile.json')}")
