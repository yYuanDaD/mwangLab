import os
import tempfile
import unittest

from langchain.agents.middleware import ModelRequest
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.messages import AIMessage
from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel

from tools.agent_state import BioinformaticsAgentState, RuntimeStateMiddleware, render_runtime_context
from tools.run_status import RunStatusTracker


class AgentStateTests(unittest.TestCase):
    def test_projection_omits_ui_only_fields(self):
        text = render_runtime_context({
            "analysis_request": {"profiles": ["geo_batch"]},
            "run_status": {
                "status": "running", "stage": "design", "elapsed_seconds": 999,
                "estimated_cost_usd": 1.23, "warning_count": 1, "failure_count": 0,
            },
            "execution_budget": {"max_calls_per_tool": 3},
        })
        self.assertIn("current stage: design", text)
        self.assertIn("warnings=1", text)
        self.assertNotIn("elapsed", text)
        self.assertNotIn("1.23", text)

    def test_middleware_injects_system_context_without_mutating_messages(self):
        with tempfile.TemporaryDirectory() as tmp:
            tracker = RunStatusTracker(os.path.join(tmp, "status.json"), run_id="r1", profile="bulk",
                                       stages=["routing", "tool"])
            tracker.start()
            tracker.set_stage("tool", current_tool="run_pca")
            middleware = RuntimeStateMiddleware(tracker)
            state = {"messages": [HumanMessage(content="run it")], "run_status": tracker.snapshot()}
            request = ModelRequest(model=None, messages=list(state["messages"]), state=state,
                                   runtime=None, system_message=SystemMessage(content="BASE"))
            captured = {}

            def handler(updated):
                captured["request"] = updated
                return "ok"

            result = middleware.wrap_model_call(request, handler)
        self.assertEqual(result, "ok")
        self.assertIn("RUNTIME STATE", captured["request"].system_message.text)
        self.assertIn("current tool: run_pca", captured["request"].system_message.text)
        self.assertEqual(request.messages, state["messages"])
        self.assertEqual(len(state["messages"]), 1)

    def test_create_agent_preserves_custom_state_without_status_messages(self):
        model = FakeMessagesListChatModel(responses=[AIMessage(content="done")])
        agent = create_agent(
            model=model, tools=[], system_prompt="BASE",
            state_schema=BioinformaticsAgentState,
            middleware=[RuntimeStateMiddleware()],
        )
        result = agent.invoke({
            "messages": [("user", "hello")],
            "analysis_request": {"profiles": ["general"]},
            "run_status": {"status": "running", "stage": "reasoning"},
            "artifacts": [], "evidence_ids": [],
            "execution_budget": {"max_calls_per_tool": 3},
        })
        self.assertEqual(result["analysis_request"]["profiles"], ["general"])
        self.assertEqual(result["run_status"]["stage"], "reasoning")
        self.assertEqual([m.type for m in result["messages"]], ["human", "ai"])
        self.assertNotIn("RUNTIME STATE", "\n".join(str(m.content) for m in result["messages"]))


if __name__ == "__main__":
    unittest.main()
