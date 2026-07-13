"""Pick a cohort accession list from a search_geo_studies CSV.

Strategy: split the candidates into "top by current sort key" + "random
sample from the rest", to get both predictable hard cases AND diverse
sampling across the keyword's universe.

Both pools are restricted to has_counts_like_supp=True so we don't waste
downloads on studies that lack supplementary count files.

CLI:
    python test/scripts/pick_cohort.py output/geo_search_Diabetes.csv --top 5 --random 5 --seed 42

Importable:
    from test.scripts.pick_cohort import pick_cohort
    acc_list = pick_cohort("output/geo_search_Diabetes.csv", n_top=5, n_random=5, seed=42)
"""

import argparse
import os
import random
import sys

import pandas as pd


def pick_cohort(search_csv: str, n_top: int = 5, n_random: int = 5,
                seed: int = 42) -> list[str]:
    """Return a list of accessions: n_top from the head + n_random from the rest.

    Both pools require has_counts_like_supp=True. Random pool uses a seeded
    RNG so re-runs are reproducible.
    """
    df = pd.read_csv(search_csv)
    if "has_counts_like_supp" not in df.columns:
        raise ValueError(f"{search_csv} missing 'has_counts_like_supp' column")
    pool = df[df["has_counts_like_supp"] == True].copy()  # noqa: E712
    if pool.empty:
        return []

    pool = pool.sort_values("n_samples", ascending=False).reset_index(drop=True)

    n_top = min(n_top, len(pool))
    top_acc = pool["accession"].iloc[:n_top].tolist()

    remaining = pool["accession"].iloc[n_top:].tolist()
    rng = random.Random(seed)
    n_random = min(n_random, len(remaining))
    random_acc = rng.sample(remaining, n_random) if n_random > 0 else []

    return top_acc + random_acc


def describe_pick(search_csv: str, accessions: list[str]) -> str:
    """One-line-per-accession summary for human eyeballing."""
    df = pd.read_csv(search_csv).set_index("accession")
    lines = []
    for i, acc in enumerate(accessions, 1):
        if acc not in df.index:
            lines.append(f"  {i:2d}. {acc} (NOT FOUND in search CSV)")
            continue
        row = df.loc[acc]
        n = int(row.get("n_samples", 0))
        title = str(row.get("title", ""))[:90]
        supp = str(row.get("supp_file_types", ""))
        lines.append(f"  {i:2d}. {acc} | n={n:3d} | supp={supp:15s} | {title}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("search_csv", help="search_geo_studies output CSV")
    ap.add_argument("--top", type=int, default=5, help="Number of top-by-size studies")
    ap.add_argument("--random", type=int, default=5, help="Number of random studies from the rest")
    ap.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    args = ap.parse_args()

    accs = pick_cohort(args.search_csv, n_top=args.top, n_random=args.random, seed=args.seed)
    print(f"Picked {len(accs)} accessions ({args.top} top + {args.random} random, seed={args.seed}):\n")
    print(describe_pick(args.search_csv, accs))
    print()
    print("Accession list (newline-separated):")
    for a in accs:
        print(a)


if __name__ == "__main__":
    main()
