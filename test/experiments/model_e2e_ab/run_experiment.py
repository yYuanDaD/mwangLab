"""Paired end-to-end model A/B on cached GEO expression matrices.

The model selects and calls the real DESeq2/limma tools. Inputs are frozen local
files, outputs are isolated per provider/case/repeat, and all scientific gates
are deterministic. Network-dependent enrichment is intentionally excluded.
"""

from __future__ import annotations

import argparse
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime
import io
import json
import os
from pathlib import Path
import statistics
import sys
import time
from typing import Any

from langchain.agents import create_agent
from langchain_core.messages import ToolMessage
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from main import system_prompt  # noqa: E402
from tools.batch_tools import _classify_matrix, _deg_sanity_flags  # noqa: E402
from tools.deseq2_tools import deg_filename, run_deseq2_analysis  # noqa: E402
from tools.evaluation_tools import compare_deg_result_files  # noqa: E402
from tools.evidence import EvidenceRecorder, file_sha256  # noqa: E402
from tools.limma_tools import run_limma_analysis  # noqa: E402
from tools.model_factory import create_chat_model, resolve_model_config  # noqa: E402
from tools.run_status import RunStatusTracker  # noqa: E402
from tools.sample_align import align_samples  # noqa: E402


PRICES = {
    "anthropic": {"cache_hit": 0.30, "cache_miss": 3.00, "output": 15.00},
    "deepseek": {"cache_hit": 0.003625, "cache_miss": 0.435, "output": 0.87},
}

CASES = [
    {
        "id": "GSE279359_raw",
        "accession": "GSE279359",
        "matrix": "data/GSE279359/GSE279359_processed_counts.txt.gz",
        "metadata": "data/GSE279359/GSE279359_metadata.csv",
        "matrix_type": "raw_counts",
        "tool": "run_deseq2_analysis",
        "method": "deseq2",
        "matrix_arg": "counts_csv",
        "design_column": "characteristics_ch1.1.time",
        "control": "pre-exercise",
        "treatment": "immediately post-exercise",
        "expected_samples": 10,
        "description": "raw integer counts; acute exercise immediately post vs pre",
    },
    {
        "id": "GSE208615_log_fpkm",
        "accession": "GSE208615",
        "matrix": "data/GSE208615/GSE208615_fpkm_log2.csv",
        "metadata": "data/GSE208615/GSE208615_metadata.csv",
        "matrix_type": "log_transformed",
        "tool": "run_limma_analysis",
        "method": "limma",
        "matrix_arg": "normalized_csv",
        "design_column": "characteristics_ch1.2.exercise parameters",
        "control": "0-0-0",
        "treatment": "14-0-0",
        "expected_samples": 30,
        "description": "already log2(FPKM+1); trained condition vs sedentary baseline",
    },
    {
        "id": "GSE297707_prefix_collision",
        "accession": "GSE297707",
        "matrix": "data/GSE297707/GSE297707_raw_counts.txt.gz",
        "metadata": "data/GSE297707/GSE297707_metadata.csv",
        "matrix_type": "raw_counts",
        "tool": "run_deseq2_analysis",
        "method": "deseq2",
        "matrix_arg": "counts_csv",
        "design_column": "characteristics_ch1.2.treatment",
        "control": "sedentary",
        "treatment": "HIIT",
        "expected_samples": 64,
        "description": "raw counts with Sample_1/Sample_10 prefix-collision alignment",
    },
]

ACTIVE_PROMPT = system_prompt + """

E2E MODEL EVALUATION SCOPE:
Only run_deseq2_analysis and run_limma_analysis are exposed. The user supplies
the exact matrix scale, design, groups, and isolated output directory. Call the
scientifically compatible tool exactly once, preserve every literal argument,
then summarize the real tool result and stop. Do not add QC, enrichment, or
preprocessing.
"""


def _abs(path: str | Path) -> str:
    return str((ROOT / Path(path)).resolve()) if not Path(path).is_absolute() else str(Path(path).resolve())


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


