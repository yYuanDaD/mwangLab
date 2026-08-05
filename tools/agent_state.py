"""Custom LangGraph agent state and ephemeral runtime-context projection."""

from __future__ import annotations

from typing import Any, NotRequired

from langchain.agents import AgentState
from langchain.agents.middleware import AgentMiddleware, ModelRequest
from langchain_core.messages import SystemMessage

from tools.run_status import RunStatusTracker


class BioinformaticsAgentState(AgentState):
    """State fields kept alongside, but separate from, the ReAct message history."""

    analysis_request: NotRequired[dict[str, Any]]
    run_status: NotRequired[dict[str, Any]]
    artifacts: NotRequired[list[dict[str, Any]]]
    evidence_ids: NotRequired[list[str]]
    execution_budget: NotRequired[dict[str, Any]]


def render_runtime_context(state: dict[str, Any]) -> str:
    """Project only decision-relevant state; omit UI-only/high-frequency fields."""
    status = state.get("run_status") or {}
    request = state.get("analysis_request") or {}
    budget = state.get("execution_budget") or {}
    artifacts = state.get("artifacts") or []
    evidence_ids = state.get("evidence_ids") or status.get("evidence_ids") or []

    lines = ["RUNTIME STATE (system-generated; not a user or assistant message):"]
    profiles = request.get("profiles") or ([status.get("profile")] if status.get("profile") else [])
    if profiles:
        lines.append(f"- profiles: {', '.join(str(x) for x in profiles)}")
    if status.get("status"):
        lines.append(f"- run status: {status['status']}")
    if status.get("accession"):
        lines.append(
            f"- study: {status['accession']} ({status.get('study_index', 0)}/{status.get('study_total', 0)})"
        )
    completed = status.get("completed_stages") or []
    if completed:
        lines.append(f"- completed stages: {', '.join(str(x) for x in completed)}")
    if status.get("stage"):
        lines.append(f"- current stage: {status['stage']}")
    if status.get("current_tool"):
        lines.append(f"- current tool: {status['current_tool']}")
    if status.get("warning_count") or status.get("failure_count"):
        lines.append(
            f"- issues: warnings={status.get('warning_count', 0)}, failures={status.get('failure_count', 0)}"
        )
    if status.get("message"):
        lines.append(f"- latest runtime note: {status['message']}")
    if artifacts:
        lines.append(f"- known artifacts: {len(artifacts)}")
    if evidence_ids:
        lines.append(f"- evidence refs: {', '.join(str(x) for x in evidence_ids[-8:])}")
    if budget:
        remaining = budget.get("remaining_tool_calls")
        cap = budget.get("max_calls_per_tool")
        if remaining is not None:
            lines.append(f"- remaining tool calls: {remaining}")
        elif cap is not None:
            lines.append(f"- per-tool unique-call cap: {cap}")
    lines.append("Use this state only when it affects the next decision; do not repeat it to the user verbatim.")
    return "\n".join(lines)


class RuntimeStateMiddleware(AgentMiddleware):
    """Synchronize external status and inject one replaceable system-state block."""

    state_schema = BioinformaticsAgentState

    def __init__(self, tracker: RunStatusTracker | None = None):
        self.tracker = tracker

    def before_model(self, state: BioinformaticsAgentState, runtime) -> dict[str, Any] | None:
        if self.tracker is None:
            return None
        return {"run_status": self.tracker.snapshot()}

    def wrap_model_call(self, request: ModelRequest, handler):
        runtime_block = render_runtime_context(request.state)
        base = request.system_message.text if request.system_message is not None else ""
        combined = f"{base}\n\n{runtime_block}" if base else runtime_block
        # Override only this model request. The runtime block is not appended to
        # state['messages'], so repeated ReAct turns do not accumulate status spam.
        return handler(request.override(system_message=SystemMessage(content=combined)))
