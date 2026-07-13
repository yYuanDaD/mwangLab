"""Zero-network unit test for the post-DA implausibility guard (_deg_sanity_flags).

Root cause it guards (GSE317978): a real but n=2-per-group contrast passes every existing check
(valid DEG file, >=4 samples) yet limma's eBayes — with zero within-group variance on 2 reps —
calls ~66% of the genome 'DE'. That result LOOKS normal and was emitted silently. The guard turns
it loud via two principled signals: implausible significant fraction (>50%) and tiny per-group n (<3).

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/unit/test_deg_sanity_guard.py
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

import pandas as pd
from tools.batch_tools import _deg_sanity_flags

OUT = os.path.join("test", "output", "test_deg_sanity")
os.makedirs(OUT, exist_ok=True)


def _meta(name, ctrl_n, treat_n):
    rows = [("control",) for _ in range(ctrl_n)] + [("exercise",) for _ in range(treat_n)]
    p = os.path.join(OUT, name)
    pd.DataFrame({"group": [r[0] for r in rows]},
                 index=[f"s{i}" for i in range(len(rows))]).to_csv(p)
    return p

# healthy: 4v4, 5% significant -> clean
md_ok = _meta("ok.csv", 4, 4)
assert _deg_sanity_flags(50, 1000, md_ok, "group", "control", "exercise") == "", "clean run must be ok"
print("[1] 4v4, 5% sig -> clean (no flag)  OK")

# GSE317978-like: 2v2, 66% significant -> BOTH flags
md_tiny = _meta("tiny.csv", 2, 2)
f = _deg_sanity_flags(11339, 17043, md_tiny, "group", "control", "exercise")
assert "implausible_sig_fraction=" in f and "tiny_n_per_group=2" in f, f
print(f"[2] 2v2, 66% sig -> flagged: {f}  OK")

# implausible fraction alone (large n but artifact) -> only the fraction flag
f2 = _deg_sanity_flags(8000, 12000, md_ok, "group", "control", "exercise")
assert f2 == f2 and "implausible_sig_fraction=" in f2 and "tiny_n_per_group" not in f2, f2
print(f"[3] 4v4 but 67% sig -> fraction flag only: {f2}  OK")

# tiny n alone (low fraction) -> only the n flag
f3 = _deg_sanity_flags(20, 1000, md_tiny, "group", "control", "exercise")
assert "tiny_n_per_group=2" in f3 and "implausible_sig_fraction" not in f3, f3
print(f"[4] 2v2 but 2% sig -> n flag only: {f3}  OK")

# boundary: exactly 50% is NOT > 0.50 -> no fraction flag; n=3 is NOT < 3 -> no n flag
md_3 = _meta("three.csv", 3, 3)
assert _deg_sanity_flags(500, 1000, md_3, "group", "control", "exercise") == "", "50% & n=3 are at the safe boundary"
print("[5] boundary 50% sig + n=3/group -> clean  OK")

print("\nPASS — _deg_sanity_flags flags implausible significant fraction (>50%) and tiny per-group "
      "n (<3), independently and together, so n=2/group GSE317978-style results are no longer silent.")
