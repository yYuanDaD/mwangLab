import sys, os, json; sys.path.insert(0, r"E:\agent\mwangLab_pdf"); os.chdir(r"E:\agent\mwangLab_pdf")
import pandas as pd
from tools import native
native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/0ae9854294e3cff10bf3aa42f2416e5d3e9bed4a"
REQ = ("Use the bioinformatics-workflow skill to analyze GSE152133 for PMID 37876943 and determine how exercise "
       "affects gene expression as the paper intends.")
run = native.RunRecorder(RUN, request=REQ, platform_name="claude-code",
                         decision_maker="Claude Code subagent (claude-opus-5-5)", case_ids=["case_01"])
case = run.case("case_01", accession="GSE152133")
P = "test/experiments/paper_screen_20261019/papers/"
paper = case.add_input(P + "PMC10597580.paper.json", "paper")
paper_md = case.add_input(P + "PMC10597580.paper.md", "paper")
META = "data/GSE152133/GSE152133_metadata.csv"; MAT = "data/GSE152133/GSE152133_full.read.counts.tsv.gz"
meta = case.add_input(META, "metadata"); mat = case.add_input(MAT, "matrix")

paper_threshold = {"metric": "padj", "adjustment": "BH (DESeq2 default)", "cutoff": 0.05, "inclusive": True,
                   "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "effect_inclusive": True,
                   "source_locator": "S3.1.1.p2"}
recon = {
  "accessions": ["GSE152133"],
  "assay": "bulk RNA-seq (poly-A, NextSeq 550, 75bp SE), tibialis anterior, STAR GeneCounts",
  "organism": "Mus musculus, male C57BL/6",
  "factors": [{"name": "age", "levels": ["6m", "24m", "28m"], "locator": "S2.1.p1"},
              {"name": "sequencing_run", "levels": ["run1 (6m vs 24m)", "run2 (6m vs 28m)"], "locator": "S2.4.p1"}],
  "exercise_factor": "none: no exercise intervention or exercise arm; exercise capacity (treadmill, voluntary wheel) "
                     "was only measured as part of the CFAB function score on all mice (S2.2.p1)",
  "sample_inclusion": "n=7 6m, 7 24m, 8 28m (one 6m and one 24m RNA failed QC); 6m libraries prepared twice, once per run, "
                      "technical replicates kept separate (S2.3.p2, S2.4.p1)",
  "primary_estimand": "age effect on TA gene expression (28m vs 6m within run2; 24m vs 6m within run1), then "
                      "association of DEG expression with CFAB functional score (S3.2.p2)",
  "planned_contrasts": [{"name": "28m_vs_6m", "locator": "S4.1.1.1.p1", "paper_counts": {"up": 605, "down": 612}},
                        {"name": "24m_vs_6m", "locator": "S4.1.1.2.p1", "paper_counts": {"up": 130, "down": 8}},
                        {"name": "DEG-vs-CFAB linear regression", "locator": "S3.2.p2"}],
  "repeated_measure_unit": "none for biology (one TA per mouse); 6m mice sequenced in both runs",
  "normalization": "DESeq2 size factors; rlog for PCA/heatmap (S3.1.1.p2)",
  "method": "DESeq2 1.22.2 (S3.1.1.p2)",
  "paper_threshold": paper_threshold,
  "requested_estimand": "effect of exercise on gene expression",
  "requested_estimand_in_paper": "not_reported (no exercise contrast; exercise appears only as a functional test and in "
                                 "discussion of external exercise datasets, S5.8.p2)",
}
case.write_json("paper_reconstruction.json", recon)
case.decide("paper_reconstruction", final=recon, evidence=[paper, paper_md], confidence="high",
            paper={"locator": "S2.4.p1"},
            reasoning="Paper is a cross-sectional aging study (6m/24m/28m male mice) with DESeq2 age contrasts and a "
                      "DEG~CFAB regression; no exercise intervention exists.")

m = pd.read_csv(META, index_col=0)
own = {"accession": "GSE152133", "matrix_file": MAT, "metadata_file": META, "owned": True,
       "checks": {"series_id": sorted(m["series_id"].astype(str).unique().tolist()),
                  "n_gsm": len(m), "age_counts": m["characteristics_ch1.0.age"].value_counts().to_dict(),
                  "run_counts": m["characteristics_ch1.1.type"].value_counts().to_dict(),
                  "paper": "7x6m (sequenced twice) + 7x24m + 8x28m = 29 libraries; GEO 29 GSMs; S4.1.1 title cites GSE152133"}}
case.decide("ownership", final=own, evidence=[paper, meta, mat], confidence="high", paper={"locator": "S10.p1"},
            reasoning="Series ID, library counts per age and run match the paper; supplementary counts file is the series' only matrix.")

aln = native.align_to_metadata(MAT, META, case.dir / "aligned", key_column="title")
print({k: v for k, v in aln.items() if k != "outputs"})
am = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
amd = case.add_output(aln["outputs"]["aligned_metadata"]["path"], "aligned_metadata")
der = native.derive_columns(aln["outputs"]["aligned_metadata"]["path"], case.dir / "aligned" / "design_metadata.csv",
    aliases={"age_raw": "characteristics_ch1.0.age", "run_raw": "characteristics_ch1.1.type"},
    patterns={"mouse": ("title", r"^(A\d+[A-Z]?)(?:_repeat)?$")},
    recode={"age_raw": {"adult (6 months old)": "m6", "older adults (24 months old)": "m24", "older adults (28 months old)": "m28"},
            "run_raw": {"First NextSeq550 Run": "run1", "Second NextSeq550 Run": "run2"}})
dm = case.add_output(case.dir / "aligned" / "design_metadata.csv", "design_metadata")
case.decide("alignment", final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
            "coverage": aln["coverage"], "unmatched_matrix_columns": aln["unmatched_matrix_columns"],
            "unmatched_metadata_samples": aln["unmatched_metadata_samples"], "derived_columns": der},
            evidence=[mat, meta, am, amd, dm], confidence="high",
            reasoning="Matrix columns are GEO titles (A22L, A22L_repeat, ...); exact match on title.")

prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
print({k: prof[k] for k in ["n_features", "n_samples", "min", "max", "integer_fraction", "missing_values", "candidates"]})
case.decide("matrix", final={"matrix_type": "raw counts", "recommended_method": "DESeq2",
            "profile": {k: prof[k] for k in ["n_features", "n_samples", "min", "max", "median", "integer_fraction",
                                             "missing_values", "negative_values", "duplicated_feature_ids"]},
            "paper_input": "STAR --quantMode GeneCounts read counts into DESeq2 (S3.1.1.p1-p2)"},
            evidence=[am, mat], confidence="high", paper={"locator": "S3.1.1.p1"},
            reasoning="All-integer non-negative values; file named full.read.counts; paper used STAR GeneCounts into DESeq2.")
d = pd.read_csv(case.dir / "aligned" / "design_metadata.csv", index_col=0)
print(pd.crosstab(d["age_raw"], d["run_raw"]))
