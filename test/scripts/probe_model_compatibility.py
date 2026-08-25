"""Low-cost live compatibility probe for an LLM provider.

This is a provider/API gate, not a full agent-quality benchmark. It checks:
plain text, repeated structured scientific routing, one exact tool call, and
continuation after a tool result. Results are written under ``output/`` with
score, coverage, blocking findings, usage, estimated cost, and provenance.

Examples:
    python test/scripts/probe_model_compatibility.py --provider deepseek
    python test/scripts/probe_model_compatibility.py --provider anthropic --structured-repeats 3
"""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import sys
import time
from typing import Literal

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tools.model_factory import (  # noqa: E402
    create_chat_model,
    create_structured_chat_model,
    resolve_model_config,
)
from tools.run_status import RunStatusTracker  # noqa: E402


PRICING_SNAPSHOT = {
    "as_of": "2026-08-17",
    "anthropic": {"cache_hit": 0.30, "cache_miss": 3.00, "output": 15.00},
    "deepseek": {"cache_hit": 0.003625, "cache_miss": 0.435, "output": 0.87},
}


class MatrixRoutingDecision(BaseModel):
    matrix_type: Literal["raw_counts", "fpkm_or_tpm", "log_transformed"]
    da_method: Literal["deseq2", "limma"]
    use_deseq2: bool
    reasoning: str = Field(description="One short sentence")


@tool
def add_numbers(a: int, b: int) -> int:
    """Add two integers and return the exact sum."""
    return a + b


def _content_text(message) -> str:
    content = getattr(message, "content", "")
    if isinstance(content, str):
        return content
    parts = []
    for block in content or []:
        if isinstance(block, dict) and block.get("type") == "text":
            parts.append(str(block.get("text", "")))
        elif hasattr(block, "text"):
            parts.append(str(block.text))
    return "\n".join(parts)


def _usage(message) -> dict[str, int]:
    metadata = getattr(message, "usage_metadata", None) or {}
    response_usage = (getattr(message, "response_metadata", None) or {}).get("usage", {}) or {}
    input_tokens = int(metadata.get("input_tokens") or response_usage.get("input_tokens") or 0)
    output_tokens = int(metadata.get("output_tokens") or response_usage.get("output_tokens") or 0)
    details = metadata.get("input_token_details") or {}
    cache_hit = int(
        details.get("cache_read")
        or response_usage.get("cache_read_input_tokens")
        or response_usage.get("prompt_cache_hit_tokens")
        or 0
    )
    cache_miss = int(
        response_usage.get("prompt_cache_miss_tokens")
        or max(0, input_tokens - cache_hit)
    )
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cache_hit_input_tokens": cache_hit,
        "cache_miss_input_tokens": cache_miss,
    }


def _estimate_cost(provider: str, usage: dict[str, int]) -> float:
    prices = PRICING_SNAPSHOT[provider]
    cost = (
        usage["cache_hit_input_tokens"] * prices["cache_hit"]
        + usage["cache_miss_input_tokens"] * prices["cache_miss"]
        + usage["output_tokens"] * prices["output"]
    ) / 1_000_000
    return round(cost, 8)


def _add_usage(total: dict[str, int], item: dict[str, int]) -> None:
    for key in total:
        total[key] += int(item.get(key, 0))


def _invoke_timed(runnable, messages):
    started = time.perf_counter()
    response = runnable.invoke(messages)
    return response, round(time.perf_counter() - started, 3)


