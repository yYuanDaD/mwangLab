"""Shared paths and the paper study map for PMID 37318869 / GSE208639."""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[6]  # repository root (run dir is 6 levels deep)
sys.path.insert(0, str(ROOT))
import os
os.chdir(ROOT)

RUN_DIR = pathlib.Path("test/experiments/large_run_pilot_20261019/runs_claude/PMID37318869")
PAPER_JSON = pathlib.Path("test/experiments/paper_screen_20261019/papers/PMC10443797.paper.json")
PAPER_MD = pathlib.Path("test/experiments/paper_screen_20261019/papers/PMC10443797.paper.md")
DATA = pathlib.Path("data/GSE208639")
META = DATA / "GSE208639_metadata.csv"
COUNTS = RUN_DIR / "case_01" / "inputs" / "GSE208639_star_counts_reverse.csv"
MERGE_REPORT = RUN_DIR / "case_01" / "inputs" / "star_merge_report.json"
MERGE_SCRIPT = RUN_DIR / "scripts" / "00_merge_star_counts.py"
FPKM = DATA / "GSE208639_FPKM.csv.gz"
EDGER_SHEET1 = DATA / "GSE208639_edgeR_output.csv"

PAPER_THRESHOLD = {
    "metric": "pvalue", "adjustment": "none", "cutoff": 0.05,
    "effect_metric": "log2FC", "effect_cutoff": 2.0, "effect_cutoff_original": "log_2FC > |2|",
    "inclusive": False, "source_locator": "S4.4.p1",
    "scope": "significant DEGs for the strength-training program; applied in S2.5.p1 to "
             "pre-training vs unaffected-control DEGs (raw P, no multiple-testing adjustment stated)",
}

STUDY_MAP = {
    "paper_id": "PMID37318869 / PMC10443797 (Davey et al., JCI Insight 2023)",
    "accessions": ["GSE208639"],
    "accessions_not_used": {"GSE184951": "cycling-training reanalysis (Mikhail et al.), separate study",
                            "GSE86356": "DMSeq.org reference data", "GSE59088": "Amar et al. meta-analysis",
                            "GSE97084": "Amar et al. meta-analysis"},
    "assay": "bulk RNA-seq, rRNA-depleted stranded (NEBNext Ultra II Directional), PE75, vastus lateralis",
    "sample_inclusion": ["9 male DM1 patients, biopsy before and after 12-week strength training (S4.3.p1, ABS.p1)",
                         "6 male unaffected controls, single biopsy, no training (S4.3.p1)"],
    "sample_exclusion": ["participants 2182 and 1955 (poor RNA quantity/quality) - not deposited (S4.4.p1, S2.2.p1)"],
    "factors": [{"name": "group", "levels": ["control (no training)", "DM1 pre-training", "DM1 post-training"]},
                {"name": "subject", "levels": "9 DM1 participants (pre/post pairs) + 6 controls"}],
    "primary_estimand": ("Effect of 12-week strength training on muscle gene expression in DM1, quantified as "
                         "the change from pre- to post-training relative to unaffected controls "
                         "(Δlog2FC = log2FC[post vs control] - log2FC[pre vs control]) and as % rescue of "
                         "pre-training DEGs; analysed grouped and per individual (S2.2.p2, S2.5.p1, S4.6.p1)"),
    "planned_contrasts": [
        {"name": "grouped_pre_vs_control", "locator": "S2.2.p2, S4.13.p1", "test": "edgeR QL F-test"},
        {"name": "grouped_post_vs_control", "locator": "S2.2.p2, S4.13.p1", "test": "edgeR QL F-test"},
        {"name": "grouped_delta_log2FC (post-vs-control minus pre-vs-control)", "locator": "S2.2.p2",
         "test": "none (difference of two fitted log2FCs; no p-value)"},
        {"name": "individual_<id>_pre_vs_control and individual_<id>_post_vs_control (n=1 vs 6 controls)",
         "locator": "S2.2.p2, FIG1, S2.5.p1", "test": "edgeR QL F-test"},
    ],
    "direct_post_vs_pre_test": "not_reported (the paper never tests post vs pre within subjects)",
    "blocking_or_covariance": {"status": "not_reported",
                               "note": "Grouped analysis pools pre and post samples as two groups each vs controls; "
                                       "no subject blocking described (S2.2.p2)"},
    "matrix_scale": "STAR gene counts (raw integer) -> edgeR (S4.4.p1; GEO data_processing)",
    "paper_method": "edgeR 3.34.1, quasi-likelihood F-test, each group vs unaffected controls (S4.4.p1, S4.13.p1)",
    "paper_filter": "Genes with less than 10 counts in each samples were filtered out (S4.4.p1)",
    "paper_formula": "not_reported",
    "normalization": "not_reported (edgeR default TMM presumed, not stated)",
    "paper_threshold": PAPER_THRESHOLD,
    "covariates_mentioned": {"age": "controls avg 32 vs DM1 avg 48 y; used only in correlation analysis (S2.5.p2); "
                                    "not in GEO metadata", "sex": "all male"},
}
