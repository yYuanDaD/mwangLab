"""case_03: paper's individual analysis (each participant's pre / post sample, n=1, vs 6 controls).

Repository two-arm executors refuse a 1-sample arm (tools/analysis_policy.py:16), so the paper's
per-individual edgeR fits run here as ONE limma model ~ 0 + C(unit) on log2(CPM+1), where every
DM1 sample is its own level and the 6 controls supply the residual variance (df = 5).
Exploratory (n = 1 per arm).
"""
import json
import sys
import numpy as np
import pandas as pd
from common import *  # noqa
from tools import native

native.enable_native_mode()
run = native.RunRecorder.open(RUN_DIR)
case = run.case("case_03")
paper = case.evidence_item("paper:PMC10443797.paper.json")
dmeta_path = case.dir / "aligned" / "design_metadata.csv"
dmeta = case.evidence_item("tool_output:design_metadata.csv")
amat = case.evidence_item("tool_output:aligned_matrix.csv")
dm = pd.read_csv(dmeta_path, index_col=0)
subjects = sorted(dm.loc[dm.grp != "ctrl", "subject"].unique(), key=lambda s: int(s[1:]))

# formula-safe unit column: <subject>_<pre|post> for DM1 samples, ctrl for controls (recorded mapping)
unit_map = {t: ("ctrl" if g == "ctrl" else f"{s}_{g}") for t, g, s in zip(dm.title, dm.grp, dm.subject)}
derived = native.derive_columns(dmeta_path, case.dir / "aligned" / "design_metadata_units.csv",
                                patterns={"unit": ("title", r"^(.*)$")}, recode={"unit": unit_map})
umeta_path = case.dir / "aligned" / "design_metadata_units.csv"
umeta = case.add_output(umeta_path, "design_metadata_units")
um = pd.read_csv(umeta_path, index_col=0)
dchk = native.design_check(um, ["unit"])
case.write_json("design_checks.json", {"derived_unit": derived, "design_check": dchk})
print("rank", dchk["rank"], "resid df", dchk["residual_df"])

coef = lambda u: f"C(unit)[{u}]"  # noqa: E731
contrasts = []
for s in subjects:
    for t in ("pre", "post"):
        contrasts.append({"name": f"{s}_{t}_vs_ctrl", "coefficients": {coef(f"{s}_{t}"): 1, coef("ctrl"): -1}})
for s in subjects:
    contrasts.append({"name": f"{s}_post_vs_pre", "coefficients": {coef(f"{s}_post"): 1, coef(f"{s}_pre"): -1}})
plan = {"analysis_type": "multilevel", "formula": "~ 0 + C(unit)", "contrasts": contrasts}
case.write_json("multigroup_plan.json", plan)

case.decide("design",
            final={"analysis_type": "multilevel: per-individual contrasts vs common control (n=1 arms)",
                   "formula": "~ 0 + C(unit)", "design_column": "unit",
                   "contrasts": [c["name"] for c in contrasts],
                   "estimand_type": ("individual descriptive change; <id>_pre/post_vs_ctrl associational; "
                                     "<id>_post_vs_pre = paper's individual Δlog2FC (post-vs-ctrl minus pre-vs-ctrl)"),
                   "derived_columns": derived},
            candidates=[{"value": "18 separate two-arm fits (paper)", "reason_rejected": "two-arm executors require "
                         ">=2 replicates per arm (tools/analysis_policy.py:16)"}],
            evidence=[paper, dmeta, umeta], paper={"locator": "S2.2.p2"}, confidence="medium",
            reasoning=("S2.2.p2/FIG1/S2.5.p1: the same pre/post-vs-control approach applied to each individual is the "
                       "paper's main analysis. One model with each DM1 sample as its own level estimates each "
                       "individual-vs-control log2FC and the individual post-minus-pre difference (= Δlog2FC)."))
case.decide("covariance",
            final={"status": "not_required", "blocking_terms": [],
                   "covariates": [{"name": "subject", "disposition": "excluded: absorbed - each unit is one "
                                   "subject x time sample; individual post_vs_pre contrasts are within-subject by "
                                   "construction"},
                                  {"name": "age", "disposition": "excluded: not in GEO metadata"}]},
            evidence=[umeta], confidence="medium",
            reasoning=f"Full rank ({dchk['rank']}), residual df {dchk['residual_df']} from the 6 controls.")
case.decide("method",
            final={"method": "limma (inmoose) moderated t, multilevel contrasts", "matrix_type": "raw counts",
                   "transform": "log2(CPM+1) via preprocess_counts (library-size CPM, no TMM)",
                   "formula": "~ 0 + C(unit)",
                   "prefilter": "preprocess_counts min_count=10, min_samples=1 (literal reading of S4.4.p1)",
                   "paper_route": {"method": "edgeR 3.34.1 QL F-test, each individual sample vs 6 controls",
                                   "status": "blocked",
                                   "reason": ("two-arm edgeR/DESeq2 executors reject a 1-sample arm "
                                              "(tools/analysis_policy.py:16 MIN_REPLICATES_PER_GROUP = 2); "
                                              "inmoose edgeR has no TMM")}},
            evidence=[amat, paper], paper={"locator": "S4.13.p1"}, confidence="medium",
            reasoning="Validated multigroup limma executor; variance from controls, as in the paper's fits.")
