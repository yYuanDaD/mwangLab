"""Execution, enrichment and study gates for case GSE151066."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40693573"
run = native.RunRecorder.open(RUN)
case = run.case("GSE151066")
paper = case.evidence_item("paper:PMC12248044.paper.json")
cdir = case.dir
res = cdir / "results"
res.mkdir(exist_ok=True)
PAPER = dict(metric="padj", cutoff=0.05, effect_cutoff=1.5)
AUDIT1 = dict(metric="padj", cutoff=0.05, effect_cutoff=1.0)
AUDIT0 = dict(metric="padj", cutoff=0.05, effect_cutoff=None)

# ---- inputs prepared at execution (value-changing steps decided in the method gate)
am = pd.read_csv(cdir / "aligned" / "aligned_matrix.csv", index_col=0)
dm = pd.read_csv(cdir / "aligned" / "design_metadata.csv", index_col=0)
human = am.loc[am.index.str.startswith("ENSG")].round().astype(int)
counts_path = res / "counts_human_rounded.csv"
human.to_csv(counts_path)
counts_ev = case.add_output(counts_path, "counts_rounded_human_genes")
males = dm[dm["sex"] == "male"]
suit = json.loads((cdir / "suitability" / "suitability.json").read_text(encoding="utf-8"))
comp_by_name = {c["name"]: c for c in suit["comparisons"]}
summary = {}

def thresholds(deg):
    return {"paper": native.apply_threshold(deg, **PAPER), "audit_log2fc1": native.apply_threshold(deg, **AUDIT1),
            "audit_padj_only": native.apply_threshold(deg, **AUDIT0)}

# ---- planned: per-cohort pre vs h3, ~ subject + time
planned = {"AS_3pe_vs_pre": "sed", "AA_3pe_vs_pre": "act"}
for name, coh in planned.items():
    sub = males[(males.cohort == coh) & males.time.isin(["pre", "h3"])]
    mpath = res / f"meta_{name}.csv"
    sub.to_csv(mpath)
    out = res / name
    try:
        msg = native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=str(counts_path), metadata_csv=str(mpath),
                               design_column="time", control_group="pre", treatment_group="h3", output_dir=str(out),
                               covariate_columns="subject")
        deg = native.deg_outputs(out)[0]
        th = thresholds(deg)
        summary[name] = th
        o = case.add_output(deg, f"deg_{name}")
        case.decide("execution",
                    final={"method": "DESeq2 ~ subject + time", "subset": name,
                           "samples": {"cohort": coh, "sex": "male", "time": ["pre", "h3"], "n": int(len(sub)),
                                       "n_subjects": int(sub.subject.nunique())},
                           "outputs": [deg], "n_deg_paper_threshold": th["paper"]["n_significant"],
                           "n_up": th["paper"]["n_up"], "n_down": th["paper"]["n_down"],
                           "audit_counts": {k: v["n_significant"] for k, v in th.items() if k != "paper"},
                           "n_tested": th["paper"]["n_tested"], "deg_sanity": th["paper"]["deg_sanity"],
                           "role": "paper_planned"},
                    evidence=[counts_ev, case.evidence_item("tool_output:design_metadata.csv"), o],
                    paper={"locator": "S3.1.p1"}, confidence="high", execution_status="completed",
                    reasoning=f"{name}: {th['paper']['rule']} -> {th['paper']['n_significant']} "
                              f"({th['paper']['n_up']} up / {th['paper']['n_down']} down).")
    except native.NativeToolError as e:
        case.decide("execution", final={"method": "DESeq2 ~ subject + time", "subset": name, "execution_error": str(e)[:2000]},
                    evidence=[counts_ev], paper={"locator": "S3.1.p1"}, confidence="high", execution_status="failed",
                    reasoning="executor failed")
        summary[name] = {"error": str(e)[:500]}
print(json.dumps(summary, indent=1, default=str))

# ---- exploratory: per-cohort joint model over pre/ip/h3
for coh in ["sed", "act"]:
    sub = males[males.cohort == coh]
    mpath = res / f"meta_joint_{coh}.csv"
    sub.to_csv(mpath)
    comps = [comp_by_name[n] for n in comp_by_name if n.startswith("time_") and n.endswith(f"cohort-{coh}")]
    out = res / f"joint_{coh}"
    try:
        r = native.call_tool("tools.joint_contrasts:run_joint_deseq2", counts_csv=str(counts_path), metadata_csv=str(mpath),
                             comparisons=comps, output_dir=str(out), covariates=["subject"])
        counts = {x["name"]: thresholds(x["path"]) for x in r["results"]}
        summary[f"joint_{coh}"] = {k: {kk: vv["n_significant"] for kk, vv in v.items()} for k, v in counts.items()}
        outs = [case.add_output(x["path"], f"deg_joint_{x['name']}") for x in r["results"]]
        case.decide("execution",
                    final={"method": "DESeq2 joint ~ subject + cell (time levels pre/ip/h3)", "subset": f"joint_{coh}",
                           "formula": r["formula"].replace("cov0", "subject"), "outputs": [x["path"] for x in r["results"]],
                           "counts_paper_threshold": {k: {"n": v["paper"]["n_significant"], "up": v["paper"]["n_up"],
                                                          "down": v["paper"]["n_down"]} for k, v in counts.items()},
                           "audit_counts": {k: {kk: vv["n_significant"] for kk, vv in v.items() if kk != "paper"}
                                            for k, v in counts.items()},
                           "role": "exploratory (h3_vs_pre here is an audit refit on three time points)"},
                    evidence=[counts_ev] + outs, paper={"locator": "S2.1.p1"}, confidence="medium",
                    execution_status="completed",
                    reasoning=f"Exploratory time contrasts for cohort {coh} from one DESeq2 model on all male samples.")
    except native.NativeToolError as e:
        case.decide("execution", final={"method": "DESeq2 joint", "subset": f"joint_{coh}", "execution_error": str(e)[:2000]},
                    evidence=[counts_ev], paper={"locator": "S2.1.p1"}, confidence="medium", execution_status="failed",
                    reasoning="executor failed")
        summary[f"joint_{coh}"] = {"error": str(e)[:500]}

# ---- exploratory: cohort difference in the 3 h response (paired change, limma on log2 CPM)
sub = males[males.time.isin(["pre", "h3"])]
pc_dir = res / "paired_change"
pc_dir.mkdir(exist_ok=True)
human[sub.index].to_csv(pc_dir / "counts_males_pre_h3.csv")
mpath = pc_dir / "meta_males_pre_h3.csv"
sub.to_csv(mpath)
try:
    native.call_tool("tools.preprocess_tools:preprocess_counts", counts_csv=str(pc_dir / "counts_males_pre_h3.csv"),
                     output_dir=str(pc_dir))
    norm = native.find_outputs(pc_dir, "*_normalized.csv")[0]
    plan = {"analysis_type": "paired_change", "subject_column": "subject", "time_column": "time", "baseline_level": "pre",
            "followup_levels": ["h3"], "group_column": "cohort", "formula": "~ C(cohort)",
            "contrasts": [{"name": "change_h3_sed_vs_act", "coefficients": {"C(cohort)[T.sed]": 1}}]}
    r = native.call_tool("tools.multigroup_tools:run_multigroup_analysis", expression_csv=norm, metadata_csv=str(mpath),
                         plan=plan, output_dir=str(pc_dir / "fit"))
    degs = native.deg_outputs(pc_dir / "fit")
    th = {pathlib.Path(d).name: thresholds(d) for d in degs}
    summary["paired_change"] = {k: {kk: vv["n_significant"] for kk, vv in v.items()} for k, v in th.items()}
    outs = [case.add_output(d, "deg_paired_change") for d in degs]
    case.decide("execution",
                final={"method": "limma paired_change (h3 - pre per subject) ~ C(cohort)", "subset": "change_h3_sed_vs_act",
                       "transform": "log2(CPM+1) after preprocess_counts low-count filter (>=10 counts in >=3 samples)",
                       "formula": "(h3 - pre) ~ cohort", "outputs": degs,
                       "counts": {k: {kk: vv["n_significant"] for kk, vv in v.items()} for k, v in th.items()},
                       "role": "exploratory (training-status difference in the acute response; associational between cohorts)"},
                evidence=[counts_ev] + outs, paper={"locator": "S3.1.p1"}, confidence="medium", execution_status="completed",
                reasoning="Within-subject change h3-pre compared between sedentary and active cohorts.")
except native.NativeToolError as e:
    case.decide("execution", final={"method": "limma paired_change", "subset": "change_h3_sed_vs_act",
                                    "execution_error": str(e)[:2000]},
                evidence=[counts_ev], paper={"locator": "S3.1.p1"}, confidence="medium", execution_status="failed",
                reasoning="executor failed")
    summary["paired_change"] = {"error": str(e)[:500]}

(res / "execution_summary.json").write_text(json.dumps(summary, indent=1, default=str), encoding="utf-8")
print(json.dumps(summary, indent=1, default=str))
