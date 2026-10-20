import sys, pathlib, json; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6]))  # repository root
from tools import native
native.enable_native_mode()
R = pathlib.Path(__file__).resolve().parents[1]
REL = "test/experiments/large_run_pilot_20261019/runs_claude/PMID41314005"
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC12702345.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC12702345.paper.md"
run = native.RunRecorder(REL, request=("Use the bioinformatics-workflow skill to analyze GSE308674 for PMID 41314005 "
    "(lactate / HIIT / MCT1/2 inhibition, mouse gastrocnemius); determine how exercise affects gene expression as the paper intends."),
    platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5[1m]) subagent", case_ids=["GSE308674"])
case = run.case("GSE308674", accession="GSE308674")
paper = case.add_input(PAPER_JSON, "paper"); paper_md = case.add_input(PAPER_MD, "paper")
meta = case.add_input("data/GSE308674/GSE308674_metadata.csv", "metadata")
raw = case.add_input("data/GSE308674/GSE308674_gene_counts.csv.gz", "matrix")

PT = {"metric": "FDR", "adjustment": "BH", "cutoff": 0.05, "effect_metric": "log2FC", "effect_cutoff": 0.5,
      "inclusive": False, "source_locator": "S2.7.1.p1"}
CONTRASTS = [
    {"name": "H_vs_C", "treatment": "H", "control": "C", "label": "HIIT vs Control (primary exercise effect)", "paper_n_deg": {"total": 474, "up": 265, "down": 209}},
    {"name": "HM_vs_C", "treatment": "HM", "control": "C", "label": "HIIT+MCT1/2 inhibitor vs Control", "paper_n_deg": {"total": 414, "up": 154, "down": 260}},
    {"name": "L_vs_C", "treatment": "L", "control": "C", "label": "Lactate vs Control", "paper_n_deg": {"total": 857, "up": 412, "down": 445}},
    {"name": "M_vs_C", "treatment": "M", "control": "C", "label": "MCT1/2 inhibitor vs Control", "paper_n_deg": {"total": 40, "up": 28, "down": 12}},
]
recon = {
    "paper_id": "PMID41314005 / PMC12702345",
    "accessions": ["GSE308674"],
    "accession_roles": {"GSE308674": "bulk mRNA-seq (QuantSeq 3') - this case",
                        "GSE308673/GSE308675": "methylation array and miRNA-seq deposits of the same paper (S10.p1); not analyzed here"},
    "assay": "bulk RNA-seq, QuantSeq 3' mRNA-Seq FWD v2, UMI-deduplicated, STAR GRCm39, featureCounts (S2.7.1.p1)",
    "organism": "Mus musculus, male BALB/c ~2 months, gastrocnemius (S2.2.p1)",
    "sample_inclusion": ["5 groups randomised n=6/group (S2.2.p1); RNA-seq n=4-6 per group (S2.7.1.p1, FIG3)"],
    "sample_exclusion": ["not_reported (Control has 4 RNA-seq libraries; reason not stated)"],
    "factors": [{"name": "Grouping", "levels": ["C (Control, PBS)", "L (Lactate i.p.)", "H (HIIT)", "M (MCT1/2 inhibitor AR-C155858)", "HM (HIIT + MCTi)"], "reference": "C"},
                {"name": "Batch", "levels": "not_reported in paper; GEO characteristics batch1/batch2"}],
    "primary_estimand": "Chronic (6-week) effect of HIIT on gastrocnemius gene expression vs PBS Control, 48 h after the last session (H vs C); companion estimands L vs C, M vs C, HM vs C (each vs Control)",
    "planned_contrasts": [c["name"] for c in CONTRASTS],
    "blocking_or_covariance": {"status": "required", "terms": ["Batch (additive)"], "repeated_measures": "none - one muscle per animal, independent animals per group", "source_locator": "S2.7.1.p1"},
    "matrix_scale": "raw featureCounts gene counts (S2.7.1.p1; GEO data_processing 'values = raw integer counts')",
    "pre_filter": "edgeR filterByExpr (S2.7.1.p1)",
    "paper_method": "DESeq2, Wald test, one model on all groups",
    "paper_formula": "~ Batch + Grouping, Control reference",
    "paper_threshold": PT,
    "paper_reported_deg_counts": {c["name"]: c["paper_n_deg"] for c in CONTRASTS} | {"source_locator": "S3.3.p1"},
    "paper_enrichment": {"ORA": "clusterProfiler GO BP + KEGG on DEGs (S2.7.1.p1)", "GSEA": "fgsea MSigDB Hallmark, 10,000 permutations, adjusted p <= 0.25 (S2.7.1.p1); H_vs_C and L_vs_C shown (FIG3, S3.3.p3)"},
}
case.write_json("paper_reconstruction.json", recon, role="paper_reconstruction")
case.decide("paper_reconstruction", final={"accessions": ["GSE308674"], "primary_estimand": recon["primary_estimand"],
            "planned_contrasts": recon["planned_contrasts"], "paper_threshold": PT, "paper_method": recon["paper_method"],
            "paper_formula": recon["paper_formula"], "assay": recon["assay"], "matrix_scale": recon["matrix_scale"]},
            evidence=[paper, paper_md], paper={"locator": "S2.7.1.p1; S2.2.p1; S3.3.p1; S10.p1"}, confidence="high",
            reasoning=("Methods S2.7.1.p1 give DESeq2 ~ Batch + Grouping with Control reference, Wald pairwise contrasts L/H/M/HM vs C, "
                       "BH FDR < 0.05 and |log2FC| > 0.5. S2.2.p1 defines 5 independent groups (no repeated measures). "
                       "S10.p1 lists three deposits; GSE308674 is the mRNA-seq one (GEO library_strategy RNA-Seq, QuantSeq protocol). "
                       "The exercise estimand is H vs C; HM vs C, L vs C and M vs C are the paper's other planned contrasts and are kept as separate contrasts."))

