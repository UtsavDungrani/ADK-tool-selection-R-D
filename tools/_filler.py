"""Generated filler tools, built as real Python functions at runtime.

Scaling the catalog to 200 or 400 means producing hundreds of extra tools. Now
that a tool *is* a function, filler has to be a function too -- a parallel
"spec-only" path would mean the thing being scaled is not the thing being
measured, and the two representations would drift.

So these are genuine function objects: real `__name__`, real `__doc__` in the
same Google style as the hand-written modules, real `__annotations__`, real
defaults. `spec_from_function` introspects them by exactly the same code path
as a hand-written tool, and `FunctionBackedTool` can call them.

They are never registered in the global registry, because they are per-run
scaffolding rather than part of the catalog.
"""

from __future__ import annotations

from typing import Callable, Optional

from ._registry import spec_from_function
from ._spec import ToolSpec

_DOC_TEMPLATE = """{description}

Args:
    id: Identifier of the {obj}.
    query: Free-text filter.
    limit: Maximum number of results.
"""


def make_filler_function(name: str, domain: str, description: str, obj: str) -> Callable:
    """Build a real, callable, introspectable filler tool function."""

    def _filler(
        id: Optional[str] = None,
        query: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> dict:
        return {"status": "stub", "tool": name, "args": {"id": id, "query": query, "limit": limit}}

    _filler.__name__ = name
    _filler.__qualname__ = name
    _filler.__doc__ = _DOC_TEMPLATE.format(description=description, obj=obj)
    _filler.__annotations__ = {
        "id": Optional[str],
        "query": Optional[str],
        "limit": Optional[int],
        "return": dict,
    }
    # Attach the same metadata @tool would, without registering globally.
    _filler._tool_domain = domain  # type: ignore[attr-defined]
    _filler._tool_confusable = ()  # type: ignore[attr-defined]
    return _filler


def make_filler_spec(name: str, domain: str, description: str, obj: str) -> ToolSpec:
    return spec_from_function(make_filler_function(name, domain, description, obj))
