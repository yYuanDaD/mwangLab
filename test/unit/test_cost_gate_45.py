"""Zero-network/zero-LLM test for cost optimizations 4 & 5:
  (4) download_geo_data short-circuits when the metadata CSV is already on disk (no SOFT download/parse),
  (5) _python_pick_is_confident gates the per-study LLM contrast validation — True only when the
      Python pick is unambiguous (arms >= 3 AND exactly one viable design column), else False.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/unit/test_cost_gate_45.py
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

import pandas as pd

# ---------- (4) download_geo_data skip-if-exists ----------
import tools.geo_tools as geo

_BASE = os.path.join("test", "output", "test_cost_gate_45")
_acc = "GSEFAKE777"
os.makedirs(os.path.join(_BASE, _acc), exist_ok=True)
meta = os.path.join(_BASE, _acc, f"{_acc}_metadata.csv")
pd.DataFrame({"x": [1, 2, 3]}, index=["s1", "s2", "s3"]).to_csv(meta)   # 3 samples already present

getgeo_calls = []
geo.GEOparse.get_GEO = lambda *a, **k: getgeo_calls.append(k) or (_ for _ in ()).throw(AssertionError("should not be called"))

_dl = getattr(geo.download_geo_data, "func", geo.download_geo_data)
msg = _dl(_acc, base_dir=_BASE)
assert getgeo_calls == [], "GEOparse.get_GEO must NOT be called when metadata already exists"
assert "already present" in msg and "3 samples" in msg, msg
print("[4] download_geo_data: metadata present -> 0 GEOparse calls, returned cached  OK")

# ---------- (5) confidence gate ----------
from tools.batch_tools import _python_pick_is_confident

def _csv(name, cols):
    p = os.path.join(_BASE, name)
    pd.DataFrame(cols, index=[f"s{i}" for i in range(len(next(iter(cols.values()))))]).to_csv(p)
    return p

TK, CK = ["exercise", "running"], ["control", "sedentary"]

# A) clean single design column, 4 vs 4 -> CONFIDENT (skip LLM)
a = _csv("A.csv", {"treatment": ["exercise"] * 4 + ["control"] * 4})
assert _python_pick_is_confident(a, ("treatment", "control", "exercise"), TK, CK) is True
print("[5a] clean 4v4 single column -> confident (LLM skipped)  OK")

# B) treatment arm too small (2) -> NOT confident (keep LLM)
b = _csv("B.csv", {"treatment": ["exercise"] * 2 + ["control"] * 4})
assert _python_pick_is_confident(b, ("treatment", "control", "exercise"), TK, CK) is False
print("[5b] arm < 3 samples -> not confident (LLM kept)  OK")

# C) cross-column ambiguity: TWO viable design columns -> NOT confident (keep LLM)
c = _csv("C.csv", {"treatment": ["exercise"] * 4 + ["control"] * 4,
                   "group":     ["running"] * 4 + ["sedentary"] * 4})
assert _python_pick_is_confident(c, ("treatment", "control", "exercise"), TK, CK) is False
print("[5c] two competing design columns -> not confident (LLM kept)  OK")

# D) no design pick -> NOT confident
assert _python_pick_is_confident(a, None, TK, CK) is False
# E) missing keywords -> NOT confident (fail safe to LLM)
assert _python_pick_is_confident(a, ("treatment", "control", "exercise"), [], CK) is False
print("[5d/e] no-design / missing-keywords -> not confident (fail safe to LLM)  OK")

print("\nPASS — (4) cached metadata skips GEOparse; (5) LLM contrast validation is skipped ONLY "
      "when the Python pick is unambiguous, kept otherwise.")
