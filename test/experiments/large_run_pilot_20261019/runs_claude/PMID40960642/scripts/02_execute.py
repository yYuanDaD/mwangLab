"""Execution: primary DESeq2 ~ visit + time, joint ~ subject + cell, 36-sample audit; thresholds; study; finish."""
import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os, json, math
ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())
os.chdir(ROOT)
import pandas as pd
from tools import native
native.enable_native_mode()

REL = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40960642"
run = native.RunRecorder.open(REL)
case = run.case("GSE292369")
cd = case.dir
A = cd / "aligned"
L2 = math.log2(1.5)
PT = json.loads((cd / "paper_reconstruction.json").read_text(encoding="utf-8"))["paper_threshold"]


def thr(path):
    r = native.apply_threshold(path, metric="padj", cutoff=0.05, effect_cutoff=L2)
    t = pd.read_csv(path, index_col=0)
    sig = t[(t["padj"] < 0.05) & (t["log2FoldChange"].abs() > L2)]
    r["up"] = int((sig["log2FoldChange"] > 0).sum())
    r["down"] = int((sig["log2FoldChange"] < 0).sum())
    r["n_padj_lt_0.05_no_fc"] = int((t["padj"] < 0.05).sum())
    return r, set(sig.index)


# integer matrices (documented rounding)
m34 = pd.read_csv(A / "aligned_matrix_34.csv", index_col=0).round().astype(int)
m34.to_csv(A / "aligned_matrix_34_int.csv")
m36 = pd.read_csv(A / "aligned_matrix.csv", index_col=0).round().astype(int)
m36.to_csv(A / "aligned_matrix_36_int.csv")
int34 = case.add_output(A / "aligned_matrix_34_int.csv", "rounded_counts_34")
dm = str(A / "design_metadata.csv")
dm_item = case.add_output(dm, "design_metadata")

summary = {}
# ---------------- primary
res_dir = cd / "results" / "primary_visit_time"
try:
    msg = native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=str(A / "aligned_matrix_34_int.csv"),
                           metadata_csv=dm, design_column="time", control_group="PRE", treatment_group="POST",
                           output_dir=str(res_dir), covariate_columns="visit")
    deg = native.deg_outputs(res_dir)[0]
    prim, prim_set = thr(deg)
    out = case.add_output(deg, "deg_table_primary")
    summary["time_POST_vs_PRE_pooled"] = prim
    case.decide("execution",
                final={"method": "DESeq2 (pydeseq2) ~ visit + time", "subset": "time_POST_vs_PRE_pooled (34 samples)",
                       "outputs": [str(deg)], "n_deg": prim["n_significant"], "up": prim["up"], "down": prim["down"],
                       "rule": prim["rule"], "n_tested": prim["n_tested"], "deg_sanity": prim["deg_sanity"],
                       "paper_count": {"total": 1561, "up": 909, "down": 652}},
                evidence=[int34, dm_item, out], execution_status="completed", confidence="high",
                reasoning="Primary exercise contrast executed; paper threshold applied with apply_threshold.")
    prim_ok = True
except native.NativeToolError as e:
    prim_ok = False
    case.decide("execution", final={"method": "DESeq2 (pydeseq2) ~ visit + time", "subset": "time_POST_vs_PRE_pooled",
                                    "execution_error": str(e)[:2000]},
                evidence=[int34, dm_item], execution_status="failed", confidence="high", reasoning="executor failed")
    print("PRIMARY FAILED", e)

# ---------------- joint cell contrasts
comps = json.loads((cd / "comparisons.json").read_text(encoding="utf-8"))
jdir = cd / "results" / "joint_subject_cell"
sets = {}
try:
    jr = native.call_tool("tools.joint_contrasts:run_joint_deseq2", counts_csv=str(A / "aligned_matrix_34.csv"),
                          metadata_csv=dm, comparisons=comps, output_dir=str(jdir), covariates=["subject"],
                          round_estimated_counts=True)
    (jdir / "joint_result.json").write_text(json.dumps(jr, indent=2, default=str), encoding="utf-8")
    outs = []
    for r in jr["results"]:
        t, s = thr(r["path"])
        summary[r["name"]] = t
        sets[r["name"]] = s
        outs.append(case.add_output(r["path"], f"deg_table_{r['name']}"))
    case.decide("execution",
                final={"method": "DESeq2 (pydeseq2) joint ~ subject + cell", "subset": "cell contrasts (34 samples)",
                       "formula": jr["formula"].replace("cov0", "subject"),
                       "outputs": [r["path"] for r in jr["results"]],
                       "n_deg": {r["name"]: summary[r["name"]]["n_significant"] for r in jr["results"]},
                       "skipped": jr["skipped"]},
                evidence=[int34, dm_item] + outs, execution_status="completed", confidence="high",
                reasoning="One DESeq2 fit on all 34 samples; each planned/exploratory cell contrast extracted from it.")
