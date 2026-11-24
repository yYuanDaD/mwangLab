import json, sys, pandas as pd
R = sys.argv[1]
md = pd.read_csv(f"{R}/prep/GSE224900_metadata_subject.csv", index_col=0)
tp = md.title.str.split().str[1].str.split("_").str[0]
excl = {}
for gsm, t in tp.items():
    if t in ("PREac", "POSTac"):
        excl[gsm] = f"{t}: post hyperinsulinemic-euglycemic clamp biopsy; paper's RNA-seq DE uses fasted PRE/POST/REC biopsies (S2.4.p1, S3.4.p1)"
    elif t == "Day1":
        excl[gsm] = "Day1: after 2-wk drug run-in, before bed rest; not part of the paper's PRE/POST/REC DE contrasts (S3.4.p1)"
key2gsm = dict(zip(md.title.str.split().str[0], md.index))
sexfix = {
    "19565X81": "sex swap: POSTbc labelled F participant 19565_S078 but XIST-absent/chrY-high, while the same participant's PREbc, PREac, Day1, POSTac and 7d biopsies are female",
    "19565X96": "sex swap: PREbc labelled F participant 19565_S096 but male by XIST/chrY, while that block's other 5 biopsies are female",
    "19565X90": "block 19565_S090 inconsistent: PREbc/PREac female but Day1/POSTbc/POSTac/7d male; participant identity of the block cannot be established",
    "19565X93": "block 19565_S090 inconsistent (see 19565X90)",
    "19565X95": "block 19565_S090 inconsistent (see 19565X90)",
}
for k, why in sexfix.items():
    excl[key2gsm[k]] = why
