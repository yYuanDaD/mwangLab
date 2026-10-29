import sys, pathlib, json, math; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os; os.chdir(ROOT)
from tools import native
native.enable_native_mode()

RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID32625117"
run = native.RunRecorder.open(RUN)
case = run.case("PMID32625117")
al = case.dir / "aligned"
PM = al / "pd_pairs" / "paired_matrix.csv"
PMETA = al / "pd_pairs" / "paired_metadata.csv"
paper = case.evidence_item("paper:PMC7311784.paper.md")
meta = case.evidence_item("metadata:GSE140089_metadata.csv")
mat = case.evidence_item("matrix:GSE140089_featureCounts.txt.gz")
pmx = case.add_output(PM, "paired_matrix")
pmeta = case.add_output(PMETA, "paired_metadata")

# ---- matrix
prof = native.profile_matrix(PM)
import pandas as pd, numpy as np
x = pd.read_csv(PM, index_col=0)
colsum = x.sum().round(0).to_dict()
frac = x.values[x.values != np.round(x.values)]
dec2 = bool(np.allclose(frac * 100, np.round(frac * 100)))
prof_ev = case.write_json("matrix_profile.json", {"profile": prof, "column_sums": colsum, "nonint_values_have_2_decimals": dec2,
                                                  "ERCC_rows": int(x.index.str.startswith("ERCC").sum())}, role="matrix_profile")
case.decide("matrix", final={"matrix_type": "estimated counts (fractional featureCounts read counts)",
                             "recommended_method": "limma on log2(CPM+1) with subject blocking (integer-only count methods refused: rounding not documented)",
                             "rounding_documented": False,
                             "evidence_summary": {"integer_fraction": prof["integer_fraction"], "min": prof["min"], "max": prof["max"],
                                                  "column_sum_range": [min(colsum.values()), max(colsum.values())],
                                                  "paper_read_depth": "25.5 M read pairs average (S2.5.p1)", "ERCC_rows": 0,
                                                  "ids": "versioned Ensembl gene IDs (GENCODE)"}},
            evidence=[pmx, mat, meta, paper, prof_ev], confidence="high", paper={"locator": "S2.5.p1"},
            candidates=[{"value": "raw integer counts", "reason_rejected": "7.8% of values non-integer (e.g. 0.1, 7.29); not a pure integer matrix"},
                        {"value": "FPKM/TPM/CPM", "reason_rejected": "column sums 14-35 M track sequencing depth (paper avg 25.5 M pairs), not a normalized constant; GEO says 'counts of reads'; featureCounts output"}],
            reasoning="featureCounts read counts with fractional assignment (2-decimal values, e.g. multi-mapping --fraction); library sums equal read depth. Treated as estimated counts: count-scale, but DESeq2/edgeR/voom executors require integers and no rounding recipe is documented.")

# ---- design
case.decide("design", final={"analysis_type": "paired", "design_column": "time", "control": "pre", "treatment": "post",
                             "formula": "~ subject + time",
                             "contrasts": [{"name": "post_vs_pre", "coefficient": "time[T.post]"}],
                             "samples": "5 PD subjects x {pre, post} = 10"},
            evidence=[paper, pmeta], confidence="high", paper={"locator": "S2.6.p1"},
            candidates=[{"value": "PD basal (12) vs OA/YA", "reason_rejected": "disease/age comparison, not the exercise estimand; PLIER-only in paper"},
                        {"value": "unpaired post (5) vs all basal PD (12)", "reason_rejected": "paper compares within the five subjects; mixes non-trained subjects"}],
            reasoning="Paper: pre vs post 16-wk RT compared within the five PD subjects (S2.6.p1); repeated measure on subject.")

# ---- covariance
pr = native.pairing_report(PMETA, "subject", "time", ["pre", "post"])
cf = native.confounding_report(PMETA, "time", ["subject", "characteristics_ch1.3.Sex", "characteristics_ch1.2.age"])
dc = native.design_check(PMETA, ["subject", "time"])
print("pairing", json.dumps(pr, default=str)[:400]); print("confound", json.dumps(cf, default=str)[:800]); print("design", json.dumps(dc, default=str)[:500])
cov_ev = case.write_json("covariance_reports.json", {"pairing": pr, "confounding": cf, "design_check": dc}, role="covariance_reports")
case.decide("covariance", final={"status": "required", "blocking_terms": ["subject"],
                                 "covariates": [{"name": "subject", "disposition": "included"},
                                                {"name": "sex", "disposition": "excluded: constant within subject; absorbed by subject block"},
                                                {"name": "age", "disposition": "excluded: constant within subject; absorbed by subject block"}],
                                 "design_rank": dc.get("rank"), "residual_df": dc.get("residual_df")},
            evidence=[pmeta, cov_ev, paper], confidence="high", paper={"locator": "S2.6.p1"},
            candidates=[{"value": "~ time", "reason_rejected": "ignores within-subject pairing stated in S2.6.p1"}],
            reasoning="5 complete pairs, no duplicates; subject is crossed with time; ~ subject + time full rank with 4 residual df.")