except native.NativeToolError as e:
    case.decide("execution", final={"method": "DESeq2 joint ~ subject + cell", "subset": "cell contrasts",
                                    "execution_error": str(e)[:2000]},
                evidence=[int34, dm_item], execution_status="failed", confidence="high", reasoning="executor failed")
    print("JOINT FAILED", e)

# overlap of per-condition exercise DEG sets (paper's '1561 overlapped DEGs between conditions')
if "time_POST_vs_PRE_cond-PLA" in sets and "time_POST_vs_PRE_cond-KME" in sets:
    ov = sets["time_POST_vs_PRE_cond-PLA"] & sets["time_POST_vs_PRE_cond-KME"]
    summary["overlap_PLA_and_KME_exercise_DEGs"] = {"n": len(ov)}
    pl = pd.read_csv(jdir / "DEG_results_time_POST_vs_PRE_cond-PLA.csv", index_col=0)
    km = pd.read_csv(jdir / "DEG_results_time_POST_vs_PRE_cond-KME.csv", index_col=0)
    ovl = sorted(ov)
    if ovl:
        summary["overlap_PLA_and_KME_exercise_DEGs"]["log2FC_pearson_r"] = float(
            pl.loc[ovl, "log2FoldChange"].corr(km.loc[ovl, "log2FoldChange"]))

# ---------------- 36-sample audit (primary model, no outlier removal)
d36 = pd.read_csv(A / "design_metadata_all36.csv", index_col=0)
adir = cd / "results" / "audit_all36_visit_time"
try:
    native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=str(A / "aligned_matrix_36_int.csv"),
                     metadata_csv=str(A / "design_metadata_all36.csv"), design_column="time", control_group="PRE",
                     treatment_group="POST", output_dir=str(adir), covariate_columns="visit")
    a36, _ = thr(native.deg_outputs(adir)[0])
    summary["audit_all36_time_POST_vs_PRE_pooled"] = a36
    case.add_output(native.deg_outputs(adir)[0], "deg_table_audit_all36")
except native.NativeToolError as e:
    summary["audit_all36_time_POST_vs_PRE_pooled"] = {"execution_error": str(e)[:500]}

# top genes check
if prim_ok:
    t = pd.read_csv(native.deg_outputs(res_dir)[0], index_col=0)
    summary["paper_top_genes_in_primary"] = {g: {"log2FC": round(float(t.loc[g, "log2FoldChange"]), 3),
                                                 "padj": float(t.loc[g, "padj"])} if g in t.index else None
                                             for g in ["NR4A3", "SOCS3", "MAFF", "PPARGC1A", "ARRDC2", "HIF3A", "DDIT4", "NR1D1"]}
rs = case.write_json("reproduction_summary.json", summary, role="reproduction_summary")
print(json.dumps(summary, indent=1, default=str))

# ---------------- study + finish
case.decide("study",
            final={"route": "declared_deviation",
                   "deviations": ["34-sample set from the deposited outlier-removed matrix (paper text silent)",
                                  "model terms chosen (~ visit + time; ~ subject + cell); Partek model not reported",
                                  "no Partek gene filter (rule not reported); pydeseq2 instead of Partek DESeq2"],
                   "primary_contrast": "time_POST_vs_PRE_pooled",
                   "n_deg_primary": summary.get("time_POST_vs_PRE_pooled", {}).get("n_significant"),
                   "paper_n_deg_primary": 1561,
                   "exploratory_contrasts": ["cond_KME_vs_PLA_time-PRE"]},
            evidence=[rs, dm_item], confidence="medium",
            execution_status="completed" if prim_ok else "failed",
            reasoning="Paper's DESeq2 route on the deposited count-scale data with declared choices where the paper is silent.")
p = summary.get("time_POST_vs_PRE_pooled", {})
case.finish(n_deg=p.get("n_significant"), deg_sanity=p.get("deg_sanity"))
run.finish()
print("finished")
