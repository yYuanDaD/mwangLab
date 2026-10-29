"""Gates paper_reconstruction .. threshold for GSE232510 (PMID 39000297)."""
import sys, pathlib, json; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import math
import pandas as pd
from tools import native

native.enable_native_mode()
ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())
RUN = pathlib.Path(__file__).resolve().parents[1]
REL = str(RUN.relative_to(ROOT)).replace("\\", "/")
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC11241292.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC11241292.paper.md"
CID = "GSE232510"

run = native.RunRecorder(REL, request=(
    "Analyze GSE232510 for PMID 39000297 (Exercise Rescues Obesogenic-Related Genes in the Female Hypothalamic "
    "Arcuate Nucleus: A Potential Role of miR-211 Modulation): how exercise affects gene expression as the paper intends."),
    platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5[1m]) subagent", case_ids=[CID])
case = run.case(CID, accession="GSE232510")
paper = case.add_input(PAPER_JSON, "paper"); paper_md = case.add_input(PAPER_MD, "paper")
meta = case.add_input("data/GSE232510/GSE232510_metadata.csv", "metadata")
tar = case.add_input("data/GSE232510/GSE232510_RAW.tar", "matrix")
counts = case.add_input(f"{REL}/inputs/GSE232510_RW_counts.csv", "matrix")
build_log = case.add_input(f"{REL}/inputs/build_counts_log.json", "matrix", label="build_counts_log.json")

PT = {"metric": "FDR", "adjustment": "BH (DESeq2 default; method not named in paper)", "cutoff": 0.1,
      "effect_metric": "log2FC", "effect_cutoff": 0.5, "effect_cutoff_original": "log2FC > 0.5 (volcano, FIG2 A)",
      "inclusive": False, "source_locator": "S2.2.p2; FIG2"}
PAPER_COUNTS = {"HFS_vs_CS": {"total": 430, "up": 165, "down": 265, "locator": "S2.2.p2 ('CS vs. HFS'); S5.6.3.p1 n = 430"},
                "HFR_vs_CS": {"total": 39, "up": 20, "down": 19, "locator": "S2.2.p2"},
                "CR_vs_CS": {"total": 128, "up": 93, "down": 35, "locator": "S2.2.p2"},
                "HFR_vs_HFS": {"total": "not_reported", "locator": "S2.2.p3 compares HFS vs HFR only on cluster-average log2FC"}}

