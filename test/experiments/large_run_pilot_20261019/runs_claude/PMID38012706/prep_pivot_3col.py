"""Pivot GSE242861_3col.tsv.gz (long format: sample, transcript, kallisto estimated count; no header)
into a wide transcript x sample matrix. Values are left unchanged (no summing to genes, no rounding)."""
import sys
import pandas as pd

src = sys.argv[1] if len(sys.argv) > 1 else "data/GSE242861/GSE242861_3col.tsv.gz"
out = sys.argv[2] if len(sys.argv) > 2 else "test/experiments/large_run_pilot_20261019/runs_claude/PMID38012706/GSE242861_transcript_counts_wide.csv"

d = pd.read_csv(src, sep="\t", header=None, names=["sample", "transcript", "count"])
dup = d.duplicated(["sample", "transcript"]).sum()
if dup:
    raise SystemExit(f"{dup} duplicated (sample, transcript) rows; refusing to aggregate silently")
w = d.pivot(index="transcript", columns="sample", values="count")
w.index.name = "transcript_id"
print("shape", w.shape, "missing", int(w.isna().sum().sum()))
w.to_csv(out)
print("wrote", out)
