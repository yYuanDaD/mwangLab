"""Shared constants for the PMID42155766 run (GSE304653, Met1-iRFP tumours, wheel running vs sedentary)."""

RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID42155766"
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC13319373.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC13319373.paper.md"
ACC = "GSE304653"
MATRIX = "data/GSE304653/GSE304653_CounTable.txt.gz"
METADATA = "data/GSE304653/GSE304653_metadata.csv"

# S3.p2 / S3.p4 / FIG2C / FIG3B: DEGs defined as "p_adj < 0.1" (BH, FIG3 legend); no fold-change rule.
PAPER_THRESHOLD = {"metric": "padj", "adjustment": "BH", "cutoff": 0.1, "effect_metric": None,
                   "effect_cutoff": None, "inclusive": False,
                   "source_locator": "S3.p2; S3.p4; FIG2; FIG3"}

CASES = {
    "TME_iRFPneg": {"celltype": "TME cells (iRFP-)", "frac": "tme", "n": {"sed": 4, "ex": 4},
                    "reported": {"n_deg": 87, "rule": "p_adj < 0.1", "locator": "S3.p2; FIG2C"},
                    "fig": "FIG2"},
    "Cancer_iRFPpos": {"celltype": "Cancer cells (iRFP+)", "frac": "cancer", "n": {"sed": 8, "ex": 7},
                       "reported": {"n_deg": 293, "rule": "p_adj < 0.1", "locator": "S3.p4; FIG3B; S2.5.p1"},
                       "fig": "FIG3"},
}
COMPARISON = "grp_ex_vs_sed"
REQUEST = ("Analyze GSE304653 for PMID 42155766 (Exercise suppresses breast cancer and reprograms the immune tumor "
           "microenvironment, cancer cell intrinsic features, and their interaction): how exercise affects gene "
           "expression as the paper intends.")
