"""case_02: paper's grouped analysis - edgeR QL pre vs ctrl and post vs ctrl, then Δlog2FC and % rescue."""
import json
import numpy as np
import pandas as pd
from common import *  # noqa
from tools import native

native.enable_native_mode()
run = native.RunRecorder.open(RUN_DIR)
case = run.case("case_02")
paper = case.evidence_item("paper:PMC10443797.paper.json")
dmeta_path = case.dir / "aligned" / "design_metadata.csv"
dmeta = case.evidence_item("tool_output:design_metadata.csv")
amat = case.evidence_item("tool_output:aligned_matrix.csv")
dm = pd.read_csv(dmeta_path, index_col=0)

checks = {}
for arm in ("pre", "post"):
    sub = dm[dm.grp.isin(["ctrl", arm])]
    checks[arm] = {"design_check": native.design_check(sub, ["grp"]),
                   "confounding": native.confounding_report(sub, "grp", ["subject"])}
case.write_json("design_checks.json", checks)

case.decide("design",
            final={"analysis_type": "two-group comparisons vs common control, fitted separately (paper grouped analysis)",
                   "design_column": "grp",
                   "contrasts": [{"name": "pre_vs_ctrl", "control": "ctrl", "treatment": "pre", "n": "6 vs 9"},
                                 {"name": "post_vs_ctrl", "control": "ctrl", "treatment": "post", "n": "6 vs 9"},
                                 {"name": "delta_log2FC", "definition": "log2FC(post vs ctrl) - log2FC(pre vs ctrl); "
                                  "derived, no test (S2.2.p2)"}],
                   "formula": "~ grp (per fit)",
                   "estimand_type": "pre/post vs control are associational (disease vs healthy); Δlog2FC is the "
                                    "paper's grouped training-effect measure"},
            candidates=[{"value": "one 3-level model ~ 0 + grp", "reason_rejected": "paper reports separate fits "
                         "(author sheets have different gene counts: 18,762 pre vs 18,804 post), and repository "
                         "edgeR is two-arm only"}],
            evidence=[paper, dmeta], paper={"locator": "S2.2.p2"}, confidence="high",
            reasoning="S2.2.p2: all pretraining samples one group, all posttraining another; each compared with "
                      "controls by QL F-test; Δlog2FC reported.")

case.decide("covariance",
            final={"status": "not_required", "blocking_terms": [],
                   "covariates": [{"name": "subject", "disposition": "excluded: one sample per subject within each fit"},
                                  {"name": "age", "disposition": "excluded: not in GEO metadata; paper notes controls "
                                   "younger (32 vs 48 y, S2.5.p2) - possible confound of the disease contrasts, "
                                   "largely cancels in Δlog2FC"},
                                  {"name": "sex", "disposition": "excluded: single level (male)"}]},
            evidence=[dmeta, paper], paper={"locator": "S2.5.p2"}, confidence="medium",
            reasoning="Within each fit every subject contributes one sample; pairing across pre/post is not part "
                      "of the paper's grouped route (handled in case_01).")

case.decide("method",
            final={"method": "edgeR QL F-test (inmoose.edgepy)", "matrix_type": "raw counts", "formula": "~ grp",
                   "prefilter": "per fit: keep genes with >=10 counts in at least one of the 15 samples (literal "
                                "reading of S4.4.p1)",
                   "normalization": "library size only (no TMM)",
                   "paper_route": {"method": "edgeR 3.34.1 (R) QL F-test with TMM normalization (edgeR default)",
                                   "status": "blocked",
                                   "reason": ("inmoose.edgepy has no calcNormFactors/TMM (tools/edger_tools.py "
                                              "module docstring); the paper's exact gene filter is ambiguous and "
                                              "does not reproduce the authors' gene counts")}},
            evidence=[amat, paper], paper={"locator": "S4.13.p1"}, confidence="medium",
            reasoning="Same model family and test as the paper; normalization differs -> declared deviation.")

case.decide("threshold",
            final={"paper_threshold": PAPER_THRESHOLD, "threshold_source": "paper_on_deviation_route",
                   "applied_threshold": {"metric": "pvalue", "adjustment": "none", "cutoff": 0.05,
                                         "effect_metric": "log2FC", "effect_cutoff": 2.0, "inclusive": False},
                   "audit_threshold": {"metric": "padj", "adjustment": "BH", "cutoff": 0.05, "effect_cutoff": None,
                                       "label": "audit"}},
            evidence=[paper], paper={"locator": "S4.4.p1"}, confidence="high",
            reasoning="Paper rule applied exactly to both grouped fits (S2.5.p1 uses it for pre-vs-control DEGs).")

