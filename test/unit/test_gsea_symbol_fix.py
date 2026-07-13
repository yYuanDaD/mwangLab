"""Zero-network regression test for the GSEA gene-symbol fix.

Problem fixed: when a raw matrix uses bare integer feature IDs (e.g. TALON gene_IDs, as in
GSE279359) with the real symbols in an annotation column, preprocessing dropped the symbol
column and GSEA ran on integers -> zero overlap with the symbol-keyed Hallmark library ->
"No gene sets passed filtering".

The fix: preprocess_counts salvages the gene-symbol column into a '<base>_id2symbol.csv'
sidecar before dropping it; run_gsea_analysis auto-discovers that sidecar (same dir as the
DEG file) and maps the integer index to symbols before ranking.

This test covers the deterministic, zero-network parts:
  1. preprocess writes the sidecar, keyed by the matrix row id, holding symbols.
  2. _looks_numeric_ids / _load_id_symbol_map / _discover_id_symbol_map behave.
  3. run_gsea_analysis on an integer-indexed DEG WITH a sidecar reaches the mapping step
     (proven by the post-mapping "<100 genes" guard, which fires BEFORE any network call).
  4. run_gsea_analysis on an integer-indexed DEG with NO sidecar returns the clear,
     actionable error instead of the opaque "no gene sets passed filtering".

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/unit/test_gsea_symbol_fix.py
"""
import os
import sys
import shutil

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

import pandas as pd

from tools.preprocess_tools import preprocess_counts
from tools.enrichment_tools import (
    _looks_numeric_ids, _load_id_symbol_map, _discover_id_symbol_map, run_gsea_analysis,
)

OUT = os.path.join("test", "output", "test_gsea_symbol_fix")
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT)

# ---- a tiny TALON-style raw matrix: integer row id (col0) + gene_ID + annot_gene_name + 6 samples ----
n = 12
raw = pd.DataFrame({
    "gene_ID": list(range(100, 100 + n)),
    "annot_gene_name": [f"Gene{i}" for i in range(n)],
    "S1": [20] * n, "S2": [22] * n, "S3": [25] * n,
    "S4": [18] * n, "S5": [19] * n, "S6": [21] * n,
}, index=[3, 5, 15, 23, 26, 31, 40, 44, 51, 60, 71, 88])   # col0 = TALON row id
raw.index.name = ""
raw_path = os.path.join(OUT, "RAWMTX_counts.csv")
raw.to_csv(raw_path)

# ---- (1) preprocess writes the sidecar ----
preprocess_counts.invoke({"counts_csv": raw_path, "output_dir": OUT, "min_count": 1, "min_samples": 1})
side = os.path.join(OUT, "RAWMTX_counts_id2symbol.csv")
assert os.path.isfile(side), "preprocess must write the id2symbol sidecar"
sd = pd.read_csv(side, index_col=0)
assert list(sd.columns) == ["symbol"], sd.columns
assert sd.loc[3, "symbol"] == "Gene0" and sd.loc[88, "symbol"] == "Gene11", sd.to_dict()
assert "gene_ID" not in sd.columns  # symbol col chosen over the numeric gene_ID col
print(f"[1] preprocess: sidecar written, {len(sd)} ids -> symbols, keyed by matrix row id  OK")

# ---- (2) helpers ----
assert _looks_numeric_ids(["3", "5", "4854", "19149"]) is True
assert _looks_numeric_ids(["Tpm1", "Myl3", "Atp2a1"]) is False
assert _looks_numeric_ids(["ENSMUSG00000033845"]) is False
m = _load_id_symbol_map(side)
assert m["3"] == "Gene0" and m["88"] == "Gene11", m
deg_for_discover = os.path.join(OUT, "DEG_results_x_vs_y.csv")
pd.DataFrame({"stat": [1.0]}, index=[3]).to_csv(deg_for_discover)
assert os.path.abspath(_discover_id_symbol_map(deg_for_discover)) == os.path.abspath(side)
print("[2] helpers: numeric-id detection, map load, sidecar auto-discovery  OK")

# ---- (3) integer-indexed DEG WITH sidecar -> mapping runs (post-map <100-gene guard, no network) ----
deg = pd.DataFrame({"stat": [3.0, -2.0, 1.5, -1.0, 0.5, -0.3,
                             2.1, -2.2, 0.9, -0.8, 1.1, -1.3]},
                   index=raw.index)
deg_path = os.path.join(OUT, "DEG_results_treat_vs_ctrl.csv")
deg.to_csv(deg_path)
msg = run_gsea_analysis.invoke({"deg_csv": deg_path, "organism": "Mouse",
                                "ranking_metric": "stat", "output_dir": OUT})
# 12 genes -> after mapping still 12 -> hits the "needs a few thousand" guard, which proves the
# mapping branch executed and we never reached the network GMT fetch.
assert "valid genes after filtering / ID conversion" in msg, msg
assert "12" in msg, msg
print("[3] GSEA with sidecar: integer index mapped to symbols before the <100-gene guard  OK")

# ---- (4) integer-indexed DEG with NO sidecar -> clear, actionable error ----
bare_dir = os.path.join(OUT, "no_sidecar")
os.makedirs(bare_dir)
deg2 = os.path.join(bare_dir, "DEG_results_a_vs_b.csv")
deg.to_csv(deg2)
msg2 = run_gsea_analysis.invoke({"deg_csv": deg2, "organism": "Mouse",
                                 "ranking_metric": "stat", "output_dir": bare_dir})
assert "bare integer feature IDs" in msg2 and "id2symbol" in msg2, msg2
assert "no gene sets passed filtering" not in msg2.lower()
print("[4] GSEA without sidecar: returns the clear integer-ID error (not the opaque one)  OK")

print("\nPASS — GSEA symbol fix: preprocess salvages the symbol column into a sidecar, "
      "GSEA auto-discovers it and maps integer feature IDs to symbols (so GSE279359-style "
      "TALON matrices now run), and fails loudly with an actionable message when it can't.")
