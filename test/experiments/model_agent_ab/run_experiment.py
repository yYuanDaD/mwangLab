"""Paired Sonnet 4.6 vs DeepSeek V4 Pro scientific-routing A/B.

All tools are deterministic local stubs. The experiment isolates model-driven
tool selection, argument construction, stopping behavior, latency, and cost;
it deliberately does not claim end-to-end biological result validity.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import statistics
import sys
import time
from typing import Any

from langchain.agents import create_agent
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.model_factory import create_chat_model, resolve_model_config  # noqa: E402
from tools.run_status import RunStatusTracker  # noqa: E402


PRICES = {
    "anthropic": {"cache_hit": 0.30, "cache_miss": 3.00, "output": 15.00},
    "deepseek": {"cache_hit": 0.003625, "cache_miss": 0.435, "output": 0.87},
}

ROUTING_SYSTEM = """You are a bioinformatics workflow agent. Follow these safety rules.
- Raw integer bulk RNA-seq counts: run_deseq2_analysis.
- Already log-transformed bulk expression such as log2(FPKM+1): run_limma_analysis, never DESeq2.
- Single-cell matrices: run_scrna_pseudobulk_da; cells are not biological replicates.
- DNA methylation beta values: run_methylation_da, never RNA-seq tools.
- Metadata-only requests: inspect_metadata only; do not add QC, PCA, or DA.
- Repeated DEG/GSEA result comparison: evaluate_repeated_subset_results.
- If no defensible two-arm contrast exists, do not call a DA tool. State that manual review is required.
Call exactly the tool requested by these rules, once, with literal user-supplied arguments. After its
result, give one short grounded final answer and stop. Do not invent files, groups, or analyses.
"""


@tool("run_deseq2_analysis")
def deseq2_stub(counts_csv: str, metadata_csv: str, design_column: str,
                control_group: str, treatment_group: str) -> str:
    """Run DESeq2 only on a raw integer bulk RNA-seq count matrix."""
    return json.dumps({"status": "ok", "method": "deseq2", "artifact": "DEG_results.csv"})


@tool("run_limma_analysis")
def limma_stub(expression_csv: str, metadata_csv: str, design_column: str,
               control_group: str, treatment_group: str) -> str:
    """Run limma on already log-scale bulk expression or proteomics values."""
    return json.dumps({"status": "ok", "method": "limma", "artifact": "DEG_results.csv"})


@tool("run_scrna_pseudobulk_da")
def scrna_stub(matrix_path: str, sample_col: str, celltype_col: str, condition_col: str,
               control_group: str, treatment_group: str) -> str:
    """Aggregate single cells by biological sample and cell type, then run pseudobulk DA."""
    return json.dumps({"status": "ok", "method": "pseudobulk", "artifact": "scrna_summary.csv"})


@tool("run_methylation_da")
def methylation_stub(beta_matrix: str, metadata_csv: str, design_column: str,
                     control_group: str, treatment_group: str) -> str:
    """Convert methylation beta values to M-values and run methylation limma."""
    return json.dumps({"status": "ok", "method": "methylation_limma", "artifact": "DMC.csv"})


@tool("inspect_metadata")
def inspect_metadata_stub(metadata_csv: str) -> str:
    """Inspect metadata columns and group values without running expression analysis."""
    return json.dumps({"status": "ok", "columns": ["condition", "sex"]})


@tool("evaluate_repeated_subset_results")
def evaluate_stub(deg_csvs: list[str], gsea_csvs: list[str]) -> str:
    """Compare repeated DEG/GSEA files for rank, direction, and overlap stability."""
    return json.dumps({"status": "ok", "deg_spearman": 0.96, "direction_agreement": 0.94})


TOOLS = [deseq2_stub, limma_stub, scrna_stub, methylation_stub,
         inspect_metadata_stub, evaluate_stub]

CASES = [
    {
        "id": "raw_counts",
        "query": ("Analyze raw integer bulk RNA-seq counts counts.csv with meta.csv. "
                  "Use condition, control=sedentary, treatment=exercise."),
        "expected_tool": "run_deseq2_analysis",
        "expected_args": {"counts_csv": "counts.csv", "metadata_csv": "meta.csv",
                          "design_column": "condition", "control_group": "sedentary",
                          "treatment_group": "exercise"},
    },
    {
        "id": "log_fpkm",
        "query": ("Analyze already log2(FPKM+1) bulk expression log_fpkm.csv with meta.csv. "
                  "Use group, control=vehicle, treatment=training."),
        "expected_tool": "run_limma_analysis",
        "expected_args": {"expression_csv": "log_fpkm.csv", "metadata_csv": "meta.csv",
                          "design_column": "group", "control_group": "vehicle",
                          "treatment_group": "training"},
    },
    {
        "id": "single_cell",
        "query": ("Run differential analysis for single-cell matrix cells.h5ad. Columns are donor_id, "
                  "cell_type, and condition; compare ctrl to exercise."),
        "expected_tool": "run_scrna_pseudobulk_da",
        "expected_args": {"matrix_path": "cells.h5ad", "sample_col": "donor_id",
                          "celltype_col": "cell_type", "condition_col": "condition",
                          "control_group": "ctrl", "treatment_group": "exercise"},
    },
    {
        "id": "methylation",
        "query": ("Analyze DNA methylation beta values beta.csv with meta.csv using condition; "
                  "compare baseline to trained."),
        "expected_tool": "run_methylation_da",
        "expected_args": {"beta_matrix": "beta.csv", "metadata_csv": "meta.csv",
                          "design_column": "condition", "control_group": "baseline",
                          "treatment_group": "trained"},
    },
    {
        "id": "metadata_only",
        "query": "Inspect metadata.csv only. Do not run preprocessing, QC, PCA, or differential analysis.",
        "expected_tool": "inspect_metadata",
        "expected_args": {"metadata_csv": "metadata.csv"},
    },
    {
        "id": "unsafe_multifactor",
        "query": ("The metadata has genotype x tissue x time with every sample in a unique combination "
                  "and no replicated two-arm contrast. Decide whether to run DA now. There is no file to inspect."),
        "expected_tool": None,
        "expected_args": {},
    },
    {
        "id": "repeated_results",
        "query": ("Evaluate stability across DEG files a.csv and b.csv and GSEA files ga.csv and gb.csv. "
                  "Do not rerun DA."),
        "expected_tool": "evaluate_repeated_subset_results",
        "expected_args": {"deg_csvs": ["a.csv", "b.csv"], "gsea_csvs": ["ga.csv", "gb.csv"]},
    },
]


def _content_text(message) -> str:
    content = getattr(message, "content", "")
    if isinstance(content, str):
        return content
    return "\n".join(
        str(block.get("text", "")) for block in (content or [])
        if isinstance(block, dict) and block.get("type") == "text"
    )


def _usage(message) -> dict[str, int]:
    metadata = getattr(message, "usage_metadata", None) or {}
    raw = (getattr(message, "response_metadata", None) or {}).get("usage", {}) or {}
    input_tokens = int(metadata.get("input_tokens") or raw.get("input_tokens") or 0)
    output_tokens = int(metadata.get("output_tokens") or raw.get("output_tokens") or 0)
    details = metadata.get("input_token_details") or {}
    cache_hit = int(details.get("cache_read") or raw.get("cache_read_input_tokens")
                    or raw.get("prompt_cache_hit_tokens") or 0)
    cache_miss = int(raw.get("prompt_cache_miss_tokens") or max(0, input_tokens - cache_hit))
    return {"input_tokens": input_tokens, "output_tokens": output_tokens,
            "cache_hit_input_tokens": cache_hit, "cache_miss_input_tokens": cache_miss}


def _cost(provider: str, usage: dict[str, int]) -> float:
    price = PRICES[provider]
    return round((usage["cache_hit_input_tokens"] * price["cache_hit"]
                  + usage["cache_miss_input_tokens"] * price["cache_miss"]
                  + usage["output_tokens"] * price["output"]) / 1_000_000, 8)


def _args_match(actual: dict, expected: dict) -> bool:
    return all(actual.get(key) == value for key, value in expected.items())


def _run_case(agent, provider: str, case: dict, repeat: int) -> dict:
    started = time.perf_counter()
    try:
        result = agent.invoke({"messages": [("user", case["query"])]},
                              config={"recursion_limit": 8})
        elapsed = round(time.perf_counter() - started, 3)
        messages = list(result.get("messages", []))
        calls, tool_messages = [], 0
        usage = {key: 0 for key in ("input_tokens", "output_tokens",
                                     "cache_hit_input_tokens", "cache_miss_input_tokens")}
        llm_calls = 0
        for message in messages:
            item_usage = _usage(message)
            if item_usage["input_tokens"] or item_usage["output_tokens"]:
                llm_calls += 1
                for key in usage:
                    usage[key] += item_usage[key]
            calls.extend(list(getattr(message, "tool_calls", None) or []))
            tool_messages += int(isinstance(message, ToolMessage))
        expected_tool = case["expected_tool"]
        if expected_tool is None:
            selection_ok = len(calls) == 0
            args_ok = True
        else:
            selection_ok = len(calls) == 1 and calls[0].get("name") == expected_tool
            args_ok = selection_ok and _args_match(calls[0].get("args", {}), case["expected_args"])
        no_duplicates = len(calls) <= (0 if expected_tool is None else 1)
        final_text = _content_text(messages[-1]).strip() if messages else ""
        completed = bool(final_text) and not list(getattr(messages[-1], "tool_calls", None) or [])
        score = 45 * selection_ok + 25 * args_ok + 15 * no_duplicates + 15 * completed
        blocking = []
        if not selection_ok:
            blocking.append("wrong_or_missing_tool")
        if not args_ok:
            blocking.append("incorrect_arguments")
        if not no_duplicates:
            blocking.append("duplicate_tool_calls")
        return {
            "case": case["id"], "repeat": repeat, "provider": provider,
            "score": float(score), "passed": score == 100, "blocking": blocking,
            "tool_calls": calls, "tool_messages": tool_messages, "llm_calls": llm_calls,
            "final_text": final_text[:500], "elapsed_seconds": elapsed,
            "usage": usage, "estimated_cost_usd": _cost(provider, usage),
        }
    except Exception as exc:
        return {
            "case": case["id"], "repeat": repeat, "provider": provider,
            "score": 0.0, "passed": False, "blocking": ["execution_error"],
            "error": f"{type(exc).__name__}: {exc}",
            "elapsed_seconds": round(time.perf_counter() - started, 3),
            "usage": {"input_tokens": 0, "output_tokens": 0,
                      "cache_hit_input_tokens": 0, "cache_miss_input_tokens": 0},
            "estimated_cost_usd": 0.0, "llm_calls": 0,
        }


def _aggregate(records: list[dict], provider: str) -> dict:
    subset = [row for row in records if row["provider"] == provider]
    passed = sum(bool(row["passed"]) for row in subset)
    total_cost = sum(float(row["estimated_cost_usd"]) for row in subset)
    return {
        "runs": len(subset),
        "mean_score": round(statistics.mean(row["score"] for row in subset), 2),
        "pass_rate": round(passed / len(subset), 4),
        "blocking_runs": sum(bool(row["blocking"]) for row in subset),
        "duplicate_call_runs": sum("duplicate_tool_calls" in row["blocking"] for row in subset),
        "median_latency_seconds": round(statistics.median(row["elapsed_seconds"] for row in subset), 3),
        "total_cost_usd": round(total_cost, 6),
        "cost_per_pass_usd": round(total_cost / passed, 6) if passed else None,
        "llm_calls": sum(int(row["llm_calls"]) for row in subset),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--output-dir", default="")
    args = parser.parse_args()
    if args.repeats < 3:
        raise SystemExit("--repeats must be >= 3 for an LLM-dependent A/B")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = Path(args.output_dir) if args.output_dir else ROOT / "output" / f"model_agent_ab_{stamp}"
    out.mkdir(parents=True, exist_ok=True)
    tracker = RunStatusTracker(str(out / "run_status.json"), run_id=out.name,
                               profile="paired_model_agent_ab", stages=["execute", "score", "report"])
    tracker.start("paired scientific-routing model A/B")
    configs = {
        "anthropic": resolve_model_config(provider="anthropic", model="claude-sonnet-4-6"),
        "deepseek": resolve_model_config(provider="deepseek", model="deepseek-v4-pro", effort="max"),
    }
    agents = {
        name: create_agent(model=create_chat_model(config), tools=TOOLS, system_prompt=ROUTING_SYSTEM)
        for name, config in configs.items()
    }
    records = []
    tracker.set_stage("execute", message=f"{len(CASES)} cases x {args.repeats} repeats x 2 models")
    for repeat in range(1, args.repeats + 1):
        for case_index, case in enumerate(CASES):
            order = ("deepseek", "anthropic") if (repeat + case_index) % 2 else ("anthropic", "deepseek")
            for provider in order:
                records.append(_run_case(agents[provider], provider, case, repeat))

    tracker.set_stage("score", message="deterministic paired scoring")
    aggregate = {provider: _aggregate(records, provider) for provider in configs}
    sonnet, deepseek = aggregate["anthropic"], aggregate["deepseek"]
    cost_ratio = (
        deepseek["cost_per_pass_usd"] / sonnet["cost_per_pass_usd"]
        if deepseek["cost_per_pass_usd"] is not None and sonnet["cost_per_pass_usd"] else None
    )
    deepseek_noninferior = deepseek["mean_score"] >= sonnet["mean_score"] - 3
    safety_pass = deepseek["blocking_runs"] == 0 and deepseek["duplicate_call_runs"] == 0
    cost_pass = cost_ratio is not None and cost_ratio <= 0.30
    verdict = "accept_pilot" if deepseek_noninferior and safety_pass and cost_pass else "reject_pilot"
    coverage = 100.0 if len(records) == len(CASES) * args.repeats * 2 else 0.0
    report = {
        "schema_version": "1.0",
        "evaluation_unit": "paired scientific tool-routing run",
        "verdict": verdict,
        "score": {provider: aggregate[provider]["mean_score"] for provider in aggregate},
        "coverage": coverage,
        "blocking_findings": sorted({
            f"{row['provider']}:{row['case']}:r{row['repeat']}:{item}"
            for row in records for item in row["blocking"]
        }),
        "conditions": {name: {"model": cfg.model, "effort": cfg.effort}
                       for name, cfg in configs.items()},
        "temperature_note": ("Sonnet uses temperature=0; DeepSeek thinking mode documents temperature "
                             "as ignored, so paired repeats measure its observed variance."),
        "case_count": len(CASES), "repeats": args.repeats,
        "aggregate": aggregate,
        "cost_ratio_deepseek_vs_sonnet": round(cost_ratio, 4) if cost_ratio is not None else None,
        "acceptance": {"quality_noninferior_within_3_points": deepseek_noninferior,
                       "deepseek_safety_and_loop_gate": safety_pass,
                       "cost_per_pass_at_most_30_percent": cost_pass},
        "records": records,
        "provenance": {
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "routing_system_sha256": hashlib.sha256(ROUTING_SYSTEM.encode()).hexdigest(),
            "cases_sha256": hashlib.sha256(json.dumps(CASES, sort_keys=True).encode()).hexdigest(),
        },
        "unmeasured_checks": [
            "real GEO/network execution", "DEG/GSEA biological result stability",
            "sample-alignment semantic fallback", "SEA-CDM full extraction and FK integrity",
        ],
    }
    (out / "model_agent_ab.json").write_text(json.dumps(report, indent=2, ensure_ascii=False),
                                              encoding="utf-8")
    lines = ["# Paired model agent A/B", "", f"- Verdict: **{verdict}**",
             f"- Coverage: **{coverage}%**", f"- Cases/repeats: **{len(CASES)} / {args.repeats}**", "",
             "| Metric | Sonnet 4.6 | DeepSeek V4 Pro |", "|---|---:|---:|",
             f"| Mean score | {sonnet['mean_score']} | {deepseek['mean_score']} |",
             f"| Pass rate | {sonnet['pass_rate']:.1%} | {deepseek['pass_rate']:.1%} |",
             f"| Blocking runs | {sonnet['blocking_runs']} | {deepseek['blocking_runs']} |",
             f"| Duplicate-call runs | {sonnet['duplicate_call_runs']} | {deepseek['duplicate_call_runs']} |",
             f"| Median latency (s) | {sonnet['median_latency_seconds']} | {deepseek['median_latency_seconds']} |",
             f"| Total cost (USD) | {sonnet['total_cost_usd']:.6f} | {deepseek['total_cost_usd']:.6f} |",
             f"| Cost/pass (USD) | {sonnet['cost_per_pass_usd']} | {deepseek['cost_per_pass_usd']} |", "",
             "## Unmeasured checks", ""]
    lines.extend(f"- {item}" for item in report["unmeasured_checks"])
    (out / "model_agent_ab.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    tracker.set_stage("report", message=verdict)
    tracker.set_usage(llm_calls=sum(row["llm_calls"] for row in records),
                      estimated_cost_usd=sum(row["estimated_cost_usd"] for row in records))
    for finding in report["blocking_findings"]:
        tracker.add_failure(finding)
    tracker.finish("completed", verdict)
    print(json.dumps({"verdict": verdict, "coverage": coverage, "aggregate": aggregate,
                      "cost_ratio": report["cost_ratio_deepseek_vs_sonnet"], "output_dir": str(out)},
                     indent=2, ensure_ascii=False))
    return 0 if verdict == "accept_pilot" else 1


if __name__ == "__main__":
    raise SystemExit(main())
