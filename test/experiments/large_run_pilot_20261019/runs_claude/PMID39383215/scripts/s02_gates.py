import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os, json
import pandas as pd
from tools import native

ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())
os.chdir(ROOT)
native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID39383215"
REQUEST = ("Analyze GSE245048 for PMID 39383215 (Loss of atrial natriuretic peptide signaling causes insulin "
           "resistance, mitochondrial dysfunction, and low endurance capacity): how exercise affects gene "
           "expression as the paper intends.")
CASE = "GSE245048_exercise"
run = native.RunRecorder(RUN, request=REQUEST, platform_name="claude-code",
                         decision_maker="Claude Opus 5.5 (claude-opus-5-5[1m]) subagent", case_ids=[CASE])
case = run.case(CASE, accession="GSE245048")

P = "test/experiments/paper_screen_20261019/papers/"
META = "data/GSE245048/GSE245048_metadata.csv"
MAT = "data/GSE245048/GSE245048_counts.csv.gz"
paper = case.add_input(P + "PMC11463261.paper.json", "paper")
paper_md = case.add_input(P + "PMC11463261.paper.md", "paper")
meta = case.add_input(META, "metadata")
mat = case.add_input(MAT, "matrix")

# ---------------- 1. paper_reconstruction
paper_threshold = {"metric": "not_reported", "adjustment": "not_reported", "cutoff": "not_reported",
                   "effect_metric": "not_reported", "effect_cutoff": "not_reported",
                   "source_locator": "S2.5.p1; S4.17.p1; FIG4",
                   "note": "190 DEGs (108 up, 82 down) reported without a stated DEG cutoff; FDR < 0.05 is stated only "
                           "for the CAMERA gene-set results (S2.5.p1)"}
recon = {
    "paper_id": "PMID39383215 / PMC11463261",
    "accessions": ["GSE245048"],
    "assay": "bulk mRNA-seq of skeletal muscle (STAR/GENCODE M24, featureCounts), male mice (S4.17.p1)",
    "sample_inclusion": ["skeletal muscle of HFD-fed male Npr1+/- and Npr1+/+ littermates (S2.5.p1, FIG4)"],
    "sample_exclusion": "not_reported",
    "factors": [{"name": "genotype", "levels": ["Npr1+/+", "Npr1+/-"], "locator": "S2.5.p1"},
                {"name": "diet", "levels": ["HFD (only)"], "locator": "FIG4"}],
    "exercise_factor": ("none in the RNA-seq: exercise (submaximal endurance test, 4-week treadmill training) was "
                        "applied to separate SD-fed cohorts with physiological readouts only (S2.6.p1-p2, S4.7.p1, "
                        "S4.8.p1, FIG6); no transcriptome was generated for trained vs sedentary mice"),
    "primary_estimand": "genotype effect (Npr1+/- vs Npr1+/+) on skeletal muscle expression in HFD-fed sedentary mice",
    "planned_contrasts": ["Npr1+/- vs Npr1+/+ (HFD)"],
    "blocking_or_covariance": {"status": "required", "terms": ["cage", "body weight"], "locator": "S4.17.p1"},
    "matrix_scale": "featureCounts read counts",
    "paper_method": "edgeR v3.38.0 glmQLFit(robust=TRUE), genotype adjusted for cage and body weight (S4.17.p1)",
    "paper_threshold": paper_threshold,
    "paper_reported_counts": {"Npr1+/- vs Npr1+/+": {"total": 190, "up": 108, "down": 82, "locator": "S2.5.p1"}},
    "requested_estimand": "effect of exercise on gene expression",
    "requested_estimand_in_paper": "not_reported for any sequenced sample",
}
case.write_json("paper_reconstruction.json", recon, role="paper_reconstruction")
case.decide("paper_reconstruction",
            final={"accessions": ["GSE245048"], "primary_estimand": recon["primary_estimand"],
                   "planned_contrasts": recon["planned_contrasts"], "paper_threshold": paper_threshold,
                   "paper_method": recon["paper_method"], "assay": recon["assay"],
                   "exercise_factor": recon["exercise_factor"],
                   "paper_reported_n_deg": recon["paper_reported_counts"]},
            evidence=[paper, paper_md], paper={"locator": "S4.17.p1; S2.5.p1; S2.6.p2; FIG4; FIG6"},
            reasoning=("GSE245048 is cited only in the RNA-seq Methods and data availability (S4.17.p1, S6.4.p1). "
                       "The RNA-seq compares Npr1+/- with Npr1+/+ HFD-fed mice (Fig. 4A, 190 DEGs). The exercise "
                       "experiments (endurance test, 4-week training, S2.6) used SD-fed cohorts and report running "
                       "capacity, OXPHOS blots, Seahorse and fiber typing, not transcriptomes."),
            confidence="high")

