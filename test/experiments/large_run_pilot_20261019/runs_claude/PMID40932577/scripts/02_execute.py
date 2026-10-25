"""Execution gate: one joint DESeq2 fit, five contrasts, paper threshold."""
import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os, json
ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())
os.chdir(ROOT)
from tools import native
native.enable_native_mode()
REL = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40932577"
run = native.RunRecorder.open(REL)
case = run.case("GSE301564")
plan = json.loads((case.dir / "reproduction_plan.json").read_text(encoding="utf-8"))
PT = plan["threshold"]
am = case.evidence_item("tool_output:aligned_matrix.csv")
dm = case.evidence_item("tool_output:design_metadata.csv")
out = case.dir / "results" / "joint_deseq2"
results = {}
try:
    res = native.call_tool("tools.joint_contrasts:run_joint_deseq2", counts_csv=plan["counts_csv"],
                           metadata_csv=plan["metadata_csv"], comparisons=plan["comparisons"],
                           output_dir=str(out), alpha=plan["alpha"])
    (out / "joint_fit.json").write_text(json.dumps(res, indent=2, default=str), encoding="utf-8")
    fit_item = case.add_output(out / "joint_fit.json", "joint_fit")
    for r in res["results"]:
        name = r["name"]
        th = native.apply_threshold(r["path"], metric="padj", cutoff=PT["cutoff"], effect_cutoff=None)
        item = case.add_output(r["path"], f"deg_table_{name}")
        results[name] = {"deg_csv": r["path"], "threshold": th, "role": plan["roles"][name], "label": plan["labels"][name]}
        case.decide("execution",
                    final={"method": "DESeq2 (pydeseq2 Wald), joint model", "subset": name, "role": plan["roles"][name],
                           "formula": res["formula"] + "  (cell = frail x run)", "contrast_kind": r["kind"],
                           "cells": r["cells"], "n_samples": res["n_samples"], "outputs": [r["path"]],
                           "n_tested": th["n_tested"], "n_deg": th["n_significant"], "n_up": th["n_up"],
                           "n_down": th["n_down"], "rule": th["rule"], "deg_sanity": th["deg_sanity"],
                           "paper_n_deg": "not_reported in main text"},
                    evidence=[am, dm, fit_item, item], paper={"locator": "S2.10.p1"}, confidence="high",
                    execution_status="completed",
                    reasoning=f"Contrast {name} extracted from one DESeq2 fit on all 15 samples; counted with apply_threshold under padj < 0.1.")
except native.NativeToolError as error:
    case.decide("execution", final={"method": "DESeq2 (pydeseq2 Wald), joint model", "execution_error": str(error)},
                evidence=[am, dm], paper={"locator": "S2.10.p1"}, confidence="high", execution_status="failed",
                reasoning="joint DESeq2 executor failed")
    results["error"] = str(error)
(case.dir / "execution_results.json").write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
for k, v in results.items():
    print(k, v if isinstance(v, str) else (v["role"], v["threshold"]["n_significant"], v["threshold"]["n_up"], v["threshold"]["n_down"], v["threshold"]["n_tested"]))
