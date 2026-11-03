import sys, pathlib
sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))
from tools import native
native.enable_native_mode()
RUN = "test/experiments/model_compare_20261103/runs/sonnet/PMID34358431"
D = "E:/agent/mwangLab_pdf/data/GSE174785"
PAPER = "E:/agent/mwangLab_pdf/test/experiments/paper_screen_20261019/papers/PMC8432967.paper.md"
run = native.RunRecorder(RUN, request="Analyze GSE174785 for PMID 34358431: how exercise affects gene expression as the paper intends. Refuse at the right gate if data do not support an exercise comparison.",
                         platform_name="claude-code", decision_maker="Claude Sonnet 5.5 (claude-sonnet-5-5)", case_ids=["PMID34358431"])
case = run.case("PMID34358431", accession="GSE174785")
paper = case.add_input(PAPER, "paper")
meta = case.add_input(f"{D}/GSE174785_metadata.csv", "metadata")
mat = case.add_input(f"{D}/GSE174785_merged_from_tar.csv", "matrix")

case.decide("paper_reconstruction", final={
    "accessions": ["GSE174785 (bulk RNA-seq, this paper)", "GSE158984 (scRNA-seq, this paper)"],
    "assay": "bulk RNA-seq of sorted CD31+CD45- muscle ECs (Methods: Smart-seq II; GEO: TruSeq stranded mRNA SE100); kallisto + DESeq2",
    "sample_inclusion": "20 samples: 5 reps each of WT and Atf4 dEC (Pdgfb-CreERT2 x Atf4 loxP, tamoxifen) x RmEC (soleus, oxidative) x WmEC (EDL, glycolytic)",
    "sample_exclusion": "not_reported",
    "factors": [{"name": "muscle_type", "levels": ["RmEC (soleus)", "WmEC (EDL)"]}, {"name": "genotype", "levels": ["WT", "Atf4 dEC"]}],
    "primary_estimand": "Paper's bulk RNA-seq estimand: transcriptional difference between oxidative (red, soleus) and glycolytic (white, EDL) muscle ECs in WT, and its dependence on endothelial Atf4. Exercise (14 d voluntary wheel running) enters the paper only via scRNA-seq (GSE158984, sedentary vs exercised GAS ECs) and histology, not via GSE174785.",
    "planned_contrasts": ["WT RmEC vs WT WmEC (782 DEGs, S2.2.p2)", "Atf4 dEC RmEC vs Atf4 dEC WmEC (S2.6.p1)"],
    "blocking_or_covariance": {"status": "not_reported"},
    "matrix_scale": "kallisto counts (raw counts into DESeq2)",
    "paper_method": "DESeq2 (size factors, dispersion, GLM); genes with <=1 count filtered; VST for PCA",
    "paper_formula": "not_reported",
    "paper_threshold": {"metric": "padj", "adjustment": "DESeq2 default (BH)", "cutoff": 0.05, "inclusive": False,
                        "effect_metric": "log2FC", "effect_cutoff": 1,
                        "effect_rule": "paper says 'log fold change > 1' without stating the base; log2 assumed",
                        "source_locator": "S4.4.3.p2, S2.6.p1"},
    "paper_deg_counts": {"WT_RmEC_vs_WmEC": 782, "second_set_stated": 140, "remaining_after_Atf4_KO": [211, 126]},
    "exercise_in_bulk_dataset": "none: no sedentary/exercised label; GEO treatment_protocol only describes tamoxifen"},
    evidence=[paper, meta], paper={"locator": "S2.2.p2"}, confidence="high",
    reasoning="GSE174785 is listed in TAB1 (RNA-seq raw data for RmECs versus WmECs, WT and Atf4 dEC) and DA.p1. Methods S4.4.3 describe bulk RNA-seq with DESeq2. Exercise (voluntary wheel running) appears only in S2.5/S2.6 histology and scRNA-seq of GAS ECs; the bulk comparison is muscle bed (oxidative vs glycolytic) by genotype.")

case.decide("ownership", final={"accession": "GSE174785", "matrix_file": mat["path"], "metadata_file": meta["path"], "owned": True,
    "checks": ["series_id GSE174785 in metadata", "20 samples GSM5328123-142 = 5 reps x 2 genotypes x 2 muscles, matching TAB1 description",
               "EC sorted from soleus/EDL matches S4.4.3.p1 and S2.6.p1", "matrix is merged kallisto est_counts from GSE174785_RAW.tar"]},
    evidence=[meta, mat, paper], paper={"locator": "TAB1"}, confidence="high",
    reasoning="Accession is the paper's own deposit; sample count, tissue and genotype labels match the paper's description.")

