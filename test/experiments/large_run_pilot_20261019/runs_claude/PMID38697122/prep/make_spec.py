"""Writes case_spec.json (one case per paper tissue). Decisions are written here by hand."""
import json
import pandas as pd
_m = pd.read_csv("data/GSE242354/GSE242354_metadata.csv", index_col=0)
VIAL2GSM = dict(zip(_m.title.str.extract(r"vial_(\d+)$")[0], _m.index))

R = "test/experiments/large_run_pilot_20261019/runs_claude/PMID38697122"
PAPER = "test/experiments/paper_screen_20261019/papers/PMC11228891.paper.md"
# file tag -> (case suffix, paper label, reference vials, damaged lines dropped, genes lost)
TISSUES = {
    "t52-hippocampus": ("HIPPOC", "hippocampus", ['80035995205', '80034885205', '80035995206', '80034885206', '80035995207', '80034885207'], 0, 0),
    "t55-gastrocnemius": ("SKMGN", "SKM-GN", ['80001995510', '80000885510', '80001995528', '80000885537', '80001995540', '80001995542', '80000885540', '80000885541', '80001995533', '80001995532', '80000885533', '80000885532'], 0, 0),
    "t58-heart": ("HEART", "heart", ['80033995819', '80032885819'], 23, 125),
    "t59-kidney": ("KIDNEY", "kidney", ['80029995909', '80028885909'], 5, 31),
    "t66-lung": ("LUNG", "lung", ['80026886619', '80027996619'], 1, 5),
    "t68-liver": ("LIVER", "liver", ['80003996808', '80002886808', '80003996809', '80002886809'], 1, 6),
    "t69-brown-adipose": ("BAT", "BAT", ['80031996905', '80030886905'], 0, 0),
    "t70-white-adipose": ("WATSC", "WAT-SC", ['80005997012', '80004887012'], 4, 23),
}
PAPER_COUNTS = {"BAT": 1237, "hippocampus": 124}
PAPER_GENES = {"hippocampus": ["Gpr37l1"], "heart": ["Adra1b", "Adra1d", "Adra2b", "Adrb1"],
               "WAT-SC": ["Adra1b", "Adra1d", "Adra2b", "Adrb1"]}
ENRICH = {"BAT", "lung", "SKM-GN"}
COMPS = ["grp_W1_vs_SED", "grp_W2_vs_SED", "grp_W4_vs_SED", "grp_W8_vs_SED"]
PT = {"metric": "padj", "adjustment": "IHW (tissue as covariate) on Fisher-combined male/female LRT p-values",
      "cutoff": 0.05, "effect_metric": None, "effect_cutoff": None, "inclusive": False,
      "extra_rule": "direction of week-8 log2FC must agree between males and females", "source_locator": "S5.4.3.p2"}
