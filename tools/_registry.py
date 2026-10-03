"""The @tool decorator and function-to-spec introspection.

Tools are plain Python functions. The decorator attaches the experiment
metadata that has no natural home in a signature (domain, confusable_with) and
registers the function so the catalog can find it.

Everything else is derived by reading the function itself:

    def github_create_issue(repo: str, title: str, body: Optional[str] = None):
        '''Open a new issue on a GitHub repository.      <- description

        Args:
            repo: Repository in owner/name form.         <- param description
        '''
        ^^^^                ^^^                          <- name, type, required

Deriving rather than declaring means the code and what the model sees cannot
drift apart: edit the docstring and the declaration changes with it.

ON DOCSTRING PARSING
We parse the Google-style `Args:` block ourselves. ADK's FunctionTool does not
-- it puts the entire docstring, Args block included, into the declaration's
top-level description and gives parameters only a name and a type. Since
per-parameter descriptions are part of what the model selects on, accepting
that would change what is being measured.
"""

from __future__ import annotations

import inspect
import re
import typing
from typing import Any, Callable, Literal, Optional, Union, get_args, get_origin

from ._spec import Param, ToolSpec

_REGISTRY: dict[str, Callable] = {}
_ORDER: list[str] = []

_PY_TO_JSON = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
}


def tool(*, domain: str, confusable_with: Optional[list[str]] = None):
    """Mark a function as a tool and attach its experiment metadata.

    Args:
        domain: Namespace used by the hierarchical routing strategy.
        confusable_with: Tools this one is intended to be mistaken for. Used
            only to classify errors, never for selection.
    """

    def decorate(fn: Callable) -> Callable:
        if fn.__name__ in _REGISTRY:
            raise ValueError(f"duplicate tool name: {fn.__name__}")
        if not (fn.__doc__ or "").strip():
            raise ValueError(f"{fn.__name__}: a tool must have a docstring")
        fn._tool_domain = domain  # type: ignore[attr-defined]
        fn._tool_confusable = tuple(confusable_with or ())  # type: ignore[attr-defined]
        _REGISTRY[fn.__name__] = fn
        _ORDER.append(fn.__name__)
        return fn

    return decorate


# -- docstring parsing -------------------------------------------------------

_ARGS_HEADER = re.compile(r"^\s*(Args|Arguments|Parameters)\s*:\s*$")
_ARG_LINE = re.compile(r"^\s{4,}(\w+)\s*:\s*(.*)$")


def parse_docstring(doc: str) -> tuple[str, dict[str, str]]:
    """Split a Google-style docstring into (summary, {param: description})."""
    lines = inspect.cleandoc(doc or "").splitlines()
    summary_lines: list[str] = []
    params: dict[str, str] = {}

    i = 0
    while i < len(lines) and not _ARGS_HEADER.match(lines[i]):
        summary_lines.append(lines[i])
        i += 1

    current: Optional[str] = None
    for line in lines[i + 1 :] if i < len(lines) else []:
        if not line.strip():
            continue
        # A section header such as "Returns:" ends the Args block.
        if re.match(r"^\s*\w+\s*:\s*$", line) and not line.startswith("        "):
            break
        m = re.match(r"^\s*(\w+)\s*:\s*(.*)$", line)
        if m and (line.startswith("    ") or current is None):
            current = m.group(1)
            params[current] = m.group(2).strip()
        elif current:
            params[current] = (params[current] + " " + line.strip()).strip()

    return " ".join(x.strip() for x in summary_lines if x.strip()).strip(), params


# -- signature introspection -------------------------------------------------


def _unwrap_optional(ann: Any) -> tuple[Any, bool]:
    """Return (inner_type, was_optional) for Optional[X] / X | None."""
    origin = get_origin(ann)
    if origin is Union or str(origin) == "types.UnionType":
        args = [a for a in get_args(ann) if a is not type(None)]
        if len(args) == 1:
            return args[0], True
    return ann, False


def _json_type(ann: Any) -> tuple[str, Optional[tuple[str, ...]]]:
    """Map a Python annotation to (json_type, enum_values)."""
    if get_origin(ann) is Literal:
        return "string", tuple(str(a) for a in get_args(ann))
    if ann in _PY_TO_JSON:
        return _PY_TO_JSON[ann], None
    origin = get_origin(ann)
    if origin in (list, set, tuple):
        return "array", None
    if ann is list:
        return "array", None
    raise TypeError(f"unsupported tool parameter annotation: {ann!r}")


def spec_from_function(fn: Callable) -> ToolSpec:
    """Derive a ToolSpec by reading a decorated function."""
    domain = getattr(fn, "_tool_domain", None)
    if domain is None:
        raise ValueError(f"{fn.__name__} is not decorated with @tool")

    summary, doc_params = parse_docstring(fn.__doc__ or "")
    hints = typing.get_type_hints(fn, include_extras=False)

    params: list[Param] = []
    for name, p in inspect.signature(fn).parameters.items():
        if name in ("self", "tool_context"):
            continue
        ann = hints.get(name, str)
        inner, optional_ann = _unwrap_optional(ann)
        jtype, enum = _json_type(inner)
        required = p.default is inspect.Parameter.empty and not optional_ann
        desc = doc_params.get(name, "")
        if not desc:
            raise ValueError(
                f"{fn.__name__}: parameter {name!r} has no description in the "
                "docstring Args block. Per-parameter descriptions are part of "
                "what the model selects on."
            )
        # The enum values are already stated in the docstring text; keep the
        # prose clean by stripping the trailing "One of: ..." sentence.
        desc = re.sub(r"\s*One of:[^.]*\.\s*$", "", desc).strip()
        params.append(Param(name=name, type=jtype, description=desc,
                            required=required, enum=enum))

    return ToolSpec(
        name=fn.__name__,
        domain=domain,
        description=summary,
        params=tuple(params),
        confusable_with=tuple(getattr(fn, "_tool_confusable", ())),
        func=fn,
    )


def registered_functions() -> list[Callable]:
    """Every decorated function, in definition order."""
    return [_REGISTRY[n] for n in _ORDER]


def registered_specs() -> list[ToolSpec]:
    return [spec_from_function(f) for f in registered_functions()]
