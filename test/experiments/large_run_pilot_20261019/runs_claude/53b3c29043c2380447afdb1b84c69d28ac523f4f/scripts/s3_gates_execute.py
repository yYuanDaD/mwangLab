import sys, os, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT)); os.chdir(ROOT)
import pandas as pd
from tools import native
native.enable_native_mode()

RUN = str(pathlib.Path(__file__).resolve().parents[1].relative_to(ROOT))
run = native.RunRecorder.open(RUN)
case = run.case("case_01")
paper = case.evidence_item("paper:PMC10614785.paper.md")
AL = case.dir / "aligned"
MATP = str(AL / "aligned_matrix.csv"); DMP = str(AL / "design_metadata.csv")
mat = case.evidence_item("tool_output:aligned_matrix.csv")
dmeta = case.evidence_item("tool_output:design_metadata.csv")
prof = json.load(open(case.dir / "matrix_profile.json", encoding="utf-8"))

# ---- matrix
case.decide("matrix", final={"matrix_type": "raw counts", "recommended_method": "DESeq2",
            "evidence": {"integer_fraction": prof["integer_fraction"], "min": prof["min"], "max": prof["max"],
                         "negative_values": prof["negative_values"], "missing_values": prof["missing_values"],
                         "library_size_range": [8045154, 11269812], "ERCC_rows": 0,
                         "duplicated_feature_ids": prof["duplicated_feature_ids"],
                         "geo_processing": "Supplementary files format and content: tab-delimited text file includes raw counts for each sample",
                         "feature_ids": "gene symbols (Partek annotation, Ensembl 99)"},
            "paper_input": "DESeq2 median-of-ratios on gene counts (S2.11.p1) — consistent"},
            evidence=[mat, dmeta, paper], confidence="high", paper={"locator": "S2.11.p1"},
            reasoning="All values non-negative integers, unequal library sizes (8.0–11.3M; normalized integers would not "
                      "differ this way), GEO processing note says raw counts; paper ran DESeq2 on counts.")

# ---- design
design = {"analysis_type": "two_group_stratified",
          "factors": {"geno": ["veh", "ko"], "ex": ["ctrl", "ex"]},
          "design_column": "grp",
          "contrasts": [{"name": "vehicle_ex_vs_ctrl", "control": "veh_ctrl", "treatment": "veh_ex",
                         "stratum": "geno == veh"},
                        {"name": "ko_ex_vs_ctrl", "control": "ko_ctrl", "treatment": "ko_ex",
                         "stratum": "geno == ko"}],
          "estimand_type": "causal (randomized acute exercise bout, S2.2.p3)",
          "interaction": "not planned: paper compares genotypes by DEG overlap (FIG1D), not by an interaction test"}
case.decide("design", final=design, evidence=[dmeta, paper], confidence="high", paper={"locator": "S3.1.p1"},
            candidates=[{"value": "pooled ex vs ctrl across genotypes (~ geno + ex)",
                         "reason_rejected": "paper's estimand is the exercise response within each genotype; pooling hides the genotype-specific response"},
                        {"value": "genotype contrast ko vs veh", "reason_rejected": "does not answer the exercise question"},
                        {"value": "geno:ex interaction", "reason_rejected": "not reported by the paper; would be a new estimand"}],
            reasoning="2x2 factorial (genotype x acute exercise), n=5 per cell. The paper reports exercise DEGs within each "
                      "genotype; each contrast is a simple effect of exercise in one genotype stratum.")

# ---- covariance
conf = native.confounding_report(DMP, "grp", candidates=["time_src", "geno"])
dc = {}
for g in ["veh", "ko"]:
    sub = pd.read_csv(DMP, index_col=0)
    sub = sub[sub["geno"] == g]
    dc[g] = native.design_check(sub, ["ex"])
