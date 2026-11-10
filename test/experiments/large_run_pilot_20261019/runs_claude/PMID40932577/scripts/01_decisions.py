"""Gates paper_reconstruction .. threshold for GSE301564 (PMID 40932577)."""
import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os, json
ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())
os.chdir(ROOT)
import pandas as pd
from tools import native
native.enable_native_mode()

REL = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40932577"
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC12972430.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC12972430.paper.md"
REQUEST = ("Analyze GSE301564 for PMID 40932577 (Increasing indices of frailty in aged female mice are associated "
           "with impaired skeletal muscle resilience to downhill running stress): how exercise affects gene expression "
           "as the paper intends.")
run = native.RunRecorder(REL, request=REQUEST, platform_name="claude-code",
                         decision_maker="Claude Opus 5.5 (claude-opus-5-5[1m]) subagent", case_ids=["GSE301564"])
case = run.case("GSE301564", accession="GSE301564")
paper = case.add_input(PAPER_JSON, "paper")
paper_md = case.add_input(PAPER_MD, "paper")
meta = case.add_input("data/GSE301564/GSE301564_metadata.csv", "metadata")
raw = case.add_input("data/GSE301564/GSE301564_counts.txt.gz", "matrix")
vst = case.add_input("data/GSE301564/GSE301564_varianceStabilizingTransformation.txt.gz", "matrix")

# ------------------------------------------------------------------ paper_reconstruction
PT = {"metric": "FDR", "adjustment": "BH", "cutoff": 0.1, "effect_metric": None, "effect_cutoff": None,
      "inclusive": False, "source_locator": "S2.10.p1",
      "note": "'DEGs were determined at an FDR q < 0.1'; no fold-change cutoff stated"}
