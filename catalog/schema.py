"""Core data model for the tool catalog.

A ToolSpec is a *declarative* description of a tool. It is deliberately
decoupled from ADK so that:
  - retrieval strategies can index specs without touching the framework
  - the same spec can be materialised as an ADK BaseTool when needed
  - catalog size is a parameter, not a constant

Scope note: tools in this study are never executed for real. `StubTool.run_async`
returns a marker dict. We measure *selection*, nothing downstream.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from google.genai import types

_TYPE_MAP = {
    "string": types.Type.STRING,
    "integer": types.Type.INTEGER,
    "number": types.Type.NUMBER,
    "boolean": types.Type.BOOLEAN,
    "array": types.Type.ARRAY,
}


@dataclass(frozen=True)
class Param:
    name: str
    type: str
    description: str
    required: bool = True
    enum: Optional[tuple[str, ...]] = None

    def to_schema(self) -> types.Schema:
        kwargs: dict[str, Any] = {
            "type": _TYPE_MAP[self.type],
            "description": self.description,
        }
        if self.enum:
            kwargs["enum"] = list(self.enum)
        if self.type == "array":
            kwargs["items"] = types.Schema(type=types.Type.STRING)
        return types.Schema(**kwargs)


@dataclass(frozen=True)
class ToolSpec:
    """One tool in the catalog.

    Attributes:
        name: Fully-qualified tool name, e.g. "github_create_issue".
        domain: Namespace used by the hierarchical strategy.
        description: Natural-language description. This is the *only* text a
            retrieval strategy is allowed to index, alongside the name --
            mirroring what a real model sees.
        params: Declared parameters.
        confusable_with: Tools this one is intended to be mistaken for. Never
            used for selection; used only to score distractor-induced errors.
    """

    name: str
    domain: str
    description: str
    params: tuple[Param, ...] = ()
    confusable_with: tuple[str, ...] = field(default=())

    def to_declaration(self) -> types.FunctionDeclaration:
        props = {p.name: p.to_schema() for p in self.params}
        required = [p.name for p in self.params if p.required]
        return types.FunctionDeclaration(
            name=self.name,
            description=self.description,
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties=props,
                required=required,
            )
            if props
            else None,
        )

    def index_text(self) -> str:
        """Text surface a retrieval strategy may index."""
        param_text = " ".join(f"{p.name} {p.description}" for p in self.params)
        return f"{self.name} {self.description} {param_text}"


class StubTool(BaseTool):
    """ADK tool that declares a real schema but performs no work.

    Selection-only harness: reaching run_async means the model *chose* this
    tool, which is the signal we record. The return value is inert.
    """

    def __init__(self, spec: ToolSpec):
        super().__init__(name=spec.name, description=spec.description)
        self.spec = spec

    def _get_declaration(self) -> Optional[types.FunctionDeclaration]:
        return self.spec.to_declaration()

    async def run_async(self, *, args: dict[str, Any], tool_context: ToolContext) -> Any:
        return {"status": "stub", "tool": self.spec.name, "args": args}


def build_tools(specs: list[ToolSpec]) -> list[StubTool]:
    return [StubTool(s) for s in specs]