derived = native.derive_columns(meta["path"], case.dir / "aligned" / "metadata_with_matrix_id.csv",
    patterns={"matrix_id": ("supplementary_file_1", r".*/(GSM\d+_\w+)\.txt\.gz$")})
mid = case.add_output(case.dir / "aligned" / "metadata_with_matrix_id.csv", "metadata_with_matrix_id")
aln = native.align_to_metadata(mat["path"], mid["path"], case.dir / "aligned", key_column="matrix_id")
aligned = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
amap = case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
ameta = case.add_output(aln["outputs"]["aligned_metadata"]["path"], "aligned_metadata")
case.decide("alignment", final={"method": aln["method"] + " (matrix_id regex-derived from metadata supplementary_file_1 file name; exact match, no position)",
    "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"], "coverage": aln["coverage"],
    "unmatched_matrix_columns": aln["unmatched_matrix_columns"], "unmatched_metadata_samples": aln["unmatched_metadata_samples"], "derived": derived},
    evidence=[meta, mat, mid, aligned, amap], confidence="high",
    reasoning="Matrix columns are GSM_label; the exact label is the supplementary file name in metadata. Full 20/20 exact coverage.")

prof = native.profile_matrix(aligned["path"])
case.write_json("matrix_profile.json", prof, "matrix_profile")
prof_ev = case.evidence_item("matrix_profile") if False else case.add_output(case.dir / "matrix_profile.json", "matrix_profile")
case.decide("matrix", final={"matrix_type": "estimated counts (kallisto est_counts, transcript-level ENSMUST ids)",
    "recommended_method": "DESeq2 on rounded est_counts after summarising transcripts to genes (paper used DESeq2 on kallisto counts)",
    "evidence": f"integer_fraction={prof['integer_fraction']}, non-negative, column sums 8.5-16M equal est_counts sums of per-sample files (tpm sums 1e6); max {prof['max']}",
    "feature_level": "transcript (ENSMUST); gene collapse needed before gene-level DE"},
    evidence=[prof_ev, mat, meta], paper={"locator": "S4.4.3.p1"}, confidence="high",
    reasoning="Matrix is count scale (est_counts), consistent with the paper's input to DESeq2. Not the blocking issue.")

meta_df = native._frame(aln["outputs"]["aligned_metadata"]["path"])
tab = meta_df.groupby(["source_name_ch1", "characteristics_ch1.2.genotype"]).size().to_dict()
case.write_json("design_cells.json", {" | ".join(k): int(v) for k, v in tab.items()}, "design_cells")
cells = case.add_output(case.dir / "design_cells.json", "design_cells")
case.decide("design", final={}, evidence=[meta, paper, cells], paper={"locator": "S2.5.p1"}, confidence="high",
    decision_status="refused", execution_status="not_run",
    stop_reason=("No exercise contrast exists in GSE174785: the 20 samples differ only by muscle bed (soleus/oxidative vs EDL/glycolytic) and EC-specific Atf4 genotype (WT vs Atf4 dEC); "
                 "there is no sedentary vs exercised (wheel running) label, no pre/post or time factor, and GEO treatment_protocol mentions only tamoxifen. The paper's exercise comparison is the scRNA-seq dataset GSE158984 (S2.5.p1), not this one. "
                 "RmEC vs WmEC is a muscle-type comparison, not an exercise effect, so analysing it would answer a different estimand than 'how exercise affects gene expression'."),
    reasoning="Candidates rejected: (1) RmEC vs WmEC in WT = baseline muscle-bed difference (paper's 782 DEGs), not exercise; (2) WT vs Atf4 dEC = genotype effect; (3) genotype x muscle interaction = ATF4 dependence of the bed difference. None estimates an exercise effect. Metadata and paper agree that no sample was labelled exercised vs sedentary.",
    candidates=[{"value": "WT oxidative (soleus) vs WT glycolytic (EDL)", "reason_rejected": "muscle bed difference, not exercise"},
                {"value": "Atf4 dEC vs WT within muscle", "reason_rejected": "genotype effect, not exercise"},
                {"value": "genotype x muscle interaction", "reason_rejected": "ATF4 dependence of bed difference, not exercise"}])
print(case.finish())
print(run.finish())
