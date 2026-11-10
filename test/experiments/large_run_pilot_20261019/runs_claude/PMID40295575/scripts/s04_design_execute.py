"""Gates 5-9: design (suitability), covariance, method, threshold, execution (joint limma)."""
import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os, json, math, re
import pandas as pd
from tools import native

ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())
os.chdir(ROOT)
native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40295575"
run = native.RunRecorder.open(RUN)
case = run.case("GSE283250")
paper = case.evidence_item("paper:PMC12038050.paper.json")
A = case.dir / "aligned"
MAT = str(A / "aligned_matrix.csv")
DM = str(A / "design_metadata.csv")
am = case.add_output(MAT, "aligned_matrix")
dm_item = case.add_output(DM, "design_metadata")
dmeta = pd.read_csv(DM, index_col=0)
dmeta["animal_no"] = dmeta["title"].str.extract(r"\(no\. (\d+)\)")[0]

# Symbol-level sums for the sex check only (X/Y marker genes are looked up by symbol).
mat = pd.read_csv(MAT, index_col=0)
sym = pd.read_csv(RUN + "/GSE283250_merge/transcript_to_symbol.csv", index_col=0)["gene_symbol"]
sexdir = case.dir / "suitability_input"
sexdir.mkdir(exist_ok=True)
mat.groupby(sym.reindex(mat.index)).sum().to_csv(sexdir / "symbol_summed_counts.csv")

PT = {"metric": "pvalue", "adjustment": "none", "cutoff": 0.05, "effect_metric": "log2FC",
      "effect_cutoff": math.log2(1.3), "effect_cutoff_original": "fold change 1.3 (|FC| >= 1.3)",
      "inclusive": False, "test": "unpaired two-tailed Student's t-test per gene (ExDEGA)",
      "source_locator": "S4.11.p2; S2.3.p1; FIG3",
      "note": "paper wording 'cutoff of 1.3 x fold change (p < 0.05)'; p is strict; whether FC = 1.3 itself counts is "
              "not stated - applied as strict (> log2 1.3); no multiple-testing correction"}
PLANNED = ["grp_SS_vs_CON", "grp_SS_vs_SES", "grp_SES_vs_SER"]
PAPER_MAP = {"grp_SS_vs_CON": "Con versus SS (FIG3b; 2305 DEGs, 1301 up / 1004 down in SS, S2.3.p1)",
             "grp_SS_vs_SES": "SS versus SES (FIG3c, FIG5, FIG6): exercise effect in effective responders; log2FC = SS - SES, "
                              "so exercise-induced increases have negative log2FC",
             "grp_SES_vs_SER": "SES versus SER (FIG3d, FIG7, FIG8): responder difference; log2FC = SES - SER"}

# ---------------- 5. design
rep, suit_item, suit_summary = case.suitability(matrix_type="estimated counts", metadata=dmeta, factors=["grp"],
                                                matrix_csv=str(sexdir / "symbol_summed_counts.csv"), organism="Mouse",
                                                subject=None, references={"grp": "CON"}, planned=PLANNED)
names = [c["name"] for c in rep["comparisons"]]
print("verdict", rep["verdict"], rep["failed"], rep["warnings"]); print(names)
print(json.dumps(rep["checks"].get("sex", {}), default=str)[:600])
assert all(p in names for p in PLANNED), names
exploratory = [n for n in names if n not in PLANNED]
dc = native.design_check(DM, ["grp"])
dc_item = case.write_json("design_check.json", {"grp": dc}, role="design_check")
case.decide("design",
            final={"analysis_type": "multilevel (one factor, 4 independent groups, n = 3 each)",
                   "design_column": "grp", "formula": "~ 0 + grp", "reference": "CON",
                   "contrasts": [{"name": n, "role": ("planned" if n in PLANNED else "exploratory"),
                                  "paper": PAPER_MAP.get(n, "not in paper")} for n in names],
                   "planned": PLANNED, "exploratory": exploratory,
                   "exercise_contrasts": {"grp_SS_vs_SES": "planned (paper)", "grp_SS_vs_SER": "exploratory: exercise in ineffective responders"},
                   "estimand_type": "causal for exercise (VWR vs sedentary within SS mice), but responder status is a "
                                    "post-hoc behavioural stratification, so SES-vs-SER and each responder-specific exercise effect are conditional/associational",
                   "suitability": suit_summary, "levels": dc["levels"] if "levels" in dc else None},
            candidates=[{"value": "pool SES + SER as 'SS/Ex' vs SS", "reason_rejected": "paper never pools the responders in the RNA-seq; skill forbids pooling distinct levels"},
                        {"value": "separate 2-group fits per comparison (paper's t-tests)", "reason_rejected": "skill rule: one model on all samples for a k-level factor; recorded as a deviation at the method gate"}],
            evidence=[dm_item, suit_item, dc_item, paper], paper={"locator": "FIG3; S2.2.p3; S4.11.p2"}, confidence="high",
            reasoning=("Four independent groups of 3 male mice. The paper's three comparisons (FIG3) are planned; the suitability "
                       "report names them grp_SS_vs_CON, grp_SS_vs_SES and grp_SES_vs_SER (reference = alphabetical later-vs-earlier, "
                       "sign noted). The other three pairs (SER/SES vs CON, SS vs SER) run as exploratory from the same model; "
                       "SS vs SER is the exercise effect in ineffective responders."))

