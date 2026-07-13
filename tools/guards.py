"""Programmatic guardrails for the agent's tool calls.

These wrappers do not depend on the LLM listening to a system prompt — the
checks run in Python. They are designed to make tool-call loops impossible:

- Dedupe: identical (tool_name, kwargs) is rejected on the second call and
  the prior result is returned to the model so it can move on.
- Per-tool cap: each tool can be invoked at most N times per agent run; the
  N+1th call is refused with a message asking the model to write its final
  answer from the data it already has.
"""

import hashlib
import json
from typing import List

from langchain_core.tools import BaseTool, StructuredTool


def _args_hash(kwargs: dict) -> str:
    """Stable short hash for a tool-call kwargs dict."""
    blob = json.dumps(kwargs, sort_keys=True, default=str)
    return hashlib.md5(blob.encode()).hexdigest()[:12]


def _wrap_one(t: BaseTool, max_calls: int) -> BaseTool:
    state = {"count": 0, "seen": {}}

    def guarded(**kwargs):
        state["count"] += 1
        if state["count"] > max_calls:
            return (
                f"[GUARD] Tool '{t.name}' has already been called {max_calls} times in this run. "
                f"Stop calling this tool and write your final answer based on the results you already have."
            )
        h = _args_hash(kwargs)
        if h in state["seen"]:
            prior = state["seen"][h]
            return (
                f"[GUARD] Tool '{t.name}' was already invoked with these exact arguments. "
                f"Reuse the prior result instead of repeating the call. Prior result:\n{prior}"
            )
        result = t.invoke(kwargs)
        state["seen"][h] = result
        return result

    return StructuredTool.from_function(
        func=guarded,
        name=t.name,
        description=t.description,
        args_schema=t.args_schema,
    )


def guard_tools(tools: List[BaseTool], max_calls_per_tool: int = 3) -> List[BaseTool]:
    """Return a list of tools wrapped with dedupe + per-tool call cap.

    Each wrapped tool keeps the original name/description/args_schema so the
    LLM sees the same interface."""
    return [_wrap_one(t, max_calls_per_tool) for t in tools]
