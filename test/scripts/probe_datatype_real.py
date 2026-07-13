"""Integration probe for req #1 on REAL cached GEO studies: runs the exact decision path the
batch loop uses (heuristic _find_expression_file -> platform hint -> LLM cross-check -> route),
so we see the live LLM data-type decision on real matrices without a full 5-min cohort.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/scripts/probe_datatype_real.py [GSE...]
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

import pandas as pd
from tools.batch_tools import (
    _find_expression_file, _classify_matrix, _platform_hint_from_metadata,
    _llm_datatype_decision, _apply_llm_matrix_type, _gather_matrix_candidates,
)

# decimal-matrix studies where the LLM actually fires (raw-count studies skip it by design)
STUDIES = sys.argv[1:] or ["GSE132520", "GSE317978", "GSE279359"]

for acc in STUDIES:
    data_dir = os.path.join("data", acc)
    print(f"\n=== {acc} ===")
    if not os.path.isdir(data_dir):
        print("  (no cached data dir — skip)")
        continue

    counts_path, matrix_type = _find_expression_file(data_dir)
    meta_csv = os.path.join(data_dir, f"{acc}_metadata.csv")
    platform_hint = ""
    if os.path.exists(meta_csv):
        platform_hint = _platform_hint_from_metadata(pd.read_csv(meta_csv, index_col=0))
    print(f"  heuristic: counts_path={os.path.basename(str(counts_path))} type={matrix_type}")
    print(f"  platform_hint: {platform_hint[:160] or '(none)'}")

    probe_path = counts_path
    h_cls = matrix_type
    if counts_path is None:
        cands = _gather_matrix_candidates(data_dir)
        if cands:
            probe_path = cands[0]
            h_cls, _ = _classify_matrix(probe_path)
            print(f"  (heuristic dropped all; rescue candidate={os.path.basename(probe_path)} cls={h_cls})")

    if probe_path is None:
        print("  no candidate to classify")
        continue

    organism = "Human" if any(h in acc for h in ()) else "Mouse"
    llm_res = _llm_datatype_decision(probe_path, h_cls, platform_hint, organism)
    if llm_res is None:
        print("  LLM not consulted (raw counts gate) or unavailable")
        continue
    new_path, mapped, note = _apply_llm_matrix_type(llm_res, probe_path)
    print(f"  LLM: type={llm_res.matrix_type} conf={llm_res.confidence}")
    print(f"       reasoning: {llm_res.reasoning}")
    print(f"  -> route: matrix_type={mapped} | {note}")
    if new_path != probe_path:
        print(f"       pre-transform wrote: {os.path.basename(new_path)}")

print("\nDONE.")
