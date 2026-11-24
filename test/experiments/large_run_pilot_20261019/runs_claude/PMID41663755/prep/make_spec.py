import json, sys, pandas as pd
R = sys.argv[1]
meta = pd.read_csv("data/GSE200283/GSE200283_metadata.csv", index_col=0)
PAPER = "test/experiments/paper_screen_20261028/papers/PMC12957370.paper.md"
pthr = {"metric": "FDR", "cutoff": 0.001, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0,
        "inclusive": True, "source_locator": "S4.7.p1",
        "note": "fold change >= 2.0 and FDR <= 0.001 (BGI PoissonDis); inclusive on both cutoffs"}
def case(tissue, n_genes, n_per, groups, fc_ref, sel_loc):
    other = "cartilage" if tissue == "synovium" else "synovium"
    excl = {g: f"{other} sample; this case analyses the {tissue} matrix only"
            for g in meta.index[meta["characteristics_ch1.1.tissue"] == other]}
    return {
      "case_id": f"GSE200283_{tissue}", "accession": "GSE200283",
      "inputs": {"paper": [PAPER], "metadata": "GSE200283/GSE200283_metadata.csv",
                 "matrix": f"{R}/prep/GSE200283_{tissue}_renamed.csv", "raw_tar": False,
                 "prep_scripts": [f"{R}/prep/rename_control.py"]},
      "gates": {
        "paper_reconstruction": {
          "final": {
            "accessions": ["GSE200283 (bulk RNA-seq)", "GSE200898 (scRNA-seq, not analysed here)"],
            "primary_estimand": ("Effect of loss of mechanical stress (knee immobilization + tail-suspension unloading, MMS) "
                                 f"on {tissue} gene expression over time (D3/D7/D14" + ("/D28" if tissue == "cartilage" else "") +
                                 " vs control), and its reversal by restored joint motion (R1) or motion + loading (R2). "
                                 "This is a disuse/unloading model, not an exercise intervention; R1/R2 are remobilization/reloading."),
            "planned_contrasts": [f"each MMS time point vs Control ({tissue}); R1 and R2 vs Control/MMS — shown only as heatmaps/module "
                                  "patterns (S2.3.p1/S2.4.p1, Figs 2-4); no DEG counts reported",
                                  f"gene selection: FC MMS {fc_ref}/control <0.67 or >1.5 with FPKM>1 -> {n_genes} genes ({sel_loc})"],
            "paper_threshold": pthr,
            "paper_method": "BGI PoissonDis on full transcriptome (S4.7.p1); iDEP 0.91 for clustering/PCA on FPKM (S4.8.p1)",
            "factors": {"intervention": groups},
            "inclusion": f"male C57BL/6J; one mouse (both knees pooled) per sample; n={n_per}/group for {tissue} (S4.7.p1)",
            "paper_results": "named genes only (synovium: Spp1, Col1a1, Ibsp, Col1a2, Postn, Mmp13, Mmp9, Il1b, Il11, Ccl2, Osm, Lif, Tgfb1, Tgfb3 up; "
                             "cartilage: Col2a1, Col11a1, Col11a2, Acan, Prg4, Sox9, Sox5 down); no DEG counts"},
          "reasoning": ("S4.7.p1 gives the DEG rule (FC>=2, FDR<=0.001, PoissonDis) but the paper reports no DEG counts; results are "
                        "heatmaps of modules and named genes (S2.3.p1, S2.4.p1, S2.5.p1). S4.8.p2 states the deposited gene sets were "
                        f"pre-selected by fold change MMS {fc_ref}/control. The intervention is disuse (S2.1.p1, S4.2.p1), with "
                        "remobilization R1 and remobilization+reloading R2 (FIG1 c, S2.2.p1)."),
          "locator": "S4.7.p1", "confidence": "high"},
        "ownership": {
          "final": {"owned": True, "checks": ["DA.p1 names GSE200283 for bulk RNA-seq",
                     f"GEO tissue={tissue} samples match the paper's groups and n={n_per}/group",
                     f"matrix has {n_genes} genes = the paper's FC-selected count in {sel_loc}"]},
          "reasoning": f"DA.p1 deposits bulk data as GSE200283; matrix row count {n_genes} equals S4.8.p2.", "confidence": "high"},
        "alignment": {
          "key_patterns": {"key": ["title", r"^(\S+(?: D\d+)?) \w+ rep(\d)$"]},
          "key_column": "key", "normalize_keys": True,
          "aliases": {"grp_raw": "characteristics_ch1.2.intervention"},
          "patterns": {"grp": ["title", r"^(Control|MMS D\d+|R1|R2) "]},
          "recode": {"grp": {"Control": "CON", "MMS D3": "D3", "MMS D7": "D7", "MMS D14": "D14", "MMS D28": "D28", "R1": "R1", "R2": "R2"}},
          "exclude_samples": excl,
          "reasoning": ("Matrix columns (cont_RepN, MMSD3_RepN, ...) correspond to GEO titles ('Control synovium rep1'); prep script only "
                        "renames 'cont_' to 'Control_' (values untouched), key derived from title group+rep, matched ignoring case/separators. "
                        "No positional alignment."),
          "confidence": "high"},
        "matrix": {
          "matrix_type": "FPKM (feature-selected subset)", "recommended_method": "none (refused)",
          "final": {"source": "GEO supplementary GSE200283_" + tissue + ".csv.gz",
                    "paper_input": "PoissonDis on full-transcriptome reads (S4.7.p1)"},
          "decision_status": "refused",
          "stop_reason": (f"The only deposited matrix is FPKM for {n_genes} genes that were PRE-SELECTED by fold change MMS {fc_ref} vs control "
                          f"(FPKM>1, FC<0.67 or >1.5; {sel_loc}). Any differential test on it is circular (features chosen on the outcome), "
                          "is not genome-wide (BH/FDR over a selected subset is invalid), and cannot reproduce the paper's PoissonDis DEG call "
                          "(needs full read counts). FPKM also cannot feed a count model. In addition the design has no exercise arm: it is a "
                          "disuse model whose only loading-restoration arms (R1/R2) have no paper-reported DEG result. A genome-wide matrix "
                          "would require re-processing the SRA reads, which is outside this run."),
          "reasoning": ("Values are non-integer (1% integer), min ~0.5-1.0 (consistent with the FPKM>1 filter), GEO data_processing: "
                        "'comma-delimited text files include FPKM values'. Row count equals the FC-selected gene counts in S4.8.p2. "
                        "Excel-date gene IDs present (e.g. 7-Mar/1-Mar), a further sign of a curated spreadsheet rather than a full matrix."),
          "candidates": [{"value": "limma on log2(FPKM+1) of the deposited subset",
                          "reason_rejected": "gene set selected on the same MMS-vs-control fold change; circular and non-genome-wide FDR"},
                         {"value": "R2 or R1 vs MMS as a 'reloading/exercise-like' contrast",
                          "reason_rejected": "same selected-subset problem; paper reports no such DE result; cartilage n=2"}],
          "confidence": "high"}
      }}
c_syn = case("synovium", 1178, 3, ["Control", "MMS D3", "MMS D7", "MMS D14", "R1", "R2"], "D14", "S4.8.p2")
c_car = case("cartilage", 1606, 2, ["Control", "MMS D3", "MMS D7", "MMS D14", "MMS D28", "R1", "R2"], "D28", "S4.8.p2")
spec = {"run_dir": R,
        "request": "Analyze GSE200283 for PMID 41663755 (Loss of mechanical stress induces synovitis, fibrosis and articular cartilage degeneration via distinct synovial cell subsets.): how exercise affects gene expression as the paper intends.",
        "decision_maker": "Claude Opus 5.5 (claude-code session)", "platform": "claude-code", "data_root": "data",
        "cases": [c_syn, c_car]}
json.dump(spec, open(f"{R}/case_spec.json", "w"), indent=1)
