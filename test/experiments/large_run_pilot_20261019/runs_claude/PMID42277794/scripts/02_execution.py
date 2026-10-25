"""Gate 9 (execution): joint DESeq2 on all 12 samples + labelled audits."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json, math
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID42277794"
CASE = "PMID42277794"
run = native.RunRecorder.open(RUN)
case = run.case(CASE)
cdir = case.dir
counts = str(cdir / "aligned" / "aligned_matrix.csv")
design = str(cdir / "aligned" / "design_metadata.csv")
comps = json.loads((cdir / "suitability" / "suitability.json").read_text(encoding="utf-8"))["comparisons"]
planned = {"ex_EXT_vs_SED_exo-ctrl": "A_ExTctrl_vs_SEDctrl", "ex_EXT_vs_SED_exo-exo": "B_ExTexo_vs_SEDexo",
           "exo_exo_vs_ctrl_ex-SED": "C_SEDexo_vs_SEDctrl"}
LFC = math.log2(1.5)
rule = dict(metric="padj", cutoff=0.05, effect_cutoff=LFC, inclusive=False)
summary = {}

# ---- primary: joint model, all 12 samples
out_dir = str(cdir / "results" / "joint_deseq2")
try:
    res = native.call_tool("tools.joint_contrasts:run_joint_deseq2", counts_csv=counts, metadata_csv=design,
                           comparisons=comps, output_dir=out_dir, alpha=0.05)
except native.NativeToolError as e:
    case.decide("execution", final={"method": "DESeq2 joint model ~ cell", "execution_error": str(e)},
                evidence=[{"id": "tool:run_joint_deseq2", "kind": "tool_output"}],
                reasoning="joint DESeq2 failed", confidence="high", execution_status="failed")
    raise
outputs, primary = [], {}
for r in res["results"]:
    item = case.add_output(r["path"], "deg_table")
    outputs.append(item)
    c = native.apply_threshold(r["path"], **rule)
    d = native.apply_threshold(r["path"], metric="padj", cutoff=0.05)
    t = pd.read_csv(r["path"], index_col=0)
    sig = (t.padj < 0.05) & (t.log2FoldChange.abs() > LFC)
    primary[r["name"]] = {"label": planned.get(r["name"], "exploratory"), "path": r["path"],
                          "n_deg_paper_rule": c["n_significant"], "n_up": int((sig & (t.log2FoldChange > 0)).sum()),
                          "n_down": int((sig & (t.log2FoldChange < 0)).sum()), "n_padj_0.05_noFC": d["n_significant"],
                          "n_tested": c.get("n_tested"), "deg_sanity": c["deg_sanity"],
                          "trem1_pathway_genes": t.reindex(["Trem1", "Tyrobp", "Il1b", "Tnf", "Il6", "Cxcl2", "Nlrp3", "Ccl2", "Tlr4", "Cd86"])[["log2FoldChange", "padj"]].round(4).to_dict("index")}
summary["primary_joint_all12"] = {"formula": res["formula"], "n_samples": res["n_samples"], "n_genes": res["n_genes"],
                                  "cells": res["cells"], "skipped": res["skipped"], "contrasts": primary}

# ---- audit 1: pairwise 6-sample DESeq2 per planned contrast
pair = {}
for name, lab in planned.items():
    comp = next(c for c in comps if c["name"] == name)
    t_cell, r_cell = comp["cells"][0]["cell"], comp["cells"][1]["cell"]
    tg, cg = f"{t_cell['ex']}_{t_cell['exo']}", f"{r_cell['ex']}_{r_cell['exo']}"
    od = str(cdir / "results" / "audit_pairwise" / lab)
    try:
        native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=counts, metadata_csv=design,
                         design_column="grp", control_group=cg, treatment_group=tg, output_dir=od, alpha=0.05)
        p = native.deg_outputs(od)[0]
        case.add_output(p, "audit_deg_table")
        pair[lab] = {"contrast": f"{tg} vs {cg}", "n_deg_paper_rule": native.apply_threshold(p, **rule)["n_significant"],
                     "n_padj_0.05_noFC": native.apply_threshold(p, metric="padj", cutoff=0.05)["n_significant"]}
    except native.NativeToolError as e:
        pair[lab] = {"execution_error": str(e)}
summary["audit_pairwise_6sample"] = pair

# ---- audit 2: joint model without GSM8187308 (FIG4A shows SED-control n=2)
dm = pd.read_csv(design, index_col=0)
d11 = cdir / "aligned" / "design_metadata_minus_GSM8187308.csv"
dm.drop(index="GSM8187308").to_csv(d11)
od = str(cdir / "results" / "audit_joint_minus_GSM8187308")
try:
    res2 = native.call_tool("tools.joint_contrasts:run_joint_deseq2", counts_csv=counts, metadata_csv=str(d11),
                            comparisons=comps, output_dir=od, alpha=0.05, include=[c["name"] for c in comps])
    a2 = {}
    for r in res2["results"]:
        case.add_output(r["path"], "audit_deg_table")
        a2[planned.get(r["name"], r["name"])] = {"n_deg_paper_rule": native.apply_threshold(r["path"], **rule)["n_significant"],
                                                 "n_padj_0.05_noFC": native.apply_threshold(r["path"], metric="padj", cutoff=0.05)["n_significant"]}
    summary["audit_joint_minus_GSM8187308"] = {"n_samples": res2["n_samples"], "contrasts": a2,
                                               "label": "audit: SED-control n=2 (QC outlier dropped) to approximate FIG4A; exploratory (cell n<3)"}
except native.NativeToolError as e:
    summary["audit_joint_minus_GSM8187308"] = {"execution_error": str(e)}

sj = case.write_json("results/execution_summary.json", summary, role="execution_summary")
print(json.dumps(summary, indent=1, default=str))
case.decide("execution",
            final={"method": "DESeq2 (pydeseq2) joint model ~ cell on all 12 samples", "formula": res["formula"],
                   "outputs": [o["path"] for o in outputs], "applied_threshold": "padj < 0.05 and |log2FC| > 0.5849625",
                   "n_deg": {v["label"] if v["label"] != "exploratory" else k: v["n_deg_paper_rule"] for k, v in primary.items()},
                   "audits": {"pairwise": pair, "minus_GSM8187308": summary["audit_joint_minus_GSM8187308"]}},
            evidence=outputs + [sj], reasoning="Joint DESeq2 completed for all 5 suitability comparisons; audits recorded separately.",
            confidence="high", execution_status="completed", paper={"locator": "S2.15.p1"})
