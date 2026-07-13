"""One-off probe: download supplementary files for a few search hits and classify
each large matrix as raw_counts / fpkm_tpm / log_transformed / etc., to estimate
how often has_counts_like_supp=True actually means usable raw counts."""

import gzip
import io
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(_PROJECT_ROOT)
sys.path.insert(0, _PROJECT_ROOT)

import numpy as np
import pandas as pd

from tools.geo_tools import download_supplementary_files

CANDIDATES = ["GSE297515", "GSE297707", "GSE283691", "GSE326587"]
BASE = "data"


def _open(path):
    return gzip.open(path, "rt", encoding="utf-8", errors="replace") if path.endswith(".gz") \
        else open(path, encoding="utf-8", errors="replace")


def classify_file(path):
    try:
        with _open(path) as fh:
            head = fh.read(8192)
        if path.endswith(".csv") or path.endswith(".csv.gz"):
            sep = ","
        elif "\t" in head:
            sep = "\t"
        else:
            sep = ","

        if path.endswith(".gz"):
            with gzip.open(path, "rt", encoding="utf-8", errors="replace") as fh:
                df = pd.read_csv(fh, sep=sep, nrows=2000, low_memory=False)
        else:
            df = pd.read_csv(path, sep=sep, nrows=2000, low_memory=False)
    except Exception as e:
        return f"unreadable ({type(e).__name__}: {e})", None

    if df.shape[1] < 3:
        return f"too few cols ({df.shape[1]})", df

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if not numeric_cols:
        return "no numeric cols (annotation only?)", df

    vals = df[numeric_cols].to_numpy(dtype=float, na_value=np.nan).ravel()
    vals = vals[~np.isnan(vals)]
    nz = vals[vals != 0]
    if len(nz) == 0:
        return "all zero / NaN", df

    has_negative = bool((nz < 0).any())
    has_decimal = bool((nz % 1 != 0).any())
    max_val = float(nz.max())
    median_val = float(np.median(nz))

    if has_negative:
        klass = "log_transformed"
    elif not has_decimal and max_val > 100:
        klass = "raw_counts"
    elif has_decimal and max_val < 1000 and median_val < 50:
        klass = "fpkm_or_tpm"
    elif has_decimal:
        klass = "normalized_decimal"
    else:
        klass = "integer_low_max"

    return (f"{klass}  (max={max_val:.1f}, median={median_val:.2f}, "
            f"decimal={has_decimal}, neg={has_negative})"), df


verdicts = {}
for acc in CANDIDATES:
    print(f"\n=== {acc} ===")
    target = os.path.join(BASE, acc)
    if not os.path.isdir(target) or not os.listdir(target):
        msg = download_supplementary_files.invoke({"geo_accession": acc, "base_dir": BASE})
        print(msg[:300])

    files = []
    if os.path.isdir(target):
        for root, _, names in os.walk(target):
            for n in names:
                p = os.path.join(root, n)
                if n.lower().endswith((".csv", ".tsv", ".txt", ".csv.gz", ".tsv.gz", ".txt.gz")):
                    files.append((os.path.getsize(p), p))
    files.sort(reverse=True)

    if not files:
        print("  no parsable matrix file found")
        verdicts[acc] = "no_file"
        continue

    study_verdict = "unusable"
    for size, p in files[:3]:
        rel = os.path.relpath(p, BASE)
        cls, df = classify_file(p)
        cols = list(df.columns)[:5] if df is not None else []
        print(f"  [{size:>11,} B] {rel}")
        print(f"    -> {cls}")
        print(f"    first cols: {cols}")
        if cls.startswith("raw_counts"):
            study_verdict = "raw_counts_ok"
    verdicts[acc] = study_verdict

print("\n\n=== VERDICT SUMMARY ===")
for acc, v in verdicts.items():
    print(f"  {acc}: {v}")
ok = sum(1 for v in verdicts.values() if v == "raw_counts_ok")
print(f"\n{ok}/{len(verdicts)} studies have a usable raw-counts matrix.")
