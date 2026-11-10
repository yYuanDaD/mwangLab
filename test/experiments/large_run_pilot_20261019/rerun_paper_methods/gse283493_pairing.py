"""GSE283493: assumed pairing of SAT and VAT libraries by group + replicate letter.

The paper takes both fat depots from each rat, but GEO has no animal ID. Library names end in
a-f within each group (SAT_AM_Cont_a, VAT_AM_Cont_a), so "group + letter" may be one rat (24
rats). This is an assumption, so we (1) test it on the data: after removing tissue x group
means, is a SAT library more correlated with the same-letter VAT library than with the other
VAT libraries of its group? and (2) rerun the phase x training interaction with the rat as a
random block (voom + duplicateCorrelation; a fixed rat effect would absorb the
between-rat interaction), next to the same model without the block.
"""

from common import HERE, count, out_dir, record

import numpy as np
import pandas as pd

from tools.pairing_check import check_pairing_key
from tools.r_de_tools import run_r_de

work = HERE / "out/GSE283493/inputs"
meta = pd.read_csv(work / "meta_44.csv", index_col=0)
counts = pd.read_csv(work / "counts_44_filtered.csv", index_col=0)
full = pd.read_csv(HERE.parent / "runs_claude/PMID39832562/interaction_lrt/aligned/design_metadata.csv", index_col=0)
meta["letter"] = full.loc[meta.index, "rep_letter"]
meta["rat"] = meta.grp + "_" + meta.letter

# (1) residual correlation across tissues (tools/pairing_check.py)
logcpm = np.log2(counts / counts.sum() * 1e6 + 1)
evidence = {
    "group_plus_letter": check_pairing_key(logcpm, meta, key=["grp", "letter"], across="tissue", within=["grp"]),
    # the first run's check: the letter alone, pairs allowed across groups
    "letter_only": check_pairing_key(logcpm, meta, key=["letter"], across="tissue"),
}

# (2) interaction with and without the rat block
meta.to_csv(work / "meta_44_rat.csv")
levels = {"training": ["ctrl", "ex"], "phase": ["EA", "LA"], "tissue": ["SAT", "VAT"]}
con = [{"name": "phase_x_training", "coef": "phaseLA.trainingex"}]
runs = {}
for name, kw in {"voom_rat_block": dict(block="rat"), "voom_no_block": {}}.items():
    res = run_r_de(str(work / "counts_44_filtered.csv"), str(work / "meta_44_rat.csv"),
                   str(out_dir("GSE283493", name)), engine="voom",
                   design="~ tissue + phase + training + phase:training", levels=levels, contrasts=con,
                   label=name, **kw)
    path = res["results"][0]["path"]
    runs[name] = {"padj<0.1": count(path, metric="padj", cutoff=0.1),
                  "consensus_correlation": res["report"].get("consensus_correlation")}
record("GSE283493_assumed_pairing", {"assumption": "rat = group + replicate letter (24 rats)",
                                     "evidence": evidence, "interaction": runs, "paper_lrt": 632})