print(json.dumps(conf, default=str)[:1200]); print(json.dumps(dc, default=str)[:1200])
case.decide("covariance", final={"status": "not_required", "blocking_terms": [],
            "covariates": [{"name": "time_src", "disposition": "excluded: it labels the arm itself (exercised mice sampled "
                            "1 h post bout, controls collected alongside as time-of-day-matched, S2.6.p1); not a nuisance variable"},
                           {"name": "geno", "disposition": "excluded: constant within each stratum (stratification variable)"},
                           {"name": "age_cohort", "disposition": "excluded: all sequenced mice from the ~30-week cohort (S2.10.p1); no column in GEO"}],
            "confounding_report": conf, "design_check": dc},
            evidence=[dmeta, paper], confidence="high", paper={"locator": "S2.10.p1"},
            reasoning="Independent mice, one sample per mouse; no subject, batch or cohort variable in the sequenced set. "
                      "Each stratum design ~ ex is full rank with 8 residual df.")

# ---- method
case.decide("method", final={"method": "DESeq2 (pydeseq2, Wald test, median-of-ratios)", "matrix_type": "raw counts",
            "formula": "~ ex (within each genotype stratum)",
            "fit_set": "10 samples per contrast (the executor fits the two requested arms only)",
            "duplicate_ids": "106 duplicated gene symbols collapsed by the executor to the highest-mean row",
            "paper_route_note": "paper used Partek Flow DESeq2 Wald; whether all 20 samples were fitted jointly is not reported"},
            evidence=[mat, paper], confidence="high", paper={"locator": "S2.11.p1"},
            candidates=[{"value": "DESeq2 ~ grp on all 20 samples with two contrasts",
                         "reason_rejected": "repository DESeq2 executor fits only the two requested arms; fit set not stated in paper"},
                        {"value": "limma multigroup on log2(CPM+1)", "reason_rejected": "changes the paper's method"}],
            reasoning="Raw integer counts; paper method is DESeq2 Wald, which the data support.")

# ---- threshold
pt = {"metric": "qvalue", "adjustment": "FDR (DESeq2 Wald, Partek Flow; BH assumed)", "cutoff": 0.05, "inclusive": False,
      "effect_metric": None, "effect_cutoff": None, "source_locator": "S3.1.p1"}
applied = {"metric": "padj", "adjustment": "BH", "cutoff": 0.05, "inclusive": False, "effect_metric": None, "effect_cutoff": None}
case.decide("threshold", final={"paper_threshold": pt, "threshold_source": "paper", "applied_threshold": applied},
            evidence=[paper], confidence="high", paper={"locator": "S3.1.p1"},
            reasoning="Paper: 'q < 0.05' for the acute exercise DEG counts, no fold-change cutoff.")

# ---- execution
results = {}
for c in design["contrasts"]:
    out = case.dir / "results" / c["name"]
    try:
        msg = native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=MATP, metadata_csv=DMP,
                               design_column="grp", control_group=c["control"], treatment_group=c["treatment"],
                               output_dir=str(out))
        print(msg)
        deg = [p for p in native.deg_outputs(out) if pathlib.Path(p).name.startswith("DEG_results_")][0]
        cnt = native.apply_threshold(deg, metric="padj", cutoff=0.05, effect_cutoff=None, inclusive=False)
        print(c["name"], {k: cnt.get(k) for k in ["n_tested", "n_significant", "n_up", "n_down", "deg_sanity"]})
        o = case.add_output(deg, f"deg_{c['name']}")
        case.decide("execution", final={"method": "DESeq2", "subset": c["name"], "outputs": [o["path"]],
                    "counts_applied_threshold": cnt}, evidence=[mat, dmeta, o], confidence="high",
                    execution_status="completed", paper={"locator": "S3.1.p1"},
                    reasoning=f"DESeq2 Wald {c['treatment']} vs {c['control']}; counted with apply_threshold padj<0.05.")
        results[c["name"]] = {"deg": str(deg), **{k: cnt.get(k) for k in ["n_tested", "n_significant", "n_up", "n_down", "deg_sanity"]}}
    except native.NativeToolError as e:
        print("FAILED", c["name"], e)
        case.decide("execution", final={"method": "DESeq2", "subset": c["name"], "execution_error": str(e)},
                    evidence=[mat, dmeta], confidence="high", execution_status="failed",
                    reasoning="DESeq2 executor failed.")
        results[c["name"]] = {"error": str(e)}
json.dump(results, open(case.dir / "results" / "deg_counts.json", "w", encoding="utf-8"), indent=1, default=str)
