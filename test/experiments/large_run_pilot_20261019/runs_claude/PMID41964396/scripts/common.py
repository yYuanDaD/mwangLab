"""Shared constants for the PMID41964396 run (imported by the numbered driver scripts)."""
import math

RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID41964396"
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC13069499.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC13069499.paper.md"

CASES = {
    "GSE276889_mRNA": {
        "accession": "GSE276889",
        "matrix_raw": "data/GSE276889/GSE276889_Human_skm_total_RNA_RAW_ENSEMBL.csv.gz",
        "metadata": "data/GSE276889/GSE276889_metadata.csv",
    },
    "GSE220280_mito_miRNA": {
        "accession": "GSE220280",
        "matrix_raw": "data/GSE220280/GSE220280_silver_hmt_raw.csv.gz",
        "matrix_norm_author": "data/GSE220280/GSE220280_2022-10-09_humanmito_normcounts.csv.gz",
        "metadata": "data/GSE220280/GSE220280_metadata.csv",
    },
}

# S2.14.p1: "MiRNAs and mRNAs with an FDR < 0.05 and log2FC > 1 or < -1 were identified as differentially expressed."
PAPER_THRESHOLD = {"metric": "FDR", "adjustment": "BH", "cutoff": 0.05, "effect_metric": "log2FC",
                   "effect_cutoff": 1.0, "effect_cutoff_original": "log2FC > 1 or < -1",
                   "inclusive": False, "source_locator": "S2.14.p1"}

COMPARISONS = ["time_post0h_vs_pre", "time_post3h_vs_pre", "time_post3h_vs_post0h"]
TIME_RECODE = {"pre": "pre", "post_0h": "post0h", "post_3h": "post3h"}
SUBJECT_RECODE = {str(i): f"p{i:02d}" for i in range(1, 13)}

# Paper-reported results per accession and contrast (locators in paper_reconstruction.json).
REPORTED = {
    "GSE276889_mRNA": {
        "time_post0h_vs_pre": {"up_FDR<0.05": 178, "locator": "S3.1.p1"},
        "time_post3h_vs_pre": {"up_FDR<0.05": 465, "locator": "S3.1.p1"},
        "time_post3h_vs_post0h": {"note": "not reported in text"},
        "n_genes_in_results": {"value": 17663, "locator": "S2.15.p1"},
        "PPARGC1A": {"post0h_FC": 4.0, "post3h_FC": 5.6, "FDR": "< 0.0001", "locator": "S3.1.p1"},
    },
    "GSE220280_mito_miRNA": {
        "time_post0h_vs_pre": {"FDR<0.05": 0, "raw_p<0.05": 16, "locator": "S3.4.p1"},
        "time_post3h_vs_pre": {"FDR<0.05": 0, "raw_p<0.05": 11, "locator": "S3.4.p1"},
        "time_post3h_vs_post0h": {"FDR<0.05": 0, "raw_p<0.05": 22, "locator": "S3.4.p1"},
        "n_mirna_in_results": {"value": 459, "locator": "S2.15.p1"},
        "hsa-miR-146b-5p": {"post3h_vs_pre": "log2FC 5.4, p 0.003, FDR 0.82",
                            "post3h_vs_post0h": "p < 0.0001, FDR 0.071", "locator": "ABS.p1; S3.4.p2"},
    },
}
