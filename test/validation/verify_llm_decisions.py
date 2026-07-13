"""Spot-check the biological correctness of LLM A/B decisions from the
Exercise_v2_llm_fallback cohort run. Reads each study's metadata + counts
file and prints the actual value distributions / column names the LLM saw.

Run from project root:
    python test/validation/verify_llm_decisions.py
"""

import os
import sys

import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, _ROOT)
os.chdir(_ROOT)


def hr(s: str):
    print("\n" + "=" * 70)
    print(s)
    print("=" * 70)


def verify_GSE297515():
    hr("GSE297515 — A overrode ch1.3 -> ch1.2; was the new contrast clean?")
    df = pd.read_csv("data/GSE297515/GSE297515_metadata.csv", index_col=0)
    print(f"Total samples: {len(df)}\n")
    candidates = [c for c in df.columns
                  if "treatment" in c.lower() or "genotype" in c.lower()
                  or c.startswith("characteristics_ch1.")]
    for col in candidates:
        vc = df[col].dropna().astype(str).value_counts()
        print(f"  {col} ({df[col].notna().sum()} non-null):")
        for v, n in vc.items():
            print(f"      {v!r}: {n}")


def verify_GSE282641():
    hr("GSE282641 — A rescued from NO MATCH; was ch1.4.treatment 'sed vs ex' correct?")
    df = pd.read_csv("data/GSE282641/GSE282641_metadata.csv", index_col=0)
    print(f"Total samples: {len(df)}\n")
    for col in df.columns:
        if not col.startswith("characteristics_ch1."):
            continue
        vc = df[col].dropna().astype(str).value_counts()
        print(f"  {col} ({df[col].notna().sum()} non-null):")
        for v, n in vc.items():
            print(f"      {v!r}: {n}")
    print("\nTitle samples (showing real label semantics):")
    print(df["title"].head(8).to_string())
    print("\nTreatment protocol (first 250 chars):")
    print(str(df["treatment_protocol_ch1"].iloc[0])[:250])


def verify_GSE326587_contrast():
    hr("GSE326587 — A confirmed ch1.3.treatment Control vs Run")
    df = pd.read_csv("data/GSE326587/GSE326587_metadata.csv", index_col=0)
    print(f"Total samples: {len(df)}\n")
    for col in df.columns:
        if not col.startswith("characteristics_ch1."):
            continue
        vc = df[col].dropna().astype(str).value_counts()
        print(f"  {col} ({df[col].notna().sum()} non-null):")
        for v, n in vc.items():
            print(f"      {v!r}: {n}")
    print("\nTitle vs ch1.3.treatment (first 10 — does title agree with label?):")
    print(df[["title", "characteristics_ch1.3.treatment"]].head(10).to_string())


def verify_GSE326587_alignment():
    hr("GSE326587 — B aligned 28/29 via LLM; spot-check the mappings")
    df_meta = pd.read_csv("data/GSE326587/GSE326587_metadata.csv", index_col=0)
    counts_path = "data/GSE326587/GSE326587_Adler_raw_counts.csv.gz"
    df_counts = pd.read_csv(counts_path, index_col=0, sep=None, engine="python", nrows=3)
    counts_cols = list(df_counts.columns)
    print(f"Counts columns ({len(counts_cols)}):")
    for c in counts_cols:
        print(f"    {c!r}")
    print(f"\nMetadata GSM IDs + titles ({len(df_meta)}):")
    show = df_meta[["title", "characteristics_ch1.3.treatment",
                    "characteristics_ch1.4.batch"]]
    print(show.to_string())

    # Re-derive the LLM mapping live by calling the alignment fallback
    print("\n-- re-running align_samples_with_llm_fallback to capture mapping --")
    from tools.llm_helpers import align_samples_with_llm_fallback
    mapping, method = align_samples_with_llm_fallback(counts_cols, df_meta)
    print(f"\nmethod: {method}")
    print(f"mappings ({len(mapping)}):")
    for gsm, col in mapping.items():
        title = df_meta.at[gsm, "title"] if gsm in df_meta.index else "(?)"
        print(f"    {gsm}  =>  {col!r}    (title: {title})")


if __name__ == "__main__":
    if not os.getenv("CLAUDE_API_KEY"):
        from dotenv import load_dotenv
        load_dotenv()
    verify_GSE297515()
    verify_GSE282641()
    verify_GSE326587_contrast()
    verify_GSE326587_alignment()
    print("\nDone.")