def run_probe(provider: str, model: str | None, effort: str | None,
              structured_repeats: int, output_dir: Path) -> dict:
    config = resolve_model_config(provider=provider, model=model, effort=effort)
    llm = create_chat_model(config)
    output_dir.mkdir(parents=True, exist_ok=True)
    tracker = RunStatusTracker(
        str(output_dir / "run_status.json"),
        run_id=output_dir.name,
        profile="model_compatibility",
        stages=["basic", "structured", "tool", "multi_turn", "agent_loop", "report"],
    )
    tracker.start(f"probing {config.label}")
    usage = {key: 0 for key in (
        "input_tokens", "output_tokens", "cache_hit_input_tokens", "cache_miss_input_tokens"
    )}
    results: dict = {
        "basic": {}, "structured": [], "tool": {}, "multi_turn": {}, "agent_loop": {}
    }
    blocking: list[str] = []

    tracker.set_stage("basic", message="plain response")
    try:
        raw, elapsed = _invoke_timed(llm, [HumanMessage(content="Reply with the single word READY.")])
        call_usage = _usage(raw)
        _add_usage(usage, call_usage)
        text = _content_text(raw).strip()
        passed = "READY" in text.upper()
        results["basic"] = {"passed": passed, "text": text[:200], "elapsed_seconds": elapsed,
                            "usage": call_usage}
        if not passed:
            blocking.append("basic response did not contain READY")
    except Exception as exc:
        results["basic"] = {"passed": False, "error": f"{type(exc).__name__}: {exc}"}
        blocking.append("basic API invocation failed")

    tracker.set_stage("structured", message=f"{structured_repeats} schema repetitions")
    structured_llm = create_structured_chat_model(config)
    structured = structured_llm.with_structured_output(MatrixRoutingDecision, include_raw=True)
    structured_prompt = (
        "Return the requested structured decision. The matrix contains non-integer FPKM values "
        "that have already been normalized. Classify it as fpkm_or_tpm, select limma, and set "
        "use_deseq2 to false."
    )
    for repeat in range(1, structured_repeats + 1):
        try:
            response, elapsed = _invoke_timed(structured, structured_prompt)
            raw = response.get("raw") if isinstance(response, dict) else None
            parsed = response.get("parsed") if isinstance(response, dict) else None
            parse_error = response.get("parsing_error") if isinstance(response, dict) else "bad response"
            call_usage = _usage(raw)
            _add_usage(usage, call_usage)
            scientifically_correct = bool(
                parsed
                and parsed.matrix_type == "fpkm_or_tpm"
                and parsed.da_method == "limma"
                and parsed.use_deseq2 is False
            )
            passed = parsed is not None and parse_error is None and scientifically_correct
            results["structured"].append({
                "repeat": repeat,
                "passed": passed,
                "scientifically_correct": scientifically_correct,
                "parsed": parsed.model_dump(mode="json") if parsed else None,
                "parsing_error": str(parse_error) if parse_error else None,
                "elapsed_seconds": elapsed,
                "usage": call_usage,
            })
            if not passed:
                blocking.append(f"structured output failed on repeat {repeat}")
        except Exception as exc:
            results["structured"].append({
                "repeat": repeat, "passed": False,
                "error": f"{type(exc).__name__}: {exc}",
            })
            blocking.append(f"structured output raised on repeat {repeat}")

    tracker.set_stage("tool", message="exact tool call")
    tool_llm = llm.bind_tools([add_numbers])
    tool_request = HumanMessage(
        content="Call add_numbers exactly once with a=2 and b=3. Do not calculate it yourself."
    )
    first = None
    try:
        first, elapsed = _invoke_timed(tool_llm, [tool_request])
        call_usage = _usage(first)
        _add_usage(usage, call_usage)
        calls = list(getattr(first, "tool_calls", None) or [])
        exact = bool(
            len(calls) == 1
            and calls[0].get("name") == "add_numbers"
            and calls[0].get("args") == {"a": 2, "b": 3}
        )
        results["tool"] = {
            "passed": exact,
            "tool_call_count": len(calls),
            "tool_calls": calls,
            "elapsed_seconds": elapsed,
            "usage": call_usage,
        }
        if not exact:
            blocking.append("tool call was missing, duplicated, or had incorrect arguments")
    except Exception as exc:
        results["tool"] = {"passed": False, "error": f"{type(exc).__name__}: {exc}"}
        blocking.append("tool invocation failed")

    tracker.set_stage("multi_turn", message="continue after tool result")
    calls = list(getattr(first, "tool_calls", None) or []) if first is not None else []
    if len(calls) == 1 and calls[0].get("name") == "add_numbers":
        try:
            result = add_numbers.invoke(calls[0].get("args", {}))
            tool_result = ToolMessage(content=str(result), tool_call_id=calls[0]["id"])
            final, elapsed = _invoke_timed(tool_llm, [tool_request, first, tool_result])
            call_usage = _usage(final)
            _add_usage(usage, call_usage)
            final_text = _content_text(final).strip()
            extra_calls = list(getattr(final, "tool_calls", None) or [])
            passed = result == 5 and "5" in final_text and not extra_calls
            results["multi_turn"] = {
                "passed": passed,
                "tool_result": result,
                "final_text": final_text[:500],
                "extra_tool_calls": extra_calls,
                "elapsed_seconds": elapsed,
                "usage": call_usage,
            }
            if not passed:
                blocking.append("model did not complete correctly after the tool result")
        except Exception as exc:
            results["multi_turn"] = {"passed": False, "error": f"{type(exc).__name__}: {exc}"}
            blocking.append("multi-turn tool continuation failed")
    else:
        results["multi_turn"] = {"passed": False, "not_measured": True,
                                  "reason": "no valid first tool call"}
        blocking.append("multi-turn continuation could not be measured")

    tracker.set_stage("agent_loop", message="LangGraph ReAct loop")
    agent_llm_calls = 0
    try:
        agent = create_agent(
            model=llm,
            tools=[add_numbers],
            system_prompt=(
                "Follow the user exactly. Call a requested tool once, use its result, "
                "then stop with a short final answer."
            ),
        )
        started = time.perf_counter()
        agent_result = agent.invoke(
            {"messages": [("user", "Use add_numbers exactly once for 7 plus 8, then report the result.")]},
            config={"recursion_limit": 8},
        )
        elapsed = round(time.perf_counter() - started, 3)
        messages = list(agent_result.get("messages", []))
        agent_calls = []
        tool_messages = 0
        for message in messages:
            message_usage = _usage(message)
            if message_usage["input_tokens"] or message_usage["output_tokens"]:
                agent_llm_calls += 1
                _add_usage(usage, message_usage)
            agent_calls.extend(list(getattr(message, "tool_calls", None) or []))
            if isinstance(message, ToolMessage):
                tool_messages += 1
        final_text = _content_text(messages[-1]).strip() if messages else ""
        exact_call = bool(
            len(agent_calls) == 1
            and agent_calls[0].get("name") == "add_numbers"
            and agent_calls[0].get("args") == {"a": 7, "b": 8}
        )
        passed = exact_call and tool_messages == 1 and "15" in final_text
        results["agent_loop"] = {
            "passed": passed,
            "tool_call_count": len(agent_calls),
            "tool_message_count": tool_messages,
            "llm_calls": agent_llm_calls,
            "final_text": final_text[:500],
            "elapsed_seconds": elapsed,
        }
        if not passed:
            blocking.append("LangGraph agent loop duplicated/missed the tool or returned the wrong result")
    except Exception as exc:
        results["agent_loop"] = {"passed": False, "error": f"{type(exc).__name__}: {exc}"}
        blocking.append("LangGraph agent loop failed")

    expected_checks = structured_repeats + 4
    measured_checks = int(bool(results["basic"])) + len(results["structured"]) + int(bool(results["tool"]))
    if not results["multi_turn"].get("not_measured"):
        measured_checks += 1
    if results["agent_loop"]:
        measured_checks += 1
    structured_pass_rate = (
        sum(bool(item.get("passed")) for item in results["structured"]) / structured_repeats
    )
    score = round(100 * (
        0.10 * bool(results["basic"].get("passed"))
        + 0.35 * structured_pass_rate
        + 0.15 * bool(results["tool"].get("passed"))
        + 0.15 * bool(results["multi_turn"].get("passed"))
        + 0.25 * bool(results["agent_loop"].get("passed"))
    ), 2)
    coverage = round(100 * measured_checks / expected_checks, 2)
    blocking = list(dict.fromkeys(blocking))
    verdict = "pass" if not blocking and coverage >= 60 else "fail"
    estimated_cost = _estimate_cost(config.provider, usage)
    probe_sha256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    report = {
        "schema_version": "1.0",
        "evaluation_unit": "provider compatibility probe",
        "verdict": verdict,
        "score": score,
        "coverage": coverage,
        "blocking_findings": blocking,
        "model": {
            "provider": config.provider,
            "model": config.model,
            "effort": config.effort,
            "base_url": config.base_url,
        },
        "structured_repeats": structured_repeats,
        "results": results,
        "usage": usage,
        "estimated_cost_usd": estimated_cost,
        "pricing_snapshot": PRICING_SNAPSHOT,
        "provenance": {"probe_script_sha256": probe_sha256},
        "unmeasured_checks": [
            "full bioinformatics workflow with GEO/file tools",
            "SEA-CDM full extraction",
            "cross-model scientific A/B",
            "DEG/GSEA result stability",
        ],
    }

    tracker.set_stage("report", message=f"verdict={verdict} score={score} coverage={coverage}")
    tracker.set_usage(
        llm_calls=(2 + structured_repeats
                   + int(not results["multi_turn"].get("not_measured", False))
                   + agent_llm_calls),
        estimated_cost_usd=estimated_cost,
    )
    with open(output_dir / "compatibility_report.json", "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)
    lines = [
        "# Model compatibility probe", "",
        f"- Verdict: **{verdict}**",
        f"- Score: **{score}/100**",
        f"- Coverage: **{coverage}%**",
        f"- Model: `{config.label}`",
        f"- Estimated cost: **${estimated_cost:.6f}**", "",
        "## Blocking findings", "",
    ]
    lines.extend([f"- {item}" for item in blocking] or ["- None"])
    lines.extend(["", "## Unmeasured checks", ""])
    lines.extend(f"- {item}" for item in report["unmeasured_checks"])
    (output_dir / "compatibility_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    for item in blocking:
        tracker.add_failure(item)
    tracker.finish("completed", f"compatibility probe verdict={verdict}")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", choices=("anthropic", "deepseek"), default="deepseek")
    parser.add_argument("--model", default=None)
    parser.add_argument("--effort", choices=("low", "medium", "high", "xhigh", "max"), default=None)
    parser.add_argument("--structured-repeats", type=int, default=10)
    parser.add_argument("--output-dir", default="")
    args = parser.parse_args()
    if args.structured_repeats < 1:
        raise SystemExit("--structured-repeats must be >= 1")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(args.output_dir) if args.output_dir else (
        ROOT / "output" / f"model_compat_{args.provider}_{stamp}"
    )
    report = run_probe(args.provider, args.model, args.effort,
                       args.structured_repeats, output_dir)
    print(json.dumps({
        "verdict": report["verdict"],
        "score": report["score"],
        "coverage": report["coverage"],
        "estimated_cost_usd": report["estimated_cost_usd"],
        "output_dir": str(output_dir),
    }, ensure_ascii=False, indent=2))
    return 0 if report["verdict"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
