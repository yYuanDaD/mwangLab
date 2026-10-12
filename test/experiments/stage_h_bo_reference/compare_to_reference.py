"""Stage H: compare a skill DE table with Bo's gold DEG list for the same contrast.

    python compare_to_reference.py <skill_deg.csv> <bo_deg.txt> [--padj 0.05] [--lfc 0.5] [--out report.json]

Bo's files are filtered DEG lists (padj < 0.05 and |log2FC| > 0.5). The skill
table is a full DE table. Both are scored on gene symbols or IDs as given.

Reported:
- gold DEG count and skill DEG count under Bo's thresholds;
- overlap, Jaccard, and direction agreement on the overlap;
- recovery: fraction of gold DEGs the skill also calls, in the same direction;
- logFC Pearson and Spearman on the gold DEGs present in the skill table;
- the gold DEGs the skill misses, with the skill's padj and log2FC, to explain differences.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

LFC_NAMES = ("log2FoldChange", "logFC", "log2FC", "lfc")
PADJ_NAMES = ("padj", "adj.P.Val", "adj.P.Value", "FDR", "qvalue", "adj_pvalue")


def _pick(frame: pd.DataFrame, names, what: str) -> str:
    lower = {c.lower(): c for c in frame.columns}
    for name in names:
        if name.lower() in lower:
            return lower[name.lower()]
    raise SystemExit(f"no {what} column among {list(frame.columns)}")


def load(path: Path) -> pd.DataFrame:
    # Bo's R tables have one header name fewer than data fields, so pandas makes the
    # unnamed first field (the Ensembl ID) the index. Skill tables write the ID as the
    # first, often unnamed, column.
    frame = pd.read_csv(path, sep=None, engine="python")
    if not isinstance(frame.index, pd.RangeIndex):
        ids = frame.index.astype(str)
    else:
        first = frame.columns[0]
        id_col = next((c for c in ("gene_id", "gene", "GeneID", "Gene", "feature") if c in frame.columns), first)
        ids = frame[id_col].astype(str)
    lfc, padj = _pick(frame, LFC_NAMES, "log2 fold change"), _pick(frame, PADJ_NAMES, "adjusted p-value")
    out = pd.DataFrame({"lfc": pd.to_numeric(frame[lfc], errors="coerce").values,
                        "padj": pd.to_numeric(frame[padj], errors="coerce").values},
                       index=pd.Index(ids).str.strip())
    return out[~out.index.duplicated(keep="first")]


def compare(ours: pd.DataFrame, gold: pd.DataFrame, padj: float, lfc: float) -> dict:
    gold_sig = gold[(gold["padj"] < padj) & (gold["lfc"].abs() > lfc)]
    our_sig = ours[(ours["padj"] < padj) & (ours["lfc"].abs() > lfc)]
    g, o = set(gold_sig.index), set(our_sig.index)
    inter = sorted(g & o)
    same_dir = int((np.sign(gold_sig.loc[inter, "lfc"]) == np.sign(our_sig.loc[inter, "lfc"])).sum())
    shared = gold_sig.index.intersection(ours.index)
    pair = pd.DataFrame({"gold": gold_sig.loc[shared, "lfc"], "ours": ours.loc[shared, "lfc"]}).dropna()
    missed = gold_sig.index.difference(o)
    missed_detail = pd.DataFrame({
        "gold_lfc": gold_sig.loc[missed, "lfc"],
        "our_lfc": ours["lfc"].reindex(missed),
        "our_padj": ours["padj"].reindex(missed),
    }).sort_values("gold_lfc", key=np.abs, ascending=False)
    every = pd.DataFrame({"gold": gold["lfc"], "ours": ours["lfc"].reindex(gold.index)}).dropna()
    return {
        "thresholds": {"padj": padj, "abs_log2fc": lfc},
        "genes_in_both_tables": len(every),
        "logfc_pearson_all_shared_genes": round(float(every["gold"].corr(every["ours"])), 4) if len(every) > 2 else None,
        "gold_deg": len(g),
        "skill_deg": len(o),
        "overlap": len(inter),
        "jaccard": round(len(inter) / len(g | o), 4) if g | o else None,
        "direction_agreement_on_overlap": round(same_dir / len(inter), 4) if inter else None,
        "recovery_same_direction": round(same_dir / len(g), 4) if g else None,
        "gold_deg_absent_from_skill_table": int(len(gold_sig.index.difference(ours.index))),
        "logfc_pearson_on_gold_deg": round(float(pair["gold"].corr(pair["ours"])), 4) if len(pair) > 2 else None,
        "logfc_spearman_on_gold_deg": (round(float(pair["gold"].corr(pair["ours"], method="spearman")), 4)
                                       if len(pair) > 2 else None),
        "missed_examples": missed_detail.head(15).round(4).reset_index(names="gene").to_dict(orient="records"),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_deg", type=Path)
    parser.add_argument("gold_deg", type=Path)
    parser.add_argument("--padj", type=float, default=0.05)
    parser.add_argument("--lfc", type=float, default=0.5)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    report = compare(load(args.skill_deg), load(args.gold_deg), args.padj, args.lfc)
    report["skill_deg_file"], report["gold_deg_file"] = str(args.skill_deg), str(args.gold_deg)
    text = json.dumps(report, indent=2)
    print(text)
    if args.out:
        args.out.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
