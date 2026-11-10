"""Gate 9 execution: paper filter -> log2(CPM+1) -> limma ~ 0 + grp + rin, five contrasts."""
import sys, pathlib; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID33486778"
run = native.RunRecorder.open(RUN)
case = run.case("PMID33486778")
cdir = case.dir
aligned = cdir / "aligned" / "aligned_matrix.csv"
design = cdir / "aligned" / "design_metadata.csv"
res_dir = cdir / "results"; res_dir.mkdir(parents=True, exist_ok=True)

# paper filter: median CPM >= 0.5 across all 24 samples (CPM on full library sizes)
counts = pd.read_csv(aligned, index_col=0)
cpm = counts / counts.sum() * 1e6
keep = cpm.median(axis=1) >= 0.5
filt_csv = res_dir / "GSE156724_counts_medcpm0.5.csv"
counts.loc[keep].to_csv(filt_csv)
print("kept", int(keep.sum()), "of", len(keep))
case.add_output(filt_csv, "filtered_counts")

msg = native.call_tool("tools.preprocess_tools:preprocess_counts", counts_csv=str(filt_csv),
                       output_dir=str(res_dir), min_count=0, min_samples=1)
print(msg)
norm = native.find_outputs(res_dir, "*_normalized.csv")[0]
case.add_output(norm, "log2cpm_matrix")

C = lambda g: f"C(grp)[{g}]"
contrasts = [
    {"name": "FOinLRT", "coefficients": {C("LFO"): 1, C("LCT"): -1}},
    {"name": "FOinHRT", "coefficients": {C("HFO"): 1, C("HCT"): -1}},
    {"name": "DELTA", "coefficients": {C("LFO"): 1, C("LCT"): -1, C("HFO"): -1, C("HCT"): 1}},
    {"name": "LRTvsHRT_CTRL", "coefficients": {C("LCT"): 1, C("HCT"): -1}},
    {"name": "LRTvsHRT_FO", "coefficients": {C("LFO"): 1, C("HFO"): -1}},
]
plan = {"analysis_type": "multilevel", "formula": "~ 0 + C(grp) + rin", "contrasts": contrasts}
out = native.call_tool("tools.multigroup_tools:run_multigroup_analysis", expression_csv=norm,
                       metadata_csv=str(design), plan=plan, output_dir=str(res_dir / "limma_rin"))
# audit: same model without RIN
plan_a = {"analysis_type": "multilevel", "formula": "~ 0 + C(grp)", "contrasts": contrasts}
out_a = native.call_tool("tools.multigroup_tools:run_multigroup_analysis", expression_csv=norm,
                         metadata_csv=str(design), plan=plan_a, output_dir=str(res_dir / "audit_limma_norin"))

PAPER = {"FOinLRT": 1866, "FOinHRT": 2460}
counts_out, outputs, audit = {}, [], {}
for r in out["results"]:
    t = native.apply_threshold(r["path"], metric="padj", cutoff=0.001, effect_cutoff=1.0)
    d = native.apply_threshold(r["path"], metric="padj", cutoff=0.05)
    counts_out[r["name"]] = {"paper_rule": t, "audit_padj0.05": {k: d[k] for k in ("n_significant", "n_up", "n_down")},
                             "paper_count": PAPER.get(r["name"], "not_reported")}
    item = case.add_output(r["path"], f"deg_{r['name']}")
    outputs.append({"contrast": r["name"], "path": r["path"], "sha256": item.get("sha256")})
for r in out_a["results"]:
    t = native.apply_threshold(r["path"], metric="padj", cutoff=0.001, effect_cutoff=1.0)
    audit[r["name"]] = {k: t[k] for k in ("n_significant", "n_up", "n_down")}
    case.add_output(r["path"], f"audit_deg_norin_{r['name']}")
# overlap of FO DEG sets (paper: 1612 common)
def sig(path):
    tb = pd.read_csv(path, index_col=0)
    return set(tb.index[(tb.padj < 0.001) & (tb.log2FoldChange.abs() > 1)])
paths = {r["name"]: r["path"] for r in out["results"]}
common = len(sig(paths["FOinLRT"]) & sig(paths["FOinHRT"]))
summary = {"n_genes_tested": int(keep.sum()), "formula": plan["formula"], "design_rank": out["design_rank"],
           "residual_df": out["residual_df"], "counts": counts_out, "common_FO_DEGs": common, "paper_common": 1612,
           "audit_without_rin_paper_rule": audit}
case.write_json("results/deg_counts.json", summary, role="deg_counts")
print(json.dumps(summary, indent=1, default=str))

case.decide("execution",
            final={"method": "limma (inmoose) on log2(CPM+1), ~ 0 + grp + rin, contrasts.fit + eBayes, BH per contrast",
                   "outputs": outputs, "n_genes_tested": int(keep.sum()), "design_rank": out["design_rank"],
                   "residual_df": out["residual_df"],
                   "deg_counts_paper_rule": {k: {x: v["paper_rule"][x] for x in ("n_significant", "n_up", "n_down")} for k, v in counts_out.items()},
                   "audit_without_rin": audit, "common_FO_DEGs": common},
            evidence=[case.add_output(cdir / "results" / "deg_counts.json", "deg_counts_summary")],
            reasoning="Approved route ran on all 24 samples; counts from native.apply_threshold under the paper rule.",
            confidence="high", execution_status="completed", decision_status="valid")
