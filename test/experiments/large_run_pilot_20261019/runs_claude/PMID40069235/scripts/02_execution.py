"""Gate 9 execution: log2(RPKM+1) -> limma ~ subject + tgrp, 4 planned contrasts."""
import sys, pathlib; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40069235"
run = native.RunRecorder.open(RUN)
case = run.case("case_01")
design = [r for r in case.records if r["stage"] == "design"][-1]["final"]
thr = [r for r in case.records if r["stage"] == "threshold"][-1]["final"]["applied_threshold"]

aligned = case.dir / "aligned" / "aligned_matrix.csv"
design_meta = case.dir / "aligned" / "design_metadata.csv"
lt = native.log_transform(aligned, case.dir / "aligned" / "log2_rpkm.csv")
log_ev = case.add_output(lt["output"], "log2_rpkm_matrix")
out_dir = case.dir / "results"
plan = {"analysis_type": "repeated_multilevel", "formula": design["formula"], "contrasts": design["contrasts"]}
method = "limma (lmFit + contrasts.fit + eBayes, inmoose) via run_multigroup_analysis"
try:
    res = native.call_tool("tools.multigroup_tools:run_multigroup_analysis", expression_csv=lt["output"],
                           metadata_csv=str(design_meta), plan=plan, output_dir=str(out_dir))
except native.NativeToolError as error:
    case.decide("execution", final={"method": method, "execution_error": str(error)},
                evidence=[log_ev], confidence="high", decision_status="valid", execution_status="failed",
                reasoning="limma executor failed")
    raise
counts, outs, evs = {}, [], [log_ev]
for r in res["results"]:
    c = native.apply_threshold(r["path"], metric="padj", cutoff=thr["cutoff"], effect_cutoff=thr["effect_cutoff"])
    fdr_only = native.apply_threshold(r["path"], metric="padj", cutoff=0.05)
    counts[r["name"]] = {"paper_rule": c, "audit_fdr_only": {k: fdr_only[k] for k in ("rule", "n_significant", "n_up", "n_down")}}
    evs.append(case.add_output(r["path"], f"deg_{r['name']}"))
    outs.append(r["path"])

# Overlaps the paper reports (shared within-time DEG sets across diets)
def sig(name):
    t = pd.read_csv([p for p in outs if name in p][0], index_col=0)
    return set(t.index[(t.padj < thr["cutoff"]) & (t.log2FoldChange.abs() > thr["effect_cutoff"])])
overlap = {}
for tp in ("H0", "H2"):
    hc, lc = sig(f"HC_{tp}_vs_BL"), sig(f"LC_{tp}_vs_BL")
    overlap[tp] = {"HC_total": len(hc), "LC_total": len(lc), "shared": len(hc & lc),
                   "HC_only": len(hc - lc), "LC_only": len(lc - hc)}
summary = {"formula": res["formula"], "n_samples": res["n_samples"], "design_rank": res["design_rank"],
           "residual_df": res["residual_df"], "n_genes_tested": counts[res["results"][0]["name"]]["paper_rule"]["n_tested"],
           "counts": counts, "overlaps_paper_rule": overlap}
case.write_json("results/execution_summary.json", summary, role="execution_summary")
case.decide("execution",
            final={"method": method, "formula": "~ subject + tgrp", "executor_formula": res["formula"],
                   "transform": lt["transform"], "outputs": outs, "residual_df": res["residual_df"],
                   "n_deg_paper_rule": {k: {"n": v["paper_rule"]["n_significant"], "up": v["paper_rule"]["n_up"],
                                            "down": v["paper_rule"]["n_down"]} for k, v in counts.items()},
                   "overlaps": overlap},
            evidence=evs, confidence="high", execution_status="completed",
            reasoning="One limma model over all 60 samples; BH within each contrast; paper threshold applied with apply_threshold.")
print(json.dumps(summary, indent=1, default=str))
