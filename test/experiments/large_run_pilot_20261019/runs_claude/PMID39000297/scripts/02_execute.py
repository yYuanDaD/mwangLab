"""Execution, audit refits, study record, finish for GSE232510."""
import sys, pathlib, json; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
from tools import native

native.enable_native_mode()
ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())
RUN = pathlib.Path(__file__).resolve().parents[1]
REL = str(RUN.relative_to(ROOT)).replace("\\", "/")
CID = "GSE232510"
run = native.RunRecorder.open(REL)
case = run.case(CID)
plan = json.loads((case.dir / "reproduction_plan.json").read_text(encoding="utf-8"))
comparisons = json.loads((case.dir / "comparisons.json").read_text(encoding="utf-8"))
PT = plan["threshold"]
PAPER = {"grp_HFS_vs_CS": {"total": 430, "up": 165, "down": 265}, "grp_HFR_vs_CS": {"total": 39, "up": 20, "down": 19},
         "grp_HFR_vs_HFS": None}
paper_item = case.evidence_item("paper:PMC11241292.paper.md")

res_dir = case.dir / "results" / "joint_deseq2"
summary = {"route": "declared_deviation", "threshold": PT, "contrasts": {}, "audit_two_group": {}}
try:
    out = native.call_tool("tools.joint_contrasts:run_joint_deseq2", counts_csv=plan["counts_csv"],
                           metadata_csv=plan["metadata_csv"], comparisons=comparisons, output_dir=str(res_dir), alpha=0.1)
except native.NativeToolError as error:
    case.decide("execution", final={"method": "DESeq2 joint ~ grp", "execution_error": str(error)},
                evidence=[paper_item], reasoning="joint DESeq2 failed", confidence="high", execution_status="failed")
    case.decide("study", final={"route": "declared_deviation"}, evidence=[paper_item], reasoning="planned route recorded", confidence="medium")
    case.finish(); run.finish(); raise
outputs, counts = [], {}
for r in out["results"]:
    item = case.add_output(r["path"], f"deg_table:{r['name']}")
    outputs.append({"name": r["name"], "path": r["path"]})
    c = native.apply_threshold(r["path"], metric="padj", cutoff=PT["cutoff"], effect_cutoff=PT["effect_cutoff"])
    a = native.apply_threshold(r["path"], metric="padj", cutoff=0.1)
    a05 = native.apply_threshold(r["path"], metric="padj", cutoff=0.05)
    counts[r["name"]] = c
    summary["contrasts"][r["name"]] = {"paper_rule": c, "audit_FDR_0.1_only": a, "audit_padj_0.05": a05, "paper_count": PAPER.get(r["name"])}
    print(r["name"], "paper rule:", c["n_significant"], f"(up {c['n_up']}, down {c['n_down']})",
          "| FDR<0.1 only:", a["n_significant"], "| padj<0.05:", a05["n_significant"], "| paper:", PAPER.get(r["name"]))
case.decide("execution", final={"method": "DESeq2 (pydeseq2) joint ~ grp, Wald contrasts, alpha 0.1", "formula": out["formula"],
            "n_samples": out["n_samples"], "n_genes_nonzero": out["n_genes"], "cells": out["cells"], "outputs": outputs,
            "n_deg_applied": {k: {"n": v["n_significant"], "up": v["n_up"], "down": v["n_down"], "rule": v["rule"], "deg_sanity": v["deg_sanity"]} for k, v in counts.items()}},
            evidence=[paper_item] + [case.evidence_item(f"tool_output:{pathlib.Path(o['path']).name}") for o in outputs],
            reasoning="Joint DESeq2 on the 10 deposited RW samples; counts from native.apply_threshold under the applied paper rule.",
            confidence="high", execution_status="completed")

# audit: strict pair-wise reading (two-group refits; executor's independent-filtering alpha is its default)
for name, ctrl, trt in (("HFS_vs_CS", "CS", "HFS"), ("HFR_vs_CS", "CS", "HFR")):
    d = case.dir / "results" / f"audit_two_group_{name}"
    try:
        native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=plan["counts_csv"], metadata_csv=plan["metadata_csv"],
                         design_column="grp", control_group=ctrl, treatment_group=trt, output_dir=str(d))
        deg = native.deg_outputs(d)[0]
        summary["audit_two_group"][name] = {"paper_rule": native.apply_threshold(deg, metric="padj", cutoff=PT["cutoff"], effect_cutoff=PT["effect_cutoff"]),
                                            "FDR_0.1_only": native.apply_threshold(deg, metric="padj", cutoff=0.1)}
        case.add_output(deg, f"audit_deg_table:{name}")
        print("audit", name, summary["audit_two_group"][name]["paper_rule"]["n_significant"], summary["audit_two_group"][name]["FDR_0.1_only"]["n_significant"])
    except native.NativeToolError as error:
        summary["audit_two_group"][name] = {"execution_error": str(error)}
        print("audit failed", name, error)

case.write_json("reproduction_summary.json", summary, role="reproduction_summary")

prim = counts["grp_HFR_vs_CS"]
case.decide("study", final={"route": "declared_deviation",
            "reason": "paper's DESeq2 route on the deposited subset (CR and one HFS library missing); CR_vs_CS blocked for missing samples",
            "contrast_routes": {"grp_HFS_vs_CS": "declared_deviation (paper planned)", "grp_HFR_vs_CS": "declared_deviation (paper planned)",
                                "grp_HFR_vs_HFS": "exploratory (not a paper gene-level test)", "CR_vs_CS": "blocked: CR not deposited"},
            "exploratory_reason": "grp_HFR_vs_HFS is not tested gene by gene in the paper; all cells n >= 3 and residual df 7, so no small-n flag"},
            evidence=[paper_item, case.evidence_item("tool_output:reproduction_summary.json")],
            reasoning="Planned contrasts ran on the paper's method with the paper's threshold; sample set reduced by the deposit.",
            confidence="medium")
case.finish(n_deg=prim["n_significant"], deg_sanity=prim["deg_sanity"])
print(run.finish())
