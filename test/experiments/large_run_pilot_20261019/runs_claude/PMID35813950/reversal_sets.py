"""Post-hoc reversal sets (paper S3.3.p1 / FIG3A,D): genes with p < 0.05 in both
MPTP vs SAL and EX vs MPTP with opposite direction, per region, from the
runner's limma tables. Paper rule: raw p < 0.05, no fold-change cutoff.
Usage: python reversal_sets.py <run_dir>
"""
import sys
from pathlib import Path

import pandas as pd

run = Path(sys.argv[1])
res = run / "GSE205907" / "results"
rows, genes = [], []
for t in ["Cereb", "Cortex", "Nigra", "Stria"]:
    pd_ = pd.read_csv(res / f"limma_{t}" / f"DEG_results_grp_MPTP_vs_SAL_tissue-{t}.csv", index_col=0)
    ex = pd.read_csv(res / f"limma_{t}" / f"DEG_results_grp_EX_vs_MPTP_tissue-{t}.csv", index_col=0)
    j = pd_[["log2FoldChange", "pvalue"]].join(ex[["log2FoldChange", "pvalue"]], lsuffix="_pd", rsuffix="_ex", how="inner")
    sig = (j.pvalue_pd < 0.05) & (j.pvalue_ex < 0.05)
    down_after_ex = j[sig & (j.log2FoldChange_pd > 0) & (j.log2FoldChange_ex < 0)]
    up_after_ex = j[sig & (j.log2FoldChange_pd < 0) & (j.log2FoldChange_ex > 0)]
    same_dir = j[sig & (j.log2FoldChange_pd * j.log2FoldChange_ex > 0)]
    rows.append({"region": t, "tested": len(j), "sig_both": int(sig.sum()),
                 "reversal_down_after_ex": len(down_after_ex), "reversal_up_after_ex": len(up_after_ex),
                 "same_direction": len(same_dir)})
    for name, df in [("down_after_ex", down_after_ex), ("up_after_ex", up_after_ex)]:
        genes.append(df.assign(region=t, set=name))
summary = pd.DataFrame(rows)
summary.to_csv(run / "reversal_sets_summary.csv", index=False)
pd.concat(genes).to_csv(run / "reversal_sets.csv")
print(summary.to_string(index=False))