# ---------------- 6. covariance
conf = native.confounding_report(dmeta, "grp", ["animal_no"])
conf_item = case.write_json("confounding_report.json", conf, role="confounding_report")
case.decide("covariance",
            final={"status": "not_required", "blocking_terms": [],
                   "covariates": [{"name": "animal_no", "disposition": "excluded: animal numbers from the title (2,8,12 / 18,19,21 / 9,10,12 / 6,19,20) "
                                   "repeat across groups (12 in CON and SES; 19 in SS and SER) but SS sedentary, SES and SER are mutually exclusive "
                                   "treatments of different animals, so these are per-cohort labels, not repeated measures"},
                                  {"name": "batch / lane", "disposition": "excluded: not reported in paper or GEO"},
                                  {"name": "sex", "disposition": "excluded: all male (S4.1.p1); constant"}],
                   "rank": dc.get("rank"), "residual_df": dc.get("residual_df")},
            evidence=[dm_item, conf_item, dc_item, paper], paper={"locator": "S4.1.p1; S2.2.p3"}, confidence="medium",
            reasoning="One vHPC sample per animal, independent groups; no batch information exists. ~ 0 + grp is full rank with 8 residual df.")

# ---------------- 7. method
case.decide("method",
            final={"method": "limma (moderated t, empirical Bayes) joint model ~ 0 + grp on log2(CPM+1), all 12 samples, contrasts per comparison",
                   "matrix_type": "estimated counts", "transform": "log2(CPM+1)",
                   "formula": "~ 0 + grp", "pre_filter": "preprocess_counts: count >= 10 in >= 3 samples",
                   "feature_level": "RefSeq transcript rows (paper's unit: 33,299 'genes')",
                   "paper_route": {"method": "unpaired Student's t-test on cuffdiff geometric-normalized FPKM, separate 2-group tests (ExDEGA)",
                                   "status": "blocked",
                                   "reason": "FPKM not deposited (only cufflinks read counts); no plain Student's t-test executor in the repository"}},
            candidates=[{"value": "DESeq2 on the integer counts", "reason_rejected": "estimated (cufflinks) counts with undocumented rounding"},
                        {"value": "limma two-group fits per comparison", "reason_rejected": "skill: one model for a k-level factor; the paper's per-pair variance is approximated by the pooled limma variance"}],
            evidence=[am, dc_item, paper], paper={"locator": "S4.11.p2"}, confidence="medium",
            reasoning=("The paper's t-test on normalized FPKM cannot be reproduced: only counts are deposited. log2(CPM+1) is the "
                       "closest library-size normalization of the deposited data, and limma's moderated t is the validated "
                       "per-gene test available; it pools variance across the 4 groups. Declared deviation."))

# ---------------- 8. threshold
case.decide("threshold",
            final={"paper_threshold": PT, "threshold_source": "paper_on_deviation_route", "applied_threshold": dict(PT),
                   "deviation_note": "paper rule (raw p < 0.05, |FC| > 1.3) applied unchanged to limma moderated-t p-values instead of Student's t",
                   "audit_threshold": {"metric": "padj", "adjustment": "BH", "cutoff": 0.05, "effect_cutoff": None,
                                       "label": "audit: BH within contrast"}},
            evidence=[paper], paper={"locator": "S4.11.p2"}, confidence="high",
            reasoning="Paper: 1.3x fold change and p < 0.05 with Student's t-test, no correction. effect_cutoff = log2(1.3) = 0.378512.")

# ---------------- 9. execution
res = case.dir / "results"
pp = native.call_tool("tools.preprocess_tools:preprocess_counts", counts_csv=MAT, output_dir=str(res / "preprocess"))
print(pp)
norm = native.find_outputs(res / "preprocess", "*_normalized.csv")[0]
norm_item = case.add_output(norm, "log2cpm_matrix")
jl = native.call_tool("tools.joint_contrasts:run_joint_limma", expression_csv=str(norm), metadata_csv=DM,
                      comparisons=rep["comparisons"], output_dir=str(res / "joint_limma"))
print(json.dumps(jl, default=str)[:1500])
outs = {}
for f in sorted((res / "joint_limma").glob("*.csv")):
    print(f.name)
summary = {}
for n in names:
    cand = [f for f in (res / "joint_limma").glob("*.csv") if n in f.name and "metadata" not in f.name]
    assert len(cand) == 1, (n, cand)
    t = native.apply_threshold(cand[0], metric="pvalue", cutoff=0.05, effect_cutoff=math.log2(1.3), inclusive=False)
    a = native.apply_threshold(cand[0], metric="padj", cutoff=0.05)
    item = case.add_output(cand[0], f"de_{n}")
    outs[n] = str(cand[0])
    summary[n] = {"role": "planned" if n in PLANNED else "exploratory", "file": str(cand[0]),
                  "applied": t, "audit_bh005": {k: a[k] for k in a if k in ("n_significant", "n_up", "n_down", "n_tested")}}
    print(n, {k: t[k] for k in t if k in ("n_significant", "n_up", "n_down", "n_tested", "deg_sanity")}, "BH:", a["n_significant"])
ex_item = case.write_json("execution_results.json", summary, role="execution_results")
case.decide("execution",
            final={"method": "limma joint model ~ 0 + grp on log2(CPM+1) (run_joint_limma -> run_multigroup_analysis)",
                   "matrix_type": "estimated counts", "transform": "log2(CPM+1)", "formula": "~ 0 + grp",
                   "outputs": outs, "n_deg_applied": {n: summary[n]["applied"]["n_significant"] for n in names},
                   "n_deg_audit_bh": {n: summary[n]["audit_bh005"]["n_significant"] for n in names}},
            evidence=[norm_item, dm_item, ex_item], paper={"locator": "S4.11.p2"}, confidence="high",
            execution_status="completed",
            reasoning="All six contrasts from one limma fit on 12 samples; thresholds applied with native.apply_threshold.")
print("done")
