"""Shared constants for the GSE243060 / PMID 39232281 run."""
import pathlib
ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID39232281"
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC11378950.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC11378950.paper.md"
META = "data/GSE243060/GSE243060_metadata.csv"
SOFT = "data/GSE243060/GSE243060_family.soft.gz"
RAW = "data/GSE243060/GSE243060_RED-S_mouse_tissue_expression_raw_counts_v1.csv.gz"
NORM = "data/GSE243060/GSE243060_RED-S_mouse_tissue_expression_normalized_counts_v1.csv.gz"

# case id (paper abbreviation, TAB1 / S4.3.5.p1) -> GEO tissue characteristic
TISSUES = {
    "PIT": "Pituitary", "HEA": "Heart", "LUN": "Lung", "BAT": "Brown adipose tissue", "LIV": "Liver",
    "ADR": "Adrenal gland", "KID": "Kidney", "SPL": "Spleen", "OVA": "Ovary", "UTE": "Uterus",
    "TES": "Testis", "QUA": "Quadriceps", "GAS": "Gastrocnemius", "GASt": "Gastrocnemius tendon",
    "EDL": "Extensor digitorum longus", "EDLt": "Extensor digitorum longus tendon", "TA": "Tibialis anterior",
    "TAt": "Tibialis anterior tendon", "SOL": "Soleus",
}
MUSCLES = ["QUA", "GAS", "EDL", "TA", "SOL"]
TENDONS = ["GASt", "EDLt", "TAt"]

PAPER_THRESHOLD = {
    "metric": "padj", "adjustment": "BH", "cutoff": 0.05, "effect_metric": None, "effect_cutoff": None,
    "inclusive": False, "source_locator": "S4.3.13.p1",
    "expressed_gene_rule": "normalized average gene counts >= 10 (S4.3.13.p1)",
}

# Counts the paper states in text (time-independent, Deficient vs Control)
PAPER_COUNTS = {
    ("UTE", "F"): {"n": 8785, "down": 4407, "up": 4378, "locator": "S2.7.p1"},
    ("OVA", "F"): {"n": 2563, "down": 1368, "up": 1195, "locator": "S2.7.p1"},
    ("KID", "M"): {"n": 6037, "down": 3301, "up": 2736, "locator": "S2.7.p1"},
}
PAPER_UNIONS = {
    ("muscles", "F"): {"n": 6476, "down": 3136, "up": 3340, "locator": "S2.6.p1"},
    ("muscles", "M"): {"n": 3182, "down": 1697, "up": 1485, "locator": "S2.6.p1"},
    ("tendons", "F"): {"n": 3823, "down": 2426, "up": 1397, "locator": "S2.6.p4"},
    ("tendons", "M"): {"n": 3055, "down": 1906, "up": 1149, "locator": "S2.6.p4"},
    ("all_tissues", "F"): {"n": 14837, "locator": "S2.3.p1"},
    ("all_tissues", "M"): {"n": 11326, "locator": "S2.3.p1"},
}
