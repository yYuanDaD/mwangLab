import json, copy

RD = "test/experiments/large_run_pilot_20261019/runs_claude/917d28883ad57a66410a4fc20fd7e6dccd3695c6"
PAPER = "test/experiments/paper_screen_20261019/papers/PMC10262399.paper.md"
PT = {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0,
      "inclusive": True}
AUDIT = {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": None}

blocks = {
    "mRNA": dict(
        file="GSE235174_mRNA_counts.csv", n=86, up=47, down=39,
        mtype="raw counts", round=False,
        mreason=("Block 1 of GSE235174_counts_allsamples.txt.gz (gene_id_mRNA + 8 columns), split by "
                 "prep_split_blocks.py: 20,028 gene symbols, 100% integers, column sums 11.5-21.3 M. S2.4.p2: "
                 "'read counts of each gene were obtained by HTSeq-count'. The FPKM file is the Cufflinks FPKM and is "
                 "not used. Paper input for DESeq is these counts."),
        genes=["CDK1", "TTK", "HJURP", "DLGAP5", "PCLAF", "GINS2", "TYMS", "DTL", "KIFC1", "ELANE", "PLCB4",
               "CCL23", "CPA3", "IGF2R", "SCN1B", "FPR3", "DEFA4", "MPO", "AZU1", "CYB5D1", "KNCN", "SPDYA"],
    ),
    "lncRNA": dict(
        file="GSE235174_lncRNA_counts.csv", n=570, up=271, down=299,
        mtype="estimated counts", round=True,
        mreason=("Block 2 (lncRNA_id + 8 columns): 52,355 known (ENST/NR/XR) and novel lncRNA transcripts; 69% integers, "
                 "non-integer values such as 5745.37, column sums 3.4-3.9 M; same transcripts have much smaller values "
                 "in the FPKM file (199.2 vs 5745.4), so this is a fragment-count estimate from Cufflinks-style "
                 "transcript quantification (S2.4.p2), not FPKM. Treated as estimated counts, rounded for DESeq2."),
        genes=[],
    ),
    "circRNA": dict(
        file="GSE235174_circRNA_counts.csv", n=2064, up=676, down=1388,
        mtype="raw counts", round=False,
        mreason=("Block 3 (id_circRNA + 8 columns): 11,526 CIRI2 circRNAs, 100% integers, column sums 17.6-71.1 k, i.e. "
                 "back-splice junction read counts (S2.4.p2: 'circRNAs were identified using CIRI'; RPM was used for "
                 "expression display, DESeq for testing). Raw junction counts are the DESeq input."),
        genes=[],
    ),
}

cases = []
for b, info in blocks.items():
    planned_name = "time_post_vs_pre"
    gates = {
        "paper_reconstruction": {
            "final": {
                "accessions": ["GSE235174"],
                "assay": "Total RNA (ribo-depleted) whole-transcriptome RNA-seq of peripheral blood leukocytes; "
                         "mRNA, lncRNA, circRNA (and small-RNA library for miRNA, not deposited here)",
                "inclusion": "4 male COPD patients, each sampled pre- and post-12-week personalized aerobic training "
                             "(S2.1.p1, S2.2.p1, TAB1); 8 libraries",
                "factors": {"time": ["pre", "post"]},
                "repeated_measure_unit": "patient (same 4 patients pre and post)",
                "primary_estimand": f"Change in {b} expression in leukocytes of COPD patients after vs before 12 weeks "
                                    "of aerobic exercise training (post vs pre)",
                "planned_contrasts": [f"post-exercise vs pre-exercise, {b} (S3.2.p1; paper: {info['n']} DE-{b}s, "
                                      f"{info['up']} up / {info['down']} down)"],
                "paper_method": "DESeq (2012) R package, two-group comparison post vs pre (pairing not stated); "
                                "HTSeq counts for mRNA, Cufflinks for lncRNA, CIRI for circRNA (S2.4.p2)",
                "paper_threshold": dict(PT, metric="pvalue", source_locator="S3.2.p1; FIG2; S4.p2"),
                "paper_results": {"mRNA": "86 (47 up, 39 down)", "lncRNA": "570 (271 up, 299 down)",
                                  "circRNA": "2064 (676 up, 1388 down) in S3.2.p1; 2087 in ABS.p3",
                                  "miRNA": "8 (not in GEO)"},
            },
            "reasoning": ("Single pre/post intervention study. S2.4.p2 names DESeq (2012) with 'P-value < 0.05'; S3.2.p1 "
                          "and S4.p2 add log2 FoldChange >= 1 (FIG2 caption writes > 1 and P < 0.05). Raw p, not FDR. "
                          "No pairing or subject term is described for the DESeq analysis (only clinical variables "
                          "use a paired t-test, S2.12.p1)."),
            "locator": "S2.4.p2; S3.2.p1",
            "confidence": "high",
        },
        "ownership": {
            "final": {"owned": True, "checks": [
                "DA.p1 says the data are in GEO; GSE235174 contact institute Pudong New Area Gongli Hospital = study site (S2.1.p1)",
                "8 GSM samples = 4 patients x pre/post, peripheral blood, Homo sapiens, total RNA, matching S2.2.p1",
                "Supplementary counts file holds mRNA, lncRNA and circRNA blocks matching S2.4.p2"]},
            "reasoning": "Accession, institution, design and assays all match the paper.",
            "confidence": "high",
        },
        "alignment": {
            "key_patterns": {"key": ["title", "^Expression_([ab]PR_\\d)$"]},
            "key_column": "key",
            "patterns": {"time": ["title", "^Expression_([ab])PR_\\d$"],
                         "subject": ["title", "^Expression_[ab]PR_(\\d)$"]},
            "recode": {"time": {"a": "post", "b": "pre"}, "subject": {"1": "P1", "2": "P2", "3": "P3", "4": "P4"}},
            "aliases": {},
            "exclude_samples": {},
            "reasoning": ("Matrix columns aPR_1..4/bPR_1..4 equal the title suffix (Expression_aPR_1). GEO treatment "
                          "field: aPR = 'after 12weeks aerobic exercises', bPR = 'NC' (pre) -> time post/pre. subject "
                          "is the numeric suffix; that aPR_k and bPR_k are the same patient is inferred from the "
                          "naming only, not stated in GEO or the paper."),
            "confidence": "high",
        },
        "matrix": {
            "matrix_type": info["mtype"],
            "recommended_method": "DESeq2",
            "final": {"source": f"prep/{info['file']} (block of GSE235174_counts_allsamples.txt.gz)",
                      "paper_input": "counts for DESeq (S2.4.p2)"},
            "reasoning": info["mreason"],
            "confidence": "high" if b != "lncRNA" else "medium",
        },
        "design": {
            "factors": ["time"],
            "references": {"time": "pre"},
            "subject": "subject",
            "organism": "Human",
            "planned": [planned_name],
            "final": {"analysis_type": "two-group", "design_column": "time", "control": "pre", "treatment": "post",
                      "contrasts": [{"name": planned_name, "control": "pre", "treatment": "post", "role": "primary"}]},
            "reasoning": ("Within-patient pre/post exercise contrast, 4 vs 4. Only one factor; all patients male (TAB1), "
                          "so no sex split. Paper estimand is the post-vs-pre change."),
            "candidates": [{"value": "characteristics_ch1.4.treatment (NC vs after 12weeks aerobic exercises)",
                            "reason_rejected": "identical split to title-derived time; title used for formula-safe levels"}],
            "confidence": "high",
        },
        "covariance": {
            "final": {"status": "not_required", "blocking_terms": [],
                      "covariates": [{"name": "subject", "disposition": "sensitivity only (paired DESeq2 secondary execution)"}]},
            "confounding_candidates": ["subject"],
            "reasoning": ("Paper's DESeq analysis is a two-group comparison with no subject term (S2.4.p2), so the "
                          "paper-aligned primary run is unblocked. The design is truly repeated-measures, but the "
                          "pairing key is only inferred from sample-name suffixes, so a subject-blocked DESeq2 run is "
                          "added as a secondary sensitivity analysis rather than the primary route."),
            "confidence": "medium",
        },
        "method": {
            "final": {"method": "DESeq2 (pydeseq2 Wald)", "formula": "~ time",
                      "paper_route": {"method": "DESeq (2012, nbinomTest)", "status": "blocked",
                                      "reason": "original DESeq package is not available in this environment; DESeq2 is its successor with the same negative-binomial counts model"},
                      "deviations": ["DESeq2 instead of DESeq (2012)"] + (
                          ["estimated counts rounded to integers for DESeq2"] if info["round"] else []),
                      **({"rounding_documented": True} if info["round"] else {})},
            "transform": "round" if info["round"] else None,
            "reasoning": "Counts -> negative-binomial model as in the paper; DESeq2 replaces DESeq as a declared deviation.",
            "confidence": "high",
        },
        "threshold": {
            "final": {"paper_threshold": PT, "threshold_source": "paper_on_deviation_route",
                      "applied_threshold": PT, "audit_threshold": AUDIT,
                      "deviation_note": "Paper rule (raw p < 0.05 and |log2FC| >= 1) applied unchanged on the DESeq2 route; BH padj < 0.05 reported as audit."},
            "reasoning": "S3.2.p1 / S4.p2: log2 FoldChange >= 1.0 and p-values < 0.05 (both directions counted).",
            "confidence": "high",
        },
        "study": {
            "final": {"route": "declared_deviation",
                      "caveats": ["n = 4 patients; raw-p threshold gives many false positives expected under the null",
                                  "DESeq2 shrinkage/dispersion differs from DESeq (2012), so exact counts will differ",
                                  "pairing in the secondary run is inferred from sample names"]},
            "paper_counts": {planned_name: info["n"]},
            "paper_genes": ({planned_name: info["genes"]} if info["genes"] else {}),
            "reasoning": f"Paper reports {info['n']} DE-{b}s for post vs pre.",
            "confidence": "high",
        },
    }
    execs = [
        {"name": planned_name, "tool": "tools.deseq2_tools:run_deseq2_analysis",
         "args": {"design_column": "time", "control_group": "pre", "treatment_group": "post", "alpha": 0.05},
         "role": "primary", "reasoning": "Paper's unpaired two-group negative-binomial test (DESeq -> DESeq2)."},
        {"name": planned_name + "_paired", "tool": "tools.deseq2_tools:run_deseq2_analysis",
         "args": {"design_column": "time", "control_group": "pre", "treatment_group": "post",
                  "covariate_columns": "subject", "alpha": 0.05},
         "role": "sensitivity", "reasoning": "Subject-blocked (~ subject + time) sensitivity; pairing inferred from aPR_k/bPR_k names."},
    ]
    if info["round"]:
        pass
    case = {
        "case_id": f"GSE235174_{b}",
        "accession": "GSE235174",
        "inputs": {"paper": [PAPER], "metadata": "GSE235174/GSE235174_metadata.csv",
                   "matrix": f"E:/agent/mwangLab_pdf/{RD}/prep/{info['file']}", "raw_tar": False,
                   "prep_scripts": [f"{RD}/prep_split_blocks.py"]},
        "gates": gates,
        "discrepancies": [
            {"item": "DE method", "paper": "DESeq (2012)", "data": "DESeq2 available", "disposition": "declared_deviation"},
            {"item": "pairing", "paper": "not stated; two-group comparison", "data": "aPR_k/bPR_k names suggest same patient k",
             "disposition": "primary unpaired as in paper; paired run as sensitivity"},
            {"item": "deposited matrix layout", "paper": "separate mRNA/lncRNA/circRNA quantification",
             "data": "three blocks pasted side by side in one TSV", "disposition": "split by prep_split_blocks.py"},
        ],
        "executions": execs,
        "enrichment": [],
    }
    if b == "mRNA":
        case["enrichment"] = [
            {"execution": planned_name, "ora": True, "gsea": False, "direction": "up",
             "reasoning": "Paper runs GO/KEGG on up-regulated DE-mRNAs separately (S3.3.p1)."},
            {"execution": planned_name, "ora": True, "gsea": False, "direction": "down",
             "reasoning": "Paper runs GO/KEGG on down-regulated DE-mRNAs separately (S3.3.p1)."},
            {"execution": planned_name, "ora": False, "gsea": True, "ranking_metric": "stat",
             "reasoning": "Hallmark GSEA on full ranking as a supporting pathway view (paper used GSVA)."},
        ]
    cases.append(case)

spec = {"run_dir": RD,
        "request": "Analyze GSE235174 for the paper (Regulation of whole-transcriptome sequencing expression in COPD after personalized precise exercise training: a pilot study): how exercise affects gene expression as the paper intends.",
        "decision_maker": "Claude Opus 5.5 (Claude Code session)", "platform": "claude-code",
        "data_root": "E:/agent/mwangLab_pdf/data", "cases": cases}
json.dump(spec, open(f"E:/agent/mwangLab_pdf/{RD}/case_spec.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("ok")