recon = {
    "paper_id": "PMID39000297 / PMC11241292",
    "accessions": ["GSE232510"],
    "accession_roles": {"GSE232510": "single deposit for both RNA-seq experiments (S5.6.2.p1, DA.p1): voluntary running (RW/DIO) and miR-211 ICV injection"},
    "assay": "bulk RNA-seq, MARS-Seq bulk adaptation, NextSeq 75 cycles; STAR to Rnor6, samtools rmdup, htseq-count -s no --mode union (S5.6.2.p1, S5.6.3.p1-p2)",
    "organism": "Rattus norvegicus, female Wistar, hypothalamic arcuate nucleus punch (S5.1.p2, S5.4.2.p1)",
    "factors": [{"name": "diet", "levels": ["chow", "60% HFD"]}, {"name": "activity", "levels": ["sedentary", "voluntary wheel running (4 wk)"]},
                {"name": "group (paper coding)", "levels": ["CS", "CR", "HFS", "HFR"], "reference": "CS"}],
    "sample_inclusion": ["RNA-seq n = 3 CS, 3 CR, 4 HFS, 4 HFR (S5.6.2.p1, FIG2)",
                         "one HFR outlier on PCA kept (S2.2.p1)"],
    "sample_exclusion": ["miR-211 injection experiment (n = 4 mimic, 4 inhibitor) is a separate, non-exercise experiment (S2.4.p1, S5.3) - out of scope for the exercise question"],
    "primary_estimand": ("Effect of 4-week voluntary wheel running on ARC gene expression in diet-induced obese female rats, "
                         "framed as rescue: HFS vs CS (DIO effect) and HFR vs CS (residual after exercise) - the reduction in "
                         "DEGs from HFS to HFR is the paper's rescue claim; CR vs CS is the exercise effect on chow."),
    "planned_contrasts": ["HFS_vs_CS", "HFR_vs_CS", "CR_vs_CS"],
    "paper_supporting_comparison": "HFR vs HFS on k-means cluster averages (S2.2.p3), not a gene-level DE test",
    "blocking_or_covariance": {"status": "not_required", "repeated_measures": "none - one ARC per animal, independent animals",
                               "batch": "experiment run twice (S5.2.p1); cohort not recorded in GEO and not modelled by the paper"},
    "matrix_scale": "htseq-count raw read counts after rmdup (S5.6.3.p2)",
    "paper_method": "DESeq2, pair-wise comparisons vs CS on a read-count matrix assembled from all RW groups (S5.6.3.p2)",
    "paper_formula": "not_reported",
    "paper_threshold": PT,
    "paper_threshold_note": "S2.2.p2 states FDR < 0.1 only; FIG2 legend (the figure the counts refer to) adds log2FC > 0.5. The legend rule is taken as the paper rule; FDR < 0.1 alone is reported as an audit.",
    "paper_reported_deg_counts": PAPER_COUNTS,
    "paper_enrichment": "GO (HOMER / ToppFun) on k-means clusters of the 430 HFS_vs_CS DEGs (S5.6.3.p2, FIG2D); not requested here",
}
case.write_json("paper_reconstruction.json", recon, role="paper_reconstruction")
case.decide("paper_reconstruction", final={k: recon[k] for k in ("accessions", "primary_estimand", "planned_contrasts", "paper_threshold",
            "paper_method", "paper_formula", "assay", "matrix_scale", "sample_inclusion", "sample_exclusion")},
            evidence=[paper, paper_md], paper={"locator": "S2.2.p2; S5.2.p1; S5.6.2.p1; S5.6.3.p2; FIG2"}, confidence="high",
            reasoning=("Four-group 2x2 design (diet x voluntary running), all compared to CS with pair-wise DESeq2 (S5.6.3.p2). "
                       "Counts given for CS vs HFS/HFR/CR at FDR < 0.1 (S2.2.p2); FIG2 legend adds log2FC > 0.5. "
                       "The rescue claim is read from HFR_vs_CS against HFS_vs_CS; the miR-211 arm in the same GEO series "
                       "is a separate pharmacology experiment and does not address exercise."))

# ---- ownership
m = pd.read_csv("data/GSE232510/GSE232510_metadata.csv", index_col=0)
case.decide("ownership", final={"accession": "GSE232510", "matrix_file": f"{REL}/inputs/GSE232510_RW_counts.csv (built from data/GSE232510/GSE232510_RAW.tar by scripts/00_build_counts.py)",
            "metadata_file": "data/GSE232510/GSE232510_metadata.csv", "owned": True,
            "checks": {"series_id": "GSE232510 in metadata series_id and in paper S5.6.2.p1/DA.p1",
                       "contact": "Noam Meiri (corresponding author N.M., BK2.p1)",
                       "tissue_sex": "hypothalamic arcuate nucleus, female (matches S5.1.p2, S5.4.2.p1)",
                       "protocol": "MARS-Seq, STAR Rnor6, samtools rmdup, htseq-count -s no --mode=union - matches S5.6.3",
                       "groups_in_geo": "CS 3, HFS 3, HFR 4, miR-211 mimic 4, inhibitor 4 (18 GSMs)",
                       "groups_in_paper": "CS 3, CR 3, HFS 4, HFR 4, mimic 4, inhibitor 4 (22)",
                       "organism_label": "GEO says 'Rattus rattus' (taxid 10117); paper and Rnor6 genome indicate Rattus norvegicus Wistar - label error"},
            "missing_samples": {"CR (chow running)": "all 3 libraries absent from GEO", "HFS": "1 of 4 absent (deposited Rep1, Rep2, Rep4)"},
            "rw_samples_used": m.index[:10].tolist()},
            evidence=[meta, tar, counts, build_log, paper], paper={"locator": "S5.6.2.p1; DA.p1"}, confidence="high",
            reasoning=("Series, lab, tissue, sex and processing all match the paper. The deposit is incomplete for the exercise "
                       "experiment: the CR group is missing entirely and HFS has 3 of 4 libraries. Per-sample HTSeq files were "
                       "merged by 00_build_counts.py (header-less read, HTSeq '__' counters removed)."))

