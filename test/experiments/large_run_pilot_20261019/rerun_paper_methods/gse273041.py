"""GSE273041 (PMID40069235): per-gene mixed-effects ANOVA on log2 RPKM, diet x time with a random
intercept per athlete, Type I ANOVA, Tukey post-hoc within diet, BH FDR < 0.05 and |log2FC| > 1.

Paper: HC H2 222, LC H0 161, LC H2 193, shared H0 198, shared H2 100; "330 HC only" (time point
unclear). The deposited 'raw_counts' file holds RPKM already floored by the authors (all > 0).
"""

import os

from common import RUNS, count, out_dir, record

import numpy as np
import pandas as pd

from tools.r_de_tools import run_r_log_de

RUN = RUNS / "PMID40069235/case_01/aligned"
meta = pd.read_csv(RUN / "design_metadata.csv", index_col=0)[["diet", "time", "subject"]]
rpkm = pd.read_csv(RUN / "aligned_matrix.csv", index_col=0)[meta.index]
assert (rpkm > 0).all().all(), "RPKM has zeros; log2 needs the authors' floor"
work = out_dir("GSE273041", "inputs")
np.log2(rpkm).to_csv(work / "log2_rpkm.csv")
meta.to_csv(work / "meta.csv")
contrasts = [{"name": f"{d}_{t}_vs_BL", "emmeans_label": f"{t} - BL", "by": d} for d in ("HC", "LC") for t in ("H0", "H2")]
res = run_r_log_de(str(work / "log2_rpkm.csv"), str(work / "meta.csv"), str(out_dir("GSE273041", "mixed_anova")),
                   engine="mixed_anova", design="~ diet * time", random="subject", emmeans_specs="~ time | diet",
                   anova_term="time", levels={"diet": ["HC", "LC"], "time": ["BL", "H0", "H2"]},
                   contrasts=contrasts, n_cores=int(os.environ.get("N_CORES", "10")), label="mixed_anova")
RULE = {"metric": "padj", "cutoff": 0.05, "effect_cutoff": 1.0}
sig = {}
out = {"paper": {"HC_H2_vs_BL": 222, "LC_H0_vs_BL": 161, "LC_H2_vs_BL": 193, "shared_H0": 198, "shared_H2": 100,
                 "HC_only_unclear_timepoint": 330},
       "formula": res["formula"], "rule": RULE}
for r in res["results"]:
    out[r["name"]] = count(r["path"], **RULE)
    t = pd.read_csv(r["path"], index_col=0)
    sig[r["name"]] = set(t.index[(t.padj < 0.05) & (t.log2FoldChange.abs() > 1)])
for tp in ("H0", "H2"):
    hc, lc = sig[f"HC_{tp}_vs_BL"], sig[f"LC_{tp}_vs_BL"]
    out[f"overlap_{tp}"] = {"shared": len(hc & lc), "HC_only": len(hc - lc), "LC_only": len(lc - hc)}
record("GSE273041", out)
