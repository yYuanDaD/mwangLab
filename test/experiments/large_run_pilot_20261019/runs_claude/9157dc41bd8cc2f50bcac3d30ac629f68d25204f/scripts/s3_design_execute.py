import sys, pathlib, json; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os; os.chdir(ROOT)
import numpy as np, pandas as pd
from tools import native
native.enable_native_mode()
RUN = pathlib.Path(__file__).resolve().parents[1]
run = native.RunRecorder.open(RUN)
case = run.case("GSE134698")
A = case.dir / "aligned"
paper = case.evidence_item("paper:9157dc41bd8cc2f50bcac3d30ac629f68d25204f.paper.md")
am = {"id": "aligned_matrix", "kind": "matrix", "path": str(A / "aligned_matrix.csv")}
am = case.add_output(str(A / "aligned_matrix.csv"), "aligned_matrix")
dm = case.add_output(str(A / "design_metadata.csv"), "design_metadata")
prof = case.add_output(str(A / "matrix_profile.json"), "tool_output")

case.decide("matrix", final={"matrix_type": "raw counts", "recommended_method": "DESeq2",
                             "evidence_summary": "integer_fraction 1.0, no negatives, max 67406, median 0; library sums 0.72-1.09M match ~0.93M reads/sample (S0.p44); file is featureCounts output with Length column; no ERCC rows; GEO data_processing: featureCounts -> DESeq2",
                             "paper_input": "featureCounts counts into DESeq2 (S0.p45, S0.p46)"},
            evidence=[am, prof, paper], paper={"locator": "S0.p45"},
            reasoning="Values, file provenance and paper all indicate unnormalized featureCounts gene counts.", confidence="high")

d = pd.read_csv(A / "design_metadata.csv", index_col=0)
case.decide("design", final={"analysis_type": "paired", "design_column": "time", "control": "before", "treatment": "after",
                             "formula": "~ subject + time", "contrasts": [{"name": "after_vs_before", "numerator": "after", "denominator": "before"}],
                             "estimand_type": "within_subject_change"},
            candidates=[{"value": "~ time (unpaired)", "reason_rejected": "paper normalizes in pairs per patient (S0.p46); ignores subject pairing"},
                        {"value": "characteristics_ch1.6.treatment as design column", "reason_rejected": "one-to-one with time; time chosen as the paper's before/after framing"}],
            evidence=[dm, paper], paper={"locator": "S0.p46"},
            reasoning="Three patients sampled before and after 12 weeks of training; paper compares two states within patient pairs.", confidence="high")

pair = native.pairing_report(d, "subject", "time", ["before", "after"])
conf = native.confounding_report(d, "time", ["subject", "characteristics_ch1.2.age", "characteristics_ch1.3.bmi"])
dchk = native.design_check(d, ["subject", "time"])
print(json.dumps({"pair": pair, "conf": conf, "dchk": dchk}, indent=1, default=str)[:3000])
json.dump({"pairing": pair, "confounding": conf, "design_check": dchk}, open(A / "covariance_reports.json", "w", encoding="utf-8"), indent=1, default=str)
cov_ev = case.add_output(str(A / "covariance_reports.json"), "tool_output")
case.decide("covariance", final={"status": "required", "blocking_terms": ["subject"],
                                 "covariates": [{"name": "subject", "disposition": "included"},
                                                {"name": "age", "disposition": "nested: subject-level constant, absorbed by subject block"},
                                                {"name": "bmi", "disposition": "nested: subject-level constant, absorbed by subject block"}],
                                 "residual_df": dchk.get("residual_df")},
            evidence=[dm, cov_ev, paper], paper={"locator": "S0.p46"},
            reasoning="3 complete pairs; subject is crossed with time; ~ subject + time is full rank with 2 residual df.", confidence="high")

# value-changing feature selection (paper S0.p45-46): top 12,000 genes by mean of quantile-normalized log2(count+1)
counts = pd.read_csv(A / "aligned_matrix.csv", index_col=0)
logc = np.log2(counts + 1)
ranks = logc.rank(axis=0, method="first")
ref = np.sort(logc.values, axis=0).mean(axis=1)
qn = logc.copy()
for c in logc.columns:
    qn[c] = ref[(ranks[c].values - 1).astype(int)]
mean_qn = qn.mean(axis=1)
order = mean_qn.sort_values(ascending=False, kind="mergesort")
top = order.index[:12000]
print("12000th mean qn log2", order.iloc[11999], "ties at boundary", int((order == order.iloc[11999]).sum()),
      "min total count in top", int(counts.loc[top].sum(axis=1).min()))
filt = counts.loc[top]
filt.to_csv(A / "counts_top12000.csv")
fsel = case.add_output(str(A / "counts_top12000.csv"), "matrix")

method_final = {"method": "DESeq2 (pydeseq2, Wald test, ~ subject + time)", "matrix_type": "raw counts",
                "formula": "~ subject + time", "coefficient": "time after vs before",
                "feature_selection": "top 12,000 genes by mean quantile-normalized log2(count+1) (paper S0.p45-46); DESeq2 run on raw counts of these genes",
                "implementation_note": "paper used R DESeq2; pydeseq2 port used here"}
case.decide("method", final=method_final, evidence=[am, fsel, paper], paper={"locator": "S0.p46"},
            reasoning="Paper route is DESeq2 with per-patient pairing on the 12k most expressed genes; data are raw counts, so the route is reproducible.", confidence="medium")

pt = {"metric": "padj", "adjustment": "BH", "cutoff": 0.1, "effect_metric": None, "effect_cutoff": None,
      "inclusive": False, "source_locator": "S0.p46"}
case.decide("threshold", final={"paper_threshold": pt, "threshold_source": "paper", "applied_threshold": dict(pt),
                                "note": "paper writes 'FDR = 0.1'; strict < used (all TAB2 genes have padj < 0.1); no FC cutoff"},
            evidence=[paper], paper={"locator": "S0.p46"}, reasoning="BH FDR 0.1, no effect-size rule.", confidence="high")

out = case.dir / "results" / "deseq2"
out.mkdir(parents=True, exist_ok=True)
try:
    msg = native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=str(A / "counts_top12000.csv"),
                           metadata_csv=str(A / "design_metadata.csv"), design_column="time", control_group="before",
                           treatment_group="after", output_dir=str(out), covariate_columns="subject")
    print(msg[-1500:])
    deg = [p for p in native.deg_outputs(out) if pathlib.Path(p).name.startswith("DEG_results_")][0]
    cnts = native.apply_threshold(deg, metric="padj", cutoff=0.1, effect_cutoff=None, min_group_n=3)
    print(cnts)
    degrec = case.add_output(str(deg), "tool_output")
    case.decide("execution", final={"method": method_final["method"], "formula": "~ subject + time",
                                    "outputs": [str(deg)], "threshold_counts": cnts},
                evidence=[fsel, dm, degrec], reasoning="DESeq2 completed.", confidence="high",
                execution_status="completed")
except native.NativeToolError as e:
    print("EXEC FAILED", e)
    case.decide("execution", final={"method": method_final["method"], "execution_error": str(e)},
                evidence=[fsel, dm], reasoning="DESeq2 failed.", confidence="high", execution_status="failed")