# ---- alignment (matrix columns are GSM ids by construction; metadata index is GSM)
rw_meta = m.iloc[:10].copy()
aligned_dir = case.dir / "aligned"; aligned_dir.mkdir(exist_ok=True)
rw_meta_path = aligned_dir / "rw_metadata.csv"; rw_meta.to_csv(rw_meta_path)
aln = native.align_to_metadata(counts["path"], rw_meta_path, aligned_dir)
am = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
amd = case.add_output(aln["outputs"]["aligned_metadata"]["path"], "aligned_metadata")
amap = case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
derived = native.derive_columns(aln["outputs"]["aligned_metadata"]["path"], aligned_dir / "design_metadata.csv",
    patterns={"grp": ("characteristics_ch1.3.treatment", r"^(.+)$"),
              "rep_label": ("supplementary_file_1", r"GSM\d+_(\w+?_Rep\d+)_count\.txt\.gz$")},
    aliases={"diet": "characteristics_ch1.2.diet"},
    recode={"grp": {"Chow, sedentary": "CS", "HFD, sedentary": "HFS", "HFD, voluntary wheel running": "HFR"},
            "diet": {"Chow": "chow", "60% HFD": "hfd"}})
dm = case.add_output(derived["output"], "design_metadata")
case.decide("alignment", final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
            "coverage": aln["coverage"], "unmatched_matrix_columns": aln["unmatched_matrix_columns"],
            "unmatched_metadata_samples": aln["unmatched_metadata_samples"],
            "derived_columns": derived["columns"], "levels": derived["levels"],
            "scope": "10 voluntary-running GSMs (GSM7349354-63); 8 miR-211 GSMs excluded as a separate experiment"},
            evidence=[counts, meta, am, amd, amap, dm], paper={"locator": "S5.6.2.p1"}, confidence="high",
            reasoning=("Matrix columns were named by GSM accession from the tar member names, so alignment is exact on the "
                       "metadata index (10/10). grp recoded from characteristics treatment; rep_label kept from the file names "
                       "(CS_Rep1/4/5, HFS_Rep1/2/4, HFR_Rep1-4) to document which paper replicates were deposited."))

# ---- matrix
prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
prof_item = case.write_json("matrix_profile.json", prof, role="matrix_profile")
print("profile", {k: prof[k] for k in prof if k not in ("columns",)})
case.decide("matrix", final={"matrix_type": "raw counts", "recommended_method": "DESeq2",
            "integer_fraction": prof.get("integer_fraction"), "min": prof.get("min"), "max": prof.get("max"),
            "missing_values": prof.get("missing_values"), "feature_ids": "Ensembl rat gene IDs (ENSRNOG), Rnor6",
            "paper_input": "htseq-count read counts (S5.6.3.p2)",
            "note": "MARS-Seq libraries after samtools rmdup; counts are integer htseq-count values (GEO: 'Read count for each sample')"},
            evidence=[am, prof_item, meta, paper], paper={"locator": "S5.6.3.p2"}, confidence="high",
            reasoning="All values are non-negative integers, no missing values; GEO data_processing and paper both say htseq-count read counts, the input DESeq2 expects.")

# ---- design (suitability first)
dmeta = pd.read_csv(derived["output"], index_col=0)
rep, s_item, s_summary = case.suitability(matrix_type="raw counts", metadata=dmeta, factors=["grp"],
                                          matrix_csv=aln["outputs"]["aligned_matrix"]["path"], organism="Rat",
                                          subject=None, references={"grp": "CS"},
                                          planned=["grp_HFS_vs_CS", "grp_HFR_vs_CS"])