# ---------------- 2. ownership
m = pd.read_csv(META, index_col=0)
own = {"accession": "GSE245048", "matrix_file": MAT, "metadata_file": META, "owned": True,
       "checks": {"series_id": sorted(m["series_id"].astype(str).unique().tolist()),
                  "n_gsm": int(len(m)),
                  "genotype_counts": m["characteristics_ch1.4.genotype"].value_counts().to_dict(),
                  "sex": m["characteristics_ch1.1.Sex"].unique().tolist(),
                  "tissue": m["characteristics_ch1.0.tissue"].unique().tolist(),
                  "cage_numbers": sorted(m["characteristics_ch1.2.cage number"].astype(str).unique().tolist()),
                  "body_weight_present": True,
                  "processing": "STAR 2.7.2b, GRCm38 / GENCODE M24, featureCounts both-ends-aligned: matches S4.17.p1",
                  "paper": "Npr1+/- vs Npr1+/+ HFD male muscle, edgeR with cage + body weight: GEO has genotype, "
                           "cage number and body weight for 16 male muscle samples"}}
case.decide("ownership", final=own, evidence=[paper, meta, mat], confidence="high",
            paper={"locator": "S4.17.p1; S6.4.p1"},
            reasoning=("Series GSE245048 is named in the paper's RNA-seq Methods; GEO samples are male skeletal muscle "
                       "with genotype het/wt, cage and body weight, which are exactly the factors of the paper's edgeR "
                       "model. The single supplementary file is the series count matrix. GEO does not state the diet; "
                       "the paper (FIG4) says HFD."))

# ---------------- 3. alignment
aln = native.align_to_metadata(MAT, META, case.dir / "aligned", key_column="description")
print({k: v for k, v in aln.items() if k != "outputs"})
am = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
amd = case.add_output(aln["outputs"]["aligned_metadata"]["path"], "aligned_metadata")
der = native.derive_columns(aln["outputs"]["aligned_metadata"]["path"], case.dir / "aligned" / "design_metadata.csv",
                            aliases={"geno_raw": "characteristics_ch1.4.genotype",
                                     "cage": "characteristics_ch1.2.cage number",
                                     "bw": "characteristics_ch1.3.body weight",
                                     "sex": "characteristics_ch1.1.Sex"},
                            recode={"geno_raw": {"heterozygous": "het", "wildtype": "wt"}})
dm = case.add_output(case.dir / "aligned" / "design_metadata.csv", "design_metadata")
case.decide("alignment", final={"method": aln["method"], "n_aligned": aln["n_aligned"],
                                "n_metadata": aln["n_metadata"], "coverage": aln["coverage"],
                                "unmatched_matrix_columns": aln["unmatched_matrix_columns"],
                                "unmatched_metadata_samples": aln["unmatched_metadata_samples"],
                                "annotation_columns_dropped": aln["annotation_columns_dropped"],
                                "derived_columns": der},
            evidence=[mat, meta, am, amd, dm], confidence="high",
            reasoning=("Matrix columns are library IDs (S044_1 ...) which equal GEO 'description' exactly; "
                       "featureCounts annotation columns (seqnames/start/end/strand/length) are not samples."))

# ---------------- 4. matrix
prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
keys = ["n_features", "n_samples", "min", "max", "median", "integer_fraction", "missing_values",
        "negative_values", "duplicated_feature_ids", "candidates"]