PLANNED = {
    "run_run_vs_sed_frail-low": "Low Run vs Low Control (LR vs LC): running effect in Low-frailty mice",
    "run_run_vs_sed_frail-high": "High Run vs High Control (HR vs HC): running effect in High-frailty mice",
    "frail_run_high_run_vs_low_sed": "Frailty x Run interaction: (HR - HC) - (LR - LC)",
}
EXPLORATORY = {
    "frail_high_vs_low_run-sed": "High vs Low frailty within sedentary controls (the 'Frailty' coefficient of the two-factor model; paper uses it only to sort GSEA output)",
    "frail_high_vs_low_run-run": "High vs Low frailty within run mice (not reported in the paper)",
}
recon = {
    "paper_id": "PMID40932577 / PMC12972430 / doi 10.1007/s11357-025-01856-7",
    "accessions": ["GSE301564"],
    "assay": "bulk RNA-seq, gastrocnemius, STAR mm10 + featureCounts Ensembl 100 gene counts, non-mitochondrial genes (S2.10.p1)",
    "organism": "Mus musculus, female C57BL/6JN, >17 months (S2.1.p1)",
    "sample_inclusion": ["n = 3-4 randomly selected per group for RNA-seq (S2.9.p1)",
                         "Low Run n=4, High Run n=4, controls n=3-4 (FIG6 legend)"],
    "sample_exclusion": ["not_reported"],
    "factors": [{"name": "Frailty", "levels": ["Low (<=1 frailty markers)", "High (>=2 markers)"], "reference": "Low",
                 "note": "retrospective stratification, not randomized (S2.2.p2)"},
                {"name": "Run", "levels": ["Control (cage sedentary)", "Run (2 bouts downhill running, harvest 24 h later)"],
                 "reference": "Control", "note": "randomized (S2.2.p2)"}],
    "primary_estimand": ("Effect of downhill running stress (24 h after 2 bouts) on gastrocnemius gene expression, "
                         "within Low- and High-frailty aged female mice, and how it differs between them (Frailty x Run)"),
    "planned_contrasts": list(PLANNED),
    "planned_contrast_labels": PLANNED,
    "blocking_or_covariance": {"status": "not_required", "note": "independent animals, one gastrocnemius per mouse; no batch reported"},
    "matrix_scale": "featureCounts raw gene counts (S2.10.p1); VST matrix also deposited",
    "paper_method": "DESeq2 (R 1.23.10 per paper / 1.32.0 per GEO) Wald test, two-factor model (Frailty, Run) with pairwise comparisons; BH FDR",
    "paper_formula": "two-factor model with interaction (coefficients Frailty, Run, Frailty x Run) - exact formula not printed (S2.10.p2)",
    "paper_threshold": PT,
    "paper_reported_deg_counts": "not_reported in the main text (DEG lists in Supplemental Tables 1-2, not available here)",
    "paper_reported_deg_examples": {"HR_vs_HC": {"up": ["Ifi47", "Iigp1", "Isg20", "Mpeg1", "Ccl8", "Ctss"], "down": ["Fosb", "Junb"],
                                                 "claim": "DEGs at FDR q < 0.1 unique to the High group (S3.5.p3, FIG6e)"}},
    "paper_enrichment": {"GSEA": "GSEA 2.2.1 preranked by Wald stat, MSigDB 2024.1.Mm H, M2 CP, M5; FDR q < 0.05 (S2.10.p2); 284 sets with Frailty x Run interaction; top: OXPHOS / ATP biosynthesis / complex I assembly, up in LR vs LC and down in HR vs HC (S3.5.p1-p2)",
                         "ORA": "DAVID EASE < 0.05 on HR vs HC and LR vs LC DEG lists; inflammation pathways only in High (S3.5.p3)"},
}
case.write_json("paper_reconstruction.json", recon, role="paper_reconstruction")
case.decide("paper_reconstruction",
            final={"accessions": ["GSE301564"], "primary_estimand": recon["primary_estimand"],
                   "planned_contrasts": list(PLANNED), "paper_threshold": PT, "paper_method": recon["paper_method"],
                   "paper_formula": recon["paper_formula"], "assay": recon["assay"], "factors": recon["factors"],
                   "paper_reported_deg_counts": recon["paper_reported_deg_counts"]},
            evidence=[paper, paper_md], paper={"locator": "S2.2.p2; S2.9.p1; S2.10.p1; S2.10.p2; S3.5.p1; S3.5.p3; FIG6"},
            confidence="high",
            reasoning=("2x2 factorial: Frailty (Low/High, retrospective) x Run (Control/downhill run, randomized). "
                       "S2.10.p1-p2: DESeq2 Wald test on a two-factor model, each coefficient and each pairwise comparison; "
                       "DEGs at BH FDR q < 0.1 with no fold-change cutoff. S3.5.p3 names the pairwise exercise contrasts "
                       "HR vs HC and LR vs LC; S3.5.p1 reports the Frailty x Run interaction. The exercise question is "
                       "answered by the two within-frailty run contrasts plus the interaction."))

# ------------------------------------------------------------------ ownership
mdf = pd.read_csv("data/GSE301564/GSE301564_metadata.csv", index_col=0)
case.decide("ownership",
            final={"accession": "GSE301564", "matrix_file": "data/GSE301564/GSE301564_counts.txt.gz",
                   "metadata_file": "data/GSE301564/GSE301564_metadata.csv", "owned": True,
                   "checks": {"series_id": sorted(mdf["series_id"].astype(str).unique().tolist()),
                              "data_availability": "S9.p1 and S2.10.p2 cite GSE301564",
                              "samples": "15 gastrocnemius libraries: robust control 4, robust 24h 4, frail control 3, frail 24h 4 = paper n=3-4/group (S2.9.p1, FIG6)",
                              "processing": "GEO data_processing: STAR mm10, featureCounts Ensembl 100 non-mitochondrial genes, DESeq2 VST, R 4.1.2 = S2.10.p1",
                              "labels": "robust = Low frailty markers, frail = High frailty markers; control = cage sedentary, 24h = 24 h after downhill running (GEO description)"},
                   "other_files": {"varianceStabilizingTransformation.txt.gz": "DESeq2 VST values; not used for DE (count route available)"}},
            evidence=[meta, raw, vst, paper], paper={"locator": "S9.p1; S2.10.p1"}, confidence="high",
            reasoning="Accession is the paper's own deposit; group sizes, tissue, protocol, and processing all match.")

