"""The data model a tool is *described* by.

A ToolSpec is no longer authored by hand -- it is derived from a real Python
function by `_registry.spec_from_function`. It exists because the selection
strategies need tool metadata as inspectable data (to index, embed, rank and
generate), which a function object does not give you directly.

So the flow is now:

    real Python function  --introspect-->  ToolSpec  --render-->  declaration
      (source of truth)                  (what strategies      (what the model
                                          index)                sees)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

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
    """Everything known about one tool, derived from its function.

    Attributes:
        name: The function's __name__.
        domain: Namespace, from the @tool decorator.
        description: The docstring summary (the Args block is stripped out --
            it becomes per-parameter descriptions instead).
        params: Derived from the signature plus the docstring Args block.
        confusable_with: Experiment metadata from @tool. Never used for
            selection; only to classify errors.
        func: The underlying callable, or None for generated filler built
            without a Python body.
    """

    name: str
    domain: str
    description: str
    params: tuple[Param, ...] = ()
    confusable_with: tuple[str, ...] = field(default=())
    func: Optional[Any] = field(default=None, compare=False, repr=False)

    def to_declaration(self) -> types.FunctionDeclaration:
        """Build the declaration the model sees.

        We construct this ourselves rather than letting ADK's FunctionTool
        derive it, because ADK does NOT parse a Google-style `Args:` block into
        per-parameter descriptions -- it dumps the whole docstring into the
        top-level description and leaves parameters with only a name and type.
        Those per-parameter descriptions are part of what the model selects on,
        so losing them would quietly change the thing being measured.
        """
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
