"""Merge the two deposited GSE324257 TPM files (Ctrl and KO) into one matrix.

Values are not changed. Rows are joined on the Ensembl gene ID; the version
suffix (".1") is stripped only after checking it creates no duplicate IDs.
Usage: python merge_tpm.py <data_dir> <out_csv>
"""
import sys
from pathlib import Path

import pandas as pd

data_dir, out_csv = Path(sys.argv[1]), Path(sys.argv[2])
ctrl = pd.read_csv(data_dir / "GSE324257_TPMs_Ctrl_.csv", index_col=0)
ko = pd.read_csv(data_dir / "GSE324257_TPMs_KO_.csv", index_col=0)
assert ctrl.index.is_unique and ko.index.is_unique
assert set(ctrl.index) == set(ko.index), "gene sets differ between files"
merged = ctrl.join(ko, how="inner")
stripped = merged.index.str.replace(r"\.\d+$", "", regex=True)
assert stripped.is_unique, "version stripping creates duplicate IDs"
merged.index = stripped
merged.index.name = "gene_id"
assert merged.notna().all().all() and (merged >= 0).all().all()
merged.to_csv(out_csv)
print(f"{merged.shape[0]} genes x {merged.shape[1]} samples -> {out_csv}")

# Low-expression filter (method decision, recorded in the method gate): keep genes
# with TPM >= 1 in at least 3 samples (the size of the smallest group). Values are
# unchanged; only rows are removed.
keep = (merged >= 1).sum(axis=1) >= 3
filt_csv = out_csv.with_name(out_csv.stem + "_expressed.csv")
merged.loc[keep].to_csv(filt_csv)
print(f"expressed filter (TPM>=1 in >=3 samples): {int(keep.sum())} genes -> {filt_csv}")