# ------------------------------------------------------------------ alignment
aligned_dir = case.dir / "aligned"
aln = native.align_to_metadata("data/GSE301564/GSE301564_counts.txt.gz", "data/GSE301564/GSE301564_metadata.csv",
                               aligned_dir, key_column="title")
am = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
amd = case.add_output(aln["outputs"]["aligned_metadata"]["path"], "aligned_metadata")
amap = case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
derived = native.derive_columns(aln["outputs"]["aligned_metadata"]["path"], aligned_dir / "design_metadata.csv",
    aliases={"frail": "characteristics_ch1.1.frailty", "run": "characteristics_ch1.2.run"},
    patterns={"animal": ("title", r" (D\d+)$")},
    recode={"frail": {"robust": "low", "frail": "high"}, "run": {"control": "sed", "24h": "run"}})
dm = case.add_output(derived["output"], "design_metadata")
case.decide("alignment",
            final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
                   "coverage": aln["coverage"], "unmatched_matrix_columns": aln["unmatched_matrix_columns"],
                   "unmatched_metadata_samples": aln["unmatched_metadata_samples"],
                   "derived_columns": derived["columns"], "levels": derived["levels"]},
            evidence=[raw, meta, am, amd, amap, dm], paper={"locator": "S2.2.p2"}, confidence="high",
            reasoning=("Count matrix columns are the GEO sample titles; exact match on title, 15/15. Derived frail "
                       "(robust->low, frail->high), run (control->sed, 24h->run) and animal (D-number from title, unique per sample)."))

# ------------------------------------------------------------------ matrix
prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
prof_item = case.write_json("matrix_profile.json", prof, role="matrix_profile")
fid = native.feature_id_report(aln["outputs"]["aligned_matrix"]["path"])
case.decide("matrix",
            final={"matrix_type": "raw counts", "recommended_method": "DESeq2",
                   "integer_fraction": prof["integer_fraction"], "min": prof["min"], "max": prof["max"],
                   "missing_values": prof["missing_values"], "negative_values": prof["negative_values"],
                   "duplicated_feature_ids": prof["duplicated_feature_ids"], "n_features": prof["n_features"],
                   "feature_ids": fid["dominant_type"], "paper_input": "featureCounts gene counts into DESeq2 (S2.10.p1)"},
            candidates=[{"value": "VST matrix + limma", "reason_rejected": "raw counts are deposited and the paper used DESeq2 on counts"}],
            evidence=[am, prof_item, meta, paper], paper={"locator": "S2.10.p1"}, confidence="high",
            reasoning=("All values non-negative integers (integer_fraction 1.0), no missing values, library sizes 19-31 M; "
                       "GEO calls the file 'matrix of counts produced by Subread featureCounts'. featureCounts output is genuine "
                       "integer counts, not estimated counts."))

# ------------------------------------------------------------------ design (suitability)
dmeta = pd.read_csv(derived["output"], index_col=0)
auto_cands = [c for c in dmeta.columns if c in ("data_processing", "library_selection", "library_source", "library_strategy")]
planned_all = list(PLANNED) + list(EXPLORATORY)
rep, suit_item, suit_summary = case.suitability(matrix_type="raw counts", metadata=dmeta, factors=["frail", "run"],
                                                matrix_csv=aln["outputs"]["aligned_matrix"]["path"], organism="Mouse",
                                                subject="animal", covariate_candidates=auto_cands,
                                                references={"frail": "low", "run": "sed"}, planned=planned_all)
