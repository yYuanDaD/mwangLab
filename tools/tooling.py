"""Optional LangChain ``@tool`` decorator for the analysis modules.

The LangChain agent needs real LangChain tools. Native skill sessions call the
same functions directly, so for them langchain-core is optional: without it,
``tool`` returns a small wrapper that keeps ``.func``, ``.name``,
``.description``, and ``.invoke`` with the same calling convention.
"""

from __future__ import annotations

import functools

try:
    from langchain_core.tools import tool
except ImportError:
    class _PlainTool:
        def __init__(self, func):
            functools.update_wrapper(self, func)
            self.func = func
            self.name = func.__name__
            self.description = (func.__doc__ or "").strip()

        def __call__(self, *args, **kwargs):
            return self.func(*args, **kwargs)

        def invoke(self, tool_input, *args, **kwargs):
            if isinstance(tool_input, dict):
                return self.func(**tool_input)
            return self.func(tool_input)

    def tool(func=None, *args, **kwargs):  # noqa: D103 - mirrors langchain_core.tools.tool
        if callable(func) and not args and not kwargs:
            return _PlainTool(func)
        return lambda f: _PlainTool(f)
