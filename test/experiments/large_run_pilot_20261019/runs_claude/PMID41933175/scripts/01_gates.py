"""Gates 1-8 (paper_reconstruction .. threshold) for GSE282942 / PMID41933175."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json, math
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID41933175"
CASE = "PMID41933175"
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC13052164.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC13052164.paper.md"
MATRIX = "data/GSE282942/GSE282942_Genes_count_table.tsv.gz"
META = "data/GSE282942/GSE282942_metadata.csv"

run = native.RunRecorder(
    RUN,
    request=("Analyze GSE282942 for PMID 41933175 (Irisin ameliorates obesity and insulin resistance via adipose "
             "tissue IL-33 and regulatory T cells): how exercise affects gene expression as the paper intends."),
    platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5) native session",
    case_ids=[CASE])
case = run.case(CASE, accession="GSE282942")
paper = case.add_input(PAPER_JSON, "paper")
case.add_input(PAPER_MD, "paper")
meta_ev = case.add_input(META, "metadata")
mat_ev = case.add_input(MATRIX, "matrix")

# FIG3 legend panel g is the only DE rule stated for the mSC dataset.
paper_threshold = {"metric": "pvalue", "adjustment": "none (raw P)", "cutoff": 0.05,
                   "effect_metric": "log2FC", "effect_cutoff": 1.0,
                   "effect_cutoff_original": "fold change > 2 (FIG3 g legend)", "inclusive": False,
                   "test": "not_reported (Multiplot Studio, GenePattern; S4.9.p4)",
                   "source_locator": "FIG3"}

# ---------------------------------------------------------------- 1 paper_reconstruction
study_map = {
    "paper_id": "PMID41933175 / PMC13052164",
    "accessions": ["GSE282942"], "accession_locator": "DA.p1",
    "other_accessions": {"GSE283234": "whole-tissue eWAT/iWAT RNA-seq of HFD mice +/- AAV-irisin (DA.p1, S2.1.p3); not requested"},
    "assay": "populational (1,000-cell) Smart-seq2 RNA-seq, ImmGen ULI protocol, NextSeq 500; STAR + featureCounts (S4.9.p4)",
    "sample_inclusion": ["FACS-sorted IL-33(EGFP)- eWAT mSCs from 12-week-old male Il33-Egfp mice, cultured 3 days with "
                         "PBS or 10 nM irisin + HSP90a; triplicate samples (S2.3.p5, S4.11.p1, FIG3 g)"],
    "sample_exclusion": ["QC: replicates with Pearson r < 0.9 or poor PCA congregation removed (S4.9.p4); none reported removed"],
    "factors": [{"name": "treatment", "levels": ["PBS", "irisin/HSP90a"], "type": "in-vitro, between culture wells",
                 "locator": "S2.3.p5, FIG3"}],
    "primary_estimand": ("Transcriptional effect of 3-day irisin/HSP90a vs PBS treatment on cultured IL-33- eWAT "
                         "mesenchymal stromal cells (Il33 and cytokine induction; attenuation of an adipogenesis-up "
                         "signature). Irisin is an exercise-induced myokine; this dataset has no exercise arm, so the "
                         "'exercise' question is answered only through this myokine (exercise-mimetic) treatment."),
    "planned_contrasts": [{"name": "grp_irisin_vs_pbs", "definition": "irisin/HSP90a vs PBS, IL-33- mSCs", "locator": "FIG3, S2.3.p5"}],
    "blocking_or_covariance": {"status": "not_required", "note": "two independent culture arms; no subject/donor key"},
    "matrix_scale": "raw featureCounts read counts (GEO data_processing; S4.9.p4)",
    "paper_method": "DESeq2 median-of-ratios normalisation, genes <15 reads or CV>0.30 removed, comparison in Multiplot Studio (GenePattern); test not named (S4.9.p4, GEO data_processing)",
    "paper_formula": "not_reported (two-group comparison)",
    "paper_threshold": paper_threshold,
    "reported_findings": {
        "n_deg": "not_reported in text (volcano plot FIG3 g only)",
        "up": "Il33 ~10-fold up; Il6, Fgf23, Ccl2, Ccl7, Cxcl5 up (S2.3.p5)",
        "down": "147 of 195 adipogenesis-up signature genes attenuated (75%), incl. Fabp4, Adipoq, Cd36, Pparg (S2.3.p5)",
        "signature_test": "chi-squared test for signature enrichment (S4.19.p1); signature 'came from gene-set enrichment analysis' (S4.9.p4)"},
    "whole_tissue_rule_not_applicable": "S4.9.p3 (DESeq2 BH padj <= 0.05 & |log2FC| >= 1) describes the adipose-tissue dataset GSE283234",
}
pr_ev = case.write_json("paper_reconstruction.json", study_map, role="paper_reconstruction")
discrepancies = [
    {"item": "exercise", "paper": "irisin framed as an exercise-induced myokine (ABS.p1, S1.p2)",
     "data": "no exercise arm; in-vitro irisin/HSP90a vs PBS on sorted mSCs",
     "classification": "executable_without_change",
     "note": "the paper's own contrast is run; it estimates an irisin (exercise-mimetic) effect, not an effect of exercise"},
    {"item": "method", "paper": "DESeq2 normalisation then Multiplot Studio comparison (test not named)",
     "data": "Multiplot Studio not available; pyDESeq2 Wald test on raw counts available",
     "classification": "requires_explicit_deviation",
     "note": "DESeq2 Wald on the paper's DESeq2-normalisation basis; paper threshold applied on the deviation route"},
    {"item": "gene filter", "paper": "genes with <15 reads across samples or CV > 0.30 removed (GEO data_processing)",
     "data": "read filter reproducible (sum >= 15: 15,477 of 55,011 genes); CV filter underspecified (which normalisation, all samples or within group)",
     "classification": "requires_explicit_deviation",
     "note": "read filter applied; CV filter not applied (raw P of the Wald test does not depend on other genes except via dispersion trend)"},
    {"item": "replicates", "paper": "'Triplicate samples' of cultured sorted cells (FIG3 g)",
     "data": "3 PBS and 3 irisin libraries; whether wells came from separate mouse pools is not reported",
     "classification": "executable_without_change",
     "note": "replicates are culture wells; inference is to culture-level variability, which may understate biological variance"},
    {"item": "threshold", "paper": "fold change > 2, P < 0.05 (raw P) for mSCs (FIG3 g); whole-tissue rule padj <= 0.05 & |log2FC| >= 1 (S4.9.p3)",
     "data": "-", "classification": "executable_without_change",
     "note": "FIG3 g rule is the paper threshold; the whole-tissue rule and BH padj < 0.05 are reported as audits"},
]
case.write_json("paper_data_discrepancies.json", discrepancies, role="paper_data_discrepancies")
case.decide("paper_reconstruction",
            final={"accessions": ["GSE282942"], "primary_estimand": study_map["primary_estimand"],
                   "planned_contrasts": ["grp_irisin_vs_pbs"], "paper_threshold": paper_threshold,
                   "paper_method": study_map["paper_method"], "matrix_scale": study_map["matrix_scale"],
                   "reported_findings": study_map["reported_findings"]},
            evidence=[paper, pr_ev], paper={"locator": "S2.3.p5"}, confidence="high",
            reasoning=("DA.p1 assigns GSE282942 to the eWAT mSC dataset. S2.3.p5 and FIG3 g: populational RNA-seq of "
                       "IL-33- eWAT mSCs cultured 3 d with irisin/HSP90a vs PBS, triplicates; threshold FC > 2 and "
                       "P < 0.05 (raw). No exercise arm exists; irisin is the paper's exercise-derived mediator."))

# ---------------------------------------------------------------- 2 ownership
meta = pd.read_csv(META, index_col=0)
own = {"series_id": sorted(meta.series_id.unique().tolist()), "n_samples": int(len(meta)),
       "titles": meta.title.tolist(), "treatment": meta["characteristics_ch1.3.treatment"].value_counts().to_dict(),
       "genotype": meta["characteristics_ch1.2.genotype"].unique().tolist(),
       "cell_type": meta["characteristics_ch1.1.cell type"].unique().tolist(),
       "tissue": meta["characteristics_ch1.0.tissue"].unique().tolist(),
       "processing": "STAR 2.7.3a mm10, featureCounts GENCODE vM25, raw read counts per sample (GEO data_processing)"}
case.decide("ownership",
            final={"accession": "GSE282942", "matrix_file": MATRIX, "metadata_file": META, "owned": True, "checks": own},
            evidence=[meta_ev, mat_ev, paper], paper={"locator": "DA.p1"}, confidence="high",
            reasoning=("Series GSE282942 = paper accession (DA.p1); 6 VAT stromal-cell libraries, genotype Il33-EGFP-, "
                       "PBS x3 / Irisin/HSP90a x3, matching FIG3 g triplicates and S4.9.p4 (STAR + featureCounts)."))

# ---------------------------------------------------------------- 3 alignment
aln = native.align_to_metadata(MATRIX, META, case.dir / "aligned", key_column="title")
assert aln["coverage"] == 1.0 and not aln["unmatched_matrix_columns"], aln
derived = native.derive_columns(
    aln["outputs"]["aligned_metadata"]["path"], case.dir / "aligned" / "design_metadata.csv",
    # The treatment column was written with mojibake ('Irisin/HSP90伪', GBK-decoded UTF-8 alpha) by
    # tools/geo_tools.py (GEOparse read without an explicit encoding), so derive grp from the title.
    patterns={"grp": ("title", r"^IL33_neg_(PBS|Irisin)#\d$"), "rep": ("title", r"#(\d)$")},
    recode={"grp": {"PBS": "pbs", "Irisin": "irisin"}})
dmc = pd.read_csv(case.dir / "aligned" / "design_metadata.csv", index_col=0)
assert (dmc.grp.eq("pbs") == dmc["characteristics_ch1.3.treatment"].eq("PBS")).all()
aligned_mat = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
design_meta = case.add_output(case.dir / "aligned" / "design_metadata.csv", "design_metadata")
case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
case.decide("alignment",
            final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
                   "coverage": aln["coverage"], "unmatched_matrix_columns": aln["unmatched_matrix_columns"],
                   "unmatched_metadata_samples": aln["unmatched_metadata_samples"],
                   "annotation_columns_dropped": aln["annotation_columns_dropped"], "derived_columns": derived},
            evidence=[mat_ev, meta_ev, aligned_mat, design_meta], confidence="high",
            reasoning="Matrix headers equal GEO titles exactly (IL33_neg_PBS#1..Irisin#3); 6/6 aligned. grp recoded pbs/irisin.")

# ---------------------------------------------------------------- 4 matrix
prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
case.write_json("matrix_profile.json", prof, role="matrix_profile")
case.decide("matrix",
            final={"matrix_type": "raw counts", "recommended_method": "DESeq2",
                   "profile": {k: prof.get(k) for k in ("integer_fraction", "min", "max", "negative_values",
                                                        "missing_values", "type_candidates") if k in prof},
                   "paper_input": "featureCounts raw read counts, DESeq2-normalised (S4.9.p4)"},
            evidence=[aligned_mat, meta_ev, paper], paper={"locator": "S4.9.p4"}, confidence="high",
            reasoning=("All values non-negative integers, library sizes 5.3-6.7 M, file named Genes_count_table, GEO "
                       "says 'raw read counts for each Sample' from featureCounts; matches the paper's input."))
print("profile:", json.dumps({k: prof.get(k) for k in prof if k != "annotation_columns"}, default=str)[:800])

# ---------------------------------------------------------------- 5 design
dm = pd.read_csv(case.dir / "aligned" / "design_metadata.csv", index_col=0)
rep, item, summary = case.suitability(matrix_type="raw counts", metadata=dm, factors=["grp"],
                                      matrix_csv=aln["outputs"]["aligned_matrix"]["path"], organism="Mouse",
                                      subject=None, references={"grp": "pbs"}, planned=["grp_irisin_vs_pbs"])
print("suitability:", summary, [c["name"] for c in rep["comparisons"]])
assert any(c["name"] == "grp_irisin_vs_pbs" for c in rep["comparisons"])
case.decide("design",
            final={"analysis_type": "two_group", "design_column": "grp", "control": "pbs", "treatment": "irisin",
                   "contrasts": ["grp_irisin_vs_pbs"], "suitability": summary,
                   "estimand_type": "interventional (in vitro)",
                   "exercise_relation": ("proxy: irisin is an exercise-induced myokine; no exercise arm in GSE282942. "
                                         "Result is an irisin/HSP90a effect on IL-33- eWAT mSCs, not an effect of exercise.")},
            evidence=[design_meta, item, paper], paper={"locator": "FIG3"}, confidence="medium",
            candidates=[{"value": "refuse: no exercise arm",
                         "reason_rejected": ("the request asks for the effect 'as the paper intends'; the paper's only "
                                             "contrast in this deposit is the myokine treatment, run with the proxy label")}],
            reasoning=("One factor, two levels, 3 vs 3 culture replicates, paper's planned contrast (FIG3 g). "
                       "Suitability verdict recorded. Exercise enters only as the irisin mediator."))

# ---------------------------------------------------------------- 6 covariance
conf = native.confounding_report(dm, "grp", candidates=["rep"])
dchk = native.design_check(dm, ["grp"])
case.write_json("covariance_checks.json", {"confounding": conf, "design_check": dchk}, role="covariance_checks")
print("design_check:", dchk)
case.decide("covariance",
            final={"status": "not_required", "blocking_terms": [],
                   "covariates": [{"name": "rep", "disposition": "excluded: replicate index within arm, no shared unit across arms"},
                                  {"name": "genotype/tissue/cell type/sex", "disposition": "excluded: single level (all Il33-EGFP-, VAT stromal, male)"}],
                   "rank": dchk.get("rank"), "residual_df": dchk.get("residual_df")},
            evidence=[design_meta, meta_ev], confidence="medium",
            reasoning=("No donor, mouse, batch or pairing key in GEO; PBS#k and Irisin#k share no reported unit, so "
                       "no blocking. Replicates are culture wells (independence across mice not reported)."))

# ---------------------------------------------------------------- 7 method
case.decide("method",
            final={"method": "DESeq2 (pyDESeq2 Wald test, MLE log2FC)", "matrix_type": "raw counts",
                   "formula": "~ grp", "gene_filter": "keep genes with total reads >= 15 across the 6 samples (paper: <15 reads removed)",
                   "paper_route": {"method": "DESeq2 normalisation + Multiplot Studio (GenePattern) comparison, CV > 0.30 filter",
                                   "status": "blocked",
                                   "reason": "Multiplot Studio test not named and not available; CV filter underspecified"}},
            evidence=[aligned_mat, paper], paper={"locator": "S4.9.p4"}, confidence="medium",
            reasoning=("Raw integer counts support DESeq2, which the paper used for normalisation. Its comparison tool "
                       "cannot be reproduced, so DESeq2 Wald runs as a declared deviation with the paper's read filter."))

# ---------------------------------------------------------------- 8 threshold
case.decide("threshold",
            final={"paper_threshold": paper_threshold, "threshold_source": "paper_on_deviation_route",
                   "applied_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FC",
                                         "effect_cutoff": 1.0, "inclusive": False},
                   "deviation_note": "raw P from the DESeq2 Wald test instead of the unnamed Multiplot Studio test",
                   "audit_thresholds": [
                       {"name": "whole_tissue_rule", "metric": "padj", "cutoff": 0.05, "effect_cutoff": 1.0, "inclusive": True,
                        "source": "S4.9.p3 (GSE283234 rule)"},
                       {"name": "workflow_default", "metric": "padj", "cutoff": 0.05, "effect_cutoff": None, "inclusive": False}]},
            evidence=[paper], paper={"locator": "FIG3"}, confidence="high",
            reasoning="FIG3 g: FC > 2 and P < 0.05 (raw), applied as raw pvalue < 0.05 and |log2FC| > 1 on the DESeq2 route.")
print("gates 1-8 recorded")