case.decide("threshold",
            final={"paper_threshold": PAPER_THRESHOLD, "threshold_source": "paper_on_deviation_route",
                   "applied_threshold": {"metric": "pvalue", "adjustment": "none", "cutoff": 0.05,
                                         "effect_metric": "log2FC", "effect_cutoff": 2.0, "inclusive": False}},
            evidence=[paper], paper={"locator": "S4.4.p1"}, confidence="high",
            reasoning="Paper's DEG rule (S4.4.p1, S2.5.p1) applied per contrast on the deviation route.")

# ---- execution
pdir = case.dir / "results" / "preprocess"
try:
    msg = native.call_tool("tools.preprocess_tools:preprocess_counts",
                           counts_csv=str(case.dir / "aligned" / "aligned_matrix.csv"),
                           output_dir=str(pdir), min_count=10, min_samples=1)
    print(msg)
    norm = native.find_outputs(pdir, "*_normalized.csv")[0]
    norm_item = case.add_output(norm, "log2cpm")
    mdir = case.dir / "results" / "multigroup"
    out = native.call_tool("tools.multigroup_tools:run_multigroup_analysis", expression_csv=norm,
                           metadata_csv=str(umeta_path), plan=plan, output_dir=str(mdir))
    counts = {}
    for r in out["results"]:
        a = native.apply_threshold(r["path"], metric="pvalue", cutoff=0.05, effect_cutoff=2.0, min_group_n=1)
        counts[r["name"]] = {k: a[k] for k in ("n_tested", "n_significant", "n_up", "n_down", "deg_sanity")}
    case.write_json("threshold_counts.json", counts)
    items = [case.add_output(r["path"], "deg_table") for r in out["results"]]
    case.decide("execution", execution_status="completed",
                final={"method": "limma (inmoose) moderated t, multilevel contrasts", "formula": "~ 0 + C(unit)",
                       "transform": "log2(CPM+1)", "outputs": [r["path"] for r in out["results"]],
                       "residual_df": out["residual_df"], "n_contrasts": out["n_contrasts"], "counts": counts},
                evidence=[norm_item] + items[:3], confidence="high",
                reasoning="27 contrasts from one fit; BH within contrast by executor; paper rule applied separately.")
except native.NativeToolError as e:
    print("FAILED", e)
    case.decide("execution", execution_status="failed",
                final={"method": "limma multilevel", "execution_error": str(e)},
                evidence=[amat], confidence="high", reasoning="executor failed")
    sys.exit(0)

# ---- paper-style per-individual rescue (S4.6.p1) and dysregulation scores (S4.7.p1) - arithmetic only
def tbl(name):
    t = pd.read_csv(mdir / f"DEG_results_{name}.csv", index_col=0)
    lfc = next(c for c in ("log2FoldChange", "logFC") if c in t.columns)
    p = next(c for c in ("pvalue", "P.Value", "PValue") if c in t.columns)
    return t[lfc], t[p]

rows = []
for s in subjects:
    lpre, ppre = tbl(f"{s}_pre_vs_ctrl")
    lpost, _ = tbl(f"{s}_post_vs_ctrl")
    lpost = lpost.reindex(lpre.index)
    dys = (ppre < 0.05) & (lpre.abs() > 2)
    pr = ((lpre - lpost) / lpre * 100)[dys]
    rows.append({"subject": s, "n_pre_DEGs": int(dys.sum()),
                 "rescued": int(((pr > 10) & (pr < 110)).sum()), "overrescued": int((pr >= 110).sum()),
                 "misrescued": int((pr < -10).sum()),
                 "pct_DEGs_rescued": round(100 * float(((pr > 10) & (pr < 110)).mean()), 1) if len(pr) else None,
                 "mean_percent_rescue": round(float(pr.mean()), 1) if len(pr) else None,
                 "dysreg_score_pre": round(float(lpre[dys].abs().mean()), 3),
                 "dysreg_score_post": round(float(lpost[dys].abs().mean()), 3)})
ind = pd.DataFrame(rows)
ipath = case.dir / "results" / "individual_rescue_summary.csv"
ind.to_csv(ipath, index=False)
case.add_output(ipath, "individual_rescue_summary")
print(ind.to_string())

# concordance with the authors' deposited individual sheets (downloaded separately; see report)
xlsx = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else None
if xlsx and xlsx.exists():
    conc = {}
    for sheet, t in (("individual pre-training", "pre"), ("individual post-training", "post")):
        a = pd.read_excel(xlsx, sheet_name=sheet).set_index("Ensembl ID")
        a = a[~a.index.duplicated()]
        for s in subjects:
            col = f"logFC.condition{s[1:]}_{t.capitalize()}"
            l, _ = tbl(f"{s}_{t}_vs_ctrl")
            j = a.index.intersection(l.index)
            conc[f"{s}_{t}"] = round(float(np.corrcoef(a.loc[j, col], l.loc[j])[0, 1]), 3)
    case.write_json("concordance_with_authors_individual.json", conc)
    print(conc)

case.decide("study", final={"route": "exploratory",
                            "exploratory_reason": "n=1 per individual arm (< 3 replicates); residual df 5",
                            "summary": "Paper's individual analysis reproduced with limma multilevel model"},
            evidence=[umeta], confidence="medium", reasoning="Singleton arms -> exploratory by contract rule.")
print(case.finish(n_deg=None, deg_sanity="tiny_n_per_group=1"))
