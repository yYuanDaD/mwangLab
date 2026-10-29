"""GSE293221 (PMID41787055): the original R DESeq package (nbinomTest), exercise vs control and
PhAm extract vs control, padj < 0.05 and fold change > 1.5. Paper: EX 32, PhAm 176 (76 up / 100 down).

The paper first keeps genes with mean RPKM > 1 in at least one group. GEO has no gene lengths
(mm9 annotation version not stated), so this is run without the filter and with a CPM proxy
(mean CPM > 1 in at least one group, i.e. RPKM > 1 for a ~1 kb transcript); the proxy is not the
paper's filter. DESeq dispersion defaults (pooled, sharingMode maximum); one fit on all 9
samples and per-pair fits are both shown, since "group-pairwise" can mean either.
"""

from common import RUNS, count, out_dir, record

import pandas as pd

from tools.r_de_tools import run_r_de

RUN = RUNS / "PMID41787055/GSE293221/aligned"
meta = pd.read_csv(RUN / "design_metadata.csv", index_col=0)[["grp"]]
counts = pd.read_csv(RUN / "aligned_matrix.csv", index_col=0)[meta.index]
counts = counts[~counts.index.astype(str).str.startswith("__")]
work = out_dir("GSE293221", "inputs")
meta.to_csv(work / "meta.csv")
cpm = counts / counts.sum() * 1e6
group_means = cpm.T.groupby(meta.grp).mean().T
inputs = {"no_filter": counts, "cpm_proxy": counts.loc[(group_means > 1).any(axis=1)]}
RULE = {"metric": "padj", "cutoff": 0.05, "effect_cutoff": 0.5849625007211562}
contrasts = [{"name": "EX_vs_CON", "test": "EX", "ref": "CON"}, {"name": "PHAM_vs_CON", "test": "PHAM", "ref": "CON"}]
out = {"paper": {"EX_vs_CON": 32, "PHAM_vs_CON": {"n": 176, "up": 76, "down": 100}}, "rule": RULE}
for fname, c in inputs.items():
    cpath = work / f"counts_{fname}.csv"
    c.to_csv(cpath)
    for fit in ("all9", "pairwise"):
        name = f"deseq1_{fit}_{fname}"
        res = run_r_de(str(cpath), str(work / "meta.csv"), str(out_dir("GSE293221", name)), engine="deseq1",
                       design="~ grp", condition="grp", contrasts=contrasts, pairwise_fit=fit == "pairwise",
                       label=name)
        out[name] = {"n_genes": len(c), "dispersion": res["report"].get("dispersion"),
                     **{r["name"]: count(r["path"], **RULE) for r in res["results"]}}
record("GSE293221", out)