# ---- derive formula-safe columns (needed first: the matrix key lives inside 'description')
aligned_dir = case.dir / "aligned"
derived = native.derive_columns("data/GSE308674/GSE308674_metadata.csv", aligned_dir / "derived_metadata_full.csv",
    aliases={"batch": "characteristics_ch1.4.batch"},
    patterns={"count_col": ("description", r"Column name in gene_counts\.csv: (\S+)$"),
              "grp": ("characteristics_ch1.3.treatment", r"^(.+)$")},
    recode={"grp": {"PBS injection": "C", "Lactate administration": "L", "HIIT": "H",
                    "MCT1/2 inhibitor": "M", "HIIT+MCT1/2 inhibitor": "HM"}})
repaired = R / "case_GSE308674_repair" / "GSE308674_gene_counts_repaired.csv"
rep = case.add_output(repaired, "repaired_matrix")
rep_log_item = case.add_output(R / "case_GSE308674_repair" / "repair_log.json", "repair_log")
case.decide("ownership", final={"accession": "GSE308674", "matrix_file": "data/GSE308674/GSE308674_gene_counts.csv.gz",
            "metadata_file": "data/GSE308674/GSE308674_metadata.csv", "owned": True,
            "checks": {"series_id": "GSE308674 in metadata", "data_availability": "S10.p1 lists GSE308674",
                       "samples": "28 RNA-seq gastrocnemius, male BALB/c; treatment levels PBS/Lactate/HIIT/MCT1/2 inhibitor/HIIT+MCT1/2 inhibitor = paper's 5 groups (S2.2.p1)",
                       "group_sizes": "C=4, L=6, H=6, M=6, HM=6, within paper's n = 4-6 (S2.7.1.p1)",
                       "protocol": "QuantSeq 3' FWD v2, NovaSeq X Plus SE75, UMI, STAR GRCm39 - matches S2.7.1.p1",
                       "contact": "Zsolt Radak, Research Center for Molecular Exercise Science (S2.1.p1 institution)"},
            "matrix_integrity_issue": "6 genes (Dst, Neb, Ttn, Syne1, Mycbp2, Huwe1) were split across continuation rows by a 32,767-character cell limit in the annotation columns; repaired deterministically (see repair_log.json)",
            "matrix_used": str(repaired)},
            evidence=[meta, raw, paper, rep, rep_log_item], paper={"locator": "S10.p1"}, confidence="high",
            reasoning="Series ID, sample count, groups, tissue, sex, strain, and library protocol all match the paper. The deposited CSV has six long genes whose featureCounts annotation strings overflowed a spreadsheet cell limit; their Length + 28 counts were reattached by scripts/repair_counts.py without changing any value.")

aln = native.align_to_metadata(repaired, aligned_dir / "derived_metadata_full.csv", aligned_dir, key_column="count_col")
am = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
amd = case.add_output(aln["outputs"]["aligned_metadata"]["path"], "aligned_metadata")
amap = case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
dmeta = native.derive_columns(aln["outputs"]["aligned_metadata"]["path"], aligned_dir / "design_metadata.csv",
                              aliases={"sample_title": "title"})
