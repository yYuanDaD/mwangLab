import sys, pathlib, json; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os; os.chdir(sys.path[0])
from tools import native
native.enable_native_mode()
import pandas as pd
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID35456380"
run = native.RunRecorder.open(RUN); case = run.case("GSE164890")
P = "test/experiments/paper_screen_20261019/papers/"
paper = case.add_input(P + "PMC9027771.paper.md", "paper")
author_r = case.add_input(RUN + "/author_code/all_analysis_and_figures.R", "paper")
adir = case.dir / "aligned"
amd = case.add_output(adir / "design_metadata.csv", "design_metadata")
am = case.add_output(adir / "aligned_matrix.csv", "aligned_matrix")
dm = pd.read_csv(adir / "design_metadata.csv", index_col=0)

# ---------- design
rep, item, summary = case.suitability(matrix_type="raw counts", metadata=dm, factors=["time"],
    matrix_csv=str(adir / "aligned_matrix.csv"), organism="Human", subject="subject", planned=["time_post_vs_pre"],
    references={"time": "pre"})
assert summary["verdict"] == "analyzable", summary
case.decide("design", final={"analysis_type": "paired (repeated measures, 2 time points)", "design_column": "time",
    "control": "pre", "treatment": "post", "formula": "~ subject + time",
    "contrasts": ["time_post_vs_pre"], "estimand_type": "within-subject effect of the exercise bout",
    "suitability": summary, "suitability_matrix_type_note": "suitability run with 'raw counts' route family; the matrix is RSEM estimated counts rounded per the authors' recipe (matrix gate)"},
    evidence=[paper, author_r, amd, item], paper={"locator": "FIG1"}, confidence="high",
    candidates=[{"value": "~ time (unpaired post vs pre)", "reason_rejected": "ignores the 7 skaters sampled twice; the paper uses 'donor + exercise' (FIG1) and notes a strong donor effect (S3.2.p1)"},
                {"value": "ComBat-corrected rlog then test", "reason_rejected": "the paper uses ComBat only for PCA/plots (S2.5.p1); testing ComBat output inflates significance"}],
    reasoning="Seven skaters each sampled before and after the bout. The paper's estimand is the after-vs-before change with donor in the model (FIG1, S3.2.p1). Suitability: analyzable, one comparison time_post_vs_pre with 7 per arm; metadata sex (female, paper) agrees with X/Y expression for all 14 samples.")

# ---------- covariance
pr = native.pairing_report(dm, "subject", "time", ["pre", "post"])
cr = native.confounding_report(dm, "time", ["subject", "sex"])
dc = native.design_check(dm, ["subject", "time"], [])
print(json.dumps({"pairing": pr, "confounding": cr, "design": dc}, default=str)[:3000])
pair_item = case.write_json("covariance_checks.json", {"pairing": pr, "confounding": cr, "design_check": dc}, "tool_output")
case.decide("covariance", final={"status": "required", "blocking_terms": ["subject"],
    "covariates": [{"name": "subject", "disposition": "included (blocking, 7 levels)"},
                   {"name": "sex", "disposition": "excluded: single level (all female)"}],
    "pairing": pr, "design_check": dc},
    evidence=[amd, pair_item, paper], paper={"locator": "FIG1"}, confidence="high",
    reasoning="All 7 subjects have exactly one pre and one post sample. subject is crossed with time; ~ subject + time is full rank with residual df = 14 - 8 = 6. No batch or other covariate is recorded; sex is constant.")

# ---------- method
case.decide("method", final={"method": "DESeq2 (pydeseq2, Wald test, refit Cooks)", "matrix_type": "estimated counts (RSEM expected counts)",
    "formula": "~ subject + time", "contrast": "time post vs pre", "rounding_documented": True,
    "transform": "round(x, 0), half to even, as in the authors' script (line 66); no gene prefilter beyond dropping all-zero genes",
    "alpha": 0.1, "paper_route": {"method": "DESeq2 ~ donor + exercise on round(RSEM counts)", "status": "reproduced"}},
    evidence=[paper, author_r, am], paper={"locator": "S2.5.p1"}, confidence="high",
    reasoning="Paper and authors' script use DESeq2 on rounded RSEM gene counts with donor + exercise. The executor's alpha is set to the paper's FDR 0.1 so independent filtering matches R's results() default.")

# ---------- threshold
pt = {"metric": "padj", "adjustment": "BH (DESeq2 results() default)", "cutoff": 0.1, "effect_metric": None,
      "effect_cutoff": None, "inclusive": True, "source_locator": "S2.5.p1; FIG1; author script lines 83-84"}
case.decide("threshold", final={"paper_threshold": pt, "threshold_source": "paper", "applied_threshold": dict(pt)},
    evidence=[paper, author_r], paper={"locator": "S2.5.p1"}, confidence="high",
    reasoning="Paper: genes retained at FDR < 0.1 (S2.5.p1), 'reported at 10% FDR' (FIG1); the script counts padj <= 0.1 with no fold-change cutoff. Applied exactly.")