def _same_path(a: Any, b: Any) -> bool:
    try:
        return Path(str(a)).resolve() == Path(str(b)).resolve()
    except Exception:
        return False


def _arguments_match(actual: dict, expected: dict, path_keys: set[str]) -> bool:
    for key, expected_value in expected.items():
        actual_value = actual.get(key)
        if key in path_keys:
            if not _same_path(actual_value, expected_value):
                return False
        elif actual_value != expected_value:
            return False
    return True


def _independent_alignment(case: dict) -> dict:
    matrix = pd.read_csv(_abs(case["matrix"]), index_col=0, sep=None, engine="python", nrows=2)
    metadata = pd.read_csv(_abs(case["metadata"]), index_col=0)
    columns = matrix.columns.astype(str).tolist()
    exact = len(set(columns) & set(metadata.index.astype(str)))
    if exact >= max(1, (min(len(columns), len(metadata)) + 1) // 2):
        aligned = metadata
        method = f"exact ({exact}/{len(columns)})"
    else:
        mapping, method = align_samples(columns, metadata)
        aligned = metadata.rename(index=mapping)
        aligned = aligned[~aligned.index.duplicated(keep="first")]
    common = [sample for sample in columns if sample in aligned.index]
    selected = aligned.loc[common]
    selected = selected[selected[case["design_column"]].astype(str).isin(
        [case["control"], case["treatment"]]
    )]
    counts = selected[case["design_column"]].astype(str).value_counts().to_dict()
    return {"method": method, "matrix_samples": len(columns), "aligned_samples": len(common),
            "selected_samples": len(selected), "group_counts": counts}


def _matrix_type(path: str) -> str:
    result = _classify_matrix(path)
    return result[0] if isinstance(result, tuple) else str(result)


def _run_one(agent, provider: str, case: dict, repeat: int, run_dir: Path) -> dict:
    run_dir.mkdir(parents=True, exist_ok=True)
    matrix = _abs(case["matrix"])
    metadata = _abs(case["metadata"])
    output_dir = str(run_dir.resolve())
    expected_args = {
        case["matrix_arg"]: matrix,
        "metadata_csv": metadata,
        "design_column": case["design_column"],
        "control_group": case["control"],
        "treatment_group": case["treatment"],
        "output_dir": output_dir,
    }
    query = (
        f"Run differential expression only for {case['accession']}. The matrix is {case['description']}. "
        f"Matrix: {matrix}. Metadata: {metadata}. Use design column {case['design_column']!r}, "
        f"control group {case['control']!r}, treatment group {case['treatment']!r}. "
        f"Save into this exact output directory: {output_dir}. Call the compatible DA tool exactly once; "
        "do not run QC, preprocessing, or enrichment."
    )
    os.environ["BIOAGENT_LLM_PROVIDER"] = provider
    os.environ["BIOAGENT_LLM_MODEL"] = (
        "claude-sonnet-4-6" if provider == "anthropic" else "deepseek-v4-pro"
    )
    if provider == "deepseek":
        os.environ["BIOAGENT_LLM_EFFORT"] = "max"
    else:
        os.environ.pop("BIOAGENT_LLM_EFFORT", None)

    captured = io.StringIO()
    started = time.perf_counter()
    error = None
    result = None
    try:
        with redirect_stdout(captured), redirect_stderr(captured):
            result = agent.invoke({"messages": [("user", query)]}, config={"recursion_limit": 8})
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
    elapsed = round(time.perf_counter() - started, 3)
    messages = list((result or {}).get("messages", []))
    calls, tool_results = [], []
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
        if isinstance(message, ToolMessage):
            tool_results.append(_content_text(message))

    selection_ok = len(calls) == 1 and calls[0].get("name") == case["tool"]
    args_ok = bool(selection_ok and _arguments_match(
        calls[0].get("args", {}), expected_args,
        {case["matrix_arg"], "metadata_csv", "output_dir"},
    ))
    no_duplicates = len(calls) == 1
    artifact = run_dir / deg_filename(case["treatment"], case["control"])
    artifact_exists = artifact.is_file()
    schema_ok = False
    n_tested = n_sig = None
    artifact_error = None
    if artifact_exists:
        try:
            deg = pd.read_csv(artifact, index_col=0)
            schema_ok = {"log2FoldChange", "padj", "pvalue"}.issubset(deg.columns)
            n_tested = len(deg)
            if schema_ok:
                padj = pd.to_numeric(deg["padj"], errors="coerce")
                lfc = pd.to_numeric(deg["log2FoldChange"], errors="coerce")
                n_sig = int(((padj < 0.05) & (lfc.abs() > 1)).sum())
        except Exception as exc:
            artifact_error = f"{type(exc).__name__}: {exc}"
    alignment = _independent_alignment(case)
    alignment_ok = (
        alignment["selected_samples"] == case["expected_samples"]
        and min(alignment["group_counts"].get(case["control"], 0),
                alignment["group_counts"].get(case["treatment"], 0)) >= 3
    )
    detected_type = _matrix_type(matrix)
    method_ok = detected_type == case["matrix_type"]
    sanity = _deg_sanity_flags(n_sig, n_tested, metadata, case["design_column"],
                               case["control"], case["treatment"]) if schema_ok else "not_measured"
    sanity_ok = sanity == ""
    tool_failed = error is not None or not tool_results or any(
        marker in "\n".join(tool_results) for marker in
        ("FATAL ERROR", "POLICY BLOCKED", "analysis failed", "Error:")
    )
    final_text = _content_text(messages[-1]).strip() if messages else ""
    completed = bool(final_text) and not list(getattr(messages[-1], "tool_calls", None) or [])

    checks = {
        "correct_tool": selection_ok,
        "correct_arguments": args_ok,
        "no_duplicate_calls": no_duplicates,
        "tool_completed": not tool_failed,
        "artifact_exists": artifact_exists,
        "artifact_schema": schema_ok,
        "matrix_method_compatible": method_ok,
        "sample_alignment_coverage": alignment_ok,
        "deg_sanity": sanity_ok,
        "final_response": completed,
    }
    weights = {"correct_tool": 15, "correct_arguments": 10, "no_duplicate_calls": 10,
               "tool_completed": 10, "artifact_exists": 10, "artifact_schema": 10,
               "matrix_method_compatible": 10, "sample_alignment_coverage": 10,
               "deg_sanity": 10, "final_response": 5}
    score = sum(weights[name] for name, passed in checks.items() if passed)
    blocking_names = {"correct_tool", "correct_arguments", "no_duplicate_calls", "tool_completed",
                      "artifact_exists", "artifact_schema", "matrix_method_compatible",
                      "sample_alignment_coverage", "deg_sanity"}
    blocking = [name for name in blocking_names if not checks[name]]
    record = {
        "case": case["id"], "accession": case["accession"], "repeat": repeat,
        "provider": provider, "model": os.environ["BIOAGENT_LLM_MODEL"],
        "score": score, "passed": score == 100 and not blocking, "blocking": sorted(blocking),
        "checks": checks, "tool_calls": calls, "tool_results": tool_results,
        "llm_calls": llm_calls, "final_text": final_text[:1000], "stdout": captured.getvalue()[-5000:],
        "elapsed_seconds": elapsed, "usage": usage, "estimated_cost_usd": _cost(provider, usage),
        "matrix_type": detected_type, "da_method": case["method"], "alignment": alignment,
        "n_tested": n_tested, "n_deg": n_sig, "deg_sanity": sanity or "ok",
        "artifact": str(artifact.resolve()) if artifact_exists else str(artifact),
        "artifact_sha256": file_sha256(str(artifact)) if artifact_exists else None,
        "artifact_error": artifact_error, "execution_error": error,
    }
    (run_dir / "trace.json").write_text(json.dumps(record, indent=2, ensure_ascii=False),
                                         encoding="utf-8")
    return record


def _aggregate(records: list[dict], provider: str) -> dict:
    rows = [row for row in records if row["provider"] == provider]
    passed = sum(bool(row["passed"]) for row in rows)
    total_cost = sum(float(row["estimated_cost_usd"]) for row in rows)
    return {"runs": len(rows), "mean_score": round(statistics.mean(r["score"] for r in rows), 2),
            "pass_rate": round(passed / len(rows), 4),
            "blocking_runs": sum(bool(r["blocking"]) for r in rows),
            "duplicate_call_runs": sum(not r["checks"]["no_duplicate_calls"] for r in rows),
            "median_latency_seconds": round(statistics.median(r["elapsed_seconds"] for r in rows), 3),
            "total_cost_usd": round(total_cost, 6),
            "cost_per_pass_usd": round(total_cost / passed, 6) if passed else None,
            "llm_calls": sum(r["llm_calls"] for r in rows)}


def _stability(records: list[dict], out: Path) -> dict:
    result = {"within_provider": {}, "cross_provider": {}}
    stability_dir = out / "stability"
    stability_dir.mkdir(exist_ok=True)
    for case in CASES:
        case_id = case["id"]
        result["within_provider"][case_id] = {}
        for provider in ("anthropic", "deepseek"):
            paths = [r["artifact"] for r in records if r["case"] == case_id
                     and r["provider"] == provider and r["checks"]["artifact_schema"]]
            if len(paths) >= 2:
                pairwise, summary = compare_deg_result_files(paths)
                pairwise.to_csv(stability_dir / f"{case_id}_{provider}_pairwise.csv", index=False)
                result["within_provider"][case_id][provider] = summary
        cross_rows = []
        repeats = sorted({r["repeat"] for r in records if r["case"] == case_id})
        for repeat in repeats:
            paths = [r["artifact"] for r in records if r["case"] == case_id
                     and r["repeat"] == repeat and r["checks"]["artifact_schema"]]
            if len(paths) == 2:
                pairwise, summary = compare_deg_result_files(paths)
                row = pairwise.iloc[0].to_dict()
                row["repeat"] = repeat
                cross_rows.append(row)
        if cross_rows:
            frame = pd.DataFrame(cross_rows)
            frame.to_csv(stability_dir / f"{case_id}_cross_provider.csv", index=False)
            result["cross_provider"][case_id] = {
                "mean_log2fc_pearson": round(frame["log2fc_pearson"].mean(), 4),
                "mean_direction_agreement": round(frame["direction_agreement"].mean(), 4),
                "mean_top50_jaccard": round(frame["top50_jaccard"].mean(), 4),
                "mean_sig_deg_jaccard": round(frame["sig_deg_jaccard"].mean(), 4),
            }
    return result


def _write_reproducibility_artifacts(out: Path, report: dict) -> tuple[Path, Path]:
    """Write the generic audit inputs without rerunning any model or DA tool."""
    within = report.get("stability", {}).get("within_provider", {})
    within_ok = bool(within) and all(
        metrics.get("mean_log2fc_pearson", 0) >= 0.99
        and metrics.get("mean_direction_agreement", 0) >= 0.99
        and metrics.get("mean_top50_jaccard", 0) >= 0.95
        for providers in within.values()
        for metrics in providers.values()
    )
    cross_ok = bool(report.get("acceptance", {}).get("cross_provider_deg_stability"))
    stable = within_ok and cross_ok
    evaluation_dir = out / "evaluation"
    evaluation_dir.mkdir(parents=True, exist_ok=True)
    evaluation_path = evaluation_dir / "model_e2e_summary.json"
    evaluation_payload = {
        "schema_version": "1.0",
        "evaluation_unit": report.get("evaluation_unit"),
        "deg": report.get("stability", {}),
        "gsea": {},
        "judge": {
            "verdict": "stable" if stable else "unstable",
            "reason": (
                "All within-provider and paired cross-provider DEG stability thresholds passed."
                if stable else
                "One or more within-provider or cross-provider DEG stability thresholds failed."
            ),
        },
    }
    evaluation_path.write_text(
        json.dumps(evaluation_payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    workflow_path = out / "workflow.log"
    workflow_lines = [
        "Paired cached-GEO end-to-end model A/B",
        f"run_dir={out.resolve()}",
        "runner=test/experiments/model_e2e_ab/run_experiment.py",
        f"evaluation_unit={report.get('evaluation_unit')}",
        f"cases={report.get('case_count')}",
        f"repeats={report.get('repeats')}",
        f"records={len(report.get('records', []))}",
        f"verdict={report.get('verdict')}",
        f"coverage={report.get('coverage')}",
        f"blocking_findings={len(report.get('blocking_findings', []))}",
        "network_steps=disabled; frozen local matrices and metadata only",
        "execution_order=alternated by case and repeat to reduce order bias",
        "stability=within-provider repeats plus paired cross-provider DEG comparison",
        f"stability_summary={evaluation_path.resolve()}",
        f"machine_report={(out / 'model_e2e_ab.json').resolve()}",
        f"summary_csv={(out / 'summary.csv').resolve()}",
        f"run_status={(out / 'run_status.json').resolve()}",
    ]
    workflow_path.write_text("\n".join(workflow_lines) + "\n", encoding="utf-8")
    return workflow_path, evaluation_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--output-dir", default="")
    parser.add_argument(
        "--postprocess-existing",
        default="",
        help="Create generic audit artifacts for an existing completed run without rerunning models.",
    )
    args = parser.parse_args()
    if args.postprocess_existing:
        existing = Path(args.postprocess_existing).resolve()
        report_path = existing / "model_e2e_ab.json"
        if not report_path.is_file():
            raise SystemExit(f"Missing report: {report_path}")
        report = json.loads(report_path.read_text(encoding="utf-8"))
        workflow_path, evaluation_path = _write_reproducibility_artifacts(existing, report)
        print(json.dumps({"workflow_log": str(workflow_path),
                          "evaluation_summary": str(evaluation_path)}, indent=2))
        return 0
    if args.repeats not in {1, 3}:
        raise SystemExit("Use --repeats 1 for preflight or --repeats 3 for the final paired A/B")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = Path(args.output_dir) if args.output_dir else ROOT / "output" / f"model_e2e_ab_{stamp}"
    out.mkdir(parents=True, exist_ok=True)
    tracker = RunStatusTracker(str(out / "run_status.json"), run_id=out.name,
                               profile="paired_model_e2e_ab",
                               stages=["validate_inputs", "execute", "stability", "report"])
    tracker.start("paired cached-GEO end-to-end model A/B")
    tracker.set_stage("validate_inputs", message="hashing and classifying frozen inputs")
    for case in CASES:
        if not Path(_abs(case["matrix"])).is_file() or not Path(_abs(case["metadata"])).is_file():
            tracker.finish("failed", f"missing input for {case['id']}")
            raise SystemExit(f"Missing frozen input for {case['id']}")
        if _matrix_type(_abs(case["matrix"])) != case["matrix_type"]:
            tracker.finish("failed", f"matrix type mismatch for {case['id']}")
            raise SystemExit(f"Matrix type mismatch for {case['id']}")

    configs = {
        "anthropic": resolve_model_config(provider="anthropic", model="claude-sonnet-4-6"),
        "deepseek": resolve_model_config(provider="deepseek", model="deepseek-v4-pro", effort="max"),
    }
    agents = {name: create_agent(model=create_chat_model(config),
                                 tools=[run_deseq2_analysis, run_limma_analysis],
                                 system_prompt=ACTIVE_PROMPT)
              for name, config in configs.items()}
    records = []
    tracker.set_stage("execute", message="3 cases x 3 repeats x 2 models")
    for repeat in range(1, args.repeats + 1):
        for index, case in enumerate(CASES):
            order = ("deepseek", "anthropic") if (repeat + index) % 2 else ("anthropic", "deepseek")
            for provider in order:
                run_dir = out / provider / case["id"] / f"r{repeat}"
                records.append(_run_one(agents[provider], provider, case, repeat, run_dir))

    tracker.set_stage("stability", message="within-provider and cross-provider DEG comparison")
    stability = _stability(records, out)
    aggregate = {provider: _aggregate(records, provider) for provider in configs}
    sonnet, deepseek = aggregate["anthropic"], aggregate["deepseek"]
    cross_ok = bool(stability["cross_provider"]) and all(
        values.get("mean_log2fc_pearson", 0) >= 0.99
        and values.get("mean_direction_agreement", 0) >= 0.99
        and values.get("mean_top50_jaccard", 0) >= 0.95
        for values in stability["cross_provider"].values()
    )
    deepseek_safety = deepseek["blocking_runs"] == 0 and deepseek["duplicate_call_runs"] == 0
    quality_ok = deepseek["mean_score"] >= sonnet["mean_score"] - 3
    ratio = (deepseek["cost_per_pass_usd"] / sonnet["cost_per_pass_usd"]
             if deepseek["cost_per_pass_usd"] is not None and sonnet["cost_per_pass_usd"] else None)
    cost_ok = ratio is not None and ratio <= 0.30
    if args.repeats == 1:
        verdict = "preflight_pass" if all((deepseek_safety, quality_ok, cross_ok)) else "preflight_fail"
    else:
        verdict = ("accept_default_switch" if all((deepseek_safety, quality_ok, cross_ok, cost_ok))
                   else "keep_sonnet_default")
    blocking = sorted({f"{r['provider']}:{r['case']}:r{r['repeat']}:{item}"
                       for r in records for item in r["blocking"]})
    coverage = 100.0 if len(records) == len(CASES) * args.repeats * 2 else 0.0

    summary_rows = []
    for r in records:
        summary_rows.append({"accession": r["accession"], "case": r["case"],
                             "provider": r["provider"], "repeat": r["repeat"],
                             "status": "completed" if r["passed"] else "failed",
                             "n_samples": r["alignment"]["selected_samples"],
                             "matrix_type": r["matrix_type"], "da_method": r["da_method"],
                             "design_col": next(c["design_column"] for c in CASES if c["id"] == r["case"]),
                             "control": next(c["control"] for c in CASES if c["id"] == r["case"]),
                             "treatment": next(c["treatment"] for c in CASES if c["id"] == r["case"]),
                             "n_deg": r["n_deg"], "deg_sanity": r["deg_sanity"],
                             "score": r["score"], "elapsed_seconds": r["elapsed_seconds"],
                             "estimated_cost_usd": r["estimated_cost_usd"],
                             "artifact": r["artifact"], "error": r["execution_error"] or r["artifact_error"] or ""})
    summary_path = out / "summary.csv"
    pd.DataFrame(summary_rows).to_csv(summary_path, index=False)
    report = {"schema_version": "1.0", "evaluation_unit": "paired cached-GEO end-to-end DA run",
              "verdict": verdict, "score": {p: aggregate[p]["mean_score"] for p in aggregate},
              "coverage": coverage, "blocking_findings": blocking, "case_count": len(CASES),
              "repeats": args.repeats, "aggregate": aggregate,
              "cost_ratio_deepseek_vs_sonnet": round(ratio, 4) if ratio is not None else None,
              "stability": stability,
              "acceptance": {"deepseek_safety_and_loop_gate": deepseek_safety,
                             "quality_noninferior_within_3_points": quality_ok,
                             "cross_provider_deg_stability": cross_ok,
                             "cost_per_pass_at_most_30_percent": cost_ok},
              "records": records,
              "unmeasured_checks": ["network-dependent GSEA/ORA", "SEA-CDM paper extraction/FK integrity"]}
    report_path = out / "model_e2e_ab.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    workflow_path, evaluation_path = _write_reproducibility_artifacts(out, report)

    evidence = EvidenceRecorder(out.name, subject_id="sonnet-vs-deepseek-cached-geo")
    source_ids = {}
    for case in CASES:
        for kind in ("matrix", "metadata"):
            path = _abs(case[kind])
            sid = evidence.add_source("metadata" if kind == "metadata" else "artifact",
                                      f"{case['id']} {kind}", uri=path,
                                      attributes={"case": case["id"], "kind": kind})
            evidence.bundle.sources[-1].sha256 = file_sha256(path)
            source_ids[(case["id"], kind)] = sid
    for r in records:
        decision = evidence.add_decision("model_tool_execution", r["tool_calls"],
                                         reason=f"{r['provider']} routed {r['case']} to {r['da_method']}",
                                         method="llm", evidence_ids=[source_ids[(r["case"], "matrix")],
                                                                    source_ids[(r["case"], "metadata")]],
                                         details={"score": r["score"], "checks": r["checks"]})
        if r["checks"]["artifact_exists"]:
            evidence.add_artifact(r["artifact"], "DEG result", produced_by=decision,
                                  evidence_ids=[source_ids[(r["case"], "matrix")],
                                                source_ids[(r["case"], "metadata")]],
                                  attributes={"provider": r["provider"], "repeat": r["repeat"],
                                              "deg_sanity": r["deg_sanity"]})
        trace = out / r["provider"] / r["case"] / f"r{r['repeat']}" / "trace.json"
        evidence.add_artifact(str(trace), "agent trace", produced_by=decision,
                              evidence_ids=[source_ids[(r["case"], "matrix")],
                                            source_ids[(r["case"], "metadata")]])
    evidence.add_claim("DeepSeek V4 Pro", "paired_e2e_verdict", verdict,
                       f"DeepSeek end-to-end paired verdict: {verdict}", method="computation",
                       evidence_ids=[a.artifact_id for a in evidence.bundle.artifacts])
    evidence.add_artifact(str(summary_path), "evaluation summary")
    evidence.add_artifact(str(report_path), "evaluation report")
    evidence.add_artifact(str(workflow_path), "reproducibility workflow log")
    evidence.add_artifact(str(evaluation_path), "repeated-run stability summary")
    evidence.finish("completed" if not blocking else "partial")
    evidence.save(str(out / "evidence.json"))

    lines = ["# Paired cached-GEO end-to-end model A/B", "", f"- Verdict: **{verdict}**",
             f"- Coverage: **{coverage}%**", f"- Blocking findings: **{len(blocking)}**", "",
             "| Metric | Sonnet 4.6 | DeepSeek V4 Pro |", "|---|---:|---:|",
             f"| Mean score | {sonnet['mean_score']} | {deepseek['mean_score']} |",
             f"| Pass rate | {sonnet['pass_rate']:.1%} | {deepseek['pass_rate']:.1%} |",
             f"| Blocking runs | {sonnet['blocking_runs']} | {deepseek['blocking_runs']} |",
             f"| Duplicate-call runs | {sonnet['duplicate_call_runs']} | {deepseek['duplicate_call_runs']} |",
             f"| Median latency (s) | {sonnet['median_latency_seconds']} | {deepseek['median_latency_seconds']} |",
             f"| Total model cost (USD) | {sonnet['total_cost_usd']:.6f} | {deepseek['total_cost_usd']:.6f} |",
             f"| Cost/pass (USD) | {sonnet['cost_per_pass_usd']} | {deepseek['cost_per_pass_usd']} |", "",
             "## Acceptance gates", ""]
    lines.extend(f"- {name}: **{'pass' if value else 'fail'}**" for name, value in report["acceptance"].items())
    lines.extend(["", "## Unmeasured checks", ""])
    lines.extend(f"- {item}" for item in report["unmeasured_checks"])
    (out / "model_e2e_ab.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    tracker.set_stage("report", message=verdict)
    tracker.set_usage(llm_calls=sum(r["llm_calls"] for r in records),
                      estimated_cost_usd=sum(r["estimated_cost_usd"] for r in records))
    for finding in blocking:
        tracker.add_failure(finding)
    tracker.finish("completed", verdict)
    print(json.dumps({"verdict": verdict, "coverage": coverage, "blocking": len(blocking),
                      "aggregate": aggregate, "cost_ratio": report["cost_ratio_deepseek_vs_sonnet"],
                      "output_dir": str(out)}, indent=2, ensure_ascii=False))
    return 0 if verdict in {"preflight_pass", "accept_default_switch"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
