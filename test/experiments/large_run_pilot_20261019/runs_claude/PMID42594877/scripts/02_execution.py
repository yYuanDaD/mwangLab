"""Execution: paired DESeq2 (~ subject + time) per planned unit; per-sex exploratory (adipose);
exploratory intensity x time interaction via limma paired_change on log2(CPM+1) (media swaps)."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID42594877"
run = native.RunRecorder.open(RUN)
state = json.load(open(pathlib.Path(RUN) / "scripts" / "plan_state.json"))
counts_all = {}


def thr(path):
    return native.apply_threshold(path, metric="padj", cutoff=0.05, effect_cutoff=None)


def paired_deseq2(case, label, mat_csv, dm, keep, role):
    od = case.dir / "results" / label
    od.mkdir(parents=True, exist_ok=True)
    sub_meta, sub_mat = od / "design_subset.csv", od / "counts_subset.csv"
    dm.loc[keep].to_csv(sub_meta)
    pd.read_csv(mat_csv, index_col=0)[list(keep)].to_csv(sub_mat)
    unit = {"subset": label, "role": role, "n_samples": len(keep),
            "n_pairs": int(dm.loc[keep, "subject"].nunique())}
    try:
        native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=str(sub_mat), metadata_csv=str(sub_meta),
                         design_column="time", control_group="pre", treatment_group="post", output_dir=str(od),
                         covariate_columns="subject", alpha=0.05)
        f = native.deg_outputs(od)[0]
        it = case.add_output(f, f"deg_{label}")
        t = thr(f)
        unit.update(path=str(f), sha256=it.get("sha256"), applied=t)
        print(case.case_id, label, {k: t[k] for k in t if k.startswith("n_")}, t.get("deg_sanity"))
        case.decide("execution",
                    final={"method": "DESeq2 (pydeseq2) Wald, ~ subject + time", "formula": "~ subject + time",
                           "subset": label, "role": role, "n_samples": len(keep), "n_pairs": unit["n_pairs"],
                           "outputs": [{"path": str(f), "sha256": it.get("sha256")}],
                           "n_deg_applied": t["n_significant"], "n_up": t.get("n_up"), "n_down": t.get("n_down"),
                           "applied_threshold": "padj < 0.05, no effect cutoff (paper S2.4.p2/S2.4.p4)"},
                    evidence=[it], paper={"locator": "S9.3.15.p1"}, confidence="high",
                    reasoning=f"Paired DESeq2 on {len(keep)} samples ({label}, {role}).", execution_status="completed")
    except native.NativeToolError as e:
        unit["execution_error"] = str(e)
        print(case.case_id, label, "FAILED", e)
        case.decide("execution", final={"method": "DESeq2 (pydeseq2) Wald, ~ subject + time", "subset": label,
                                        "execution_error": str(e)},
                    evidence=[{"id": "tool:run_deseq2_analysis", "kind": "tool_output"}], confidence="high",
                    reasoning=f"Paired DESeq2 failed for {label}.", execution_status="failed")
    return unit


for cid, st in state.items():
    case = run.case(cid)
    dm = pd.read_csv(st["design_csv"], index_col=0)
    dm["subject"] = dm["subject"].astype(str)
    units = {}
    if not st["two_arm"]:
        units["post_vs_pre"] = paired_deseq2(case, "post_vs_pre", st["aligned_matrix"], dm, list(dm.index), "planned")
        # exploratory per-sex fits (sex inferred from X/Y genes; paper pooled sexes)
        sex_tsv = case.dir / "suitability" / "aligned_matrix_sex_check.tsv"
        sx = pd.read_csv(sex_tsv, sep="\t", index_col=0)
        col = next(c for c in sx.columns if "pred" in c.lower() or c.lower() == "sex")
        dm["sex_inferred"] = sx.loc[dm.index, col].astype(str)
        per_subject = dm.groupby("subject")["sex_inferred"].nunique()
        assert (per_subject == 1).all(), "inferred sex differs within a subject"
        for s in sorted(dm["sex_inferred"].unique()):
            keep = list(dm.index[dm["sex_inferred"] == s])
            units[f"post_vs_pre_sex-{s}"] = paired_deseq2(case, f"post_vs_pre_sex-{s}", st["aligned_matrix"], dm, keep,
                                                         "exploratory (per-sex split; paper pooled sexes)")
    else:
        for lab in ("SIE_post_vs_pre", "MIE_post_vs_pre"):
            keep = list(dm.index[dm["intensity"] == lab.split("_")[0]])
            units[lab] = paired_deseq2(case, lab, st["aligned_matrix"], dm, keep, "planned")
        # exploratory interaction: (post - pre) per donor on log2(CPM+1), ~ C(intensity), SIE vs MIE
        od = case.dir / "results" / "interaction_SIE_vs_MIE_change"
        od.mkdir(parents=True, exist_ok=True)
        unit = {"subset": "interaction_SIE_vs_MIE_change", "role": "exploratory (not tested in the paper)"}
        try:
            native.call_tool("tools.preprocess_tools:preprocess_counts", counts_csv=st["aligned_matrix"],
                             output_dir=str(od / "preprocess"))
            norm = native.find_outputs(od / "preprocess", "*_normalized.csv")[0]
            plan = {"analysis_type": "paired_change", "subject_column": "subject", "time_column": "time",
                    "baseline_level": "pre", "followup_levels": ["post"], "group_column": "intensity",
                    "formula": "~ C(intensity)",
                    "contrasts": [{"name": "SIE_change_vs_MIE_change", "coefficients": {"C(intensity)[T.SIE]": 1}}]}
            from tools.multigroup_tools import run_multigroup_analysis
            res = native.call_tool(run_multigroup_analysis, expression_csv=str(norm), metadata_csv=st["design_csv"],
                                   plan=plan, output_dir=str(od))
            r = res["results"][0]
            it = case.add_output(r["path"], "deg_interaction")
            t = thr(r["path"])
            unit.update(path=r["path"], applied=t, residual_df=r.get("residual_df"),
                        excluded_subjects=r.get("excluded_subjects"))
            print(cid, "interaction", {k: t[k] for k in t if k.startswith("n_")}, "excluded", r.get("excluded_subjects"))
            case.decide("execution",
                        final={"method": "limma paired_change (multigroup_tools), (post - pre) per donor ~ C(intensity)",
                               "transform": "log2(CPM+1) via preprocess_counts (min_count 10 in >= 3 samples)",
                               "formula": "~ C(intensity) on within-donor differences",
                               "subset": "interaction_SIE_vs_MIE_change", "role": "exploratory",
                               "outputs": [{"path": r["path"], "sha256": it.get("sha256")}, {"path": str(norm)}],
                               "residual_df": r.get("residual_df"), "n_deg_applied": t["n_significant"],
                               "n_up": t.get("n_up"), "n_down": t.get("n_down")},
                        evidence=[it], paper={"locator": "S2.4.p2"}, confidence="medium",
                        reasoning="Exploratory test of whether the post-vs-pre response differs between SIE and MIE plasma.",
                        execution_status="completed")
        except native.NativeToolError as e:
            unit["execution_error"] = str(e)
            print(cid, "interaction FAILED", e)
            case.decide("execution", final={"method": "limma paired_change", "subset": "interaction_SIE_vs_MIE_change",
                                            "transform": "log2(CPM+1)", "execution_error": str(e)},
                        evidence=[{"id": "tool:run_multigroup_analysis", "kind": "tool_output"}], confidence="medium",
                        reasoning="Exploratory interaction model failed.", execution_status="failed")
        units["interaction_SIE_vs_MIE_change"] = unit
    case.write_json("results/deg_counts.json", {"units": units, "paper_reported": st["reported"]}, role="deg_counts")
    counts_all[cid] = {k: (v.get("applied", {}).get("n_significant"), v.get("applied", {}).get("n_up"),
                           v.get("applied", {}).get("n_down")) for k, v in units.items()}
print(json.dumps(counts_all, indent=1))
