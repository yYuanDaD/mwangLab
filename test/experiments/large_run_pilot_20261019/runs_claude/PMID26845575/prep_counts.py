"""Reconstruct read counts from GSE69699 RPM files and apply the paper's 125 RPM gene filter.

Deposited files hold RPM only (data_processing: "Read counts were converted to RPM").
RPM values are quantized: every value is an exact multiple (to 6 significant digits) of
the sample's smallest non-zero RPM, i.e. one read = 1e6 / library_size. Counts are
recovered as round(RPM / min_nonzero_RPM); the reconstructed column sums equal
1e6 / min_nonzero_RPM within <= 4 reads (rounding of 6-significant-digit RPM values).

Paper filter (S2.6.p2, S2.7.p1, FIG3): genes > 125 RPM, n = 1011. The rule
"mean RPM of the two replicates > 125 in at least one of the four assay x condition
groups" reproduces exactly 1011 genes, so it is used.

Usage: python prep_counts.py <merged_from_tar.csv> <out_dir>
"""
import sys, os, re
import numpy as np
import pandas as pd

src, out_dir = sys.argv[1], sys.argv[2]
rpm = pd.read_csv(src, index_col=0)
rpm.columns = [re.match(r"^(GSM\d+)", c).group(1) for c in rpm.columns]

unit = rpm.apply(lambda s: s[s > 0].min())
counts = (rpm / unit).round().astype(int)
dev = ((rpm / unit) - counts).abs().max()
print("library sizes (1e6/min RPM):", (1e6 / unit).round().astype(int).to_dict())
print("reconstructed sums:", counts.sum().to_dict())
print("max |RPM/unit - round| per sample:", dev.round(3).to_dict())

groups = {"mRNA_ctrl": ["GSM1707648", "GSM1707649"], "mRNA_ex": ["GSM1707650", "GSM1707651"],
          "RPF_ctrl": ["GSM1707652", "GSM1707653"], "RPF_ex": ["GSM1707654", "GSM1707655"]}
gmean = pd.concat({g: rpm[s].mean(axis=1) for g, s in groups.items()}, axis=1)
keep = gmean.max(axis=1) > 125
print("genes passing 125 RPM filter:", int(keep.sum()))

os.makedirs(out_dir, exist_ok=True)
counts.to_csv(os.path.join(out_dir, "GSE69699_counts_reconstructed_all.csv"))
counts.loc[keep].to_csv(os.path.join(out_dir, "GSE69699_counts_reconstructed_125RPM.csv"))
