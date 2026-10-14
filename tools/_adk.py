"""ADK bridge: expose a tool function to an agent.

We do not use ADK's `FunctionTool` directly, for one specific reason: it does
not parse a Google-style `Args:` block into per-parameter descriptions. It puts
the whole docstring (Args block included) into the declaration's top-level
description and leaves each parameter with only a name and a type.

Those per-parameter descriptions are part of the text the model selects on and
part of what the retrieval strategies index, so accepting ADK's lossy default
would change the thing this project measures. `FunctionBackedTool` therefore
builds the declaration from the introspected ToolSpec, and is otherwise an
ordinary ADK tool.

Unlike the earlier stub-only version, `run_async` really does call the Python
function. The bodies currently return a stub marker because the study scores
selection rather than execution -- but the call path is real, so swapping a
stub body for a live API call needs no change here.
"""

from __future__ import annotations

import inspect
from typing import Any, Optional

from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from google.genai import types

from ._spec import ToolSpec


_INVOCATION_USED_TOOLS: dict[str, list[str]] = {}
_LAST_INVOCATION_ID: Optional[str] = None


def record_tool_used(name: str, invocation_id: Optional[str] = None) -> None:
    global _LAST_INVOCATION_ID
    if invocation_id:
        _LAST_INVOCATION_ID = invocation_id
        if invocation_id not in _INVOCATION_USED_TOOLS:
            _INVOCATION_USED_TOOLS[invocation_id] = []
        if name not in _INVOCATION_USED_TOOLS[invocation_id]:
            _INVOCATION_USED_TOOLS[invocation_id].append(name)
    else:
        key = _LAST_INVOCATION_ID or "__default__"
        if key not in _INVOCATION_USED_TOOLS:
            _INVOCATION_USED_TOOLS[key] = []
        if name not in _INVOCATION_USED_TOOLS[key]:
            _INVOCATION_USED_TOOLS[key].append(name)


def get_recorded_tool_names(invocation_id: Optional[str] = None) -> list[str]:
    key = invocation_id or _LAST_INVOCATION_ID
    if key and key in _INVOCATION_USED_TOOLS:
        return list(_INVOCATION_USED_TOOLS[key])
    if "__default__" in _INVOCATION_USED_TOOLS:
        return list(_INVOCATION_USED_TOOLS["__default__"])
    return []


class FunctionBackedTool(BaseTool):
    """An ADK tool backed by a real Python function."""

    def __init__(self, spec: ToolSpec):
        super().__init__(name=spec.name, description=spec.description)
        self.spec = spec

    def _get_declaration(self) -> Optional[types.FunctionDeclaration]:
        return self.spec.to_declaration()

    async def run_async(self, *, args: dict[str, Any], tool_context: ToolContext) -> Any:
        invoc_id = getattr(tool_context, "invocation_id", None) if tool_context else None
        record_tool_used(self.spec.name, invocation_id=invoc_id)
        if tool_context and hasattr(tool_context, "state"):
            try:
                used = tool_context.state.get("used_tools", [])
                if self.spec.name not in used:
                    tool_context.state["used_tools"] = [*used, self.spec.name]
            except Exception:
                pass

        fn = self.spec.func
        if fn is None:
            return {"status": "stub", "tool": self.spec.name, "args": args}

        # The model can emit arguments that are not in the signature. Dropping
        # them rather than raising keeps a selection run from dying on an
        # argument mistake -- we are scoring the choice of tool, and an
        # argument error is a different failure we do not want conflated with
        # a selection error.
        accepted = {p.name for p in self.spec.params}
        call_args = {k: v for k, v in (args or {}).items() if k in accepted}

        result = fn(**call_args)
        if inspect.isawaitable(result):
            result = await result
        return result


def build_tools(specs: list[ToolSpec]) -> list[FunctionBackedTool]:
    return [FunctionBackedTool(s) for s in specs]