names = [c["name"] for c in rep["comparisons"]]
assert set(planned_all) == set(names), names
contrasts = []
for c in rep["comparisons"]:
    contrasts.append({"name": c["name"], "kind": c["kind"], "cells": c["cells"],
                      "role": "planned" if c["name"] in PLANNED else "exploratory",
                      "description": PLANNED.get(c["name"]) or EXPLORATORY.get(c["name"])})
case.write_json("comparisons.json", rep["comparisons"], role="comparisons")
case.decide("design",
            final={"analysis_type": "factorial (2x2, independent animals) - one joint model, planned simple effects + interaction",
                   "formula": "~ cell  (cell = frail x run, 4 levels; equivalent to ~ frail * run)",
                   "factors": {"frail": ["low", "high"], "run": ["sed", "run"]},
                   "references": {"frail": "low", "run": "sed"},
                   "contrasts": contrasts, "primary_contrasts": list(PLANNED),
                   "estimand_type": "causal for run (randomized); frailty is an observed stratifier",
                   "cell_sizes": {"low/sed": 4, "low/run": 4, "high/sed": 3, "high/run": 4},
                   "suitability": suit_summary},
            candidates=[{"value": "pooled run vs sed across frailty (~ frail + run main effect)",
                         "reason_rejected": "paper reports within-frailty run effects and the interaction; pooling hides the divergent response the paper studies"},
                        {"value": "two-group DESeq2 per contrast (run_deseq2_analysis)",
                         "reason_rejected": "paper fits one two-factor model; a joint fit on all 15 samples keeps the dispersion pooling"}],
            evidence=[dm, suit_item, paper], paper={"locator": "S2.10.p2; S3.5.p1; S3.5.p3"}, confidence="high",
            reasoning=("Suitability report: data type, grouping, sample size (>=3 per cell), sex (all 15 predicted female, as in the paper) pass. "
                       "The automatic batch-column regex flags 'characteristics_ch1.2.run' (the source column of the run factor itself); "
                       "candidates were passed explicitly without it. Planned: the two within-frailty run contrasts and the interaction; "
                       "frailty-within-condition contrasts are exploratory."))

# ------------------------------------------------------------------ covariance
dc = native.design_check(derived["output"], ["frail", "run"], interactions=[("frail", "run")])
conf = native.confounding_report(derived["output"], "run", ["frail", "animal"])
pair = native.pairing_report(derived["output"], "animal", "run", ["sed", "run"])
cov_item = case.write_json("covariance_checks.json", {"design_check": dc, "confounding": conf, "pairing": pair},
                           role="covariance_checks")
case.decide("covariance",
            final={"status": "not_required", "blocking_terms": [],
                   "covariates": [{"name": "animal", "disposition": "excluded: unique per sample (identifier, no repeated measures)"},
                                  {"name": "batch / lane", "disposition": "excluded: no such field in GEO metadata or paper"},
                                  {"name": "library_* / data_processing", "disposition": "excluded: constant"}],
                   "rank": dc.get("rank"), "residual_df": dc.get("residual_df"),
                   "run_vs_frail": conf[0]["status"]},
            evidence=[dm, cov_item, paper], paper={"locator": "S2.9.p1; S2.10.p1"}, confidence="high",
            reasoning="Each library is a different mouse (animal IDs unique); frail and run are crossed; ~ frail * run is full rank with residual df "
                      f"{dc.get('residual_df')}. No batch information to adjust for, and the paper reports none.")

