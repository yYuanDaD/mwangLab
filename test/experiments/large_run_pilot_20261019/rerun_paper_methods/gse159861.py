"""GSE159861 (PMID35025912): limma-voom with RIN covariate, hindlimb unloading (HI) vs control
within each muscle and rat line; FDR < 0.05 and |logFC| > 1.

One model on all 48 samples, ~ 0 + grp + rin, after the filter that reproduces the paper's
14,789 genes (median CPM >= 0.5). Paper: PLN LRT 744, PLN HRT 251, SOL LRT 294, SOL HRT 326.
"""

from common import RUNS, count, out_dir, record

import pandas as pd

from tools.r_de_tools import run_r_de

RUN = RUNS / "PMID35025912/PMID35025912/aligned"
meta = pd.read_csv(RUN / "design_metadata.csv", index_col=0)[["grp", "rin", "line_c", "trt_c", "tis_c"]]
counts = pd.read_csv(RUN / "aligned_matrix.csv", index_col=0)[meta.index]
cpm = counts / counts.sum() * 1e6
counts = counts.loc[cpm.median(axis=1) >= 0.5]
work = out_dir("GSE159861", "inputs")
counts.to_csv(work / "counts_median_cpm05.csv")
meta.to_csv(work / "meta.csv")
PAPER = {"PLN_HIinLRT": 744, "PLN_HIinHRT": 251, "SOL_HIinLRT": 294, "SOL_HIinHRT": 326}
contrasts = [{"name": f"{tis}_HIin{line}", "expr": f"grp{tis}_{line}_HI - grp{tis}_{line}_CTRL"}
             for tis in ("PLN", "SOL") for line in ("LRT", "HRT")]
RULE = {"metric": "padj", "cutoff": 0.05, "effect_cutoff": 1.0}
out = {"paper": PAPER, "n_genes": len(counts), "rule": RULE}
for name, kw in {"voom_rin": dict(design="~ 0 + grp + rin", numeric=["rin"]),
                 "voom_rin_qualityweights": dict(design="~ 0 + grp + rin", numeric=["rin"], quality_weights=True),
                 "voom_no_rin": dict(design="~ 0 + grp")}.items():
    res = run_r_de(str(work / "counts_median_cpm05.csv"), str(work / "meta.csv"), str(out_dir("GSE159861", name)),
                   engine="voom", contrasts=contrasts, label=name, **kw)
    out[name] = {r["name"]: count(r["path"], **RULE) for r in res["results"]}
record("GSE159861", out)
