import json, sys
rd = sys.argv[1]
paper = "test/experiments/paper_screen_20261019/papers/PMC11861322.paper.md"
LEVELS = {"Control": "Control", "Single_1hr": "S1", "Single_4hr": "S4", "Single_24hr": "S24", "Repeated_24hr": "R24"}
PAIRS = [("S1", "Control"), ("S4", "Control"), ("S24", "Control"), ("R24", "Control"),
         ("S4", "S1"), ("S24", "S4"), ("R24", "S24")]
names = [f"grp_{t}_vs_{c}" for t, c in PAIRS]
PT = {"metric": "FDR", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0,
      "inclusive": False, "source_locator": "S4.4.p2"}
AT = {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "inclusive": False}
AUD = {"metric": "padj", "cutoff": 0.05, "effect_cutoff": None}
GENES = {
 "synovium": {"grp_S1_vs_Control": ["Nr4a3", "Inhba", "Il1b", "Saa3", "Clec4d", "Calca", "Ecel1"],
              "grp_S4_vs_Control": ["Nr4a3", "Saa3", "Clec4d", "Calca", "Ecel1"],
              "grp_S24_vs_Control": ["Saa3", "Clec4d", "Calca", "Ecel1"],
              "grp_R24_vs_Control": ["Inhba", "Saa3", "Il1b"],
              "grp_S24_vs_S4": ["Nr4a3"], "grp_R24_vs_S24": ["Inhba"]},
 "cartilage": {"grp_S1_vs_Control": ["Nr4a3", "Wnt1", "Tnf", "Saa3"],
               "grp_S4_vs_Control": ["Wnt1", "Tnf", "Saa3"],
               "grp_S24_vs_Control": ["Wnt1", "Tnf", "Saa3"],
               "grp_R24_vs_Control": ["Saa3", "Col2a1", "Acan", "Comp", "Dcn", "Col1a1", "Col1a2", "Sox9", "Sox5",
                                      "Timp1", "Timp3", "Nrg2", "Ccl4", "Pgf", "Cxcl2"],
               "grp_S4_vs_S1": ["Nr4a3"]},
}
cases = []
for tissue, prefix, n_ex in [("synovium", "Syn", 3), ("cartilage", "Cart", 2)]:
    small = n_ex < 3
    other = "cartilage" if tissue == "synovium" else "synovium"
    cid = f"GSE280656_{tissue}"
    ex_name = "joint_all_timepoints"
    gates = {
     "paper_reconstruction": {"final": {
        "accessions": ["GSE280656"],
        "primary_estimand": f"Effect of overloading exercise (treadmill + 20 g weight) on the {tissue} transcriptome at 1, 4, 24 h after a single bout (S1, S4, S24) and 24 h after 4 daily bouts (R24), each versus non-running controls; plus adjacent time-point comparisons",
        "planned_contrasts": ["S1 vs control (Fig 3a/4a)", "S4 vs S1 (Fig 3b/4b)", "S24 vs S4 (Fig 3c/4c)",
                              "S4 vs control (Fig 3d/4d)", "S24 vs control (Fig 3e/4e)", "R24 vs control (Fig 5)",
                              "R24 vs S24 (Fig 8b)"],
        "paper_threshold": PT,
        "factors": {"grp": ["Control", "S1", "S4", "S24", "R24"]},
        "inclusion": "male C57BL/6J, 10-13 wk; each RNA-seq sample is a pool (synovium 6 knees, cartilage 9 knees); no exclusions (S4.1.p1, S4.4.p1)",
        "paper_method": "iDEP web app (default DESeq2 on RSEM counts across all groups), FDR < 0.1 and fold change > 2 (S4.4.p2)",
        "paper_results": "DEG counts per comparison only in Fig 2b (numbers not in text); overlaps: synovium S1&S4 vs control share 52 DEGs, S4&S24 share 9, common S1/S4/S24 = Clec4d, Calca, Ecel1, Saa3 (S2.3.p2); cartilage S1&S4 share 32, S4&S24 share 5, 11 common incl Wnt1, Tnf, Saa3 (S2.4.p2); R24 vs control >> S24 vs control DEGs (S2.5.p1)"},
        "reasoning": "S2.1.p1 defines groups control/S1/S4/S24/R24; S2.2.p1 and Fig 2b compare time points pairwise; S4.4.p2 states iDEP defaults FDR < 0.1, FC > 2. Each tissue is a separate matrix and separate analysis in the paper (Fig 3 synovium, Fig 4 cartilage).",
        "confidence": "high", "locator": "S4.4.p2"},
     "ownership": {"final": {"owned": True, "checks": [
        "S8.p1 names GSE280656", "metadata contact Yusuke Arino (first author Y.A.)",
        f"matrix GSE280656_{tissue}_gene_count.txt.gz columns equal the {tissue} sample titles",
        "data_processing (fastp, STAR 2.7.8a, GRCm39/gencode vM33, RSEM 1.3.1) matches S4.4.p2"]},
        "reasoning": "Accession, processing pipeline and sample groups match the paper.", "confidence": "high"},
     "alignment": {"key_column": "title",
        "patterns": {"grp": ["title", rf"^{prefix}_(Control|Single_1hr|Single_4hr|Single_24hr|Repeated_24hr)_rep\d+$"]},
        "recode": {"grp": LEVELS}, "aliases": {}, "exclude_samples": {},
        "reasoning": f"Matrix columns equal metadata title exactly ({'15' if tissue=='synovium' else '11'}/{'15' if tissue=='synovium' else '11'}); the other tissue's samples are in a separate matrix. grp parsed from the title.",
        "confidence": "high"},
     "matrix": {"matrix_type": "estimated counts", "recommended_method": "DESeq2",
        "final": {"source": f"GSE280656_{tissue}_gene_count.txt.gz (57 all-NaN rows dropped by prep/drop_nan_rows.py)",
                  "paper_input": "RSEM expression levels analysed in iDEP with DESeq2 normalization (S4.4.p2-p3)"},
        "reasoning": "93% integer values with fractional remainder, library sums ~18-26 M, data_processing says RSEM 'gene count': RSEM expected counts, so DESeq2 after rounding (same as the paper's DESeq2 in iDEP).",
        "confidence": "high"},
     "design": {"factors": ["grp"], "references": {"grp": "Control"}, "subject": None, "organism": "Mouse",
        "planned": names, "covariate_candidates": [], "strata": [],
        "final": {"analysis_type": "multi-group, one model with planned pairwise contrasts",
                  "design_column": "grp",
                  "contrasts": [{"name": n, "control": c, "treatment": t,
                                 "role": "primary" if c == "Control" else "secondary"} for n, (t, c) in zip(names, PAIRS)]},
        "reasoning": "Five independent groups of pooled animals (no subject repeated across groups: separate mice per time point, S2.1.p1). One DESeq2 model on all samples of the tissue, as iDEP does, with the paper's pairwise comparisons. Rejected: pooling single-bout time points; tissue as a factor (paper analyzes tissues separately, separate matrices)."
                     + (" Cartilage exercise arms have n=2 (control n=3), so all cartilage contrasts are exploratory." if small else ""),
        "candidates": [{"value": "pool S1/S4/S24 as 'single'", "reason_rejected": "paper treats time points as distinct levels"},
                       {"value": "tissue x grp joint model", "reason_rejected": "paper analyzes tissues separately; separate deposited matrices"}],
        "confidence": "high"},
     "covariance": {"final": {"status": "not_required", "blocking_terms": [], "covariates": []},
        "confounding_candidates": None,
        "reasoning": "Each sample is an independent pool of different mice; no batch, sex (all male) or subject key recorded in GEO or paper.",
        "confidence": "medium"},
     "method": {"final": {"method": "DESeq2 (pydeseq2 Wald, joint model)", "formula": "~ grp",
                          "rounding_documented": True,
                          "paper_route": {"method": "DESeq2 via iDEP", "status": "reproduced_approximately",
                                          "reason": "iDEP defaults (DESeq2 on all groups); exact iDEP prefilter and version not stated"},
                          "deviations": ["RSEM expected counts rounded to integers for DESeq2",
                                         "low-count filter CPM >= 0.5 in >= 1 sample assumed as the iDEP default (not stated in paper)",
                                         "pydeseq2 rather than R DESeq2"]},
        "transform": None,
        "reasoning": "Paper used iDEP's DESeq2 (S4.4.p2-p3); matrix holds RSEM estimated counts which DESeq2 accepts after rounding.",
        "confidence": "medium"},
     "threshold": {"final": {"paper_threshold": PT, "threshold_source": "paper", "applied_threshold": AT,
                             "audit_threshold": AUD},
        "reasoning": "S4.4.p2: default iDEP thresholds FDR < 0.1 and fold change > 2, i.e. padj < 0.1 and |log2FC| > 1. Audit: padj < 0.05 without effect cutoff.",
        "confidence": "high"},
     "study": {"final": {"route": "paper_aligned",
                         "caveats": ["Paper DEG counts are only in Fig 2b (not in text); count comparison not possible from text",
                                     "pooled samples; small n per group"] + (
                                     ["cartilage exercise arms n=2"] if small else [])}
                         | ({"exploratory_reason": "cartilage exercise arms have 2 pooled replicates (< 3)"} if small else {}),
        "paper_counts": {}, "paper_genes": {f"{ex_name}/{k}": v for k, v in GENES[tissue].items()},
        "reasoning": "Paper's own route (DESeq2, all groups, FDR<0.1 & FC>2) reproduced with documented rounding and assumed iDEP prefilter."
                     + (" Labelled exploratory: n=2 in exercise arms." if small else ""),
        "confidence": "medium"},
    }
    if small:
        gates["study"]["final"]["route"] = "exploratory"
    execu = [{"name": ex_name, "tool": "tools.joint_contrasts:run_joint_deseq2",
              "args": {"comparisons": names, "covariates": [], "alpha": 0.1, "round_estimated_counts": True,
                       **({"include": names} if small else {})},
              "filter_low_counts": {"min_cpm": 0.5, "min_samples": 1},
              "role": "primary",
              "reasoning": "one DESeq2 model on all groups of this tissue (iDEP style), all planned pairwise contrasts"
                           + ("; included despite n=2 per exercise arm (exploratory)" if small else "")}]
    enr = []
    for comp in ["grp_S1_vs_Control", "grp_R24_vs_Control"]:
        for d in ["up", "down"]:
            enr.append({"execution": f"{ex_name}/{comp}", "ora": True, "gsea": d == "up", "direction": d,
                        "ranking_metric": "stat",
                        "reasoning": f"paper reports GO BP enrichment of {d}-regulated DEGs (Metascape) for this comparison (Fig 3a/4a, Fig 5)"})
    cases.append({"case_id": cid, "accession": "GSE280656",
        "inputs": {"paper": [paper], "metadata": "GSE280656/GSE280656_metadata.csv",
                   "matrix": f"E:/agent/mwangLab_pdf/{rd}/prep/GSE280656_{tissue}_gene_count_noNaN.csv", "raw_tar": False,
                   "prep_scripts": [f"{rd}/prep/drop_nan_rows.py"]},
        "gates": gates,
        "discrepancies": [
            {"item": "DE software", "paper": "iDEP web app (DESeq2 default)", "data": "pydeseq2 joint model", "disposition": "executable_without_change"},
            {"item": "input values", "paper": "RSEM expression levels", "data": "RSEM expected counts with decimals; 57 all-NaN rows", "disposition": "executable_without_change"},
            {"item": "replicates", "paper": "group sizes in figures", "data": f"{tissue}: control 3, exercise arms {n_ex}", "disposition": "executable_without_change"}],
        "executions": execu, "enrichment": enr})
spec = {"run_dir": rd,
        "request": "Analyze GSE280656 for PMID 40000838 (Short-term overloading exercise attenuates articular chondrocyte features partly via synovium-cartilage interactions mediated by inhibin subunit beta A.): how exercise affects gene expression as the paper intends.",
        "decision_maker": "Claude Opus 5.5 (claude-code subagent)", "platform": "claude-code",
        "data_root": "E:/agent/mwangLab_pdf/data", "cases": cases}
json.dump(spec, open(f"{rd}/case_spec.json", "w"), indent=1)
print("ok")
