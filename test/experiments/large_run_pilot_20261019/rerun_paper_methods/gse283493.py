"""GSE283493 (PMID39832562): DESeq2 + 2 sva SVs + apeglm, padj < 0.1 and |shrunken LFC| > 0.5;
interaction by LRT (SVs + tissue + phase + training + phase:training vs no interaction).

Same 44 libraries and gene filter as the large run (4 paper outliers removed; >= 10 reads in
>= 6 libraries). Paper: SAT_EA 7, SAT_LA 353, VAT_EA 2, VAT_LA 14; LRT 632.
"""

from common import RUNS, count, out_dir, record

import pandas as pd

from tools.r_de_tools import run_r_de

RUN = RUNS / "PMID39832562"
PAPER = {"sat_ea": 7, "sat_la": 353, "vat_ea": 2, "vat_la": 14, "LRT": 632}
OUTLIERS = ["SAT_PM_Exp_d", "SAT_PM_Exp_f", "VAT_AM_Cont_e", "VAT_AM_Exp_c"]
RULE = {"metric": "padj", "cutoff": 0.1, "effect_cutoff": 0.5}

meta = pd.read_csv(RUN / "interaction_lrt/aligned/design_metadata.csv", index_col=0)
meta = meta[~meta.library.isin(OUTLIERS)][["tissue", "phase", "training", "grp"]]
meta["cell"] = meta.tissue + "_" + meta.grp
counts = pd.read_csv(RUN / "interaction_lrt/aligned/aligned_matrix.csv", index_col=0)[meta.index]
counts = counts.loc[(counts >= 10).sum(axis=1) >= 6]
work = out_dir("GSE283493", "inputs")
counts.to_csv(work / "counts_44_filtered.csv")
meta.to_csv(work / "meta_44.csv")
levels = {"training": ["ctrl", "ex"], "phase": ["EA", "LA"], "tissue": ["SAT", "VAT"]}
out = {"n_libraries": len(meta), "n_genes": len(counts), "paper": PAPER, "rule": RULE}

# per arm: SVs estimated within the arm, ~ SV1 + SV2 + training
per_arm = {}
for arm, (tissue, phase) in {"sat_ea": ("SAT", "EA"), "sat_la": ("SAT", "LA"),
                             "vat_ea": ("VAT", "EA"), "vat_la": ("VAT", "LA")}.items():
    res = run_r_de(str(work / "counts_44_filtered.csv"), str(work / "meta_44.csv"),
                   str(out_dir("GSE283493", f"per_arm_{arm}")), engine="deseq2", design="~ training",
                   levels=levels, n_sv=2, shrink="apeglm", subset={"tissue": [tissue], "phase": [phase]},
                   contrasts=[{"name": arm, "factor": "training", "test": "ex", "ref": "ctrl"}], label=arm)
    path = res["results"][0]["path"]
    per_arm[arm] = {"formula": res["formula"], "n_samples": res["n_samples"], **count(path, **RULE),
                    "unshrunk": count(path, effect_column="log2FoldChange_mle", **RULE)}
out["per_arm_sv2_apeglm"] = per_arm

# one model on all 44: ~ SV1 + SV2 + cell, SVs protected against tissue x phase x training
cells = [{"name": arm, "factor": "cell", "test": f"{t}_{p}E", "ref": f"{t}_{p}C"}
         for arm, (t, p) in {"sat_ea": ("SAT", "EA"), "sat_la": ("SAT", "LA"),
                             "vat_ea": ("VAT", "EA"), "vat_la": ("VAT", "LA")}.items()]
res = run_r_de(str(work / "counts_44_filtered.csv"), str(work / "meta_44.csv"), str(out_dir("GSE283493", "joint")),
               engine="deseq2", design="~ cell", n_sv=2, shrink="apeglm", contrasts=cells, label="joint")
out["joint_sv2_apeglm"] = {r["name"]: {**count(r["path"], **RULE),
                                       "unshrunk": count(r["path"], effect_column="log2FoldChange_mle", **RULE)}
                           for r in res["results"]}
out["joint_formula"] = res["formula"]

# interaction LRT, as the paper wrote it
res = run_r_de(str(work / "counts_44_filtered.csv"), str(work / "meta_44.csv"), str(out_dir("GSE283493", "lrt")),
               engine="deseq2", design="~ tissue + phase + training + phase:training",
               reduced="~ tissue + phase + training", n_sv=2, sv_null="~ tissue + phase", levels=levels,
               lrt_name="phase_x_training_LRT", label="lrt")
path = res["results"][0]["path"]
out["lrt_sv2"] = {"formula": res["formula"], "reduced": res["report"].get("reduced"),
                  "padj<0.1": count(path, metric="padj", cutoff=0.1),
                  "padj<0.05": count(path, metric="padj", cutoff=0.05)}
record("GSE283493", out)