print("suitability", json.dumps(s_summary, indent=1))
print("comparisons", [(c["name"], c["analyzable"]) for c in rep["comparisons"]])
print("sex", json.dumps(rep["checks"].get("sex"), default=str)[:800])
dc = native.design_check(derived["output"], ["grp"])
dc_item = case.write_json("design_check.json", dc, role="design_check")
names = [c["name"] for c in rep["comparisons"]]
assert {"grp_HFS_vs_CS", "grp_HFR_vs_CS"} <= set(names), names
# the enumerator orders HFR/HFS alphabetically (grp_HFS_vs_HFR, HFR reference); the exercise
# question needs HFR tested against HFS, so that comparison is re-oriented here and saved.
import copy
base = next(c for c in rep["comparisons"] if c["name"] == "grp_HFS_vs_HFR")
hfr_vs_hfs = copy.deepcopy(base)
hfr_vs_hfs.update(name="grp_HFR_vs_HFS", test="HFR", reference="HFS", cells=list(reversed(base["cells"])))
comparisons = [c for c in rep["comparisons"] if c["name"] in ("grp_HFS_vs_CS", "grp_HFR_vs_CS")] + [hfr_vs_hfs]
comp_item = case.write_json("comparisons.json", comparisons, role="comparisons")
hfr_hfs = "grp_HFR_vs_HFS"
contrasts = [
    {"name": "grp_HFS_vs_CS", "control": "CS", "treatment": "HFS", "role": "paper planned (DIO effect, 430 DEGs)"},
    {"name": "grp_HFR_vs_CS", "control": "CS", "treatment": "HFR", "role": "paper planned (residual after exercise on HFD, 39 DEGs)"},
    {"name": hfr_hfs, "control": "HFS", "treatment": "HFR", "role": "exploratory: direct exercise effect within HFD (paper tests it only on cluster averages, S2.2.p3)"},
]
case.decide("design", final={"analysis_type": "multilevel (one factor grp, 3 deposited levels of a 2x2 diet x activity design; CR cell missing)",
            "design_column": "grp", "formula": "~ grp", "control": "CS", "treatment": ["HFS", "HFR"],
            "contrasts": contrasts, "primary_contrast": "grp_HFR_vs_CS (read against grp_HFS_vs_CS for the rescue claim)",
            "estimand_type": "causal (assigned diet and wheel access)", "suitability": s_summary,
            "levels": dc.get("levels"),
            "sex_check_note": "suitability sex check returned 'unknown' for all 10 (no rat Ensembl X/Y markers); all GEO samples labelled female, paper female-only",
            "not_estimable": {"CR_vs_CS": "CR group not deposited", "diet x activity interaction": "needs the CR cell"}},
            candidates=[{"value": "diet x activity factorial with interaction", "reason_rejected": "CR cell missing from GEO; interaction not estimable"},
                        {"value": "CR_vs_CS (paper planned)", "reason_rejected": "no CR samples deposited; recorded as blocked in reproduction_plan.json"},
                        {"value": "include miR-211 mimic/inhibitor samples in the model", "reason_rejected": "different experiment, extraction kit and file processing (UMI-corrected); not an exercise contrast"}],
            evidence=[dm, s_item, dc_item, comp_item, paper], paper={"locator": "S2.2.p2; S2.2.p3; S5.6.3.p2"}, confidence="high",
            reasoning=("Independent animals in three deposited groups; the paper compares every group to CS. HFR vs HFS is the direct "
                       "exercise effect on the HFD background and is kept as exploratory, since the paper did not test it gene by gene. "
                       "All groups have n >= 3 (CS 3, HFS 3, HFR 4)."))

# ---- covariance
conf = native.confounding_report(derived["output"], "grp", ["diet"])
cv_item = case.write_json("confounding.json", conf, role="confounding_report")
case.decide("covariance", final={"status": "not_required", "blocking_terms": [],
            "covariates": [{"name": "diet", "disposition": "nested: diet is a function of grp (CS=chow; HFS/HFR=hfd), absorbed by ~ grp"},
                           {"name": "experiment cohort (run twice, S5.2.p1)", "disposition": "excluded: not recorded in GEO; the paper did not model it"},
                           {"name": "subject", "disposition": "excluded: one sample per animal, no repeated measures"}],
            "design_rank": dc.get("rank"), "residual_df": dc.get("residual_df")},
            evidence=[dm, cv_item, dc_item, paper], paper={"locator": "S5.2.p1; S5.6.3.p2"}, confidence="medium",
            reasoning=("Each GSM is a different rat; no pairing. Diet is nested in grp. The two-cohort structure (S5.2.p1) cannot be "
                       "modelled because GEO does not say which cohort each library came from; confidence medium for that reason."))