print({k: prof[k] for k in keys})
case.decide("matrix", final={"matrix_type": "raw counts", "recommended_method": "edgeR / DESeq2",
                             "profile": {k: prof[k] for k in keys},
                             "paper_input": "featureCounts gene counts into edgeR (S4.17.p1)"},
            evidence=[am, mat], confidence="high", paper={"locator": "S4.17.p1"},
            reasoning=("Non-negative integers, featureCounts output with gene lengths, GEO data_processing says "
                       "'csv file with read counts'."))

# ---------------- 5. design (refused: no exercise arm)
d = pd.read_csv(case.dir / "aligned" / "design_metadata.csv", index_col=0)
print(pd.crosstab(d["geno_raw"], d["cage"]))
rep, item, summary = case.suitability(matrix_type="raw counts", metadata=d, factors=["geno_raw"],
                                      matrix_csv=aln["outputs"]["aligned_matrix"]["path"], organism="Mouse",
                                      subject=None, references={"geno_raw": "wt"})
print(json.dumps(summary, indent=1))
print([c.get("name") for c in rep["comparisons"]])
disc = [{"item": "requested estimand", "paper": "exercise studied only physiologically in SD-fed cohorts (S2.6)",
         "data": "GSE245048 factors are genotype (8 het, 8 wt), cage and body weight; no exercise, training or "
                 "sedentary/trained label in any GSM",
         "classification": "blocks_reproduction", "consequence": "exercise effect not identifiable"},
        {"item": "library kit", "paper": "Illumina TruSeq Stranded mRNA (S4.17.p1)",
         "data": "GEO extract protocol: Tecan Universal Plus mRNA-seq with NuQuant",
         "classification": "executable_without_change"},
        {"item": "featureCounts version", "paper": "v1.6.2", "data": "GEO: v1.6.4",
         "classification": "executable_without_change"},
        {"item": "diet", "paper": "HFD-fed (FIG4)", "data": "not stated in GEO",
         "classification": "executable_without_change"}]
case.write_json("paper_data_discrepancies.json", disc, role="paper_data_discrepancies")
plan = {"paper_aligned_route": "none for the requested exercise estimand",
        "paper_own_analysis": "edgeR glmQLFit(robust=TRUE) ~ cage + body weight + genotype, Npr1+/- vs +/+ (not an "
                              "exercise question; not run)",
        "decision": "refused at design"}
case.write_json("reproduction_plan.json", plan, role="reproduction_plan")
case.decide("design", final={"suitability": summary}, evidence=[paper, dm, item],
            decision_status="refused", execution_status="not_run", confidence="high",
            paper={"locator": "S2.5.p1; S2.6.p2; S4.17.p1; FIG4"},
            candidates=[{"value": "geno_raw: het vs wt (paper's Fig. 4A contrast, 8 vs 8)",
                         "reason_rejected": "answers the Npr1 genotype question in HFD-fed sedentary mice, not exercise"},
                        {"value": "trained vs sedentary / post-exercise vs rest",
                         "reason_rejected": "no such samples were sequenced; exercise cohorts (S2.6, FIG6) have only "
                                            "physiological readouts"}],
            stop_reason=("no exercise contrast in the sequenced samples: GSE245048 contains 16 male HFD-fed muscle "
                         "samples split only by Npr1 genotype (8 het, 8 wt), with cage and body weight; the paper's "
                         "exercise experiments (endurance test, 4-week training, S2.6) were not transcriptomically "
                         "profiled"),
            reasoning=("The requested estimand (effect of exercise on gene expression) has no arm in the data. The "
                       "suitability report finds the genotype comparison analyzable, but a genotype contrast does not "
                       "answer an exercise question (decision-gates: contrast gate)."))
case.write_json("reproduction_summary.json",
                {"status": "refused at design", "paper_reported": {"Npr1+/- vs +/+": 190},
                 "reason": "no exercise contrast in GSE245048"}, role="reproduction_summary")
print(case.finish())
print(run.finish())
