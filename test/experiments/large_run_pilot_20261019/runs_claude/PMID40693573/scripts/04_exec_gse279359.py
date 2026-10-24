"""Execution and study gates for case GSE279359."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40693573"
run = native.RunRecorder.open(RUN)
case = run.case("GSE279359")
cdir = case.dir
res = cdir / "results"
res.mkdir(exist_ok=True)
PAPER = dict(metric="padj", cutoff=0.05, effect_cutoff=1.5)
AUDIT1 = dict(metric="padj", cutoff=0.05, effect_cutoff=1.0)
AUDIT0 = dict(metric="padj", cutoff=0.05, effect_cutoff=None)
REPORTED = {"ipe_vs_pre": (23, 46), "1pe_vs_pre": (13, 32), "24pe_vs_pre": (31, 49)}

def thresholds(deg):
    return {"paper": native.apply_threshold(deg, **PAPER), "audit_log2fc1": native.apply_threshold(deg, **AUDIT1),
            "audit_padj_only": native.apply_threshold(deg, **AUDIT0)}

gc = pd.read_csv(cdir / "aligned" / "gene_counts_all.csv", index_col=0)
ann = pd.read_csv(cdir / "aligned" / "gene_annotation.csv", index_col=0)
dm = pd.read_csv(cdir / "aligned" / "design_metadata.csv", index_col=0)
known = gc.loc[ann.index[ann.gene_novelty == "Known"]]
suit = json.loads((cdir / "suitability" / "suitability.json").read_text(encoding="utf-8"))
comp_by_name = {c["name"]: c for c in suit["comparisons"]}
design_ev = case.evidence_item("tool_output:design_metadata.csv")
summary = {}

# ---- planned: pairwise vs pre, paper's per-comparison detection filter
planned = {"ipe_vs_pre": "ipe", "1pe_vs_pre": "h1", "24pe_vs_pre": "h24"}
for name, lvl in planned.items():
    sub = dm[dm.time.isin(["pre", lvl])]
    k = known[sub.index]
    keep = (k > 0).sum(axis=1) >= len(sub) / 2
    kp = res / f"counts_{name}.csv"
    k[keep].to_csv(kp)
    mp = res / f"meta_{name}.csv"
    sub.to_csv(mp)
    cev = case.add_output(kp, f"counts_filtered_{name}")
    out = res / name
    try:
        native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=str(kp), metadata_csv=str(mp),
                         design_column="time", control_group="pre", treatment_group=lvl, output_dir=str(out))
        deg = native.deg_outputs(out)[0]
        d = pd.read_csv(deg, index_col=0)
        d.insert(0, "symbol", ann.reindex(d.index)["annot_gene_name"].values)
        d.to_csv(deg)
        th = thresholds(deg)
        sig = d[(d.padj < 0.05) & (d.log2FoldChange.abs() > 1.5)]
        val = {g: d.loc[d.symbol == g, ["log2FoldChange", "padj"]].round(4).to_dict("records") for g in ["Ube2d1", "Fbxo32", "Fos"]}
        summary[name] = {**{kk: vv["n_significant"] for kk, vv in th.items()},
                         "up": th["paper"]["n_up"], "down": th["paper"]["n_down"], "genes_tested_input": int(keep.sum()),
                         "paper_reported_1.5_1.0": REPORTED[name], "validated_genes": val,
                         "top_sig": sig.sort_values("padj").head(15)["symbol"].tolist()}
        o = case.add_output(deg, f"deg_{name}")
        case.decide("execution",
                    final={"method": "DESeq2 ~ time (pairwise)", "subset": name,
                           "samples": {"time": ["pre", lvl], "n": int(len(sub))},
                           "genes_after_filter": int(keep.sum()), "outputs": [deg],
                           "n_deg_paper_threshold": th["paper"]["n_significant"], "n_up": th["paper"]["n_up"],
                           "n_down": th["paper"]["n_down"],
                           "audit_counts": {kk: vv["n_significant"] for kk, vv in th.items() if kk != "paper"},
                           "paper_reported": {"log2fc_1.5": REPORTED[name][0], "log2fc_1.0": REPORTED[name][1]},
                           "validated_genes_check": val, "deg_sanity": th["paper"]["deg_sanity"], "role": "paper_planned"},
                    evidence=[cev, design_ev, o], paper={"locator": "S3.1.p2"}, confidence="high",
                    execution_status="completed",
                    reasoning=f"{name}: {th['paper']['rule']} -> {th['paper']['n_significant']} (paper {REPORTED[name][0]}).")
    except native.NativeToolError as e:
        case.decide("execution", final={"method": "DESeq2 ~ time (pairwise)", "subset": name, "execution_error": str(e)[:2000]},
                    evidence=[cev], paper={"locator": "S3.1.p2"}, confidence="high", execution_status="failed",
                    reasoning="executor failed")
        summary[name] = {"error": str(e)[:500]}

# ---- exploratory + audit: joint model on all 20
keep = (known > 0).sum(axis=1) >= len(dm) / 2
jp = res / "counts_joint.csv"
known[keep].to_csv(jp)
jev = case.add_output(jp, "counts_filtered_joint")
try:
    comps = list(comp_by_name.values())
    r = native.call_tool("tools.joint_contrasts:run_joint_deseq2", counts_csv=str(jp),
                         metadata_csv=str(cdir / "aligned" / "design_metadata.csv"), comparisons=comps,
                         output_dir=str(res / "joint"))
    counts = {x["name"]: thresholds(x["path"]) for x in r["results"]}
    summary["joint"] = {kk: {a: b["n_significant"] for a, b in v.items()} for kk, v in counts.items()}
    outs = [case.add_output(x["path"], f"deg_joint_{x['name']}") for x in r["results"]]
    case.decide("execution",
                final={"method": "DESeq2 joint ~ time (4 levels, all 20 samples)", "subset": "joint_all_time_contrasts",
                       "formula": r["formula"], "genes_after_filter": int(keep.sum()),
                       "outputs": [x["path"] for x in r["results"]],
                       "counts_paper_threshold": {kk: {"n": v["paper"]["n_significant"], "up": v["paper"]["n_up"],
                                                       "down": v["paper"]["n_down"]} for kk, v in counts.items()},
                       "audit_counts": {kk: {a: b["n_significant"] for a, b in v.items() if a != "paper"} for kk, v in counts.items()},
                       "role": "exploratory (non-pre contrasts); audit refit of the planned vs-pre contrasts"},
                evidence=[jev, design_ev] + outs, paper={"locator": "S3.1.p2"}, confidence="medium",
                execution_status="completed", reasoning="All six pairwise time contrasts from one 20-sample DESeq2 model.")
except native.NativeToolError as e:
    case.decide("execution", final={"method": "DESeq2 joint", "subset": "joint_all_time_contrasts", "execution_error": str(e)[:2000]},
                evidence=[jev], paper={"locator": "S3.1.p2"}, confidence="medium", execution_status="failed",
                reasoning="executor failed")
    summary["joint"] = {"error": str(e)[:500]}

(res / "execution_summary.json").write_text(json.dumps(summary, indent=1, default=str), encoding="utf-8")
print(json.dumps(summary, indent=1, default=str))