# ------------------------------------------------------------------ method
case.decide("method",
            final={"method": "DESeq2 (pydeseq2 Wald test), joint cell-means model on all 15 samples",
                   "matrix_type": "raw counts", "formula": "~ cell (cell = frail x run); contrasts as cell differences / difference-in-differences",
                   "executor": "tools.joint_contrasts:run_joint_deseq2",
                   "independent_filtering_alpha": 0.1,
                   "pre_filter": "all-zero genes dropped by the executor; DESeq2 independent filtering at alpha 0.1 (R results() default, = paper FDR)",
                   "effect_size": "MLE log2FoldChange (unshrunken)",
                   "implementation_note": "pydeseq2 0.5.4 instead of R DESeq2 1.32; same model family, test, and BH adjustment"},
            candidates=[{"value": "limma on VST", "reason_rejected": "counts available; paper used DESeq2"},
                        {"value": "edgeR / limma-voom", "reason_rejected": "not the paper's method; two-arm executors cannot fit the interaction"}],
            evidence=[prof_item, cov_item, paper], paper={"locator": "S2.10.p1; S2.10.p2"}, confidence="high",
            reasoning="Raw integer counts support the paper's DESeq2 Wald route. The cell-means parameterization spans the same column space as ~ frail * run, so the simple effects and the interaction coefficient are the same contrasts the paper tested.")

# ------------------------------------------------------------------ threshold
case.decide("threshold",
            final={"paper_threshold": PT, "threshold_source": "paper", "applied_threshold": dict(PT)},
            evidence=[paper], paper={"locator": "S2.10.p1"}, confidence="high",
            reasoning="Paper: DEGs at BH FDR q < 0.1 (S2.10.p1), no effect-size rule. Applied exactly via apply_threshold(metric='padj', cutoff=0.1).")

plan = {"case": "GSE301564", "executor": "tools.joint_contrasts:run_joint_deseq2",
        "counts_csv": aln["outputs"]["aligned_matrix"]["path"], "metadata_csv": derived["output"],
        "comparisons": rep["comparisons"], "roles": {c["name"]: c["role"] for c in contrasts},
        "labels": {**PLANNED, **EXPLORATORY}, "alpha": 0.1, "threshold": PT,
        "enrichment": {"GSEA": "Hallmark (gseapy prerank, mh.all 2024.1.Mm) on the 3 planned contrasts, ranking stat",
                       "paper_route": "GSEA 2.2.1, H + M2 CP + M5, FDR q < 0.05"}}
case.write_json("reproduction_plan.json", plan, role="reproduction_plan")
disc = [
    {"item": "DESeq2 implementation", "paper": "R DESeq2 (1.23.10 in paper text, 1.32.0 in GEO)", "data": "pydeseq2 0.5.4", "disposition": "executable_without_change", "action": "recorded as implementation note"},
    {"item": "model parameterization", "paper": "two-factor model (Frailty, Run, interaction)", "data": "cell-means ~ cell", "disposition": "executable_without_change", "action": "same column space; contrasts identical"},
    {"item": "DESeq2 version in paper vs GEO", "paper": "1.23.10", "data": "GEO data_processing says 1.32.0", "disposition": "executable_without_change", "action": "none"},
    {"item": "featureCounts version", "paper": "1.6.2", "data": "GEO says 2.0.3", "disposition": "executable_without_change", "action": "none (counts deposited)"},
    {"item": "GSEA gene sets", "paper": "H + M2 CP + M5 (Entrez), GSEA 2.2.1, FDR q < 0.05", "data": "repository runs Hallmark only (gseapy prerank)", "disposition": "requires_explicit_deviation", "action": "Hallmark GSEA only; compare OXPHOS direction"},
    {"item": "FIG2 legend group sizes", "paper": "legend says High n=35, Low n=12 (swapped vs S2.2.p2/S3.1.p1)", "data": "n/a (RNA-seq subset 4/4/3/4)", "disposition": "executable_without_change", "action": "typo in legend; does not affect RNA-seq"},
]
case.write_json("paper_data_discrepancies.json", disc, role="paper_data_discrepancies")
print(json.dumps(suit_summary, indent=1))
print("decisions recorded; residual df", dc.get("residual_df"), "rank", dc.get("rank"))
