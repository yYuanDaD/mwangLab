"""Determinism check for the v1 SEA-CDM extractor (meeting requirement #3).

Re-runs `extract_tables_from_text` N times on the SAME cached paper full-text, at
the SAME temperature=0, then quantifies how (in)consistent the JSON output is across
runs at three levels:

  1. whole-output  — is the entire 13-table dict byte-identical across all N runs?
  2. structural    — per-table row counts; do they stay the same run-to-run?
  3. field-level   — for each (table, row_index, field) present in ALL runs, is the
                     `value` / `_source` identical? Reports stable-% and lists drifters.

Run:  PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/determinism/determinism_check_seacdm.py
Cost: N * 3 Sonnet structured-output calls (default N=5 -> 15 calls on one paper).
"""

import os
import sys
import json
import hashlib
from collections import defaultdict

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)
sys.path.insert(0, _ROOT)

from tools.determinism_similarity import summarize_rouge_l
from tools.seacdm_tools import extract_tables_from_text

# --- config: the test3 demo-success paper (GSE208615, single experiment, rich extraction) ---
PAPER_TXT = os.path.join("data", "papers", "ce74938ff6bc79920a89e84c09b0c0300e7c634f.txt")
STUDY_ID = "GSE208615"
ORGANISM = "Mouse"
N = int(os.environ.get("DET_N", "5"))
MAX_CHARS = 100000  # mirror the @tool's cost guard so we test the real pipeline input
OUT_DIR = os.path.join("output", "_determinism_check")


def _canon_hash(obj) -> str:
    blob = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:12]


