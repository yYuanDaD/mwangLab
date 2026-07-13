"""Synthetic validation for run_methylation_da (data-coverage P1): plant differential methylation
in a β matrix and confirm β→M-value→limma recovers it. Zero network, zero LLM.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/unit/test_methylation_da.py
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

import numpy as np
import pandas as pd
from tools.methylation_tools import run_methylation_da, _beta_to_mvalue, _looks_like_beta

OUT = os.path.join("test", "output", "test_methylation")
os.makedirs(OUT, exist_ok=True)
np.random.seed(0)

N_SITES, N_DMC, N_PER = 1000, 50, 4
samples = [f"ctrl{i}" for i in range(N_PER)] + [f"treat{i}" for i in range(N_PER)]

# realistic: each CpG has its OWN baseline methylation level (~U(0.1,0.9)) + per-sample noise;
# planted DMCs are hyper-methylated in treatment (+0.4). (A degenerate all-sites-at-0.5 matrix
# would choke inmoose's eBayes variance trend — real β data is not like that.)
base = np.random.uniform(0.1, 0.9, (N_SITES, 1))
beta = np.clip(base + np.random.normal(0, 0.05, (N_SITES, 2 * N_PER)), 0.02, 0.98)
dmc_idx = np.arange(N_DMC)
beta[dmc_idx, N_PER:] = np.clip(beta[dmc_idx, :1] + 0.40 + np.random.normal(0, 0.04, (N_DMC, N_PER)), 0.02, 0.98)
sites = [f"cg{i:05d}" for i in range(N_SITES)]
beta_df = pd.DataFrame(beta, index=sites, columns=samples)
beta_csv = os.path.join(OUT, "synthetic_beta.csv")
beta_df.to_csv(beta_csv)

meta = pd.DataFrame({"group": ["control"] * N_PER + ["exercise"] * N_PER}, index=samples)
meta_csv = os.path.join(OUT, "meta.csv")
meta.to_csv(meta_csv)

# ---- unit checks on the transform ----
assert _looks_like_beta(beta_df), "should detect a β matrix"
assert not _looks_like_beta(pd.DataFrame(np.random.randint(0, 5000, (10, 4)))), "raw counts != β"
m = _beta_to_mvalue(beta_df.iloc[:3])
assert m.shape == (3, 8) and np.isfinite(m.values).all(), "M-values finite"
# β=0.2 -> M<0 ; β=0.75 -> M>0
assert _beta_to_mvalue(pd.DataFrame({"s": [0.2]})).iloc[0, 0] < 0 < _beta_to_mvalue(pd.DataFrame({"s": [0.75]})).iloc[0, 0]
# percent input (0..100) auto-scaled
assert abs(_beta_to_mvalue(pd.DataFrame({"s": [50.0]})).iloc[0, 0]) < 0.1, "50% ≈ β0.5 -> M≈0"
print("[1] β-detection + β→M-value transform (incl. percent auto-scale, sign)  OK")

# ---- end-to-end: run_methylation_da recovers the planted DMCs ----
msg = run_methylation_da.invoke({
    "beta_matrix_csv": beta_csv, "metadata_csv": meta_csv, "design_column": "group",
    "control_group": "control", "treatment_group": "exercise", "output_dir": OUT,
})
assert os.path.isfile(os.path.join(OUT, "synthetic_beta_mvalues.csv")), "M-value matrix written"
deg = pd.read_csv(os.path.join(OUT, "DEG_results_exercise_vs_control.csv"), index_col=0)
sig = set(deg.index[(deg["padj"] < 0.05)])
planted = set(sites[:N_DMC])
recovered = len(planted & sig)
false_pos = len(sig - planted)
print(f"[2] end-to-end: {recovered}/{N_DMC} planted DMCs recovered (padj<0.05); "
      f"{false_pos} false positives of {N_SITES - N_DMC} null sites")
assert recovered >= int(0.9 * N_DMC), f"expected >=90% recovery, got {recovered}/{N_DMC}"
assert false_pos <= int(0.02 * (N_SITES - N_DMC)), f"too many false positives: {false_pos}"
# direction: planted are hyper-methylated in treatment -> positive ΔM (log2FoldChange > 0)
planted_lfc = deg.loc[list(planted), "log2FoldChange"]
assert (planted_lfc > 0).mean() > 0.95, "planted DMCs should be hyper-methylated (ΔM > 0) in treatment"
print(f"[3] direction: {(planted_lfc > 0).mean()*100:.0f}% of planted DMCs hyper-methylated (ΔM>0) as designed")

print("\nPASS — run_methylation_da: β→M-value transform correct, limma recovers planted "
      "differential methylation with the right direction and low false-positive rate. "
      "DNA-methylation grid cell (P1) now covered by reusing the limma backend.")
