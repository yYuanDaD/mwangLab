"""Unit test for the per-stage cost/timing profiler (user directive 2026-06-23).

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/unit/test_cost_timing.py
"""
import os
import sys
import time
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

import tools.cohort_tools  # noqa: F401 — import-clean check (profiler wiring doesn't break the module)
from tools.cost_timing import RunProfiler, usd_for


def test_usd_formula():
    # 100k input + 20k output at Sonnet 4.6 $3/$15 per Mtok = 0.30 + 0.30 = 0.60
    assert abs(usd_for(100_000, 20_000) - 0.6) < 1e-9, usd_for(100_000, 20_000)
    assert usd_for(0, 0) == 0.0
    print("  [ok] usd_for: $3/Mtok in + $15/Mtok out")


def test_profiler_accumulate_and_csv():
    p = RunProfiler()
    with p.stage("search"):
        time.sleep(0.005)
    p.add_time("search", 1.5)  # accumulates onto the same slot
    with p.stage("extraction"):
        time.sleep(0.005)
    p.add_llm_usage("extraction", [{"input_tokens": 35826, "output_tokens": 6550}])
    p.add_llm_usage("findings_#5", [])              # lean path: merged → no tokens here
    p.add_time("analysis_batch(DA+GSEA)", 120.0)    # free CPU: time, no tokens

    # extraction $ = 35826*3/1e6 + 6550*15/1e6
    exp = 35826 * 3 / 1e6 + 6550 * 15 / 1e6
    assert abs(p.total_usd() - exp) < 1e-6, (p.total_usd(), exp)
    assert p.total_llm() == 1
    assert p.total_wall() >= 121.5  # 1.5 (search) + 120 (batch) + the two sleeps
    assert p.total_in() == 35826 and p.total_out() == 6550

    # free-CPU stage shows $0 but real seconds
    rows = {r[0]: r for r in p.rows()}
    assert rows["analysis_batch(DA+GSEA)"][5] == 0.0  # usd_est
    assert rows["analysis_batch(DA+GSEA)"][1] == 120.0  # wall_s
    assert rows["findings_#5"][2] == 0  # n_llm_calls

    out = os.path.join(tempfile.mkdtemp(), "cost_timing.csv")
    p.write_csv(out)
    txt = open(out, encoding="utf-8").read()
    assert "stage,wall_s,n_llm_calls,input_tokens,output_tokens,usd_est" in txt
    assert "TOTAL" in txt
    print("  [ok] profiler: accumulation, $ math, free-CPU=$0+wall, CSV has header+TOTAL")
    print("\n".join(p.summary_lines()))


if __name__ == "__main__":
    test_usd_formula()
    test_profiler_accumulate_and_csv()
    print("\nALL TESTS PASSED.")