AT = {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": None, "inclusive": False}

cases = []
for tag, (suf, label, refs, nbad, nlost) in TISSUES.items():
    excl = {VIAL2GSM[v]: f"vial {v}: MoTrPAC pooled reference RNA (treatment 'Reference'), not an animal of the study design" for v in refs}
    if label == "BAT":
        excl[VIAL2GSM["90266016902"]] = ("vial 90266016902: ""S2.1.p1: one female BAT sample clustered with WAT-SC and was excluded; our check "
                               "(log2CPM correlation to the BAT vs WAT-SC median profile) singles out this "
                               "female control (r_BAT 0.763 vs r_WAT 0.765; every other BAT sample r_BAT - r_WAT > 0.07)")
    if nbad:
        repair_note = (f"GEO file has {nbad} damaged lines (NUL-byte blocks, same bytes on the GEO FTP server); "
                       f"prep/repair_matrix.py drops them, losing {nlost} of 32,883 genes")
    else:
        repair_note = "GEO file intact; prep/repair_matrix.py only converted it to CSV (no rows dropped)"
    paper_counts = {"pooled/grp_W8_vs_SED": PAPER_COUNTS[label]} if label in PAPER_COUNTS else {}
    paper_genes = {"pooled/grp_W8_vs_SED": PAPER_GENES[label]} if label in PAPER_GENES else {}
    ex_common = {"round_estimated_counts": True, "alpha": 0.05}
    flt = {"min_cpm": 0.5, "min_samples": 2}
    executions = [
        {"name": "pooled", "tool": "tools.joint_contrasts:run_joint_deseq2",
         "args": {**ex_common, "comparisons": COMPS, "covariates": ["sex"]}, "filter_low_counts": flt,
         "role": "primary",
         "reasoning": "One DESeq2 fit on all 50 animals of the tissue (5 groups x 5 M + 5 F), ~ sex + grp. "
                      "grp_W8_vs_SED is the paper's 8-week EET vs control estimand (S2.7.p1; S5.4.3.p2 week-8 log2FC); "
                      "W1/W2/W4 vs SED come from the same fit and are exploratory (the paper's LRT used all groups)."},
        {"name": "male", "tool": "tools.joint_contrasts:run_joint_deseq2",
         "args": {**ex_common, "comparisons": COMPS}, "filter_low_counts": flt, "subset": {"sex": ["male"]},
         "role": "secondary",
         "reasoning": "S5.4.3.p2 tests males and females separately with all training groups in the model; "
                      "male model ~ grp (25 animals); week-8 contrast feeds the sign-agreement rule."},
        {"name": "female", "tool": "tools.joint_contrasts:run_joint_deseq2",
         "args": {**ex_common, "comparisons": COMPS}, "filter_low_counts": flt, "subset": {"sex": ["female"]},
         "role": "secondary",
         "reasoning": "Female model ~ grp, as for males (S5.4.3.p2)."},
    ]
    enrichment = []
    if label in ENRICH:
        for d in ("up", "down"):
            enrichment.append({"execution": "pooled/grp_W8_vs_SED", "ora": True, "gsea": False, "direction": d,
                               "reasoning": "S2.7.p2/FIG6C: paper runs ORA (Metascape) on up- and down-regulated ERGs "
                                            "per tissue; run for the three tissues whose pathways the text names "
                                            "(BAT immune up / TCA down, lung immune down, SKM-GN mitochondrial up)."})
    planned = [f"8-week EET vs control, {label} (S2.7.p1, FIG6A); ERGs total 3,477 across 8 tissues; "
               + (f"paper: {PAPER_COUNTS[label]} ERGs" if label in PAPER_COUNTS else "per-tissue count only in Figure 6A (not in text)")]
    case = {
        "case_id": f"GSE242354_{suf}", "accession": "GSE242354",
        "inputs": {"paper": [PAPER], "metadata": "GSE242354/GSE242354_metadata.csv",
                   "matrix": f"{R}/prep/{tag}_counts.csv", "raw_tar": False,
                   "prep_scripts": [f"{R}/prep/repair_matrix.py"]},
        "gates": {
            "paper_reconstruction": {
                "final": {
                    "accessions": ["GSE242358 (SuperSeries, S5.2.3.p1)", "GSE242354 (RNA-seq SubSeries)"],
                    "tissue": label,
                    "primary_estimand": f"Effect of 8 weeks of endurance exercise training (EET) vs sedentary control on gene expression in rat {label} (F344, 6 months old, 5 M + 5 F per group)",
                    "planned_contrasts": planned,
                    "factors": {"training group": ["control (8 w sedentary)", "1 w", "2 w", "4 w", "8 w"], "sex": ["male", "female"]},
                    "sample_inclusion": "5 animals per sex per group randomly selected for assays (S5.4.2.p1); one female BAT sample excluded (S2.1.p1)",
                    "paper_method": "DESeq2 LRT per sex: full ~ technical covariates + training group (control,1,2,4,8 w) vs reduced ~ technical covariates; Fisher sum-of-logs across sexes; IHW across tissues; 5% FDR; keep genes whose week-8 log2FC agrees in sign in both sexes (S5.4.3.p2)",
                    "low_count_filter": "remove genes with CPM <= 0.5 in all but one sample, per tissue (S5.4.3.p1)",
                    "paper_threshold": PT,
                    "paper_results": "3,477 ERGs across 8 tissues; BAT 1,237 (largest), hippocampus 124 (smallest); lung ~2x more down than up (S2.7.p1)",
                },
                "reasoning": "S2.7.p1 and S5.4.3.p2 define ERGs; S5.4.2.p1 sample selection; S5.4.3.p1 filtering. The paper's estimand is EET vs control at 8 weeks, with the LRT including the 1/2/4 w groups.",
                "confidence": "high", "locator": "S5.4.3.p2"},
            "ownership": {
                "final": {"owned": True, "checks": [
                    "S5.2.3.p1 deposits RNA-seq at GEO GSE242358; GSE242354 metadata series_id = 'GSE242354,GSE242358'",
                    f"matrix is the MoTrPAC PASS1B {tag} RSEM gene-count file of GSE242354",
                    "10 animals per group (5 M, 5 F) for control-8w and 1/2/4/8 w training, matching S5.4.2.p1 / S5.4.10.p1",
                    repair_note]},
                "reasoning": "Series id, tissue, species (Rattus norvegicus) and group sizes match the paper.",
                "confidence": "high", "locator": "S5.2.3.p1"},
            "alignment": {
                "key_column": "vial",
                "key_patterns": {"vial": ["title", r"_vial_(\d+)$"]},
                "patterns": {"sex": ["title", r"_(male|female)_"]},
                "aliases": {"grp": "characteristics_ch1.1.treatment"},
                "recode": {"grp": {"Control - 8 weeks": "SED", "Training - 1 week": "W1", "Training - 2 weeks": "W2",
                                   "Training - 4 weeks": "W4", "Training - 8 weeks": "W8", "Reference": "REF"}},
                "combine": {},
                "exclude_samples": excl,
                "reasoning": "Matrix columns are MoTrPAC vial labels, which end every GEO title ('..._vial_<label>'); exact match on that derived key. Sex and group from the title and the treatment field. Reference RNA vials are not study animals.",
                "confidence": "high"},
            "matrix": {
                "matrix_type": "estimated counts", "recommended_method": "DESeq2",
                "final": {"source": "GEO file name 'rsem-genes-count'; data_processing names RSEM; ~92% integer values with fractional entries (RSEM expected counts)",
                          "paper_input": "RSEM gene counts, filtered, then DESeq2 (S5.4.3.p1)"},
                "reasoning": "RSEM expected counts: DESeq2 after rounding, as in the paper's pipeline (S5.4.3.p1).",
                "confidence": "high", "locator": "S5.4.3.p1"},
            "design": {
                "factors": ["grp"], "references": {"grp": "SED"}, "organism": "Rat",
                "covariate_candidates": ["sex"], "planned": ["grp_W8_vs_SED"],
                "final": {"analysis_type": "multi-group (one control, four training durations), independent animals",
                          "formula": "~ sex + grp",
                          "contrasts": [{"name": "grp_W8_vs_SED", "control": "SED", "treatment": "W8", "role": "primary"},
                                        {"name": "grp_W4_vs_SED", "control": "SED", "treatment": "W4", "role": "exploratory"},
                                        {"name": "grp_W2_vs_SED", "control": "SED", "treatment": "W2", "role": "exploratory"},
                                        {"name": "grp_W1_vs_SED", "control": "SED", "treatment": "W1", "role": "exploratory"}],
                          "estimand_type": "causal (randomized to control or training, S5.4.1.p1)"},
                "candidates": [{"value": "LRT over all 5 groups per sex + Fisher + IHW (paper)", "reason_rejected": "no LRT/Fisher/IHW executor in the runner; Wald W8 vs SED from the same all-group model is the closest available estimand"},
                               {"value": "W8 vs SED using only those 20 animals", "reason_rejected": "the paper's model includes all training groups; one model on all samples is preferred"}],
                "reasoning": "One control (8-week sedentary) with four training durations: one model with planned contrasts vs control, never pooled levels. Sex kept as a covariate in the pooled model and analysed separately in per-sex models as the paper does.",
                "confidence": "medium", "locator": "S5.4.3.p2"},
            "covariance": {
                "confounding_candidates": ["sex"],
                "final": {"status": "required", "blocking_terms": [],
                          "covariates": [{"name": "sex", "disposition": "included"},
                                         {"name": "technical covariates (RIN, UMI duplication, etc.)", "disposition": "excluded: the paper does not list which technical covariates it used (S5.4.3.p2 cites ref 2); not chosen by column name"}]},
                "reasoning": "Animals are independent (one sample per animal per tissue), no blocking. Sex balanced across groups; included as a covariate in the pooled model; per-sex models need none.",
                "confidence": "medium", "locator": "S5.4.3.p2"},
            "method": {
                "transform": None,
                "final": {"method": "DESeq2 (pydeseq2 Wald, ~ sex + grp; per-sex ~ grp)", "formula": "~ sex + grp",
                          "rounding_documented": True,
                          "paper_route": {"method": "DESeq2 LRT per sex + Fisher combination + IHW + sign agreement", "status": "blocked",
                                          "reason": "runner has no LRT, Fisher meta-analysis or IHW executor"},
                          "deviations": ["Wald W8 vs SED instead of LRT over all groups",
                                         "pooled-sex model with sex covariate instead of Fisher-combined per-sex tests (per-sex models run as secondary)",
                                         "BH instead of IHW", "technical covariates not included", "RSEM expected counts rounded to integers",
                                         "low-count filter: CPM >= 0.5 in >= 2 samples of the execution (paper: genes with CPM <= 0.5 in all but one sample removed)"]},
                "reasoning": "Paper used DESeq2 on filtered RSEM counts; same family here, with declared deviations.",
                "confidence": "medium", "locator": "S5.4.3.p2"},
            "threshold": {
                "final": {"paper_threshold": PT, "threshold_source": "paper_on_deviation_route", "applied_threshold": AT,
                          "deviation_note": "paper: 5% IHW-FDR on Fisher-combined per-sex LRT p plus sex sign agreement at week 8; applied: BH padj < 0.05 on the pooled Wald W8 vs SED test, no fold-change rule (the paper has none). Sign agreement is computed afterwards in HANDBACK as a supplementary count."},
                "reasoning": "S5.4.3.p2: ERGs at 5% IHW FDR, no fold-change cutoff.", "confidence": "high", "locator": "S5.4.3.p2"},
            "study": {
                "final": {"route": "declared_deviation",
                          "caveats": ["paper ERGs are LRT-based (any training time point) with Fisher/IHW; ours are Wald week-8 vs control with BH, so counts are not expected to match exactly",
                                      "technical covariates omitted", repair_note]},
                "paper_counts": paper_counts, "paper_genes": paper_genes,
                "reasoning": "Paper counts from S2.7.p1 text; other tissues' counts are only in Figure 6A.",
                "confidence": "medium"},
        },
        "discrepancies": [
            {"item": "differential test", "paper": "DESeq2 LRT per sex, Fisher, IHW, sign agreement",
             "data": "runner offers Wald contrasts with BH", "disposition": "declared_deviation"},
            {"item": "matrix integrity", "paper": "-", "data": repair_note,
             "disposition": "repaired" if nbad else "executable_without_change"},
        ],
        "executions": executions,
        "enrichment": enrichment,
    }
    cases.append(case)

spec = {"run_dir": R,
        "request": "Analyze GSE242354 for PMID 38697122 (Molecular adaptations in response to exercise training are associated with tissue-specific transcriptomic and epigenomic signatures.): how exercise affects gene expression as the paper intends.",
        "decision_maker": "Claude Opus 5.5 (claude-code session)", "platform": "claude-code", "data_root": "data", "cases": cases}
json.dump(spec, open(f"{R}/case_spec.json", "w"), indent=1)
print("wrote", len(cases), "cases")
