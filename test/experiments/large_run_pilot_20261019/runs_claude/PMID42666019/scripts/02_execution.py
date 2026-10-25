"""Gate 9 (execution): joint DESeq2 ~ grp on all 9 samples, three Wald contrasts."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID42666019"
CASE = "PMID42666019"
run = native.RunRecorder.open(RUN)
case = run.case(CASE)
ALIGNED = str(case.dir / "aligned" / "aligned_matrix.csv")
DESIGN = str(case.dir / "aligned" / "design_metadata.csv")
comps = json.loads((case.dir / "comparisons.json").read_text(encoding="utf-8"))
OUT = case.dir / "results" / "deseq2_joint"
ROLE = {"grp_CE_vs_SED": "planned", "grp_EE_vs_CE": "planned", "grp_EE_vs_SED": "exploratory"}
al_mat = case.evidence_item("artifact:" + ALIGNED) if False else case.add_output(ALIGNED, "aligned_matrix")
al_meta = case.add_output(DESIGN, "design_metadata")

try:
    res = native.call_tool("tools.joint_contrasts:run_joint_deseq2", counts_csv=ALIGNED, metadata_csv=DESIGN,
                           comparisons=comps, output_dir=str(OUT), alpha=0.05, n_cpus=4)
except native.NativeToolError as error:
    for name in ROLE:
        case.decide("execution", final={"method": "DESeq2 joint ~ grp", "subset": name, "execution_error": str(error)},
                    evidence=[al_mat, al_meta], reasoning="joint DESeq2 failed", confidence="high",
                    execution_status="failed")
    raise
case.write_json("results/deseq2_joint/joint_result.json", res, role="joint_deseq2_manifest")
counts = {}
for r in res["results"]:
    name = r["name"]
    c = native.apply_threshold(r["path"], metric="padj", cutoff=0.05, effect_cutoff=1.0, min_group_n=3)
    wd = native.apply_threshold(r["path"], metric="padj", cutoff=0.05, effect_cutoff=None)
    counts[name] = {"paper_threshold": c, "audit_padj_only": wd}
    out_ev = case.add_output(r["path"], f"deg_table_{name}")
    case.decide("execution",
                final={"method": "DESeq2 (pydeseq2) joint model ~ grp, Wald test", "subset": name,
                       "role": ROLE[name], "cells": r["cells"], "formula": res["formula"],
                       "n_samples": res["n_samples"], "n_genes_tested": res["n_genes"],
                       "outputs": [r["path"]], "threshold_counts": c,
                       "audit_counts_padj_lt_0.05_no_lfc": {k: wd[k] for k in ("n_significant", "n_up", "n_down")}},
                evidence=[al_mat, al_meta, out_ev], confidence="high", execution_status="completed",
                reasoning=f"{name}: {c['n_significant']} DEGs ({c['n_up']} up / {c['n_down']} down) under {c['rule']}.")
(case.dir / "results" / "threshold_counts.json").write_text(json.dumps(counts, indent=2), encoding="utf-8")

# Check the paper's highlighted genes (S3.8.p1): sequential increase SED < CE < EE.
genes = ["gene-Prkag3", "gene-Cox7a1", "gene-Cox6a2", "gene-Cox8b", "gene-Myog", "gene-Myod1"]
check = {}
for r in res["results"]:
    t = pd.read_csv(r["path"], index_col=0)
    check[r["name"]] = t.reindex(genes)[["log2FoldChange", "padj"]].round(4).to_dict(orient="index")
(case.dir / "results" / "paper_gene_check.json").write_text(json.dumps(check, indent=2), encoding="utf-8")
print(json.dumps({k: {kk: (v[kk]["n_significant"], v[kk]["n_up"], v[kk]["n_down"]) for kk in v} for k, v in counts.items()}, indent=1))
print(json.dumps(check, indent=1))
