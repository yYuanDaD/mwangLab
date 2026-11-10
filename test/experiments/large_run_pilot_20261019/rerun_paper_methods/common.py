"""Shared helpers for rerunning the 8 papers with the paper's own DE method (tools/r_de_tools.py).

Inputs are the aligned matrices and metadata the large run saved under runs_claude/; nothing
is downloaded and no LLM is called. Each paper script appends its numbers to results.json.
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

import pandas as pd  # noqa: E402

from tools import native  # noqa: E402

HERE = Path(__file__).resolve().parent
RUNS = HERE.parent / "runs_claude"
RESULTS = HERE / "results.json"


def out_dir(paper: str, name: str) -> Path:
    path = HERE / "out" / paper / name
    path.mkdir(parents=True, exist_ok=True)
    return path


def count(deg_csv: str, **rule) -> dict:
    r = native.apply_threshold(deg_csv, **rule)
    return {k: r[k] for k in ("rule", "n_tested", "n_significant", "n_up", "n_down")}


def overlap(a_csv: str, b_csv: str, rule_a: dict, rule_b: dict) -> dict:
    """Genes significant in both tables, and the log2FC correlation over genes tested in both."""
    def sig(path, rule):
        t = pd.read_csv(path, index_col=0)
        p = pd.to_numeric(t[next(c for c in ("padj", "FDR", "adj.P.Val") if c in t)], errors="coerce")
        keep = p <= rule["cutoff"] if rule.get("inclusive") else p < rule["cutoff"]
        if rule.get("effect_cutoff"):
            keep &= t["log2FoldChange"].abs() > rule["effect_cutoff"]
        return t, set(t.index[keep])
    ta, sa = sig(a_csv, rule_a)
    tb, sb = sig(b_csv, rule_b)
    common = ta.index.intersection(tb.index)
    r = ta.loc[common, "log2FoldChange"].corr(tb.loc[common, "log2FoldChange"])
    return {"n_a": len(sa), "n_b": len(sb), "shared": len(sa & sb), "lfc_r_all_genes": round(float(r), 3)}


def record(paper: str, payload: dict) -> None:
    data = json.loads(RESULTS.read_text(encoding="utf-8")) if RESULTS.exists() else {}
    data[paper] = payload
    RESULTS.write_text(json.dumps(data, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False, default=str)[:4000])
