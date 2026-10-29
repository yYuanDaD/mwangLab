"""Synthetic checks for tools/r_de_tools.py: every R engine finds planted DE genes.

Needs R with DESeq2, edgeR, limma, sva, apeglm, lme4, lmerTest, emmeans and DESeq
(the original package; see scripts/install_deseq1.R). Skips cleanly without Rscript.
"""

import os
import sys
import tempfile

os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.getcwd())

import numpy as np
import pandas as pd

from tools.limma_voom_tools import _find_rscript
from tools.r_de_tools import run_r_de, run_r_log_de

N_DE = 40


def _counts(seed: int = 1, n_genes: int = 600):
    rng = np.random.default_rng(seed)
    subjects = [f"s{i}" for i in range(8)]
    rows = []
    for s_i, s in enumerate(subjects):
        for t in ("pre", "post"):
            rows.append({"sample": f"{s}_{t}", "subject": s, "time": t, "sex": "F" if s_i % 2 else "M",
                         "age": 40 + 3 * s_i, "batch": "b1" if s_i < 4 else "b2"})
    meta = pd.DataFrame(rows).set_index("sample")
    base = rng.gamma(2.0, 150.0, n_genes)
    subj_eff = {s: rng.normal(0, 0.3, n_genes) for s in subjects}
    batch_eff = rng.normal(0, 0.5, n_genes)
    lfc = np.zeros(n_genes)
    lfc[:N_DE] = np.where(np.arange(N_DE) % 2, 1.5, -1.5)
    cols = {}
    for sample, r in meta.iterrows():
        mu = base * np.exp(subj_eff[r.subject] + (batch_eff if r.batch == "b2" else 0)
                           + (np.log(2) * lfc if r.time == "post" else 0))
        cols[sample] = rng.negative_binomial(10, 10 / (10 + mu))
    counts = pd.DataFrame(cols, index=[f"g{i}" for i in range(n_genes)])
    return counts, meta


def _recall(path: str, cutoff: float = 0.05) -> tuple[float, int]:
    t = pd.read_csv(path, index_col=0)
    sig = set(t.index[pd.to_numeric(t["padj"], errors="coerce") < cutoff])
    planted = {f"g{i}" for i in range(N_DE)}
    return len(sig & planted) / N_DE, len(sig - planted)


def main() -> int:
    if not _find_rscript():
        print("SKIP: Rscript not found")
        return 0
    counts, meta = _counts()
    work = tempfile.mkdtemp(prefix="test_r_de_")
    cpath, mpath = os.path.join(work, "counts.csv"), os.path.join(work, "meta.csv")
    counts.to_csv(cpath)
    meta.to_csv(mpath)
    lv = {"time": ["pre", "post"]}
    post = [{"name": "post_vs_pre", "factor": "time", "test": "post", "ref": "pre"}]
    runs = {
        "deseq2_wald_sva_apeglm": lambda o: run_r_de(cpath, mpath, o, engine="deseq2", design="~ time", levels=lv,
                                                     contrasts=post, n_sv=1, shrink="apeglm"),
        "deseq2_covariates": lambda o: run_r_de(cpath, mpath, o, engine="deseq2", design="~ sex + age + time",
                                                levels=lv, numeric=["age"], contrasts=post),
        "deseq2_lrt": lambda o: run_r_de(cpath, mpath, o, engine="deseq2", design="~ subject + time",
                                         reduced="~ subject", levels=lv),
        "edger_ql_paired": lambda o: run_r_de(cpath, mpath, o, engine="edger_ql", design="~ subject + time",
                                              levels=lv, contrasts=[{"name": "post_vs_pre", "coef": "timepost"}]),
        "voom_block": lambda o: run_r_de(cpath, mpath, o, engine="voom", design="~ time", block="subject",
                                         levels=lv, contrasts=[{"name": "post_vs_pre", "coef": "timepost"}]),
        "voom_covariate": lambda o: run_r_de(cpath, mpath, o, engine="voom", design="~ subject + age + time",
                                             numeric=["age"], levels=lv,
                                             contrasts=[{"name": "post_vs_pre", "coef": "timepost"}]),
        "deseq1": lambda o: run_r_de(cpath, mpath, o, engine="deseq1", design="~ time", condition="time",
                                     contrasts=[{"name": "post_vs_pre", "test": "post", "ref": "pre"}]),
    }
    log = np.log2(counts / counts.sum() * 1e6 + 1)
    lpath = os.path.join(work, "log.csv")
    log.iloc[:150].to_csv(lpath)
    runs["mixed_anova"] = lambda o: run_r_log_de(
        lpath, mpath, o, engine="mixed_anova", design="~ batch * time", random="subject",
        emmeans_specs="~ time | batch", levels=lv, n_cores=2, anova_term="time",
        contrasts=[{"name": "b1_post_vs_pre", "emmeans_label": "post - pre", "by": "b1"},
                   {"name": "b2_post_vs_pre", "emmeans_label": "post - pre", "by": "b2"}])
    failed = 0
    for name, fn in runs.items():
        out = os.path.join(work, name)
        try:
            res = fn(out)
        except Exception as exc:  # report every engine before failing
            print(f"FAIL {name}: {type(exc).__name__}: {str(exc)[:600]}")
            failed += 1
            continue
        for r in res["results"]:
            recall, false_pos = _recall(r["path"], cutoff=0.1 if name == "mixed_anova" else 0.05)
            ok = recall >= (0.3 if name == "mixed_anova" else 0.6) and false_pos <= 15
            failed += not ok
            print(f"{'ok  ' if ok else 'FAIL'} {name}/{r['name']}: recall {recall:.2f}, false positives "
                  f"{false_pos}  [{res['method']}; {res['formula']}]")
        if name == "deseq2_wald_sva_apeglm":
            t = pd.read_csv(res["results"][0]["path"], index_col=0)
            shrunk = (t["log2FoldChange"].abs() <= t["log2FoldChange_mle"].abs() + 1e-9).mean()
            ok = "log2FoldChange_mle" in t and shrunk > 0.95 and res["report"].get("surrogate_variables")
            failed += not ok
            print(f"{'ok  ' if ok else 'FAIL'} apeglm shrinks toward 0 in {shrunk:.0%} of genes; SV estimated")
    print("FAILED" if failed else "ALL PASSED", f"({failed} failures)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
