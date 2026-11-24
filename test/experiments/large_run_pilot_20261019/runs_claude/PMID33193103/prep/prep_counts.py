"""Repair GSE155230 featureCounts tables for the case runner.

The deposited files start with a '# Program:featureCounts ...' comment line, which
the runner's separator sniffer reads as the header (inspect showed the real header
as a data row). This script drops the comment, keeps Geneid + count columns, and
renames each BAM path column to the sample key used in GEO `description`
(e.g. bam/NG-8752_HRTT_1_lib99128_4266_3_1...bam -> HRTT_1). Values are unchanged.
"""
import re
import sys
from pathlib import Path

import pandas as pd

DATA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/GSE155230")
OUT = Path(__file__).resolve().parent
PAT = re.compile(r"NG-8752_([A-Z]+_\d)_lib\d+_\d+_(\d)_\d")
lanes = {}

for name in ["GSE155230_lrt_hrt_counts.tsv.gz", "GSE155230_lcr_hcr_counts.tsv.gz"]:
    df = pd.read_csv(DATA / name, sep="\t", comment="#", index_col=0)
    ren = {}
    for c in df.columns:
        m = PAT.search(c)
        if not m:
            raise SystemExit(f"unmatched column {c} in {name}")
        ren[c] = m.group(1)
        lanes[m.group(1)] = f"L{m.group(2)}"
    df = df.rename(columns=ren)
    assert df.index.is_unique and df.shape[1] == len(set(df.columns))
    out = OUT / name.replace(".tsv.gz", "_clean.csv")
    df.to_csv(out)
    print(out, df.shape, list(df.columns))

# Metadata copy with the sequencing lane parsed from the FASTQ names
# (<project>_<sample>_<lib>_<run>_<lane>_<read>), so the confounding report can test it.
meta = pd.read_csv(DATA / "GSE155230_metadata.csv", index_col=0)
meta["lane"] = meta["description"].map(lanes)
assert meta["lane"].notna().all()
meta.to_csv(OUT / "GSE155230_metadata_lane.csv")
print(meta[["description", "lane"]].to_string())
