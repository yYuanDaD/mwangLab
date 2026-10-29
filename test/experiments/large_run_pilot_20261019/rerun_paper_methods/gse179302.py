"""GSE179302 (PMID36468768-era RA cohort): DESeq2 ~ sex + age + race + ethnicity + 1 sva SV,
most vs least active tertile, IHW padj < 0.1. Paper: 767 DEGs.

IHW cannot be installed in this R (needs Rtools to compile lpsymphony), so padj is BH; IHW
usually calls somewhat more genes than BH at the same level. Gene filter: the large run's
30%-per-group rule without ERCC rows (19,260 genes in the paper).
"""

from common import RUNS, count, out_dir, record

import pandas as pd

from tools.r_de_tools import run_r_de

RUN = RUNS / "2f2aeb1cc53680f371f7452796ed7c9168968c09/GSE179302/aligned"
meta = pd.read_csv(RUN / "design_metadata.csv", index_col=0)[["tert", "sex", "age", "race", "hisp"]]
counts = pd.read_csv(RUN / "counts_filtered_paper30pct_noERCC.csv", index_col=0)
meta = meta.loc[[s for s in meta.index if s in counts.columns]]
work = out_dir("GSE179302", "inputs")
counts[meta.index].to_csv(work / "counts.csv")
meta.to_csv(work / "meta.csv")
RULE = {"metric": "padj", "cutoff": 0.1}
con = [{"name": "active_vs_inactive", "factor": "tert", "test": "active", "ref": "inactive"}]
levels = {"tert": ["inactive", "intermediate", "active"]}
out = {"paper": 767, "n_genes": len(counts), "rule": RULE, "adjustment": "BH (IHW unavailable)",
       "tertile_n": meta.tert.value_counts().to_dict()}
variants = {
    "all35_sv1_sex_age_race_hisp": dict(design="~ sex + age + race + hisp + tert", n_sv=1),
    "all35_sv1_sex_age_race": dict(design="~ sex + age + race + tert", n_sv=1),
    "two_arm_sv1_sex_age_race": dict(design="~ sex + age + race + tert", n_sv=1,
                                     subset={"tert": ["active", "inactive"]}),
    "all35_sv1_no_race": dict(design="~ sex + age + tert", n_sv=1),
}
for name, kw in variants.items():
    try:
        res = run_r_de(str(work / "counts.csv"), str(work / "meta.csv"), str(out_dir("GSE179302", name)),
                       engine="deseq2", contrasts=con, levels=levels, numeric=["age"], label=name, **kw)
        out[name] = {"formula": res["formula"], "n_samples": res["n_samples"],
                     **count(res["results"][0]["path"], **RULE),
                     "padj<0.05": count(res["results"][0]["path"], metric="padj", cutoff=0.05)["n_significant"]}
    except Exception as exc:
        out[name] = {"error": str(exc)[:400]}
record("GSE179302", out)
