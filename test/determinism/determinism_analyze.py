"""Analyze-only companion to determinism_check_seacdm.py (meeting requirement #3).

Loads every already-saved output/_determinism_check/run_*.json (no LLM calls, zero cost)
and reports the same three levels of (in)consistency: whole-output identity, per-table
row counts, and field-level value/source stability.

Run:  PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/determinism/determinism_analyze.py
"""

import os
import sys
import json
import glob
import hashlib
from collections import defaultdict

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)
sys.path.insert(0, _ROOT)

from tools.determinism_similarity import summarize_rouge_l

OUT_DIR = os.path.join("output", "_determinism_check")


def _canon_hash(obj) -> str:
    blob = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:12]


def main():
    paths = sorted(glob.glob(os.path.join(OUT_DIR, "run_*.json")),
                   key=lambda p: int(os.path.basename(p)[4:-5]))
    if len(paths) < 2:
        print(f"Need >=2 run_*.json in {OUT_DIR}, found {len(paths)}.")
        sys.exit(1)
    runs = []
    for p in paths:
        with open(p, encoding="utf-8") as f:
            runs.append(json.load(f))
    N = len(runs)
    print(f"Analyzing {N} runs: {[os.path.basename(p) for p in paths]}\n")

    table_names = list(runs[0].keys())

    # ---- level 1 ----
    hashes = [_canon_hash(t) for t in runs]
    whole_identical = len(set(hashes)) == 1
    print("=" * 70)
    print("LEVEL 1 — whole-output identity")
    print("  per-run sha256[:12] :", hashes)
    print("  ALL runs byte-identical :", whole_identical)

    # ---- level 2 ----
    print("\n" + "=" * 70)
    print("LEVEL 2 — per-table row counts across runs")
    structural_stable = True
    for name in table_names:
        counts = [len(r[name]) for r in runs]
        if not any(counts):
            continue
        varies = len(set(counts)) != 1
        structural_stable &= not varies
        print(f"  {name:15s} {counts}{'   <-- VARIES' if varies else ''}")
    print(f"  -> structural stable across all runs : {structural_stable}")

    # ---- level 3 ----
    field_vals = defaultdict(list)
    for r in runs:
        for name in table_names:
            for idx, row in enumerate(r[name]):
                for field, val in row.items():
                    field_vals[(name, idx, field)].append(val)

    val_total = val_stable = src_total = src_stable = 0
    variable_values, variable_sources = [], []
    for (name, idx, field), vals in field_vals.items():
        if len(vals) != N:
            continue
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

    def pct(a, b):
        return f"{(100.0 * a / b):.1f}%" if b else "n/a"

    print("\n" + "=" * 70)
    print("LEVEL 3 — field-level stability (rows aligned across ALL runs)")
    print(f"  VALUE fields  : {val_stable}/{val_total} stable ({pct(val_stable, val_total)})  "
          f"-> {len(variable_values)} drift")
    print(f"  SOURCE quotes : {src_stable}/{src_total} stable ({pct(src_stable, src_total)})  "
          f"-> {len(variable_sources)} drift")

    if variable_values:
        print("\n  --- VALUE fields that DIFFER across runs (semantic non-determinism) ---")
        for name, idx, field, vals in variable_values:
            print(f"  [{name}#{idx}.{field}]")
            for i, v in enumerate(vals, 1):
                shown = v if not isinstance(v, str) or len(v) <= 100 else v[:100] + "..."
                print(f"      run{i}: {shown!r}")

    if variable_sources:
        print(f"\n  --- SOURCE-quote drift: {len(variable_sources)} fields "
              f"(provenance wording; showing up to 6) ---")
        for name, idx, field, vals in variable_sources[:6]:
            print(f"  [{name}#{idx}.{field}]")
            for i, v in enumerate(vals, 1):
                shown = v if not isinstance(v, str) or len(v) <= 100 else v[:100] + "..."
                print(f"      run{i}: {shown!r}")

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

    summary = {
        "n_runs": N,
        "runs": [os.path.basename(p) for p in paths],
        "whole_output_identical": whole_identical,
        "per_run_hash": hashes,
        "structural_stable": structural_stable,
        "row_counts": {name: [len(r[name]) for r in runs] for name in table_names
                       if any(len(r[name]) for r in runs)},
        "value_fields_total": val_total, "value_fields_stable": val_stable,
        "value_fields_drift": len(variable_values),
        "source_fields_total": src_total, "source_fields_stable": src_stable,
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
    with open(os.path.join(OUT_DIR, "SUMMARY.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"\nSummary written to {os.path.join(OUT_DIR, 'SUMMARY.json')}")


if __name__ == "__main__":
    main()
