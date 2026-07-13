"""Refined read of the 3 determinism runs: separate REAL non-determinism from
positional-alignment artifacts (the `material` table is an unordered list, so
row-index comparison is unfair). Zero LLM cost — reads run_*.json only."""

import os
import sys
import json
import glob
from collections import defaultdict

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
OUT_DIR = os.path.join("output", "_determinism_check")

runs = []
for p in sorted(glob.glob(os.path.join(OUT_DIR, "run_*.json")),
                key=lambda p: int(os.path.basename(p)[4:-5])):
    with open(p, encoding="utf-8") as f:
        runs.append(json.load(f))
N = len(runs)
print(f"{N} runs loaded\n")

# 1) material as a SET (by material_name), order-independent
def names(run):
    return {(r.get("material_name") or "").strip().lower()
            for r in run["material"] if (r.get("material_name") or "").strip()}
sets = [names(r) for r in runs]
inter = set.intersection(*sets)
union = set.union(*sets)
print("=" * 64)
print("MATERIAL table compared as a SET (order-independent, by name)")
for i, s in enumerate(sets, 1):
    print(f"  run{i}: {len(s)} distinct material names")
print(f"  common to ALL 3 runs : {len(inter)}")
print(f"  union (any run)      : {len(union)}")
print(f"  set Jaccard (|∩|/|∪|): {len(inter)/len(union):.2f}")
only = [s - inter for s in sets]
for i, s in enumerate(only, 1):
    if s:
        print(f"  only in run{i} ({len(s)}): {sorted(s)[:6]}{' ...' if len(s) > 6 else ''}")

# 2) value-field stability EXCLUDING the unordered material table
field_vals = defaultdict(list)
for r in runs:
    for name, rows in r.items():
        if name == "material":
            continue
        for idx, row in enumerate(rows):
            for field, val in row.items():
                field_vals[(name, idx, field)].append(val)

val_t = val_s = 0
drift = []
for (name, idx, field), vals in field_vals.items():
    if len(vals) != N or field.endswith("_source"):
        continue
    distinct = {json.dumps(v, ensure_ascii=False, sort_keys=True) for v in vals}
    val_t += 1
    if len(distinct) == 1:
        val_s += 1
    else:
        drift.append((name, idx, field, vals))

print("\n" + "=" * 64)
print("VALUE fields EXCLUDING material (positionally comparable tables only)")
print(f"  stable: {val_s}/{val_t} ({100.0*val_s/val_t:.1f}%)  -> {len(drift)} drift")

# 3) classify the remaining drift: case-only vs real
def case_only(vals):
    norm = {(v.strip().lower() if isinstance(v, str) else v) for v in vals}
    return len(norm) == 1
case_drift = [d for d in drift if case_only(d[3])]
real_drift = [d for d in drift if not case_only(d[3])]
print(f"  of which CASE/whitespace-only : {len(case_drift)}")
print(f"  of which REAL content diff     : {len(real_drift)}")
print("\n  REAL content drift (excluding material):")
for name, idx, field, vals in real_drift:
    print(f"  [{name}#{idx}.{field}]")
    for i, v in enumerate(vals, 1):
        sv = v if not isinstance(v, str) or len(v) <= 95 else v[:95] + "..."
        print(f"      run{i}: {sv!r}")

# 4) the headline structural risk
print("\n" + "=" * 64)
print("STRUCTURAL RISK — experiment/group split is non-deterministic")
print(f"  experiment rows : {[len(r['experiment']) for r in runs]}")
print(f"  groups rows     : {[len(r['groups']) for r in runs]}")
print(f"  subject rows    : {[len(r['subject']) for r in runs]}")
