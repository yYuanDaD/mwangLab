import json
R = "test/experiments/model_compare_20261103/runs/sonnet/PMID34142717"
thr = {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": None, "inclusive": True}
paper_thr = {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": None,
             "inclusive": True, "source_locator": "S3.3.p2"}
comps = [  # name, control, treatment, tissue subset, role, paper count
    ("Ex0_ZT0_vs_SedZT0", "SedZT0", "Ex0ZT0", "quad", "primary", None),
    ("Ex3_ZT0_vs_SedZT4", "SedZT4", "Ex3ZT0", "quad", "primary", None),
    ("Ex0_ZT12_vs_SedZT12", "SedZT12", "Ex0ZT12", "quad", "primary", None),
    ("Ex3_ZT12_vs_SedZT16", "SedZT16", "Ex3ZT12", "quad", "primary", None),
    ("DayAct_vs_NightCtrl_ZT4", "NightZT4", "DayZT4", "gastroc", "secondary", 2094),
    ("NightCtrl_vs_DayAct_ZT16", "DayZT16", "NightZT16", "gastroc", "secondary", 368),
]
planned = [f"grp_{t}_vs_{c}" for _, c, t, _, _, _ in comps]
exes = []
for n, c, t, ts, role, pc in comps:
    exes.append({"name": f"grp_{t}_vs_{c}", "tool": "tools.deseq2_tools:run_deseq2_analysis",
                 "args": {"design_column": "grp", "control_group": c, "treatment_group": t, "alpha": 0.05},
                 "subset": {"tissue": [ts]}, "role": role,
                 "reasoning": f"Two-group DESeq2 (Wald) within the {ts} samples only; control {c} is the sedentary/other-group arm matched to the time of sacrifice."})
spec = {
    "run_dir": R,
    "request": "Analyze GSE178262 for PMID 34142717 (Transcriptomic, proteomic and phosphoproteomic underpinnings of daily exercise performance and zeitgeber activity of training in mouse muscle.): how exercise affects gene expression as the paper intends.",
    "decision_maker": "Claude Sonnet 5.5 (claude-sonnet-5-5) session", "platform": "claude-code",
    "data_root": "E:/agent/mwangLab_pdf/data",
    "cases": [{
        "case_id": "GSE178262", "accession": "GSE178262",
        "inputs": {"paper": ["E:/agent/mwangLab_pdf/test/experiments/paper_screen_20261019/papers/PMC9290843.paper.md"],
                   "metadata": "GSE178262/GSE178262_metadata.csv", "matrix": f"{R}/prep/GSE178262_gsm_counts.csv",
                   "raw_tar": False, "prep_scripts": [f"{R}/prep/merge_lanes.py"]},
        "gates": {
            "paper_reconstruction": {
                "final": {
                    "accessions": ["GSE178262"],
                    "primary_estimand": "Effect of an acute bout of high-intensity treadmill exercise (sacrificed 0 h or 3 h after exhaustion, started at ZT0 or ZT12) on quadriceps gene expression versus time-of-sacrifice-matched sedentary mice; secondary: daytime versus night-time voluntary wheel-running training (DA vs CTRL) in gastrocnemius at ZT4 and ZT16.",
                    "planned_contrasts": ["Ex+0h ZT0 vs Sed ZT0 (S3.3.p2; Fig 5A)",
                                          "Ex+3h ZT0 vs Sed ZT4 (FIG2 legend: Sed ZT4 is the 3 h control; Fig 5B)",
                                          "Ex+0h ZT12 vs Sed ZT12", "Ex+3h ZT12 vs Sed ZT16",
                                          "DA vs CTRL at ZT4: 2094 DEGs (S3.8.p1; Fig 12A)",
                                          "CTRL vs DA at ZT16: 368 DEGs (S3.8.p1; Fig 12A)"],
                    "paper_threshold": paper_thr,
                    "paper_method": "kallisto -> tximport lengthScaledTPM gene pseudo-counts -> DESeq2 1.26.0, shrunken LFC (S2.8.p2); DEGs FDR <= 0.05 (S3.3.p2)",
                    "sample_inclusion": "RNA-seq of quadriceps (treadmill, n=3/group) and gastrocnemius (wheel, n=4/group); 40 samples, each sequenced on two lanes of the same library",
                    "paper_results": {"treadmill": "Venn counts only in Fig 5A/B and Supp Table 1 (not in text); ~25% of DEGs shared between ZT0 and ZT12",
                                      "wheel": "2094 DEGs at ZT4, 368 at ZT16 (S3.8.p1)"}},
                "reasoning": "S3.3.p1-p2: RNA-seq at ZT0 and ZT12 acute treadmill exercise vs sedentary, DEGs FDR<=0.05. S3.8.p1: DA vs CTRL wheel DEG counts. S2.3.p1: the wheel contrast is day- versus night-time training; sedentary vs wheel is explicitly out of scope. The FIG2 legend fixes the sedentary control as matched to the time of sacrifice.",
                "confidence": "high", "locator": "S3.3.p2"},
            "ownership": {
                "final": {"owned": True, "checks": ["GSE178262 data_processing restates the paper's kallisto/tximport/DESeq2 methods (S2.8.p2)", "sample titles Sed/Ex +0h/Ex +3h/CTRL/DA at ZT0/4/12/16 match the paper design", "contact is the Handschin lab, Biozentrum Basel"]},
                "reasoning": "S2.8.p2 method text is reproduced in GEO data_processing; sample labels mirror the Fig 5 and Fig 12 designs."},
            "alignment": {
                "key_column": None,
                "patterns": {"grp": ["title", r"^(Sed|Ex \+0h|Ex \+3h|CTRL|DA)\s+(ZT\d+)\s+\d+$"],
                             "tissue": ["source_name_ch1", r"^(Quadriceps|Gastrocnemius) muscle$"]},
                "recode": {"grp": {"Sed_ZT0": "SedZT0", "Ex +0h_ZT0": "Ex0ZT0", "Ex +3h_ZT0": "Ex3ZT0", "Sed_ZT4": "SedZT4",
                                   "Sed_ZT12": "SedZT12", "Ex +0h_ZT12": "Ex0ZT12", "Ex +3h_ZT12": "Ex3ZT12", "Sed_ZT16": "SedZT16",
                                   "CTRL_ZT4": "NightZT4", "DA_ZT4": "DayZT4", "CTRL_ZT16": "NightZT16", "DA_ZT16": "DayZT16"},
                           "tissue": {"Quadriceps": "quad", "Gastrocnemius": "gastroc"}},
                "aliases": {}, "exclude_samples": {},
                "reasoning": "The deposited matrix has 80 lane columns (L001/L002 of one library per sample; GEO description says same library). prep/merge_lanes.py sums the two lanes of each sample (paired by the sample number S<n> present in both the column name and the GSM description) and renames to GSM ids, so alignment is exact on the metadata index. grp = title treatment + ZT; tissue = source_name_ch1 (tissue is fully nested in experiment)."},
            "matrix": {"matrix_type": "estimated counts", "recommended_method": "DESeq2",
                       "reasoning": "Non-integer tximport lengthScaledTPM gene-level pseudo-counts (data_processing; integer fraction 0.30 before lane summing), the same input as the paper's DESeq2 (S2.8.p2). Rounded for pydeseq2. Row IDs are Entrez gene IDs."},
            "design": {
                "factors": ["grp"], "references": {"grp": "SedZT0"}, "organism": "Mouse", "planned": planned, "strata": ["tissue"],
                "final": {"analysis_type": "two-group", "design_column": "grp", "control": "SedZT0", "treatment": "Ex0ZT0",
                          "contrasts": [{"name": f"grp_{t}_vs_{c}", "control": c, "treatment": t, "role": role} for _, c, t, _, role, _ in comps]},
                "reasoning": "Independent animals per group (n=3 treadmill, n=4 wheel). Six pairwise contrasts, each a separate two-group fit within its tissue. Treadmill: acute exercise vs sedentary mice sacrificed at the matched ZT (FIG2 legend). Wheel: the paper compares day vs night-time wheel activity at the ZT where each group runs (S3.8.p1), not sedentary vs wheel (S2.3.p1), so it is a training-timing contrast.",
                "candidates": [{"value": "pooled Sed vs pooled Ex", "reason_rejected": "circadian phase confounded; paper stratifies by ZT and sacrifice time"},
                               {"value": "sedentary vs wheel", "reason_rejected": "no wheel-free sedentary group in the gastrocnemius set; paper excludes it (S2.3.p1)"}]},
            "covariance": {"final": {"status": "not_required", "blocking_terms": [], "covariates": []}, "confounding_candidates": None,
                           "reasoning": "Independent animals; no litter or batch column. Lane replicates are summed per library so no pseudo-replication. Tissue is nested in experiment and handled by subsetting."},
            "method": {"final": {"method": "DESeq2 (pydeseq2 Wald)", "formula": "~ grp",
                                 "paper_route": {"method": "DESeq2 1.26.0 on tximport lengthScaledTPM counts", "status": "reproduced_with_python_port"},
                                 "rounding_documented": True,
                                 "deviations": ["pydeseq2 instead of R DESeq2 1.26.0", "pseudo-counts rounded to integers", "LFC not shrunk (does not change padj)", "two-group fit per contrast; paper's exact model formula not stated"]},
                       "transform": "round",
                       "reasoning": "Estimated counts; DESeq2 is the paper's method (S2.8.p2). Rounded pseudo-counts are the documented route for estimated counts."},
            "threshold": {"final": {"paper_threshold": paper_thr, "threshold_source": "paper", "applied_threshold": thr,
                                    "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "inclusive": False}},
                          "reasoning": "S3.3.p2: DEGs FDR <= 0.05, no fold-change cutoff. The wheel section gives no rule; the same FDR rule is assumed. Audit: add |log2FC| > log2(1.5) as a labelled stricter comparison."},
            "study": {"final": {"route": "paper_aligned",
                                "caveats": ["treadmill DEG counts only in Venn diagrams (not in text)", "wheel contrast is day-vs-night training timing, not exercise vs sedentary",
                                            "DA mice are also under time-restricted wheel and food access (S2.3.p1)", "n=3 (treadmill) and n=4 (wheel) per arm: low power",
                                            "Entrez IDs: enrichment and runner gene lookups not run"]},
                      "paper_counts": {f"grp_{t}_vs_{c}": pc for _, c, t, _, _, pc in comps if pc},
                      "paper_genes": {},
                      "reasoning": "Planned contrasts and threshold taken from the paper; gene-level lookups skipped because the matrix is keyed by Entrez IDs."}},
        "discrepancies": [{"item": "matrix lanes", "paper": "one count per sample", "data": "two lane columns per sample", "disposition": "resolved_by_prep: summed"},
                          {"item": "count type", "paper": "tximport lengthScaledTPM into DESeq2", "data": "non-integer pseudo-counts", "disposition": "executable_with_rounding"}],
        "executions": exes, "enrichment": []}]}
json.dump(spec, open(f"{R}/case_spec.json", "w"), indent=1)