dm = case.add_output(dmeta["output"], "design_metadata")
case.decide("alignment", final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
            "coverage": aln["coverage"], "unmatched_matrix_columns": aln["unmatched_matrix_columns"],
            "unmatched_metadata_samples": aln["unmatched_metadata_samples"], "derived_columns": derived["columns"],
            "levels": {"grp": derived["levels"]["grp"], "batch": derived["levels"]["batch"], "count_col": "28 unique"}},
            evidence=[raw, rep, meta, am, amd, amap, dm], paper={"locator": "S2.7.1.p1"}, confidence="high",
            reasoning="GEO 'description' states the gene_counts.csv column name of each GSM; extracted it as count_col by regex and aligned exactly (28/28). grp recoded from characteristics treatment (PBS injection = C, the paper's Control); batch copied from characteristics batch.")

prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
prof_item = case.write_json("matrix_profile.json", prof, role="matrix_profile")
case.decide("matrix", final={"matrix_type": "raw counts", "recommended_method": "DESeq2", "integer_fraction": prof["integer_fraction"],
            "min": prof["min"], "max": prof["max"], "missing_values": prof["missing_values"], "duplicated_feature_ids": prof["duplicated_feature_ids"],
            "feature_ids": "MGI gene symbols / NCBI LOC ids (featureCounts Geneid, GRCm39 RefSeq annotation)",
            "paper_input": "raw featureCounts counts (S2.7.1.p1)"},
            evidence=[am, prof_item, meta, paper], paper={"locator": "S2.7.1.p1"}, confidence="high",
            reasoning="All values non-negative integers (integer_fraction 1.0, no missing after repair, no duplicated IDs). GEO data_processing states 'values = raw integer counts' from featureCounts on UMI-deduplicated BAMs; paper imports raw counts into DESeq2. UMI-dedup counts are genuine integer counts, not estimated counts.")

design_check = native.design_check(dmeta["output"], ["grp", "batch"])
conf = native.confounding_report(dmeta["output"], "grp", ["batch"])
dc_item = case.write_json("design_check.json", {"full_model": design_check, "confounding": conf}, role="design_check")
contrasts_rec = [{"name": c["name"], "control": "C", "treatment": c["treatment"], "description": c["label"]} for c in CONTRASTS]
case.decide("design", final={"analysis_type": "multilevel (one factor, 5 independent groups, planned treatment-vs-Control contrasts)",
            "design_column": "grp", "formula": "~ batch + grp", "control": "C", "treatment": ["H", "HM", "L", "M"],
            "contrasts": contrasts_rec, "primary_contrast": "H_vs_C", "estimand_type": "causal (randomised intervention)",
            "levels": design_check["levels"]["grp"]},
            candidates=[{"value": "pool HIIT and HIIT+MCTi as 'exercise'", "reason_rejected": "biologically distinct levels; paper contrasts each vs Control"},
                        {"value": "H vs HM (MCT effect within trained)", "reason_rejected": "not a planned contrast in the paper's DE (S2.7.1.p1)"},
                        {"value": "H vs C only", "reason_rejected": "paper plans all four vs Control; HM/L/M kept as separate contrasts, H_vs_C marked primary for the exercise question"}],
            evidence=[dm, dc_item, paper], paper={"locator": "S2.7.1.p1; S2.2.p1"}, confidence="high",
            reasoning="Five randomised, independent groups with Control as reference; the paper fits Wald contrasts L/H/M/HM vs C. Control n=4, others n=6; every arm replicated.")

case.decide("covariance", final={"status": "required", "blocking_terms": [],
            "covariates": [{"name": "batch", "disposition": "included (H_vs_C, the only contrast in which batch varies: H batch1=3, batch2=3; C all batch1); constant within the L/M/HM vs C sample subsets, so not estimable there and dropped"}],
            "full_model_rank": design_check["rank"], "full_model_residual_df": design_check["residual_df"],
            "batch_vs_grp": conf[0]["status"], "pairing": "each GSM is a different animal (titles control1-4, hiit1-6, ...); no repeated measures"},
            candidates=[{"value": "no batch term", "reason_rejected": "paper models ~ Batch + Grouping; batch2 holds 3 of 6 HIIT samples, so omitting it would confound part of the HIIT effect with batch"}],
            evidence=[dm, dc_item, paper], paper={"locator": "S2.7.1.p1"}, confidence="high",
            reasoning="batch is crossed with grp (not aliased): batch2 contains only HIIT samples, so the batch effect is identified only by the 3+3 split of HIIT. ~ grp + batch is full rank (rank 6, residual df 22). No subject/animal blocking needed (independent animals).")

