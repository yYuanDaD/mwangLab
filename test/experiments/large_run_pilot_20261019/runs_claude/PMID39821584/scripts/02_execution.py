"""Gate 9: execution (joint DESeq2 on 30 HFD samples) + pairwise audit + sex QC by gene_name."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json, math
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID39821584"
CASE = "PMID39821584"
run = native.RunRecorder.open(RUN)
case = run.case(CASE)
cdir = case.dir
HFD_META = cdir / "aligned" / "design_metadata.csv"
HFD_MAT = cdir / "aligned" / "aligned_matrix_hfd.csv"
comps = json.loads((cdir / "suitability_comparisons.json").read_text(encoding="utf-8"))
planned = {"grp_r25_vs_sed": (1347, 25), "grp_r50_vs_sed": (1823, 78),
           "grp_r75_vs_sed": (1103, 15), "grp_rU_vs_sed": (1107, 16)}

# --- informal sex QC from gene_name (suitability's check found no markers: Entrez IDs)
raw = pd.read_csv("data/GSE275818/GSE275818_Casperson_gene_count.txt.gz", sep="\t")
hfd = pd.read_csv(HFD_META, index_col=0)
sexg = raw[raw.gene_name.isin(["Xist", "Ddx3y", "Uty", "Eif2s3y", "Kdm5d"])].set_index("gene_name")[hfd.title.tolist()]
sex_qc = sexg.to_dict(orient="index")
sex_summary = {g: {"min": int(v.min()), "max": int(v.max())} for g, v in sexg.iterrows()}
print("sex markers", sex_summary)
case.write_json("sex_marker_qc.json", {"by_gene_name": sex_qc, "summary": sex_summary}, role="sex_qc")

out = cdir / "results" / "joint_deseq2"
try:
    res = native.call_tool("tools.joint_contrasts:run_joint_deseq2", counts_csv=str(HFD_MAT),
                           metadata_csv=str(HFD_META), comparisons=comps, output_dir=str(out))
except native.NativeToolError as error:
    case.decide("execution", final={"method": "DESeq2 joint", "execution_error": str(error)},
                evidence=[{"id": "tool:run_joint_deseq2", "kind": "tool_output"}],
                reasoning="joint DESeq2 failed", confidence="high", execution_status="failed")
    raise
print(json.dumps({k: v for k, v in res.items() if k != "results"}, default=str)[:800])

counts, outputs, ev = {}, [], []
for r in res["results"]:
    prim = native.apply_threshold(r["path"], metric="pvalue", cutoff=0.05, inclusive=True)
    sec = native.apply_threshold(r["path"], metric="padj", cutoff=0.05, effect_cutoff=1.0, inclusive=True)
    fdr = native.apply_threshold(r["path"], metric="padj", cutoff=0.05, inclusive=True)
    counts[r["name"]] = {"role": "planned" if r["name"] in planned else "exploratory",
                         "paper_rule_p<=0.05": {k: prim[k] for k in ("n_tested", "n_significant", "n_up", "n_down", "deg_sanity")},
                         "secondary_FDR<=0.05&|LFC|>=1": {k: sec[k] for k in ("n_significant", "n_up", "n_down")},
                         "audit_FDR<=0.05": fdr["n_significant"],
                         "paper_reported": dict(zip(("p<=0.05", "FDR<=0.05&|LFC|>=1"), planned[r["name"]])) if r["name"] in planned else None}
    ev.append(case.add_output(r["path"], f"deg_{r['name']}"))
    outputs.append(r["path"])

# --- audit: separate two-group DESeq2 per planned pair (Novogene-style pairwise fit)
audit = {}
for name in planned:
    test = name.split("_")[1]
    aout = cdir / "results" / "audit_pairwise" / name
    try:
        native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=str(HFD_MAT),
                         metadata_csv=str(HFD_META), design_column="grp", control_group="sed",
                         treatment_group=test, output_dir=str(aout))
        deg = native.deg_outputs(aout)[0]
        a = native.apply_threshold(deg, metric="pvalue", cutoff=0.05, inclusive=True)
        s = native.apply_threshold(deg, metric="padj", cutoff=0.05, effect_cutoff=1.0, inclusive=True)
        audit[name] = {"p<=0.05": a["n_significant"], "up": a["n_up"], "down": a["n_down"],
                       "FDR<=0.05&|LFC|>=1": s["n_significant"], "path": deg}
        case.add_output(deg, f"audit_pairwise_{name}")
    except native.NativeToolError as error:
        audit[name] = {"error": str(error)[:500]}
print(json.dumps(counts, indent=1))
print(json.dumps(audit, indent=1))
case.write_json("deg_counts.json", {"joint": counts, "audit_pairwise": audit}, role="deg_counts")
case.decide("execution",
            final={"method": "DESeq2 (pydeseq2) joint model ~ cell, 30 HFD samples", "formula": res["formula"],
                   "n_samples": res["n_samples"], "n_genes_nonzero": res["n_genes"], "cells": res["cells"],
                   "outputs": outputs, "deg_counts": counts, "audit_pairwise_two_group_deseq2": audit,
                   "skipped": res["skipped"]},
            evidence=ev, reasoning="Joint DESeq2 completed; paper threshold applied with native.apply_threshold.",
            confidence="high", execution_status="completed")
print("execution done")
