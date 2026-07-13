"""Evaluation helpers for repeated subset / rerun stability checks.

The intended workflow is:
  1. Run the same analysis several times on bootstrap/subset samples or on
     repeated extraction/analysis runs.
  2. Pass the resulting DEG and/or GSEA CSV files here.
  3. Inspect pairwise overlap/correlation metrics, with an optional LLM judge
     for a human-readable stability verdict.
"""

import itertools
import json
import os
from statistics import mean
from typing import Any

import pandas as pd
from langchain_core.tools import tool


def _as_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [x.strip() for x in value.split(",") if x.strip()]
    return [str(x) for x in value if str(x).strip()]


def _safe_float(value, default=None):
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def _jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    union = a | b
    return len(a & b) / len(union) if union else 1.0


def _mean_or_none(vals: list[float | None]):
    vals = [v for v in vals if v is not None]
    return round(mean(vals), 4) if vals else None


def _read_deg(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, index_col=0)
    required = {"log2FoldChange"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path} missing required DEG columns: {sorted(missing)}")
    df.index = df.index.astype(str)
    df["log2FoldChange"] = pd.to_numeric(df["log2FoldChange"], errors="coerce")
    if "padj" in df.columns:
        df["padj"] = pd.to_numeric(df["padj"], errors="coerce")
    if "pvalue" in df.columns:
        df["pvalue"] = pd.to_numeric(df["pvalue"], errors="coerce")
    return df


def _deg_top_set(df: pd.DataFrame, top_n: int) -> set[str]:
    work = df.copy()
    if "padj" in work.columns:
        work["_rank"] = work["padj"].fillna(1.0)
        work = work.sort_values(["_rank", "pvalue" if "pvalue" in work.columns else "_rank"])
    elif "pvalue" in work.columns:
        work["_rank"] = work["pvalue"].fillna(1.0)
        work = work.sort_values("_rank")
    else:
        work["_rank"] = work["log2FoldChange"].abs()
        work = work.sort_values("_rank", ascending=False)
    return set(work.head(top_n).index.astype(str))


def _deg_sig_set(df: pd.DataFrame, padj_cutoff: float, log2fc_cutoff: float) -> set[str]:
    if "padj" not in df.columns:
        return set()
    sig = df[(df["padj"] < padj_cutoff) & (df["log2FoldChange"].abs() >= log2fc_cutoff)]
    return set(sig.index.astype(str))


