import unittest

from langchain_core.tools import tool

from tools.guards import guard_tools


class GuardTests(unittest.TestCase):
    def test_duplicate_does_not_consume_unique_call_budget(self):
        calls = []

        @tool
        def echo(value: int) -> str:
            """Return a value and record a real execution."""
            calls.append(value)
            return str(value)

        guarded = guard_tools([echo], max_calls_per_tool=2, run_id="test-run")[0]
        self.assertEqual(guarded.invoke({"value": 1}), "1")
        duplicate = guarded.invoke({"value": 1})
        self.assertIn("cached result", duplicate)
        self.assertEqual(guarded.invoke({"value": 2}), "2")
        self.assertIn("reached its limit", guarded.invoke({"value": 3}))
        self.assertEqual(calls, [1, 2])

    def test_new_guard_set_has_fresh_state(self):
        @tool
        def echo(value: int) -> str:
            """Return a value."""
            return str(value)

        first = guard_tools([echo], max_calls_per_tool=1, run_id="run-1")[0]
        second = guard_tools([echo], max_calls_per_tool=1, run_id="run-2")[0]
        self.assertEqual(first.invoke({"value": 1}), "1")
        self.assertIn("reached its limit", first.invoke({"value": 2}))
        self.assertEqual(second.invoke({"value": 2}), "2")

    def test_invalid_limit_is_rejected(self):
        with self.assertRaises(ValueError):
            guard_tools([], max_calls_per_tool=0)


if __name__ == "__main__":
    unittest.main()