case.decide("method", final={"method": "DESeq2 (pydeseq2, Wald test), one two-group fit per contrast",
            "matrix_type": "raw counts", "formula": "~ batch + grp (H_vs_C); ~ grp (HM_vs_C, L_vs_C, M_vs_C, batch constant in subset)",
            "pre_filter": "all-zero genes dropped by the executor; DESeq2 independent filtering of padj",
            "effect_size": "MLE log2FoldChange (unshrunken, as DESeq2 results() default)",
            "paper_route": {"method": "DESeq2 ~ Batch + Grouping on all 28 samples after edgeR filterByExpr", "status": "blocked",
                            "reason": "run_deseq2_analysis fits only the two arms of a contrast (select_valid_two_group_design subsets samples), so dispersions are estimated from the 2-group subset rather than all 5 groups; no filterByExpr executor in the repository (inmoose.edgepy lacks filterByExpr)"}},
            candidates=[{"value": "limma multigroup on log2(CPM+1), ~ 0 + grp + batch, all 28 samples", "reason_rejected": "keeps the single-model structure but changes the statistical method away from the paper's count model; DESeq2 per-contrast stays closer to the paper"},
                        {"value": "edgeR / limma-voom", "reason_rejected": "no covariate interface; batch required for H_vs_C"}],
            evidence=[prof_item, dc_item, paper], paper={"locator": "S2.7.1.p1"}, confidence="medium",
            reasoning="Raw integer counts support the paper's DESeq2 route. The repository DESeq2 executor accepts the batch covariate but subsets to the two contrast arms, and filterByExpr is unavailable, so this is a declared deviation in dispersion pooling and gene pre-filtering, not in method family or contrast.")

case.decide("threshold", final={"paper_threshold": PT, "threshold_source": "paper_on_deviation_route",
            "applied_threshold": dict(PT), "deviation_note": "paper rule applied unchanged to the two-group DESeq2 fits (route deviation is in model scope/pre-filter, not in the threshold)"},
            evidence=[paper], paper={"locator": "S2.7.1.p1"}, confidence="high",
            reasoning="Paper: genes with BH FDR < 0.05 and |log2FC| > 0.5 are DEGs (S2.7.1.p1, S3.3.p1). Applied exactly via native.apply_threshold on padj and log2FoldChange.")

plan = {"case": "GSE308674", "contrasts": CONTRASTS, "executor": "tools.deseq2_tools:run_deseq2_analysis",
        "counts_csv": aln["outputs"]["aligned_matrix"]["path"], "metadata_csv": dmeta["output"],
        "covariates": {"H_vs_C": "batch"}, "threshold": PT,
        "enrichment": {"GSEA": "Hallmark (MSigDB mh.all) on H_vs_C, HM_vs_C, L_vs_C, M_vs_C, ranking stat",
                       "ORA": "Enrichr GO BP/MF/CC + KEGG on H_vs_C DEGs (applied threshold)"}}
case.write_json("reproduction_plan.json", plan, role="reproduction_plan")
disc = [
    {"item": "deposited count CSV", "paper": "featureCounts counts", "data": "6 genes split across continuation rows (spreadsheet 32,767-char cell overflow in annotation columns)", "disposition": "executable_without_change", "action": "deterministic repair, no values altered (repair_log.json)"},
    {"item": "model scope", "paper": "one DESeq2 model on all 5 groups, ~ Batch + Grouping", "data": "executor fits two arms per contrast", "disposition": "requires_explicit_deviation", "action": "two-group DESeq2; batch kept where estimable (H_vs_C)"},
    {"item": "pre-filter", "paper": "edgeR filterByExpr", "data": "not available in repository", "disposition": "requires_explicit_deviation", "action": "only all-zero genes removed; DESeq2 independent filtering"},
    {"item": "batch layout", "paper": "Batch not described", "data": "batch2 = 3 HIIT samples only", "disposition": "executable_without_change", "action": "batch in H_vs_C model; batch effect identified only from HIIT samples"},
    {"item": "Control n", "paper": "n = 4-6 RNA-seq", "data": "Control 4 libraries", "disposition": "executable_without_change", "action": "none"},
    {"item": "GSEA engine", "paper": "fgsea, 10,000 permutations, padj <= 0.25", "data": "gseapy prerank Hallmark", "disposition": "requires_explicit_deviation", "action": "gseapy prerank on Wald stat; reported separately"},
]
case.write_json("paper_data_discrepancies.json", disc, role="paper_data_discrepancies")
print("decisions recorded")