thr = {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": None, "inclusive": False}
planned = ["time_POST_vs_PRE_trt-Pla", "time_REC_vs_PRE_trt-Pla", "time_POST_vs_PRE_trt-Met", "time_REC_vs_PRE_trt-Met"]
spec = {
 "run_dir": R,
 "request": "Analyze GSE224900 for PMID 37486024 (Disuse-induced muscle fibrosis, cellular senescence, and senescence-associated secretory phenotype in older adults are alleviated during re-ambulation with metformin pre-treatment.): how exercise affects gene expression as the paper intends.",
 "decision_maker": "Claude Opus 5.5 (claude-code session)", "platform": "claude-code",
 "data_root": "E:/agent/mwangLab_pdf/data",
 "cases": [{
  "case_id": "GSE224900", "accession": "GSE224900",
  "inputs": {"paper": ["test/experiments/paper_screen_20261028/papers/PMC10652302.paper.md"],
             "metadata": f"E:/agent/mwangLab_pdf/{R}/prep/GSE224900_metadata_subject.csv",
             "matrix": f"E:/agent/mwangLab_pdf/{R}/prep/GSE224900_merged_counts.csv.gz",
             "raw_tar": False, "prep_scripts": [f"{R}/prep/prep_merge.py"]},
  "gates": {
   "paper_reconstruction": {"final": {
      "accessions": ["GSE224900"],
      "assay": "bulk total RNA-seq (rRNA-depleted), vastus lateralis, older adults (S2.7.p1)",
      "primary_estimand": "Within-participant change in muscle gene expression with 5 d bed rest (disuse; POST vs PRE) and after 7 d re-ambulation (REC vs PRE), separately in the placebo and metformin arms (S3.4.p1, Fig 5a-d). Physical-activity axis = disuse/reloading, not structured exercise.",
      "factors": {"time": ["PRE", "POST", "REC"], "treatment": ["Placebo", "Metformin"]},
      "repeated_measure_unit": "participant (biopsies at PRE, DAY1, POST, REC; S2.4.p1)",
      "inclusion": "fasted biopsies at PRE, POST, REC; N = 9-10/group (Fig 5 legend)",
      "planned_contrasts": ["Placebo POST vs PRE (S3.4.p1; paper 441 DEGs)", "Metformin POST vs PRE (S3.4.p1; 377)",
                            "Placebo REC vs PRE (S3.4.p1; 3550)", "Metformin REC vs PRE (S3.4.p1; 1386)"],
      "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": None, "source_locator": "S2.7.p1"},
      "paper_method": "DESeq2 1.30 via hciR (S2.7.p1); formula not stated",
      "paper_results": "collagen isoforms highly upregulated in placebo REC (S3.4.p1); CDKN1A, TP53 up in placebo not metformin after bed rest and recovery (S3.5.p1)"},
     "reasoning": "S2.7.p1 gives DESeq2 + 5% FDR, no fold-change rule; S3.4.p1 gives the four within-arm DEG counts vs PRE. The paper's activity manipulation is bed-rest disuse followed by re-ambulation; there is no exercise-training arm, so the activity estimand is disuse/reloading within each arm.",
     "confidence": "high", "locator": "S2.7.p1"},
   "ownership": {"final": {"owned": True, "checks": ["S2.7.p1 and S11.p1 name GSE224900", "GEO contact Drummond lab (senior author)", "timepoint labels PRE/Day1/POST/7d and Placebo/Metformin match the trial design (S2.3.p1)", "10 metformin participants (5F/5M = Table 1) and 9 placebo (paper N=9-10/group)"]},
     "reasoning": "Both count files (19565R, 20063R sequencing runs) belong to GSE224900 and the paper names it.", "confidence": "high"},
   "alignment": {"key_column": "key",
     "patterns": {"time": ["title", r"^\S+ (PREbc|PREac|Day1|POSTbc|POSTac|7d)_(?:Con|Met)$"],
                  "trt": ["title", r"_(Con|Met)$"]},
     "recode": {"time": {"PREbc": "PRE", "POSTbc": "POST", "7d": "REC", "PREac": "PREac", "POSTac": "POSTac", "Day1": "DAY1"},
                "trt": {"Con": "Pla", "Met": "Met"}},
     "aliases": {}, "exclude_samples": excl,
     "final": {"subject_key": "derived in prep_merge.py from consecutive per-participant biopsy blocks; age/sex/treatment constant within each block"},
     "reasoning": "Matrix columns (19565X1...) equal the first token of title, written as column `key` by prep_merge.py (two count files merged on identical Ensembl IDs). GEO has no participant ID; prep_merge.py assigns `subject` by sample-number blocks that each start at a PREbc biopsy - every block has one age, one sex and one treatment, giving 9 placebo + 10 metformin participants. Clamp (ac) and Day1 biopsies excluded: the paper's DE uses fasted PRE/POST/REC.",
     "confidence": "medium"},
   "matrix": {"matrix_type": "raw counts", "recommended_method": "DESeq2",
     "final": {"source": "GSE224900_19565R_counts.txt.gz + GSE224900_20063R_counts.txt.gz merged", "paper_input": "DESeq2 on counts (S2.7.p1)"},
     "reasoning": "All values integer, median 0, max ~1.2e7; data_processing: STAR two-pass alignment to GRCh38/Ensembl 104 with gene counts; paper used DESeq2.", "confidence": "high"},
   "design": {"factors": ["time"], "references": {"time": "PRE"}, "subject": "subject", "organism": "Human",
     "strata": ["trt"], "planned": planned, "covariate_candidates": [],
     "final": {"analysis_type": "repeated-measures, within-arm time contrasts", "formula": "~ subject + time (per arm)",
               "contrasts": [{"name": p, "control": "PRE", "treatment": p.split("_")[1], "role": "primary" if "Pla" in p else "secondary"} for p in planned],
               "estimand_type": "within-subject change; no non-bed-rest control arm"},
     "candidates": [{"value": "treatment x time interaction", "reason_rejected": "the paper's reported DEG counts are within-arm vs PRE; interaction is the drug question, not the activity estimand"},
                    {"value": "include DAY1", "reason_rejected": "DAY1 reflects 2-wk drug run-in, not disuse; paper's RNA-seq DE uses PRE/POST/REC (S3.4.p1)"}],
     "reasoning": "Placebo arm isolates disuse/re-ambulation (primary); metformin arm reproduces the paper's second set but mixes drug exposure with disuse (secondary). Each arm fitted separately as the paper reports per-arm volcano plots.", "confidence": "high"},
   "covariance": {"final": {"status": "required", "blocking_terms": ["subject"],
       "covariates": [{"name": "sex", "disposition": "nested within subject; absorbed by subject block (per-sex fits run as exploratory)"},
                      {"name": "run", "disposition": "sequencing run nested within subject; absorbed by subject block"}]},
     "confounding_candidates": ["run", "sex"],
     "reasoning": "Repeated biopsies per participant -> subject block. Sex and sequencing run are constant within subject, so the subject term absorbs them.", "confidence": "high"},
   "method": {"final": {"method": "DESeq2 (pydeseq2 Wald)", "formula": "~ subject + time",
       "paper_route": {"method": "DESeq2 1.30 (hciR)", "status": "reproduced_approximately"},
       "deviations": ["pydeseq2 instead of R DESeq2 1.30/hciR; hciR default filtering and formula not stated in the paper", "subject derived from sample-number blocks"]},
     "transform": None, "reasoning": "Raw counts support the paper's DESeq2 route; one model per arm with all three timepoints and subject blocking.", "confidence": "medium"},
   "threshold": {"final": {"paper_threshold": thr, "threshold_source": "paper", "applied_threshold": thr},
     "reasoning": "S2.7.p1: 5% FDR, no fold-change cutoff; Fig 5 legend: adjusted p < 0.05.", "confidence": "high"},
   "study": {"final": {"route": "paper_aligned", "caveats": [
        "Activity axis is bed-rest disuse and re-ambulation, not exercise training.",
        "No time-matched non-bed-rest control: time contrasts include any time/season effect; metformin-arm contrasts also include drug exposure (POST) or withdrawal (REC).",
        "Participant IDs were derived from sample-number blocks, not given in GEO.",
        "Expression-inferred sex contradicts GEO labels in 7 metformin-arm biopsies: 5 biopsies excluded, one block relabelled F; the metformin arm therefore differs from the paper's sample set (paper presumably used the labels as deposited)."]},
     "paper_counts": {"pla/time_POST_vs_PRE_trt-Pla": 441, "pla/time_REC_vs_PRE_trt-Pla": 3550,
                      "met/time_POST_vs_PRE_trt-Met": 377, "met/time_REC_vs_PRE_trt-Met": 1386},
     "paper_genes": {"pla/time_REC_vs_PRE_trt-Pla": ["COL1A1", "COL3A1", "COL1A2", "CDKN1A", "TP53"],
                     "pla/time_POST_vs_PRE_trt-Pla": ["CDKN1A", "TP53"]},
     "reasoning": "All four contrasts follow the paper's DESeq2 + FDR 5% route.", "confidence": "medium"}},
  "discrepancies": [
    {"item": "participant ID", "paper": "paired design, 9-10/group", "data": "GEO lacks participant IDs; derived from biopsy blocks (age/sex constant)", "disposition": "executable_without_change"},
    {"item": "placebo n", "paper": "Table 1: 10 placebo (6F/4M)", "data": "9 placebo participants sequenced (5F/4M); Fig 5 N = 9-10/group", "disposition": "executable_without_change"},
    {"item": "sample sex labels (metformin arm)", "paper": "metformin 5F/5M (Table 1)", "data": "XIST/chrY: 19565_S084 block entirely female though GEO says M (label corrected, block kept); single swapped biopsies 19565X81 and 19565X96 excluded; block 19565_S090 switches sex between PREac and Day1, all its PRE/POST/REC biopsies excluded. Metformin arm analysed with 9 participants (PRE 8, POST 8, REC 9).", "disposition": "executable_with_exclusions"},
    {"item": "two sequencing runs", "paper": "not mentioned", "data": "19565R (17 participants) and 20063R (2 placebo participants)", "disposition": "executable_without_change"}],
  "executions": [
    {"name": "pla", "tool": "tools.joint_contrasts:run_joint_deseq2", "subset": {"trt": ["Pla"]},
     "args": {"comparisons": ["time_POST_vs_PRE_trt-Pla", "time_REC_vs_PRE_trt-Pla"], "covariates": ["subject"]},
     "role": "primary", "reasoning": "placebo arm: disuse and re-ambulation vs PRE, ~ subject + time"},
    {"name": "met", "tool": "tools.joint_contrasts:run_joint_deseq2", "subset": {"trt": ["Met"]},
     "args": {"comparisons": ["time_POST_vs_PRE_trt-Met", "time_REC_vs_PRE_trt-Met"], "covariates": ["subject"]},
     "role": "secondary", "reasoning": "metformin arm, same model"}] + [
    {"name": f"{arm.lower()}_unpaired", "tool": "tools.joint_contrasts:run_joint_deseq2", "subset": {"trt": [arm]},
     "args": {"comparisons": [f"time_POST_vs_PRE_trt-{arm}", f"time_REC_vs_PRE_trt-{arm}"], "covariates": []},
     "role": "sensitivity", "reasoning": "~ time without subject: tests whether the paper's (unstated) hciR model ignored pairing"}
    for arm in ("Pla", "Met")] + [
    {"name": f"{arm.lower()}_{sx}", "tool": "tools.joint_contrasts:run_joint_deseq2", "subset": {"trt": [arm], "sex": [sx]},
     "args": {"comparisons": [f"time_POST_vs_PRE_trt-{arm}", f"time_REC_vs_PRE_trt-{arm}"], "covariates": ["subject"]},
     "role": "exploratory", "reasoning": f"per-sex exploratory fit ({arm}, sex {sx}); paper pooled sexes"}
    for arm in ("Pla", "Met") for sx in ("F", "M")],
  "enrichment": [
    {"execution": "pla/time_REC_vs_PRE_trt-Pla", "ora": False, "gsea": True, "ranking_metric": "stat", "reasoning": "paper ran fgsea (KEGG/Reactome) on recovery; Hallmark GSEA as a check of collagen/TGF-beta direction"},
    {"execution": "met/time_REC_vs_PRE_trt-Met", "ora": False, "gsea": True, "ranking_metric": "stat", "reasoning": "same for metformin arm"}]
 }]}
json.dump(spec, open(f"{R}/case_spec.json", "w"), indent=1)
print(len(excl))