# ---- method
case.decide("method", final={"method": "DESeq2 (pydeseq2, Wald) joint model on all 10 deposited RW samples, contrasts extracted per comparison",
            "matrix_type": "raw counts", "formula": "~ grp", "effect_size": "MLE log2FoldChange (unshrunken)",
            "independent_filtering_alpha": 0.1,
            "paper_route": {"method": "DESeq2 pair-wise vs CS on a count matrix of all 4 RW groups (14 samples)", "status": "blocked",
                            "reason": "CR (3) and one HFS library are not deposited, so the paper's sample set cannot be rebuilt; same method run on the 10 deposited samples as a declared deviation"},
            "audit": "two-group DESeq2 refits (run_deseq2_analysis) for HFS_vs_CS and HFR_vs_CS, for the strict 'pair-wise' reading"},
            candidates=[{"value": "edgeR / limma-voom", "reason_rejected": "paper used DESeq2; counts support it"},
                        {"value": "two-group refits as primary", "reason_rejected": "paper wording ('matrix assembled from all RW groups ... pair-wise analysis') fits one model with pairwise contrasts at least as well; kept as audit"}],
            evidence=[prof_item, dc_item, paper], paper={"locator": "S5.6.3.p2"}, confidence="medium",
            reasoning="Integer htseq counts support the paper's DESeq2 route; only the sample set deviates (missing CR and one HFS).")

# ---- threshold
case.decide("threshold", final={"paper_threshold": PT, "threshold_source": "paper_on_deviation_route", "applied_threshold": dict(PT),
            "deviation_note": "paper rule applied unchanged; the route deviation is the reduced deposited sample set",
            "audit_threshold": {"metric": "FDR", "cutoff": 0.1, "effect_metric": None, "effect_cutoff": None,
                                "reason": "S2.2.p2 text states FDR < 0.1 without an effect cutoff"}},
            evidence=[paper], paper={"locator": "S2.2.p2; FIG2"}, confidence="medium",
            reasoning="FIG2 legend: FDR < 0.1 and log2FC > 0.5 (read as |log2FC| > 0.5, since up and down genes are counted). Text gives FDR < 0.1 only, so that rule is computed as an audit.")

plan = {"case": CID, "executor": "tools.joint_contrasts:run_joint_deseq2", "counts_csv": aln["outputs"]["aligned_matrix"]["path"],
        "metadata_csv": derived["output"], "comparisons_json": str(case.dir / "comparisons.json"), "comparisons": [c["name"] for c in contrasts], "alpha": 0.1, "threshold": PT,
        "audit": {"two_group_refits": ["HFS_vs_CS", "HFR_vs_CS"], "threshold_FDR_only": 0.1},
        "blocked": {"CR_vs_CS": "CR samples not deposited"}}
case.write_json("reproduction_plan.json", plan, role="reproduction_plan")
disc = [
    {"item": "CR group", "paper": "n = 3 CR libraries (S5.6.2.p1)", "data": "absent from GSE232510", "disposition": "blocks_reproduction", "action": "CR_vs_CS not run"},
    {"item": "HFS group size", "paper": "n = 4", "data": "3 (Rep1, Rep2, Rep4)", "disposition": "requires_explicit_deviation", "action": "run on 3"},
    {"item": "threshold", "paper": "text FDR < 0.1; FIG2 legend FDR < 0.1 and log2FC > 0.5", "data": "-", "disposition": "executable_without_change", "action": "legend rule applied; FDR-only audit"},
    {"item": "organism label", "paper": "Wistar rat (R. norvegicus)", "data": "GEO 'Rattus rattus'", "disposition": "executable_without_change", "action": "none"},
    {"item": "cohort", "paper": "experiment run twice", "data": "cohort not in GEO", "disposition": "executable_without_change", "action": "not modelled (paper did not either)"},
]
case.write_json("paper_data_discrepancies.json", disc, role="paper_data_discrepancies")
print("design_check", json.dumps(dc, default=str)[:400])
print("done gates 1-8")