counts = pd.read_csv(case.dir / "aligned" / "aligned_matrix.csv", index_col=0)
res = {}
summary = {}
for arm in ("pre", "post"):
    sub_meta = dm[dm.grp.isin(["ctrl", arm])]
    sub = counts[sub_meta.index]
    keep = (sub >= 10).any(axis=1)
    rdir = case.dir / "results" / f"{arm}_vs_ctrl"
    rdir.mkdir(parents=True, exist_ok=True)
    cpath, mpath = rdir / "counts_filtered.csv", rdir / "design_metadata.csv"
    sub.loc[keep].to_csv(cpath)
    sub_meta.to_csv(mpath)
    try:
        msg = native.call_tool("tools.edger_tools:run_edger_analysis", counts_csv=str(cpath),
                               metadata_csv=str(mpath), design_column="grp", control_group="ctrl",
                               treatment_group=arm, output_dir=str(rdir))
        print(msg)
        deg = native.deg_outputs(rdir)[0]
        applied = native.apply_threshold(deg, metric="pvalue", cutoff=0.05, effect_cutoff=2.0, min_group_n=6)
        audit = native.apply_threshold(deg, metric="padj", cutoff=0.05, min_group_n=6)
        item = case.add_output(deg, f"deg_table_{arm}_vs_ctrl")
        summary[arm] = {"applied": applied, "audit": audit, "n_genes_after_prefilter": int(keep.sum())}
        res[arm] = pd.read_csv(deg, index_col=0)
        case.decide("execution",
                    final={"method": "edgeR QL F-test (inmoose.edgepy)", "formula": "~ grp", "subset": f"{arm}_vs_ctrl",
                           "outputs": [deg], "applied_counts": applied, "audit_counts": audit},
                    evidence=[item, amat], confidence="high", execution_status="completed",
                    reasoning=f"edgeR completed for {arm} vs ctrl (9 vs 6).")
    except native.NativeToolError as e:
        print("FAILED", arm, e)
        case.decide("execution", final={"method": "edgeR QL F-test (inmoose.edgepy)", "subset": f"{arm}_vs_ctrl",
                                        "execution_error": str(e)},
                    evidence=[amat], confidence="high", execution_status="failed", reasoning="executor failed")

# ---- derived grouped training effect (arithmetic on fitted log2FCs, as in S2.2.p2 / S4.6.p1 / S4.7.p1)
if len(res) == 2:
    pre, post = res["pre"], res["post"]
    common = pre.index.intersection(post.index)
    d = pd.DataFrame({"log2FC_pre_vs_ctrl": pre.loc[common, "log2FoldChange"],
                      "pvalue_pre_vs_ctrl": pre.loc[common, "pvalue"],
                      "log2FC_post_vs_ctrl": post.loc[common, "log2FoldChange"],
                      "pvalue_post_vs_ctrl": post.loc[common, "pvalue"]})
    d["delta_log2FC_post_minus_pre"] = d.log2FC_post_vs_ctrl - d.log2FC_pre_vs_ctrl
    dys = (d.pvalue_pre_vs_ctrl < 0.05) & (d.log2FC_pre_vs_ctrl.abs() > 2)
    # percent rescue = (pre - post) / (pre - ctrl) * 100 = Δ(pre-post) / log2FC_pre_vs_ctrl
    d["percent_rescue"] = np.where(dys, (d.log2FC_pre_vs_ctrl - d.log2FC_post_vs_ctrl) / d.log2FC_pre_vs_ctrl * 100, np.nan)
    pr = d.loc[dys, "percent_rescue"]
    cat = pd.cut(pr, [-np.inf, -10, 10, 110, np.inf], labels=["misrescued", "unchanged", "rescued", "overrescued"],
                 right=False)
    dpath = case.dir / "results" / "grouped_delta_log2FC.csv"
    d.to_csv(dpath)
    derived = {"n_pre_vs_ctrl_DEGs_paper_rule": int(dys.sum()),
               "rescue_categories": cat.value_counts().to_dict(),
               "median_percent_rescue": float(pr.median()) if len(pr) else None,
               "dysregulation_score_pre": float(d.loc[dys, "log2FC_pre_vs_ctrl"].abs().mean()),
               "dysregulation_score_post": float(d.loc[dys, "log2FC_post_vs_ctrl"].abs().mean()),
               "note": "rescue categories per S4.6.p1 (rescued 10-110%, over >=110%, misrescued < -10%)"}
    # concordance with the authors' deposited grouped pre-training sheet (only sheet that survived conversion)
    try:
        auth = pd.read_csv(EDGER_SHEET1).set_index("Ensembl ID")
        auth = auth[~auth.index.duplicated()]
        j = auth.index.intersection(pre.index)
        derived["concordance_pre_vs_ctrl_with_authors"] = {
            "n_shared_genes": int(len(j)),
            "pearson_logFC": float(np.corrcoef(auth.loc[j, "logFC"], pre.loc[j, "log2FoldChange"])[0, 1]),
            "authors_n_DEG_paper_rule": int(((auth.PValue < 0.05) & (auth.logFC.abs() > 2)).sum()),
            "authors_sheet": "GSE208639_edgeR_output.xlsx sheet 'Grouped pre-training'"}
    except Exception as e:  # noqa
        derived["concordance_error"] = str(e)
    case.add_output(dpath, "grouped_delta_log2FC")
    case.write_json("grouped_training_effect.json", {"per_fit": summary, "derived": derived})
    print(json.dumps(derived, indent=1, default=str))

case.decide("study", final={"route": "declared_deviation",
                            "summary": "Paper grouped route (edgeR QL vs controls + Δlog2FC); deviation: no TMM."},
            evidence=[dmeta], confidence="medium", reasoning="edgeR without TMM; otherwise as the paper.")
n = summary.get("pre", {}).get("applied", {})
print(case.finish(n_deg=n.get("n_significant"), deg_sanity=n.get("deg_sanity")))
