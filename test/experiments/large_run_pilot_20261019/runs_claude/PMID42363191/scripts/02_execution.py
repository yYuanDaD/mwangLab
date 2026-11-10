"""Execution: joint DESeq2 (~ cell) on all 16 samples; paper threshold; pairwise sensitivity audit."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json, math
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID42363191"
run = native.RunRecorder.open(RUN)
case = run.case("PMID42363191")
cdir = case.dir
st = json.loads((cdir / "plan_state.json").read_text(encoding="utf-8"))
planned = st["planned"]
rep = json.loads((cdir / "suitability" / "suitability.json").read_text(encoding="utf-8"))
comps = rep["comparisons"]
paper_label = {planned[0]: "T_vs_C", planned[1]: "TE_vs_T"}
reported = {"T_vs_C": {"n": 486, "up": 273, "down": 213}, "TE_vs_T": {"n": 270, "up": 165, "down": 105}}
EFF = math.log2(2.0)

out_dir = cdir / "results" / "joint_deseq2"
try:
    res = native.call_tool("tools.joint_contrasts:run_joint_deseq2", counts_csv=st["aligned_matrix"],
                           metadata_csv=st["design_csv"], comparisons=comps, output_dir=str(out_dir), alpha=0.05)
except native.NativeToolError as e:
    case.decide("execution", final={"method": "DESeq2 joint ~ cell", "execution_error": str(e)},
                evidence=[case.evidence_item("aligned_matrix:aligned_matrix.csv") if False else {"id": "run", "kind": "tool_output"}],
                reasoning="joint DESeq2 failed", confidence="high", execution_status="failed")
    raise
print(json.dumps({k: v for k, v in res.items() if k != "results"}, default=str))

counts, outputs, evid = {}, [], []
for r in res["results"]:
    it = case.add_output(r["path"], f"deg_{r['name']}")
    evid.append(it)
    paper_rule = native.apply_threshold(r["path"], metric="padj", cutoff=0.05, effect_cutoff=EFF)
    audit = native.apply_threshold(r["path"], metric="padj", cutoff=0.05, effect_cutoff=None)
    lab = paper_label.get(r["name"])
    counts[r["name"]] = {"paper_label": lab, "role": "planned" if lab else "exploratory",
                         "applied": paper_rule, "audit_padj_only": audit,
                         "paper_reported": reported.get(lab)}
    outputs.append({"contrast": r["name"], "paper_label": lab, "path": r["path"], "sha256": it.get("sha256"),
                    "n_deg_applied": paper_rule["n_significant"]})
    print(r["name"], lab, "applied:", {k: paper_rule[k] for k in paper_rule if k.startswith("n_")},
          "audit:", audit["n_significant"], "sanity:", paper_rule.get("deg_sanity"))

# Sensitivity audit: pairwise two-group DESeq2 fits for the planned contrasts (vendor-style subset fits).
pair_specs = {"T_vs_C": ("C", "T"), "TE_vs_T": ("T", "TE")}
pairwise = {}
for lab, (ctrl, trt) in pair_specs.items():
    od = cdir / "results" / "pairwise_audit" / lab
    dm = pd.read_csv(st["design_csv"], index_col=0)
    keep = dm.index[dm["grp"].isin([ctrl, trt])]
    sub_meta = od / "meta.csv"; sub_mat = od / "counts.csv"
    od.mkdir(parents=True, exist_ok=True)
    dm.loc[keep].to_csv(sub_meta)
    pd.read_csv(st["aligned_matrix"], index_col=0)[list(keep)].to_csv(sub_mat)
    try:
        native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=str(sub_mat), metadata_csv=str(sub_meta),
                         design_column="grp", control_group=ctrl, treatment_group=trt, output_dir=str(od), alpha=0.05)
        f = native.deg_outputs(od)[0]
        case.add_output(f, f"audit_pairwise_{lab}")
        pairwise[lab] = {"path": str(f), "applied": native.apply_threshold(f, metric="padj", cutoff=0.05, effect_cutoff=EFF),
                         "audit_padj_only": native.apply_threshold(f, metric="padj", cutoff=0.05)["n_significant"]}
    except native.NativeToolError as e:
        pairwise[lab] = {"error": str(e)}
    print("PAIRWISE", lab, json.dumps(pairwise[lab], default=str)[:400])

cnt = case.write_json("results/deg_counts.json", {"joint": counts, "pairwise_audit": pairwise}, role="deg_counts")
case.decide("execution",
            final={"method": "DESeq2 (pydeseq2) joint model ~ cell, Wald contrasts", "formula": res["formula"],
                   "n_samples": res["n_samples"], "n_genes_nonzero": res["n_genes"], "cells": res["cells"],
                   "outputs": outputs, "skipped": res["skipped"],
                   "applied_threshold": "padj < 0.05 and |log2FC| > 1 (paper S2.7.p2)",
                   "deg_counts": {k: {"n": v["applied"]["n_significant"], "up": v["applied"].get("n_up"),
                                      "down": v["applied"].get("n_down"), "paper": v["paper_reported"],
                                      "audit_padj_only": v["audit_padj_only"]["n_significant"]} for k, v in counts.items()},
                   "pairwise_audit": {k: ({"n": v["applied"]["n_significant"], "up": v["applied"].get("n_up"),
                                           "down": v["applied"].get("n_down")} if "applied" in v else v) for k, v in pairwise.items()}},
            evidence=evid + [cnt], paper={"locator": "S2.7.p2; S3.3.p3"},
            reasoning="Joint DESeq2 ran on all 16 samples; counts under the paper rule plus padj-only and pairwise-fit audits.",
            confidence="high", execution_status="completed")
