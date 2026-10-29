"""Paper S4.7.p1 low-count rule, per case: "Genes with fewer than 10 reads across
samples within any condition were removed." Interpreted as: keep a gene when at least
one condition of that experiment has >= 10 summed reads. All 90 columns are kept; only
rows are filtered, using the case's own samples (matrix columns = GEO titles)."""
import sys
from pathlib import Path
import pandas as pd

src = Path(sys.argv[1]); out_dir = Path(sys.argv[2]); out_dir.mkdir(parents=True, exist_ok=True)
x = pd.read_csv(src, sep="\t", index_col=0)
P = "Pdgfra.CRE_Piezo1."
cases = {
    "AEX": {"SED": [f"WT_sed#{i}" for i in (1, 2, 3)], "AEX": [f"WT_exe#{i}" for i in (1, 2, 3)]},
    "EXT": {"SED": [f"WT.SED#{i}" for i in (1, 2, 3)], "EXT": [f"WT.EXT#{i}" for i in (1, 2, 3)]},
    "PIEZO": {k: [f"{P}{g}_{c}#{i}" for i in (1, 2, 3)] for k, (g, c) in
              {"WT_SED": ("WT", "SED"), "WT_AEX": ("WT", "AEXd1"),
               "FL_SED": ("FL", "SED"), "FL_AEX": ("FL", "AEXd1")}.items()},
}
for name, conds in cases.items():
    keep = pd.concat([x[c].sum(axis=1) >= 10 for c in conds.values()], axis=1).any(axis=1)
    out = out_dir / f"GSE297515_counts_filtered_{name}.csv"
    x.loc[keep].to_csv(out)
    print(name, int(keep.sum()), "of", len(x), "genes kept ->", out)