def main():
    if not os.path.exists(PAPER_TXT):
        print(f"ERROR: cached paper text not found: {PAPER_TXT}")
        sys.exit(1)
    with open(PAPER_TXT, encoding="utf-8", errors="ignore") as f:
        text = f.read()[:MAX_CHARS]
    os.makedirs(OUT_DIR, exist_ok=True)

    print(f"Determinism check: {STUDY_ID}  ({len(text)} chars)  x {N} runs  @ temp=0\n")

    runs = []
    for i in range(1, N + 1):
        print(f"  [run {i}/{N}] extracting ...", flush=True)
        rep: dict = {}
        tables = extract_tables_from_text(STUDY_ID, text, ORGANISM, verify=True, report=rep)
        with open(os.path.join(OUT_DIR, f"run_{i}.json"), "w", encoding="utf-8") as fh:
            json.dump(tables, fh, indent=2, ensure_ascii=False)
        runs.append(tables)
    print()

    table_names = list(runs[0].keys())

    # ---- level 1: whole-output identity ----
    hashes = [_canon_hash(t) for t in runs]
    whole_identical = len(set(hashes)) == 1
    print("=" * 70)
    print("LEVEL 1 — whole-output identity")
    print("  per-run sha256[:12] :", hashes)
    print("  ALL N runs byte-identical :", whole_identical)

    # ---- level 2: structural (row counts) ----
    print("\n" + "=" * 70)
    print("LEVEL 2 — per-table row counts across runs")
    structural_stable = True
    for name in table_names:
        counts = [len(r[name]) for r in runs]
        if not any(counts):
            continue
        varies = len(set(counts)) != 1
        if varies:
            structural_stable = False
        print(f"  {name:15s} {counts}{'   <-- VARIES' if varies else ''}")
    print(f"  -> structural stable across all runs : {structural_stable}")

    # ---- level 3: field-level (aligned by row index, only keys present in ALL runs) ----
    field_vals = defaultdict(list)
    for r in runs:
        for name in table_names:
            for idx, row in enumerate(r[name]):
                for field, val in row.items():
                    field_vals[(name, idx, field)].append(val)

    val_total = val_stable = src_total = src_stable = 0
    variable_values = []   # semantic drift (the .value differs)
    variable_sources = []  # provenance-quote wording drift (the _source differs)
    for (name, idx, field), vals in field_vals.items():
        if len(vals) != N:
            continue  # row absent in some run -> already captured by level-2 count diff
        distinct = {json.dumps(v, ensure_ascii=False, sort_keys=True) for v in vals}
        stable = len(distinct) == 1
        if field.endswith("_source"):
            src_total += 1
            src_stable += stable
            if not stable:
                variable_sources.append((name, idx, field, vals))
        else:
            val_total += 1
            val_stable += stable
            if not stable:
                variable_values.append((name, idx, field, vals))

    print("\n" + "=" * 70)
    print("LEVEL 3 — field-level stability (rows aligned across ALL runs)")

    def pct(a, b):
        return f"{(100.0 * a / b):.1f}%" if b else "n/a"

    print(f"  VALUE fields  : {val_stable}/{val_total} stable ({pct(val_stable, val_total)})  "
          f"-> {len(variable_values)} drift")
    print(f"  SOURCE quotes : {src_stable}/{src_total} stable ({pct(src_stable, src_total)})  "
          f"-> {len(variable_sources)} drift")

    if variable_values:
        print("\n  --- VALUE fields that DIFFER across runs (semantic non-determinism) ---")
        for name, idx, field, vals in variable_values:
            print(f"  [{name}#{idx}.{field}]")
            for i, v in enumerate(vals, 1):
                shown = v if not isinstance(v, str) or len(v) <= 90 else v[:90] + "..."
                print(f"      run{i}: {shown!r}")

    if variable_sources:
        print(f"\n  --- SOURCE-quote drift: {len(variable_sources)} fields "
              f"(provenance wording varies; showing up to 5) ---")
        for name, idx, field, vals in variable_sources[:5]:
            print(f"  [{name}#{idx}.{field}]")
            for i, v in enumerate(vals, 1):
                shown = v if not isinstance(v, str) or len(v) <= 90 else v[:90] + "..."
                print(f"      run{i}: {shown!r}")

    # ---- level 4: ROUGE-L for descriptive text drift ----
    value_rouge = summarize_rouge_l(variable_values)
    source_rouge = summarize_rouge_l(variable_sources)
    print("\n" + "=" * 70)
    print("LEVEL 4 — ROUGE-L similarity for drifted text fields")
    print(f"  VALUE fields  : scored={value_rouge['fields_scored']}  "
          f"mean F1={value_rouge['mean_rouge_l_f1']}  min F1={value_rouge['min_rouge_l_f1']}")
    print(f"  SOURCE quotes : scored={source_rouge['fields_scored']}  "
          f"mean F1={source_rouge['mean_rouge_l_f1']}  min F1={source_rouge['min_rouge_l_f1']}")
    if value_rouge["below_threshold"]:
        print("  Low-similarity VALUE fields (min pairwise F1 < 0.90; showing up to 8):")
        for item in value_rouge["below_threshold"][:8]:
            print(f"    [{item['table']}#{item['row']}.{item['field']}] "
                  f"mean={item['rouge_l_f1_mean']} min={item['rouge_l_f1_min']}")

    # ---- machine-readable summary ----
    summary = {
        "study_id": STUDY_ID,
        "paper_txt": PAPER_TXT,
        "n_runs": N,
        "temperature": 0,
        "max_chars": MAX_CHARS,
        "whole_output_identical": whole_identical,
        "per_run_hash": hashes,
        "structural_stable": structural_stable,
        "row_counts": {name: [len(r[name]) for r in runs] for name in table_names
                       if any(len(r[name]) for r in runs)},
        "value_fields_total": val_total,
        "value_fields_stable": val_stable,
        "value_fields_drift": len(variable_values),
        "source_fields_total": src_total,
        "source_fields_stable": src_stable,
        "source_fields_drift": len(variable_sources),
        "variable_value_fields": [
            {"table": n, "row": i, "field": fld, "values": vs}
            for (n, i, fld, vs) in variable_values
        ],
        "variable_source_fields": [
            {"table": n, "row": i, "field": fld, "values": vs}
            for (n, i, fld, vs) in variable_sources
        ],
        "rouge_l": {
            "value_fields": value_rouge,
            "source_fields": source_rouge,
        },
    }
    with open(os.path.join(OUT_DIR, "SUMMARY.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False)
    print(f"\nSummary written to {os.path.join(OUT_DIR, 'SUMMARY.json')}")


if __name__ == "__main__":
    main()
