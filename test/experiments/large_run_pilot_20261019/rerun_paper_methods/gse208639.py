"""GSE208639 (PMID37318869): edgeR QL F-test with TMM, grouped DM1 pre-training vs controls.

Paper rule P < 0.05 and |logFC| > 2. The authors deposited their own edgeR table for this
contrast (176 genes under the rule, 18,762 genes tested), so we compare gene by gene.
"""

from common import ROOT, RUNS, count, out_dir, record

import pandas as pd

from tools.r_de_tools import run_r_de

RUN = RUNS / "PMID37318869" / "case_02"
RULE = {"metric": "pvalue", "cutoff": 0.05, "effect_cutoff": 2.0}
auth = pd.read_csv(ROOT / "data/GSE208639/GSE208639_edgeR_output.csv").set_index("Ensembl ID")
auth = auth[~auth.index.duplicated()]
auth_sig = set(auth.index[(auth.PValue < 0.05) & (auth.logFC.abs() > 2)])

meta = pd.read_csv(RUN / "aligned/design_metadata.csv", index_col=0)[["grp", "subject"]]
counts = pd.read_csv(RUN / "aligned/aligned_matrix.csv", index_col=0)[meta.index]
work = out_dir("GSE208639", "inputs")
meta.to_csv(work / "meta.csv")
out = {"paper_pre_vs_ctrl": len(auth_sig), "authors_genes_tested": len(auth), "rule": RULE}


def compare(path: str) -> dict:
    t = pd.read_csv(path, index_col=0)
    sig = set(t.index[(t.pvalue < 0.05) & (t.log2FoldChange.abs() > 2)])
    common = t.index.intersection(auth.index)
    return {"ours": len(sig), "authors": len(auth_sig), "shared": len(sig & auth_sig),
            "genes_tested": len(t), "logFC_r": round(float(t.loc[common, "log2FoldChange"].corr(auth.loc[common, "logFC"])), 4),
            "pvalue_rank_r": round(float(t.loc[common, "pvalue"].rank().corr(auth.loc[common, "PValue"].rank())), 4)}


for filt in ("any10", "filterByExpr"):
    for arm in ("pre", "post"):
        sub = meta[meta.grp.isin(["ctrl", arm])]
        c = counts[sub.index]
        if filt == "any10":  # the large run's filter: >= 10 counts in at least one sample of the fit
            c = c.loc[(c >= 10).any(axis=1)]
        cpath = work / f"counts_{arm}_{filt}.csv"
        c.to_csv(cpath)
        res = run_r_de(str(cpath), str(work / "meta.csv"), str(out_dir("GSE208639", f"{arm}_{filt}")),
                       engine="edger_ql", design="~ grp", levels={"grp": ["ctrl", arm]},
                       subset={"grp": ["ctrl", arm]}, filter_by_expr=filt == "filterByExpr",
                       contrasts=[{"name": f"{arm}_vs_ctrl", "coef": f"grp{arm}"}], label=f"{arm}_{filt}")
        path = res["results"][0]["path"]
        out[f"{arm}_vs_ctrl_{filt}"] = {**count(path, **RULE), **(compare(path) if arm == "pre" else {})}

# one model on all 24 samples (controls, pre, post), TMM, filterByExpr
c = counts.copy()
c.to_csv(work / "counts_all.csv")
res = run_r_de(str(work / "counts_all.csv"), str(work / "meta.csv"), str(out_dir("GSE208639", "joint3")),
               engine="edger_ql", design="~ grp", levels={"grp": ["ctrl", "pre", "post"]}, filter_by_expr=True,
               contrasts=[{"name": "pre_vs_ctrl", "coef": "grppre"}, {"name": "post_vs_ctrl", "coef": "grppost"}],
               label="joint3")
for r in res["results"]:
    out[f"joint3_{r['name']}"] = {**count(r["path"], **RULE), **(compare(r["path"]) if r["name"] == "pre_vs_ctrl" else {})}
record("GSE208639", out)