# ---- method
case.decide("method", final={"method": "limma (moderated t, eBayes) on log2(CPM+1), subject as blocking covariate",
                             "matrix_type": "estimated counts (fractional featureCounts read counts)",
                             "transform": "log2(CPM+1) via preprocess_counts (filter: count>=10 in >=5 of 10 samples)",
                             "formula": "~ subject + time", "coefficient": "time post vs pre",
                             "paper_route": {"method": "limma-voom (paired, within subject)", "status": "blocked",
                                             "reason": "run_limma_voom_analysis takes no covariates/blocking (two-arm only) and, with DESeq2/edgeR, refuses non-integer counts; matrix holds fractional counts with no documented rounding"}},
            evidence=[paper, pmx, cov_ev], confidence="medium", paper={"locator": "S2.6.p1"},
            candidates=[{"value": "limma-voom unpaired", "reason_rejected": "drops pairing; also refuses non-integer counts"},
                        {"value": "DESeq2 ~ subject + time on rounded counts", "reason_rejected": "rounding recipe not documented; further from paper's limma route"}],
            reasoning="Closest available route to paired limma-voom: same limma linear model with subject blocking, on log2(CPM+1) (limma-trend style, without voom precision weights). Declared deviation.")

# ---- threshold
pt = {"metric": "FDR", "adjustment": "BH", "cutoff": 0.05, "effect_metric": None, "effect_cutoff": None, "inclusive": False,
      "source_locator": "S2.6.p1; S3.1.p1; FIG1"}
case.decide("threshold", final={"paper_threshold": pt, "threshold_source": "paper_on_deviation_route",
                                "applied_threshold": {"metric": "padj", "adjustment": "BH", "cutoff": 0.05, "effect_metric": None, "effect_cutoff": None, "inclusive": False},
                                "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0,
                                                    "label": "paper interpretation rule (S2.6.p1; FIG1: 42 up / 29 down)"}},
            evidence=[paper], confidence="high", paper={"locator": "S3.1.p1"},
            reasoning="Paper's DEG call (706 = 304 up / 402 down) is BH FDR<0.05 without fold-change filter; |log2FC|>1 is a secondary interpretation filter, reported as audit.")

# ---- execution
res = case.dir / "results"
exec_final = {"method": "limma on log2(CPM+1), ~ subject + time"}
try:
    msg = native.call_tool("tools.preprocess_tools:preprocess_counts", counts_csv=str(PM), output_dir=str(res / "preprocess"), min_count=10, min_samples=5)
    print(msg[:600])
    norm = native.find_outputs(res / "preprocess", "*_normalized.csv")[0]
    print("norm", norm, pd.read_csv(norm, index_col=0).shape)
    msg2 = native.call_tool("tools.limma_tools:run_limma_analysis", normalized_csv=norm, metadata_csv=str(PMETA), design_column="time",
                            control_group="pre", treatment_group="post", output_dir=str(res / "limma"), covariate_columns="subject")
    print(msg2[:1200])
    deg = [p for p in native.deg_outputs(res / "limma") if pathlib.Path(p).name.startswith("DEG_results_")][0]
    main = native.apply_threshold(deg, metric="padj", cutoff=0.05, effect_cutoff=None)
    aud = native.apply_threshold(deg, metric="padj", cutoff=0.05, effect_cutoff=1.0)
    print("MAIN", json.dumps(main, default=str)[:700]); print("AUDIT", json.dumps(aud, default=str)[:700])
    o1 = case.add_output(norm, "normalized_matrix"); o2 = case.add_output(deg, "deg_table")
    case.write_json("threshold_counts.json", {"applied": main, "audit_log2fc1": aud}, role="threshold_counts")
    exec_final.update({"outputs": [o1["path"], o2["path"]], "n_genes_tested": main.get("n_tested"),
                       "applied_counts": {k: main.get(k) for k in ("n_significant", "n_up", "n_down")},
                       "audit_counts": {k: aud.get(k) for k in ("n_significant", "n_up", "n_down")}})
    case.decide("execution", final=exec_final, evidence=[o1, o2], confidence="high", execution_status="completed",
                reasoning="preprocess_counts then run_limma_analysis with covariate_columns=subject completed.")
    (case.dir / "stage3_state.json").write_text(json.dumps({"deg": deg, "main": main, "audit": aud}, default=str, indent=1), encoding="utf-8")
except native.NativeToolError as e:
    print("EXEC FAILED", e)
    exec_final["execution_error"] = str(e)
    case.decide("execution", final=exec_final, evidence=[pmx], confidence="high", execution_status="failed", reasoning="tool failed")
