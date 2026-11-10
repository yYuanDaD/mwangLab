"""Execution: joint DESeq2 ~ grp on all 14 samples (paper-aligned), plus exploratory
~ sex + grp sensitivity and female-only fit. Counts genes and RE separately."""
import sys, pathlib; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import pandas as pd
from tools import native
from tools.suitability import enumerate_comparisons

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID33257951"
run = native.RunRecorder.open(RUN)
case = run.case("PMID33257951")
D = case.dir
MAT = str(D / "aligned" / "aligned_matrix.csv")
META = str(D / "aligned" / "design_metadata.csv")
rep = json.loads((D / "suitability" / "suitability.json").read_text(encoding="utf-8"))
comps = rep["comparisons"]
NAMES = {"grp_O_vs_Y": "O_vs_Y", "grp_OEX_vs_Y": "OEX_vs_Y", "grp_OEX_vs_O": "OEX_vs_O"}
ROLE = {"O_vs_Y": "paper_planned", "OEX_vs_Y": "paper_planned", "OEX_vs_O": "exploratory"}


def split_and_count(path, label):
    res = pd.read_csv(path, index_col=0)
    is_re = res.index.astype(str).str.contains(":")
    out = {}
    for part, mask in (("all", slice(None)), ("genes", ~is_re), ("RE", is_re)):
        p = pathlib.Path(path).with_name(pathlib.Path(path).stem + f"__{part}.csv")
        res.loc[mask].to_csv(p)
        c = native.apply_threshold(p, metric="padj", cutoff=0.1)
        a = native.apply_threshold(p, metric="padj", cutoff=0.05)
        out[part] = {"paper_FDR0.1": {k: c[k] for k in ("n_tested", "n_significant", "n_up", "n_down", "deg_sanity")},
                     "audit_padj0.05": {k: a[k] for k in ("n_significant", "n_up", "n_down")},
                     "median_log2FC": float(res.loc[mask, "log2FoldChange"].median())}
    return out


def run_unit(tag, meta_csv, comparisons, covariates=()):
    outdir = str(D / "results" / tag)
    try:
        r = native.call_tool("tools.joint_contrasts:run_joint_deseq2", counts_csv=MAT, metadata_csv=meta_csv,
                             comparisons=comparisons, output_dir=outdir, covariates=tuple(covariates), alpha=0.1)
    except native.NativeToolError as e:
        return {"error": str(e)}
    counts = {}
    for item in r["results"]:
        nm = NAMES.get(item["name"].split("__")[0], item["name"])
        case.add_output(item["path"], f"deg_table_{tag}_{nm}")
        counts[nm] = split_and_count(item["path"], nm)
        counts[nm]["path"] = item["path"]
    return {"formula": r["formula"], "n_samples": r["n_samples"], "n_features": r["n_genes"],
            "cells": r["cells"], "skipped": r["skipped"], "counts": counts}


units = {}
# 1. paper-aligned
units["paper_grp"] = run_unit("joint_grp", META, comps)
# 2. exploratory sex-adjusted sensitivity
units["sens_sex_grp"] = run_unit("joint_sex_grp", META, comps, covariates=("sex",))
# 3. exploratory female-only
dm = pd.read_csv(META, index_col=0)
fem = dm[dm.sex == "Female"]
fem_csv = D / "aligned" / "design_metadata_female.csv"
fem.to_csv(fem_csv)
case.add_output(fem_csv, "design_metadata_female")
fcomps = enumerate_comparisons(fem, ["grp"], references={"grp": "Y"})
units["female_grp"] = run_unit("female_grp", str(fem_csv), fcomps)
units["female_grp"]["group_n"] = fem.grp.value_counts().to_dict()

# reproduction check: are O-vs-Y genes 'largely reversed' in OEX?
u = units["paper_grp"]["counts"]
oy = pd.read_csv(u["O_vs_Y"]["path"], index_col=0)
ey = pd.read_csv(u["OEX_vs_Y"]["path"], index_col=0).reindex(oy.index)
eo = pd.read_csv(u["OEX_vs_O"]["path"], index_col=0).reindex(oy.index)
sig = oy.padj < 0.1
genes = ~oy.index.astype(str).str.contains(":")
rev = {}
for part, m in (("genes", genes), ("RE", ~genes)):
    s = sig & m
    rev[part] = {"n_O_vs_Y_sig": int(s.sum()),
                 "also_sig_OEX_vs_Y_same_dir": int((s & (ey.padj < 0.1) & (ey.log2FoldChange * oy.log2FoldChange > 0)).sum()),
                 "OEX_vs_O_opposite_dir_fraction": float(((eo.log2FoldChange * oy.log2FoldChange) < 0)[s].mean()) if s.sum() else None,
                 "median_ratio_lfc_OEXvsY_over_OvsY": float((ey.log2FoldChange / oy.log2FoldChange)[s].median()) if s.sum() else None}
units["attenuation_check"] = rev
case.write_json("execution_summary.json", units, role="execution_summary")
print(json.dumps({k: (v if k == "attenuation_check" else {kk: vv for kk, vv in v.items() if kk != "cells"}) for k, v in units.items()}, indent=1, default=str))
