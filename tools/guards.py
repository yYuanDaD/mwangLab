"""Per-run, programmatic guardrails for ReAct tool calls."""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from threading import Event, RLock
from typing import Any, Dict, List
from uuid import uuid4

from langchain_core.tools import BaseTool, StructuredTool


def _args_hash(kwargs: dict) -> str:
    """Stable hash for a tool-call argument object."""
    blob = json.dumps(kwargs, sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]


@dataclass
class ToolGuardState:
    """Mutable state owned by exactly one guarded tool set / agent run."""

    run_id: str = field(default_factory=lambda: uuid4().hex)
    attempts: Dict[str, int] = field(default_factory=dict)
    seen: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    in_flight: Dict[str, Dict[str, Event]] = field(default_factory=dict)
    lock: RLock = field(default_factory=RLock, repr=False)


def _wrap_one(t: BaseTool, max_calls: int, state: ToolGuardState) -> BaseTool:
    def guarded(**kwargs):
        args_key = _args_hash(kwargs)
        with state.lock:
            tool_cache = state.seen.setdefault(t.name, {})
            if args_key in tool_cache:
                prior = tool_cache[args_key]
                return (
                    f"[GUARD run={state.run_id}] Tool '{t.name}' already ran with these exact arguments. "
                    f"Reusing the cached result; duplicate calls do not consume the call budget.\n"
                    f"Prior result:\n{prior}"
                )
            tool_in_flight = state.in_flight.setdefault(t.name, {})
            wait_for = tool_in_flight.get(args_key)
            if wait_for is not None:
                owns_execution = False
            else:
                owns_execution = True
            attempts = state.attempts.get(t.name, 0)
            if owns_execution and attempts >= max_calls:
                return (
                    f"[GUARD run={state.run_id}] Tool '{t.name}' reached its limit of "
                    f"{max_calls} unique execution attempts for this run. Stop calling it and "
                    "answer from existing results."
                )
            if owns_execution:
                # Reserve both the budget and argument key while holding the
                # lock. Concurrent identical calls wait for this result.
                state.attempts[t.name] = attempts + 1
                wait_for = Event()
                tool_in_flight[args_key] = wait_for

        if not owns_execution:
            wait_for.wait()
            with state.lock:
                if args_key in state.seen[t.name]:
                    prior = state.seen[t.name][args_key]
                    return (
                        f"[GUARD run={state.run_id}] Concurrent duplicate call to '{t.name}' "
                        f"reused the first execution's cached result.\nPrior result:\n{prior}"
                    )
            return (
                f"[GUARD run={state.run_id}] Concurrent duplicate call to '{t.name}' was not "
                "executed because the first identical attempt failed."
            )

        try:
            result = t.invoke(kwargs)
        except Exception:
            with state.lock:
                state.in_flight[t.name].pop(args_key, None)
                wait_for.set()
            raise
        with state.lock:
            state.seen[t.name][args_key] = result
            state.in_flight[t.name].pop(args_key, None)
            wait_for.set()
        return result

    return StructuredTool.from_function(
        func=guarded,
        name=t.name,
        description=t.description,
        args_schema=t.args_schema,
        return_direct=getattr(t, "return_direct", False),
    )


def guard_tools(
    tools: List[BaseTool],
    max_calls_per_tool: int = 3,
    *,
    run_id: str | None = None,
) -> List[BaseTool]:
    """Create an isolated guarded tool set for one agent run.

    Reusing the returned wrappers intentionally reuses their budget. Calling
    ``guard_tools`` again creates fresh state, even for the same underlying tools.
    """
    if max_calls_per_tool < 1:
        raise ValueError("max_calls_per_tool must be at least 1")
    state = ToolGuardState(run_id=run_id or uuid4().hex)
    return [_wrap_one(t, max_calls_per_tool, state) for t in tools]