def compare_deg_result_files(
    deg_csvs: list[str],
    top_n: int = 50,
    padj_cutoff: float = 0.05,
    log2fc_cutoff: float = 1.0,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Pairwise stability metrics over repeated DEG CSVs."""
    paths = _as_list(deg_csvs)
    if len(paths) < 2:
        raise ValueError("Need at least two DEG CSV files for stability evaluation.")
    dfs = {p: _read_deg(p) for p in paths}
    rows = []
    for a, b in itertools.combinations(paths, 2):
        da, db = dfs[a], dfs[b]
        common = da.index.intersection(db.index)
        corr = None
        direction_agreement = None
        if len(common) >= 3:
            joined = pd.DataFrame({
                "a": da.loc[common, "log2FoldChange"],
                "b": db.loc[common, "log2FoldChange"],
            }).dropna()
            if len(joined) >= 3:
                corr = _safe_float(joined["a"].corr(joined["b"]))
                nonzero = joined[(joined["a"] != 0) & (joined["b"] != 0)]
                if len(nonzero):
                    direction_agreement = float((nonzero["a"].gt(0) == nonzero["b"].gt(0)).mean())
        top_a, top_b = _deg_top_set(da, top_n), _deg_top_set(db, top_n)
        sig_a = _deg_sig_set(da, padj_cutoff, log2fc_cutoff)
        sig_b = _deg_sig_set(db, padj_cutoff, log2fc_cutoff)
        rows.append({
            "run_a": os.path.basename(a),
            "run_b": os.path.basename(b),
            "n_common_genes": int(len(common)),
            "log2fc_pearson": None if corr is None else round(corr, 4),
            "direction_agreement": None if direction_agreement is None else round(direction_agreement, 4),
            f"top{top_n}_jaccard": round(_jaccard(top_a, top_b), 4),
            "sig_deg_jaccard": round(_jaccard(sig_a, sig_b), 4),
            "n_sig_a": len(sig_a),
            "n_sig_b": len(sig_b),
        })
    pairwise = pd.DataFrame(rows)
    summary = {
        "n_runs": len(paths),
        "top_n": top_n,
        "padj_cutoff": padj_cutoff,
        "log2fc_cutoff": log2fc_cutoff,
        "mean_log2fc_pearson": _mean_or_none(pairwise["log2fc_pearson"].tolist()),
        "mean_direction_agreement": _mean_or_none(pairwise["direction_agreement"].tolist()),
        f"mean_top{top_n}_jaccard": _mean_or_none(pairwise[f"top{top_n}_jaccard"].tolist()),
        "mean_sig_deg_jaccard": _mean_or_none(pairwise["sig_deg_jaccard"].tolist()),
        "min_sig_deg_jaccard": _safe_float(pairwise["sig_deg_jaccard"].min()),
        "mean_n_sig": round(mean([len(_deg_sig_set(df, padj_cutoff, log2fc_cutoff)) for df in dfs.values()]), 2),
    }
    return pairwise, summary


def _read_gsea(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    term_col = "Term" if "Term" in df.columns else "Name" if "Name" in df.columns else None
    if term_col is None:
        raise ValueError(f"{path} missing GSEA term column ('Term' or 'Name').")
    if "NES" not in df.columns:
        raise ValueError(f"{path} missing required GSEA column: NES")
    fdr_col = "FDR q-val" if "FDR q-val" in df.columns else "FDR" if "FDR" in df.columns else None
    df = df.rename(columns={term_col: "Term"})
    if fdr_col:
        df = df.rename(columns={fdr_col: "FDR q-val"})
        df["FDR q-val"] = pd.to_numeric(df["FDR q-val"], errors="coerce")
    df["NES"] = pd.to_numeric(df["NES"], errors="coerce")
    df["Term"] = df["Term"].astype(str)
    return df.dropna(subset=["Term", "NES"])


def _gsea_top_set(df: pd.DataFrame, top_n: int) -> set[str]:
    work = df.copy()
    if "FDR q-val" in work.columns:
        work["_rank"] = work["FDR q-val"].fillna(1.0)
        work = work.sort_values(["_rank", "NES"], ascending=[True, False])
    else:
        work["_rank"] = work["NES"].abs()
        work = work.sort_values("_rank", ascending=False)
    return set(work.head(top_n)["Term"])


def _gsea_sig_set(df: pd.DataFrame, fdr_cutoff: float) -> set[str]:
    if "FDR q-val" not in df.columns:
        return set()
    return set(df.loc[df["FDR q-val"] < fdr_cutoff, "Term"].astype(str))


def compare_gsea_result_files(
    gsea_csvs: list[str],
    top_n: int = 20,
    fdr_cutoff: float = 0.25,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Pairwise stability metrics over repeated GSEA CSVs."""
    paths = _as_list(gsea_csvs)
    if len(paths) < 2:
        raise ValueError("Need at least two GSEA CSV files for stability evaluation.")
    dfs = {p: _read_gsea(p) for p in paths}
    rows = []
    for a, b in itertools.combinations(paths, 2):
        da, db = dfs[a].set_index("Term"), dfs[b].set_index("Term")
        common = da.index.intersection(db.index)
        corr = None
        if len(common) >= 3:
            joined = pd.DataFrame({"a": da.loc[common, "NES"], "b": db.loc[common, "NES"]}).dropna()
            if len(joined) >= 3:
                corr = _safe_float(joined["a"].corr(joined["b"]))
        top_a, top_b = _gsea_top_set(dfs[a], top_n), _gsea_top_set(dfs[b], top_n)
        sig_a, sig_b = _gsea_sig_set(dfs[a], fdr_cutoff), _gsea_sig_set(dfs[b], fdr_cutoff)
        rows.append({
            "run_a": os.path.basename(a),
            "run_b": os.path.basename(b),
            "n_common_terms": int(len(common)),
            "nes_pearson": None if corr is None else round(corr, 4),
            f"top{top_n}_pathway_jaccard": round(_jaccard(top_a, top_b), 4),
            "sig_pathway_jaccard": round(_jaccard(sig_a, sig_b), 4),
            "n_sig_a": len(sig_a),
            "n_sig_b": len(sig_b),
        })
    pairwise = pd.DataFrame(rows)
    summary = {
        "n_runs": len(paths),
        "top_n": top_n,
        "fdr_cutoff": fdr_cutoff,
        "mean_nes_pearson": _mean_or_none(pairwise["nes_pearson"].tolist()),
        f"mean_top{top_n}_pathway_jaccard": _mean_or_none(pairwise[f"top{top_n}_pathway_jaccard"].tolist()),
        "mean_sig_pathway_jaccard": _mean_or_none(pairwise["sig_pathway_jaccard"].tolist()),
        "min_sig_pathway_jaccard": _safe_float(pairwise["sig_pathway_jaccard"].min()),
        "mean_n_sig": round(mean([len(_gsea_sig_set(df, fdr_cutoff)) for df in dfs.values()]), 2),
    }
    return pairwise, summary


def _heuristic_verdict(summary: dict[str, Any]) -> dict[str, str]:
    deg = summary.get("deg") or {}
    gsea = summary.get("gsea") or {}
    score_parts = []
    if deg.get("mean_log2fc_pearson") is not None:
        score_parts.append(float(deg["mean_log2fc_pearson"]))
    for key in ("mean_sig_deg_jaccard",):
        if deg.get(key) is not None:
            score_parts.append(float(deg[key]))
    if gsea.get("mean_nes_pearson") is not None:
        score_parts.append(float(gsea["mean_nes_pearson"]))
    if gsea.get("mean_sig_pathway_jaccard") is not None:
        score_parts.append(float(gsea["mean_sig_pathway_jaccard"]))
    score = mean(score_parts) if score_parts else 0.0
    if score >= 0.80:
        label = "stable"
    elif score >= 0.55:
        label = "mixed"
    else:
        label = "unstable"
    return {
        "verdict": label,
        "reasoning": (
            f"Heuristic stability score={score:.2f}. Prioritize log2FC/NES correlations for ranking "
            "stability and Jaccard overlap for threshold-sensitive significant calls."
        ),
    }


def evaluate_repeated_results_core(
    deg_csvs=None,
    gsea_csvs=None,
    output_dir: str = "./output/evaluation",
    label: str = "stability",
    top_genes: int = 50,
    top_pathways: int = 20,
    padj_cutoff: float = 0.05,
    log2fc_cutoff: float = 1.0,
    gsea_fdr_cutoff: float = 0.25,
    use_llm_judge: bool = False,
) -> dict[str, Any]:
    os.makedirs(output_dir, exist_ok=True)
    summary: dict[str, Any] = {"label": label, "deg": None, "gsea": None, "judge": None}
    artifacts = {}

    deg_paths = _as_list(deg_csvs)
    if len(deg_paths) >= 2:
        deg_pairwise, deg_summary = compare_deg_result_files(
            deg_paths, top_n=top_genes, padj_cutoff=padj_cutoff, log2fc_cutoff=log2fc_cutoff)
        deg_out = os.path.join(output_dir, f"{label}_deg_pairwise.csv")
        deg_pairwise.to_csv(deg_out, index=False)
        summary["deg"] = deg_summary
        artifacts["deg_pairwise_csv"] = deg_out

    gsea_paths = _as_list(gsea_csvs)
    if len(gsea_paths) >= 2:
        gsea_pairwise, gsea_summary = compare_gsea_result_files(
            gsea_paths, top_n=top_pathways, fdr_cutoff=gsea_fdr_cutoff)
        gsea_out = os.path.join(output_dir, f"{label}_gsea_pairwise.csv")
        gsea_pairwise.to_csv(gsea_out, index=False)
        summary["gsea"] = gsea_summary
        artifacts["gsea_pairwise_csv"] = gsea_out

    if summary["deg"] is None and summary["gsea"] is None:
        raise ValueError("Provide at least two DEG CSVs or at least two GSEA CSVs.")

    if use_llm_judge:
        try:
            from tools.llm_helpers import judge_evaluation_with_llm
            judge = judge_evaluation_with_llm(summary)
            summary["judge"] = judge.model_dump() if judge is not None else _heuristic_verdict(summary)
        except Exception as e:
            summary["judge"] = {"verdict": "judge_failed", "reasoning": f"{type(e).__name__}: {e}"}
    else:
        summary["judge"] = _heuristic_verdict(summary)

    summary["artifacts"] = artifacts
    summary_path = os.path.join(output_dir, f"{label}_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    summary["artifacts"]["summary_json"] = summary_path
    return summary


@tool
def evaluate_repeated_subset_results(
    deg_csvs: list[str] | str = "",
    gsea_csvs: list[str] | str = "",
    output_dir: str = "./output/evaluation",
    label: str = "stability",
    top_genes: int = 50,
    top_pathways: int = 20,
    padj_cutoff: float = 0.05,
    log2fc_cutoff: float = 1.0,
    gsea_fdr_cutoff: float = 0.25,
    use_llm_judge: bool = False,
) -> str:
    """Evaluate whether repeated subset/rerun outputs tell the same biological story.

    Pass two or more DEG CSVs and/or two or more GSEA CSVs from repeated subset runs
    of the same study/contrast. The tool writes pairwise metric CSVs plus a summary JSON.
    If use_llm_judge=True and CLAUDE_API_KEY is configured, a separate structured LLM judge
    interprets the metrics; otherwise a deterministic heuristic verdict is used.
    """
    try:
        summary = evaluate_repeated_results_core(
            deg_csvs=deg_csvs,
            gsea_csvs=gsea_csvs,
            output_dir=output_dir,
            label=label,
            top_genes=top_genes,
            top_pathways=top_pathways,
            padj_cutoff=padj_cutoff,
            log2fc_cutoff=log2fc_cutoff,
            gsea_fdr_cutoff=gsea_fdr_cutoff,
            use_llm_judge=use_llm_judge,
        )
        lines = [f"Evaluation complete: {label}", f"Verdict: {summary['judge']['verdict']}"]
        if summary.get("deg"):
            deg = summary["deg"]
            lines.append(
                f"DEG: mean log2FC r={deg.get('mean_log2fc_pearson')}, "
                f"mean significant-gene Jaccard={deg.get('mean_sig_deg_jaccard')}"
            )
        if summary.get("gsea"):
            gsea = summary["gsea"]
            lines.append(
                f"GSEA: mean NES r={gsea.get('mean_nes_pearson')}, "
                f"mean significant-pathway Jaccard={gsea.get('mean_sig_pathway_jaccard')}"
            )
        lines.append(f"Reasoning: {summary['judge']['reasoning']}")
        lines.append("Artifacts:")
        for name, path in summary["artifacts"].items():
            lines.append(f"- {name}: {path}")
        return "\n".join(lines)
    except Exception as e:
        return f"Evaluation failed. Error: {type(e).__name__}: {e}"
