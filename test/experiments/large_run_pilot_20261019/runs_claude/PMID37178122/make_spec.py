# Writes case_spec.json for PMID37178122 / GSE230102 (5 tissues). Decisions are written here by hand;
# the script only expands them per tissue and generates the 50-level strain recode map.
import json
import pandas as pd

ROOT = "E:/agent/mwangLab_pdf"
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID37178122"
PAPER = "test/experiments/paper_screen_20261027/papers/PMC11352395.paper.md"
m = pd.read_csv(f"{ROOT}/data/GSE230102/GSE230102_metadata.csv", index_col=0)
sids = sorted(m.title.str.extract(r"^(\d+)_")[0].unique(), key=int)
strain_recode = {s: f"S{s}" for s in sids}
TH = {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": None, "inclusive": False}
PTH = {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": None,
       "source_locator": "S4.4.1.p3"}
FOUR = ["Slc25a1", "Acly", "Ccn1", "Dusp1"]
tissues = [  # (case suffix, file stem, title suffix, label, paper locator, paper genes)
    ("quad", "quad", "quadriceps", "quadriceps skeletal muscle", "S2.4.p3", FOUR + ["Myoz2", "Esrrb"]),
    ("gWAT", "gWAT", "gWAT", "gonadal white adipose tissue", "S2.5.p1", FOUR + ["Clic4", "Tomm5"]),
    ("liver", "liver", "liver", "liver", "S2.6.p1", ["Mki67"] + FOUR),
    ("heart", "heart", "heart", "heart", "S2.7.p1", FOUR),
    ("BAT", "BAT", "BAT", "brown adipose tissue", "S2.8.p1", FOUR),
]
# Added after attempt 1 (results moved to _previous/): result-vs-paper conflicts belong in the study caveats.
RESULT_CAVEATS = {
    "liver": ["Direction conflict: the paper reports liver DEGs enriched for mitosis/cell cycle and argues for hepatocyte proliferation after training (S2.6.p1, S3.p4); in our strain-blocked model HALLMARK_G2M_CHECKPOINT is DOWN in TRN (NES -1.57, FDR 0.011), E2F targets trend down (NES -1.35, FDR 0.077), and Mki67 is not DE (log2FC -0.12, padj 0.69)."],
    "heart": ["Of the four genes the paper reports DE in all tissues except liver (S2.9.p1), only Dusp1 reaches padj < 0.05 in heart (Slc25a1 0.87, Acly 0.59, Ccn1 0.12)."],
    "gWAT": ["Of the four genes the paper reports DE in all tissues except liver (S2.9.p1), Slc25a1 and Acly reach padj < 0.05 in gWAT; Ccn1 (0.053) and Dusp1 (0.057) narrowly miss."],
    "quad": ["Strain-blocked quadriceps gives ~4,000 DEGs, about equal to BAT, whereas the paper says BAT had the most DEGs (S2.8.p1); in the unblocked sensitivity model BAT (2,037) clearly exceeds quadriceps (378)."],
}
cases = []
for cid, stem, suf, label, loc, genes in tissues:
    prim = f"{cid}_TRN_vs_SED_strainblocked"
    sens = f"{cid}_TRN_vs_SED_unblocked"
    disc = [
        {"item": "number of strains", "paper": "100-strain HMDP (S2.1.p1)",
         "data": "50 strains in GEO, one SED + one TRN animal per strain per tissue",
         "disposition": "executable_without_change"},
        {"item": "technical covariates",
         "paper": "limma correction for library prep batch and flow-cell lane (S4.4.1.p2)",
         "data": "not in GEO metadata", "disposition": "declared_deviation"},
    ]
    if cid == "quad":
        disc.append({"item": "quadriceps sample count", "paper": "not stated",
                     "data": "99 samples; 129X1/SvJ has no SED quadriceps",
                     "disposition": "executable_without_change"})
    cases.append({
        "case_id": f"GSE230102_{cid}", "accession": "GSE230102",
        "inputs": {"paper": [PAPER], "metadata": "GSE230102/GSE230102_metadata.csv",
                   "matrix": f"GSE230102/GSE230102_{stem}.counts.txt.gz", "raw_tar": False, "prep_scripts": []},
        "gates": {
            "paper_reconstruction": {
                "final": {
                    "accessions": ["GSE230102"],
                    "primary_estimand": f"Effect of 30 d voluntary wheel running (TRN) vs sedentary (SED) on {label} gene expression in female HMDP mice, pooled across strains (S2.1.p1, {loc}).",
                    "planned_contrasts": [f"TRN vs SED in {label} across all strains ({loc}; per-tissue DEG count shown only in figures, not in text)"],
                    "paper_threshold": PTH,
                    "paper_method": "kallisto v0.45 counts -> DESeq2 v1.28.0, corrected using limma v3.44.1 for library prep batch and sequencing flow-cell lane (S4.4.1.p2)",
                    "factors": {"group": ["SED", "TRN"],
                                "strain": "HMDP inbred strain; mice of each strain randomized to SED or TRN (S2.1.p1)"},
                    "inclusion": "female mice; GEO holds one SED and one TRN animal per strain per tissue (50 strains; the paper describes a 100-strain panel)",
                    "paper_results": "No per-tissue DEG counts in text. 'top 500 DEGs from each tissue (the average number of DEGs in a tissue)' (S2.9.p3); BAT has the most DEGs (S2.8.p1); liver and heart fewer DEGs than muscle and gWAT (S2.6.p1, S2.7.p1); Slc25a1, Acly, Ccn1 and Dusp1 DE in all tissues except liver (S2.9.p1).",
                },
                "reasoning": "S2.1.p1: mice from each strain randomly divided into TRN or SED, 30 d in-cage wheel. S4.3.6.1.p1: quadriceps, gWAT, heart, BAT and liver sequenced. S4.4.1.p2: kallisto + DESeq2 with limma correction for library prep batch and flow-cell lane. S4.4.1.p3 and Figure 5A/6A legends: FDR < 0.05, no fold-change rule. Each tissue is a separate TRN vs SED comparison.",
                "locator": "S4.4.1.p2", "confidence": "high"},
            "ownership": {
                "final": {"owned": True, "checks": [
                    "S4.1.3.p1 and TAB1 name GSE230102 as 'RNAsequencing Exc HMDP, This paper'",
                    "GEO extract protocol matches S4.3.6.1.p1; data_processing names kallisto v0.45 / Ensembl v97 as in S4.4.1.p2",
                    f"matrix GSE230102_{stem}.counts.txt.gz columns all end with _{suf} and equal GEO titles of this tissue"]},
                "reasoning": "The accession is the paper's own deposit for the ExcHMDP tissues; the per-tissue count file is used.",
                "confidence": "high"},
            "alignment": {
                "key_column": "title",
                "aliases": {"grp": "characteristics_ch1.3.exercise group"},
                "patterns": {"strain": ["title", r"^(\d+)_\d+_[A-Za-z]+$"]},
                "recode": {"grp": {"Exercised": "TRN", "Sedentary": "SED"}, "strain": strain_recode},
                "exclude_samples": {},
                "reasoning": "Matrix columns equal the GEO title (inspect alignment_keys). The first number of the title is the HMDP strain code (checked 1:1 with the strain characteristic across all 499 samples: 50 codes, 50 strains); recoded to S<n> so it is categorical. grp comes from the exercise-group characteristic.",
                "confidence": "high"},
            "matrix": {
                "matrix_type": "estimated counts",
                "recommended_method": "DESeq2",
                "reasoning": "GEO data_processing: counts and TPM obtained with kallisto v0.45. The .counts file is non-integer (~74% integer, median 1), i.e. kallisto estimated counts; the paper ran DESeq2 on these counts (S4.4.1.p2). Rounded before DESeq2.",
                "confidence": "high"},
            "design": {
                "factors": ["grp"], "references": {"grp": "SED"}, "subject": "strain", "organism": "Mouse",
                "planned": ["grp_TRN_vs_SED"],
                "covariate_candidates": ["strain"],
                "final": {"analysis_type": "two-group", "design_column": "grp", "control": "SED", "treatment": "TRN",
                          "contrasts": [{"name": "grp_TRN_vs_SED", "control": "SED", "treatment": "TRN", "role": "primary"}]},
                "candidates": [
                    {"value": "strain x group interaction", "reason_rejected": "one animal per strain per arm; interaction not estimable and not the paper's DE estimand"},
                    {"value": "all tissues in one model", "reason_rejected": "the paper analyses each tissue separately (S2.4-S2.8)"}],
                "reasoning": "The paper's DE estimand per tissue is TRN vs SED across strains (Figure 5A/6A legends: 'across all strains ... relative to sedentary'). Animals were randomized within strain, so strain is the matching unit (one SED and one TRN per strain).",
                "confidence": "high"},
            "covariance": {
                "final": {"status": "required", "blocking_terms": ["strain"],
                          "covariates": [
                              {"name": "strain", "disposition": "blocking term in the primary model (randomization unit; transcriptomes cluster by strain, S2.9.p3)"},
                              {"name": "library prep batch", "disposition": "not in GEO metadata; the paper adjusted for it (S4.4.1.p2); cannot be reproduced"},
                              {"name": "flow cell lane", "disposition": "not in GEO metadata; the paper adjusted for it (S4.4.1.p2); cannot be reproduced"},
                              {"name": "housing (single vs group)", "disposition": "fully aliased with grp (S4.2.2.p1: TRN singly housed, SED 1-4 per cage); not estimable; caveat, not a covariate"}]},
                "confounding_candidates": ["strain"],
                "reasoning": "Each inbred strain contributes one SED and one TRN animal, so strain is a pairing/blocking unit; S2.9.p3 shows transcriptomes cluster by strain rather than group. The paper's batch and lane covariates are not deposited. The unblocked ~ grp model runs as a sensitivity analysis. CAVEAT: Housing is aliased with exercise: TRN mice were individually housed with a wheel, SED mice were group-housed 1-4 per cage (S4.2.2.p1). Housing cannot be separated from TRN vs SED in any model, so every result is a TRN-plus-single-housing effect, not wheel running alone.",
                "confidence": "medium"},
            "method": {
                "final": {"method": "DESeq2 (pydeseq2 Wald)", "formula": "~ strain + grp",
                          "rounding_documented": True,
                          "paper_route": {"method": "DESeq2 + limma correction for library prep batch and flow-cell lane",
                                          "status": "blocked",
                                          "reason": "library prep batch and flow-cell lane are not in the GEO metadata"},
                          "deviations": ["batch/lane adjustment omitted (not deposited)",
                                         "strain added as blocking term in the primary model; unblocked ~ grp as sensitivity",
                                         "kallisto estimated counts rounded to integers for DESeq2",
                                         "GEO holds 50 strains, not the 100 described"]},
                "transform": "round",
                "reasoning": "DESeq2 is the paper's method and the matrix supports it (estimated counts, rounded).",
                "confidence": "high"},
            "threshold": {
                "final": {"paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": None},
                          "threshold_source": "paper_on_deviation_route",
                          "applied_threshold": TH},
                "reasoning": "S4.4.1.p3 and Figure 5A/6A legends: significant at FDR < 0.05; no fold-change rule stated.",
                "confidence": "high"},
            "study": {
                "final": {"route": "declared_deviation",
                          "caveats": [
                              "The paper gives no per-tissue DEG count in the text (figures S11A/S12A only): only an average of ~500 DEGs per tissue, BAT the most, liver and heart fewer.",
                              "The paper's batch and flow-cell lane adjustment cannot be reproduced.",
                              "The GEO deposit has 50 strains x 1 animal per arm per tissue; the paper describes 100 strains.",
                              "Housing is aliased with exercise: TRN mice were individually housed with a wheel, SED mice were group-housed 1-4 per cage (S4.2.2.p1). Housing cannot be separated from TRN vs SED in any model, so every result is a TRN-plus-single-housing effect, not wheel running alone."]
                              + RESULT_CAVEATS.get(cid, [])},
                "paper_counts": {},
                "paper_genes": {prim: genes, sens: genes},
                "reasoning": "The paper's estimand and method are reproduced on the deposited data with declared deviations (no batch/lane, strain blocking).",
                "confidence": "medium"},
        },
        "discrepancies": disc,
        "executions": [
            {"name": prim, "tool": "tools.deseq2_tools:run_deseq2_analysis",
             "args": {"design_column": "grp", "control_group": "SED", "treatment_group": "TRN",
                      "covariate_columns": ["strain"], "alpha": 0.05},
             "role": "primary", "reasoning": "DESeq2 ~ strain + grp: TRN vs SED blocked on the randomization unit."},
            {"name": sens, "tool": "tools.deseq2_tools:run_deseq2_analysis",
             "args": {"design_column": "grp", "control_group": "SED", "treatment_group": "TRN", "alpha": 0.05},
             "role": "sensitivity", "reasoning": "DESeq2 ~ grp: the paper's model minus the undeposited batch/lane terms."},
        ],
        "enrichment": [
            {"execution": prim, "ora": True, "gsea": True, "direction": "all", "ranking_metric": "stat",
             "reasoning": "The paper reports GO enrichment of DEGs per tissue (Pantherdb, FDR < 0.05)."}],
    })
spec = {"run_dir": RUN,
        "request": "Analyze GSE230102 for PMID 37178122 (Conserved multi-tissue transcriptomic adaptations to exercise training in humans and mice.): how exercise affects gene expression as the paper intends.",
        "decision_maker": "Claude Opus 5.5 (claude-code session)", "platform": "claude-code",
        "data_root": "E:/agent/mwangLab_pdf/data", "cases": cases}
with open(f"{ROOT}/{RUN}/case_spec.json", "w", encoding="utf-8") as fh:
    json.dump(spec, fh, indent=1)
print("ok", len(cases))
