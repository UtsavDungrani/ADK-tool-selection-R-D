#!/usr/bin/env python
"""ONE-TIME codegen: turn the legacy ToolSpec catalog into real Python modules.

After this runs, `tools/*.py` is the source of truth and the declarative
ToolSpec lists in `catalog/domains*.py` are dead. Keep this script only as a
record of the migration -- do not run it again, it would overwrite hand edits.

Usage:
    python scripts/generate_tool_modules.py
"""

from __future__ import annotations

import keyword
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "tools"

_PY_TYPE = {
    "string": "str",
    "integer": "int",
    "number": "float",
    "boolean": "bool",
    "array": "list[str]",
}

_RETURN_STUB = (
    '    return {"status": "stub", "tool": "%s", "args": locals()}'
)


def _annotation(p) -> str:
    if p.enum:
        inner = ", ".join(repr(e) for e in p.enum)
        base = f"Literal[{inner}]"
    else:
        base = _PY_TYPE[p.type]
    return base if p.required else f"Optional[{base}]"


def _wrap(text: str, width: int, indent: str) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if len(trial) + len(indent) > width and cur:
            lines.append(indent + cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(indent + cur)
    return lines


def render_function(spec) -> str:
    # Python requires parameters without defaults first.
    params = sorted(spec.params, key=lambda p: not p.required)
    for p in params:
        assert not keyword.iskeyword(p.name), f"{spec.name}: param {p.name} is a keyword"

    sig_parts = []
    for p in params:
        ann = _annotation(p)
        sig_parts.append(f"{p.name}: {ann}" if p.required else f"{p.name}: {ann} = None")
    sig = ", ".join(sig_parts)

    lines: list[str] = []
    meta = [f'domain="{spec.domain}"']
    if spec.confusable_with:
        conf = ", ".join(f'"{c}"' for c in spec.confusable_with)
        meta.append(f"confusable_with=[{conf}]")
    lines.append(f"@tool({', '.join(meta)})")

    head = f"def {spec.name}({sig}) -> dict:"
    if len(head) <= 88:
        lines.append(head)
    else:
        lines.append(f"def {spec.name}(")
        for part in sig_parts:
            lines.append(f"    {part},")
        lines.append(") -> dict:")

    # Google-style docstring: summary line, then Args with one entry per param.
    lines.append('    """' + spec.description)
    if params:
        lines.append("")
        lines.append("    Args:")
        for p in params:
            desc = p.description
            if p.enum:
                desc += " One of: " + ", ".join(p.enum) + "."
            body = _wrap(f"{p.name}: {desc}", 88, "        ")
            lines.append(body[0])
            for extra in body[1:]:
                lines.append("    " + extra)
    lines.append('    """')
    lines.append(_RETURN_STUB % spec.name)
    return "\n".join(lines)


def render_module(domain: str, specs, blurb: str) -> str:
    needs_optional = any(not p.required for s in specs for p in s.params)
    needs_literal = any(p.enum for s in specs for p in s.params)
    typing_imports = [n for n, need in (("Literal", needs_literal), ("Optional", needs_optional)) if need]

    header = [
        f'"""{domain} tools.',
        "",
    ]
    header += _wrap(blurb, 78, "")
    header += [
        "",
        "Every function here is a real Python function. Its docstring is the tool",
        "description the model sees, its Args block supplies per-parameter",
        "descriptions, and its signature supplies the schema. Bodies are stubs:",
        "this project measures which tool gets chosen, not what it would do.",
        '"""',
        "",
        "from __future__ import annotations",
        "",
    ]
    if typing_imports:
        header.append(f"from typing import {', '.join(sorted(typing_imports))}")
        header.append("")
    header.append("from ._registry import tool")
    header.append("")
    header.append("")
    header.append("")
    body = "\n\n\n".join(render_function(s) for s in specs)
    return "\n".join(header) + body + "\n"


def main() -> int:
    import sys

    sys.path.insert(0, str(ROOT))
    from catalog.domains import DOMAIN_DESCRIPTIONS, DOMAINS
    from catalog.domains_ext import DOMAIN_DESCRIPTIONS_EXT, DOMAINS_EXT

    all_domains = {**DOMAINS, **DOMAINS_EXT}
    all_blurbs = {**DOMAIN_DESCRIPTIONS, **DOMAIN_DESCRIPTIONS_EXT}

    OUT.mkdir(exist_ok=True)
    for domain, specs in all_domains.items():
        path = OUT / f"{domain}.py"
        path.write_text(render_module(domain, specs, all_blurbs[domain]), encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}  ({len(specs)} functions)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
