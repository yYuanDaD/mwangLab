"""Gates 1-8 (paper_reconstruction .. threshold) for GSE275818 / PMID39821584."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json, math
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID39821584"
CASE = "PMID39821584"
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC11738645.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC11738645.paper.md"
MATRIX = "data/GSE275818/GSE275818_Casperson_gene_count.txt.gz"
META = "data/GSE275818/GSE275818_metadata.csv"

run = native.RunRecorder(
    RUN,
    request=("Analyze GSE275818 for PMID 39821584 (Effects of defined voluntary running distances coupled with "
             "high-fat diet consumption on the skeletal muscle transcriptome of male mice): how exercise affects "
             "gene expression as the paper intends."),
    platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5) native session",
    case_ids=[CASE])
case = run.case(CASE, accession="GSE275818")
paper = case.add_input(PAPER_JSON, "paper")
case.add_input(PAPER_MD, "paper")
meta_ev = case.add_input(META, "metadata")
mat_ev = case.add_input(MATRIX, "matrix")

# Figure 2a / S3.p1 DEG counts: "DESeq2 p-value <= 0.05", raw p, no effect cutoff (S2.5.p1, FIG2 legend).
paper_threshold = {"metric": "pvalue", "adjustment": "none (raw DESeq2 p-value)", "cutoff": 0.05,
                   "effect_metric": None, "effect_cutoff": None, "inclusive": True,
                   "source_locator": "S2.5.p1; FIG2; S2.3.p1",
                   "note": ("S2.3.p1 adds 'raw count average >= 25' for the enrichment gene list only; "
                            "Fig 3 / S3.p3 report a second, stricter list at DESeq2 FDR <= 0.05 and |log2FC| >= 1 "
                            "(25/78/15/16 genes); that rule is computed as a labelled secondary count.")}
secondary_rule = {"metric": "padj", "adjustment": "BH", "cutoff": 0.05, "effect_metric": "log2FC",
                  "effect_cutoff": 1.0, "inclusive": True, "source_locator": "S3.p3; FIG3; S2.3.p1"}

planned = [
    {"name": "grp_r25_vs_sed", "definition": "HFD-25% (2.1 km/day) vs HFD-C sedentary", "paper_label": "HFD-25%",
     "reported_deg_p05": 1347, "reported_fdr05_lfc1": 25},
    {"name": "grp_r50_vs_sed", "definition": "HFD-50% (4.2 km/day) vs HFD-C", "paper_label": "HFD-50%",
     "reported_deg_p05": 1823, "reported_fdr05_lfc1": 78},
    {"name": "grp_r75_vs_sed", "definition": "HFD-75% (6.3 km/day) vs HFD-C", "paper_label": "HFD-75%",
     "reported_deg_p05": 1103, "reported_fdr05_lfc1": 15},
    {"name": "grp_rU_vs_sed", "definition": "HFD-U unrestricted (8.3 km/day) vs HFD-C", "paper_label": "HFD-U",
     "reported_deg_p05": 1107, "reported_fdr05_lfc1": 16},
]

# ---------------------------------------------------------------- 1 paper_reconstruction
study_map = {
    "paper_id": "PMID39821584 / PMC11738645 (Physiol Rep 2025)",
    "accessions": ["GSE275818"], "accession_locator": "S2.3.p1, DA.p1",
    "assay": "bulk RNA-seq, gastrocnemius, Novogene: Hisat2 v2.0.5 + featureCounts v1.5.0-p3, HiSeq 4000 (S2.3.p1)",
    "sample_inclusion": ["male C57BL/6 mice, 12 weeks HFD (45% fat), 5 groups: HFD-C sedentary, HFD-25%, HFD-50%, "
                         "HFD-75%, HFD-U wheel running; n = 6 per group with RQN > 6.3 (S2.2.p1, S2.3.p1, FIG3)"],
    "sample_exclusion": ["not_reported within HFD groups; GEO additionally deposits 6 NFD-C (normal-fat sedentary, "
                         "'CS_*') samples that the paper never analyses"],
    "factors": [{"name": "running distance group (grp)", "levels": ["sed (HFD-C)", "r25", "r50", "r75", "rU"],
                 "type": "between-animal, randomised", "locator": "S2.2.p1"}],
    "primary_estimand": ("Effect of voluntary wheel running at each defined distance (25/50/75/100% of unrestricted) "
                         "vs sedentary, all on HFD, on the gastrocnemius transcriptome: four exercise-group vs HFD-C "
                         "contrasts (FIG2a, S3.p1)."),
    "planned_contrasts": planned,
    "other_analyses_not_reproduced": [
        "'HFD-C vs all exercise groups combined' = 1094 DEGs (S3.p1): pools four distinct levels; not run (skill: never pool levels)",
        "DRomics dose-response (S3.p4): no executor; not reproduced",
        "RT-qPCR (S3.p5): not data in GEO",
        "KEGG ORA (clusterProfiler) of up/down lists (S3.p6, FIG6-7)"],
    "blocking_or_covariance": {"status": "not_required", "reason": "one muscle sample per mouse, independent groups"},
    "matrix_scale": "featureCounts raw read counts (S2.3.p1; GEO data_processing)",
    "paper_method": "DESeq2 (Novogene; DESeq2 1.20.0 per GEO), per comparison vs HFD-C; model details not reported",
    "paper_formula": "not_reported",
    "paper_threshold": paper_threshold,
    "secondary_paper_rule": secondary_rule,
    "reported_counts": {p["name"]: {"p<=0.05": p["reported_deg_p05"], "FDR<=0.05&|LFC|>=1": p["reported_fdr05_lfc1"]}
                        for p in planned},
    "reported_unique_genes_venn": {"r25": 107, "r50": 169, "r75": 67, "rU": 89, "all_four": 9729,
                                   "note": "9729 'overlapping' in Venn exceeds every per-group DEG count - internally inconsistent"},
    "enrichment": {"method": "KEGG ORA (clusterProfiler) on up- and down-regulated lists, p <= 0.05 & raw count avg >= 25",
                   "locator": "S2.3.p1, S3.p6"},
}
pr_ev = case.write_json("paper_reconstruction.json", study_map, role="paper_reconstruction")
discrepancies = [
    {"item": "sample set", "paper": "5 HFD groups x 6 = 30", "data": "GEO deposits 36: adds 6 NFD-C (CS_*)",
     "classification": "executable_without_change", "note": "NFD-C excluded from the model (paper sample set)"},
    {"item": "threshold", "paper": "S2.5.p1 says p-values were BH adjusted, yet DEGs are assigned at raw p <= 0.05; FIG2a counts at raw p <= 0.05",
     "data": "-", "classification": "executable_without_change",
     "note": "raw p <= 0.05 is the count-bearing rule (paper_threshold); FDR <= 0.05 & |LFC| >= 1 reported as secondary paper rule"},
    {"item": "GEO processing text", "paper": "DESeq2 p <= 0.05",
     "data": "GEO data_processing is Novogene boilerplate (two replicates per condition; padj <= 0.05; edgeR FC 2)",
     "classification": "executable_without_change", "note": "boilerplate; the paper text governs"},
    {"item": "model", "paper": "Novogene DESeq2, presumably one fit per pair (not stated)",
     "data": "skill route: one DESeq2 model on all 30 HFD samples with planned contrasts",
     "classification": "executable_without_change",
     "note": "dispersion shared across 5 groups; counts may differ from a pairwise fit; pairwise fit run as audit"},
    {"item": "pooled contrast", "paper": "HFD-C vs all exercise combined (1094 DEGs)", "data": "-",
     "classification": "requires_explicit_deviation", "note": "not run: pools biologically distinct levels"},
    {"item": "enrichment", "paper": "KEGG ORA via clusterProfiler",
     "data": "repository ORA: Enrichr KEGG_2019_Mouse/GO; GSEA Hallmark", "classification": "requires_explicit_deviation"},
]
case.write_json("paper_data_discrepancies.json", discrepancies, role="paper_data_discrepancies")
case.decide("paper_reconstruction",
            final={"accessions": ["GSE275818"], "primary_estimand": study_map["primary_estimand"],
                   "planned_contrasts": [p["name"] for p in planned],
                   "paper_threshold": paper_threshold, "secondary_paper_rule": secondary_rule,
                   "paper_method": study_map["paper_method"], "matrix_scale": study_map["matrix_scale"],
                   "reported_counts": study_map["reported_counts"]},
            evidence=[paper, pr_ev], paper={"locator": "S2.3.p1"}, confidence="high",
            reasoning=("GSE275818 is the paper's own deposit (S2.3.p1, DA.p1). Five randomised HFD groups, n=6, "
                       "one gastrocnemius per mouse. Planned: each running group vs HFD-C sedentary with DESeq2. "
                       "DEG counts (1347/1823/1103/1107) are at raw DESeq2 p <= 0.05 with no fold-change rule "
                       "(FIG2 legend, S2.5.p1); that is the paper_threshold."))

# ---------------------------------------------------------------- 2 ownership
meta = pd.read_csv(META, index_col=0)
own = {"series_id": sorted(meta.series_id.unique().tolist()), "n_samples": int(len(meta)),
       "treatment_counts": meta["characteristics_ch1.4.treatment"].value_counts().to_dict(),
       "diet": meta["characteristics_ch1.1.diet"].value_counts().to_dict(),
       "strain": meta["characteristics_ch1.2.strain"].unique().tolist(),
       "contact": "Shanon Casperson, USDA-ARS Grand Forks (paper's institution)",
       "matrix_name": "GSE275818_Casperson_gene_count.txt.gz (only supplementary file)"}
case.decide("ownership",
            final={"accession": "GSE275818", "matrix_file": MATRIX, "metadata_file": META, "owned": True, "checks": own},
            evidence=[meta_ev, mat_ev, paper], paper={"locator": "DA.p1"}, confidence="high",
            reasoning=("Series GSE275818 = paper accession; C57BL/6 skeletal muscle, HFD-C/25/50/75/U with 6 each "
                       "as in the paper, plus 6 NFD-C not analysed by the paper; submitter at the paper's center."))

# ---------------------------------------------------------------- 3 alignment
aln = native.align_to_metadata(MATRIX, META, case.dir / "aligned", key_column="title")
sample_cols = [c for c in meta.title]
assert aln["coverage"] == 1.0, aln
derived = native.derive_columns(
    aln["outputs"]["aligned_metadata"]["path"], case.dir / "aligned" / "design_metadata_all36.csv",
    aliases={"trt": "characteristics_ch1.4.treatment", "diet": "characteristics_ch1.1.diet"},
    patterns={"grp": ("characteristics_ch1.4.treatment", r"^(NFD-C|HFD-C|HFD-25%|HFD-50%|HFD-75%|HFD-U)$")},
    recode={"grp": {"NFD-C": "nfd", "HFD-C": "sed", "HFD-25%": "r25", "HFD-50%": "r50", "HFD-75%": "r75",
                    "HFD-U": "rU"}})
d36 = pd.read_csv(case.dir / "aligned" / "design_metadata_all36.csv", index_col=0)
# title prefix agrees with treatment label (cross-check, not used for the mapping)
prefix_map = {"CS": "nfd", "HFS": "sed", "HF25": "r25", "HF50": "r50", "HF75": "r75", "HFuR": "rU"}
title_check = bool((d36.title.str.split("_").str[0].map(prefix_map) == d36.grp).all())
assert title_check
hfd = d36[d36.grp != "nfd"].copy()
HFD_META = case.dir / "aligned" / "design_metadata.csv"
hfd.to_csv(HFD_META)
am = pd.read_csv(aln["outputs"]["aligned_matrix"]["path"], index_col=0)
HFD_MAT = case.dir / "aligned" / "aligned_matrix_hfd.csv"
am.loc[:, hfd.index].to_csv(HFD_MAT)
aligned_ev = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
hfd_meta_ev = case.add_output(HFD_META, "design_metadata")
hfd_mat_ev = case.add_output(HFD_MAT, "aligned_matrix_hfd")
case.decide("alignment",
            final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
                   "coverage": aln["coverage"],
                   "unmatched_matrix_columns": aln["unmatched_matrix_columns"],
                   "note": "unmatched matrix columns are numeric annotation (gene_start/gene_end/gene_length), not samples",
                   "derived_columns": derived, "title_prefix_crosscheck": title_check,
                   "analysis_subset": {"kept": int(len(hfd)), "excluded_nfd": d36.index[d36.grp == "nfd"].tolist(),
                                       "reason": "paper sample set is the 5 HFD groups"},
                   "design_metadata": str(HFD_META), "aligned_matrix_for_analysis": str(HFD_MAT)},
            evidence=[mat_ev, meta_ev, aligned_ev, hfd_meta_ev, hfd_mat_ev], paper={"locator": "S2.2.p1"},
            confidence="high",
            reasoning=("Matrix columns are the GEO sample titles (CS_1..HFuR_6); exact match on 'title' aligns 36/36. "
                       "grp derived from the GEO treatment field and cross-checked with the title prefix. The 6 "
                       "NFD-C samples are dropped from the analysis set because the paper studies HFD groups only."))

# ---------------------------------------------------------------- 4 matrix
prof = native.profile_matrix(HFD_MAT)
case.decide("matrix",
            final={"matrix_type": "raw counts", "recommended_method": "DESeq2",
                   "profile": {k: prof[k] for k in ("n_features", "n_samples", "min", "max", "median",
                                                     "integer_fraction", "negative_values", "missing_values",
                                                     "duplicated_feature_ids", "candidates")},
                   "feature_ids": "Entrez gene IDs (gene_id) with gene_name annotation in the deposited file"},
            evidence=[hfd_mat_ev, meta_ev, paper], paper={"locator": "S2.3.p1"}, confidence="high",
            reasoning=(f"All values non-negative integers (integer fraction {prof['integer_fraction']}), max "
                       f"{prof['max']:.0f}; file is 'gene_count', GEO says 'Raw counts of sequencing reads (before "
                       "normalization)' from featureCounts, which matches the paper's DESeq2 input."))

# ---------------------------------------------------------------- 5 design
rep, suit_item, suit_summary = case.suitability(
    matrix_type="raw counts", metadata=hfd, factors=["grp"], matrix_csv=str(HFD_MAT), organism="Mouse",
    subject=None, references={"grp": "sed"},
    planned=[p["name"] for p in planned])
names = [c["name"] for c in rep["comparisons"]]
missing = [p["name"] for p in planned if p["name"] not in names]
assert not missing, (missing, names)
case.write_json("suitability_comparisons.json", rep["comparisons"], role="comparisons")
print("suitability", suit_summary, names)
print(json.dumps(rep["checks"].get("sex", {}), indent=1, default=str)[:1500])
exploratory = [n for n in names if n not in {p["name"] for p in planned}]
case.decide("design",
            final={"analysis_type": "multilevel (one factor, 5 levels, between-animal)",
                   "formula": "~ grp", "design_column": "grp",
                   "contrasts": [{"name": p["name"], "test": p["name"].split("_")[1], "reference": "sed",
                                  "role": "planned"} for p in planned]
                                + [{"name": n, "role": "exploratory"} for n in exploratory],
                   "estimand_type": "causal (randomised groups)",
                   "suitability": suit_summary},
            evidence=[hfd_meta_ev, suit_item, paper], paper={"locator": "FIG2"}, confidence="high",
            candidates=[{"value": "HFD-C vs pooled exercise groups (paper S3.p1, 1094 DEGs)",
                         "reason_rejected": "pools four distinct running-distance levels"},
                        {"value": "include NFD-C as a further level", "reason_rejected": "outside the paper's sample set; a diet, not exercise, contrast"},
                        {"value": "separate two-group DESeq2 per contrast",
                         "reason_rejected": "skill rule: one model with planned contrasts; run as an audit only"}],
            reasoning=("Five randomised HFD groups; the paper's estimand is each running group vs sedentary HFD-C. "
                       "One factor with five levels: one model on all 30 HFD samples, the four planned vs-sed "
                       "contrasts as the paper route, the six exercise-vs-exercise pairs as exploratory."))

# ---------------------------------------------------------------- 6 covariance
dc = native.design_check(HFD_META, ["grp"])
conf = native.confounding_report(HFD_META, "grp", candidates=["diet", "characteristics_ch1.2.strain",
                                                              "characteristics_ch1.3.genotype"])
case.decide("covariance",
            final={"status": "not_required", "blocking_terms": [],
                   "covariates": [{"name": "diet", "disposition": "excluded: single level (HFD) in analysis set"},
                                  {"name": "strain/genotype", "disposition": "excluded: single level"},
                                  {"name": "sex", "disposition": "excluded: all male (paper S2.1.p1)"},
                                  {"name": "mouse id", "disposition": "excluded: one sample per mouse, nothing to block"}],
                   "design_check": dc, "confounding": conf},
            evidence=[hfd_meta_ev, paper], paper={"locator": "S2.3.p1"}, confidence="high",
            reasoning=(f"One gastrocnemius per mouse, independent randomised groups, no batch or other varying "
                       f"covariate in GEO. Design ~grp full rank={dc['full_rank']}, residual df={dc['residual_df']}, "
                       f"min cell {dc['min_cell_size']}."))

# ---------------------------------------------------------------- 7 method
case.decide("method",
            final={"method": "DESeq2 (pydeseq2 joint model ~ cell on 30 HFD samples, Wald contrasts)",
                   "matrix_type": "raw counts", "formula": "~ grp",
                   "executor": "tools.joint_contrasts:run_joint_deseq2",
                   "audit_route": "tools.deseq2_tools:run_deseq2_analysis per planned pair (12 samples each)",
                   "paper_route": {"method": "DESeq2 (R 1.20.0, Novogene)", "status": "reproduced_with_pydeseq2",
                                   "note": "R vs pydeseq2 implementation; paper's fit structure (pairwise vs joint) not stated"}},
            evidence=[hfd_mat_ev, paper], paper={"locator": "S2.3.p1"}, confidence="high",
            reasoning="Raw integer featureCounts counts; the paper used DESeq2, which is the default raw-count route.")

# ---------------------------------------------------------------- 8 threshold
case.decide("threshold",
            final={"paper_threshold": paper_threshold, "threshold_source": "paper",
                   "applied_threshold": paper_threshold,
                   "secondary_paper_rule": secondary_rule,
                   "multiplicity": "none for the count-bearing rule (raw p); BH within each contrast for the secondary rule"},
            evidence=[paper], paper={"locator": "FIG2"}, confidence="high",
            reasoning=("FIG2 legend and S2.5.p1: DEGs assigned at DESeq2 p-value <= 0.05 (raw), no fold-change "
                       "cutoff; applied exactly. FDR <= 0.05 & |log2FC| >= 1 (FIG3) is reported alongside."))
print("gates done")
