"""GSE140089 (PMID32625117): paired limma-voom, post vs pre resistance training in Parkinson's.

Paper: 706 DEGs at BH FDR < 0.05 (304 up / 402 down); gene filter not stated. The matrix
holds fractional featureCounts counts, which voom takes as they are.
"""

from common import RUNS, count, out_dir, record

import pandas as pd

from tools.r_de_tools import run_r_de

PAIRS = RUNS / "PMID32625117/PMID32625117/aligned/pd_pairs"
meta = pd.read_csv(PAIRS / "paired_metadata.csv", index_col=0)[["subject", "time"]]
counts = pd.read_csv(PAIRS / "paired_matrix.csv", index_col=0)[meta.index]
work = out_dir("GSE140089", "inputs")
meta.to_csv(work / "meta.csv")
RULE = {"metric": "padj", "cutoff": 0.05}
out = {"paper": {"n": 706, "up": 304, "down": 402}, "n_samples": len(meta), "n_pairs": meta.subject.nunique()}
filters = {"count10_in5": counts.loc[(counts >= 10).sum(axis=1) >= 5], "filterByExpr": counts}
for fname, c in filters.items():
    cpath = work / f"counts_{fname}.csv"
    c.to_csv(cpath)
    common = dict(levels={"time": ["pre", "post"]}, filter_by_expr=fname == "filterByExpr",
                  contrasts=[{"name": "post_vs_pre", "coef": "timepost"}])
    fixed = run_r_de(str(cpath), str(work / "meta.csv"), str(out_dir("GSE140089", f"fixed_{fname}")),
                     engine="voom", design="~ subject + time", label=f"fixed_{fname}", **common)
    block = run_r_de(str(cpath), str(work / "meta.csv"), str(out_dir("GSE140089", f"block_{fname}")),
                     engine="voom", design="~ time", block="subject", label=f"block_{fname}", **common)
    out[f"voom_subject_fixed_{fname}"] = count(fixed["results"][0]["path"], **RULE)
    out[f"voom_subject_block_{fname}"] = {**count(block["results"][0]["path"], **RULE),
                                          "consensus_correlation": block["report"].get("consensus_correlation")}
record("GSE140089", out)
