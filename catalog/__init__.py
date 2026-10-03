"""Catalog loading, with catalog size as a first-class experimental parameter.

The headline question of this study is how selection behaves as the catalog
grows. That requires growing the catalog *without* changing the task set --
otherwise accuracy changes are confounded by the tasks getting easier or harder.

The approach:

  - The 50 hand-written tools in `domains.py` are the **core**. Every gold
    answer in the task set is one of these. The core never changes.
  - `pad_to(n)` generates additional **filler** tools from realistic SaaS
    templates. Filler tools are distractors by construction: a filler is never
    the correct answer to any task.

So sweeping 50 -> 100 -> 200 -> 400 varies exactly one thing -- the number of
wrong answers the selector has to reject -- while the questions stay fixed.
That is what makes the resulting curve interpretable.

Filler generation is seeded and deterministic, so runs are reproducible.
"""

from __future__ import annotations

import random

from .domains import ALL_SPECS, DOMAIN_DESCRIPTIONS, DOMAINS
from .schema import Param, StubTool, ToolSpec, build_tools

__all__ = [
    "ALL_SPECS",
    "DOMAINS",
    "DOMAIN_DESCRIPTIONS",
    "Param",
    "ToolSpec",
    "StubTool",
    "build_tools",
    "load_catalog",
    "CORE_NAMES",
]

CORE_NAMES: frozenset[str] = frozenset(s.name for s in ALL_SPECS)

# Filler vocabulary. Deliberately chosen to be plausible *neighbours* of the
# core domains. Padding with obviously unrelated tools (weather, horoscopes)
# would make the scaling curve look far better than reality, because a
# retriever rejects them trivially.
_FILLER_SYSTEMS: dict[str, str] = {
    "notion": "Notion workspace",
    "confluence": "Confluence wiki",
    "linear": "Linear issue tracker",
    "asana": "Asana project tracker",
    "gitlab": "GitLab repository host",
    "zendesk": "Zendesk support desk",
    "pagerduty": "PagerDuty on-call system",
    "salesforce": "Salesforce CRM",
    "hubspot": "HubSpot CRM",
    "stripe": "Stripe payments platform",
    "datadog": "Datadog observability platform",
    "sentry": "Sentry error tracker",
    "figma": "Figma design tool",
    "zoom": "Zoom meeting platform",
    "onedrive": "OneDrive file storage",
    "dropbox": "Dropbox file storage",
    "outlook": "Outlook mail client",
    "teams": "Microsoft Teams chat",
    "trello": "Trello kanban board",
    "bitbucket": "Bitbucket repository host",
}

# (verb, object, description template) triples.
_FILLER_ACTIONS: list[tuple[str, str, str]] = [
    ("create", "record", "Create a new {obj} record in {sys}."),
    ("update", "record", "Update the fields of an existing {obj} record in {sys}."),
    ("delete", "record", "Delete a {obj} record from {sys}."),
    ("list", "records", "List {obj} records available in {sys}."),
    ("search", "records", "Search {obj} records in {sys} by free-text query."),
    ("get", "record", "Fetch a single {obj} record from {sys} by identifier."),
    ("archive", "record", "Archive a {obj} record in {sys} without deleting it."),
    ("assign", "owner", "Assign an owner to a {obj} record in {sys}."),
    ("export", "report", "Export a {obj} report from {sys} to a downloadable file."),
    ("list", "activity", "List recent {obj} activity events recorded in {sys}."),
]

_FILLER_OBJECTS = [
    "page", "ticket", "task", "comment", "attachment", "label",
    "webhook", "template", "dashboard", "notification",
]


def _filler_spec(system: str, sys_label: str, action, obj: str, idx: int) -> ToolSpec:
    verb, slot, template = action
    name = f"{system}_{verb}_{obj}"
    return ToolSpec(
        name=name,
        domain=system,
        description=template.format(sys=sys_label, obj=obj),
        params=(
            Param("id", "string", f"Identifier of the {obj}.", required=False),
            Param("query", "string", "Free-text filter.", required=False),
            Param("limit", "integer", "Maximum number of results.", required=False),
        ),
    )


def pad_to(core: list[ToolSpec], n: int, seed: int = 0) -> list[ToolSpec]:
    """Grow `core` to exactly `n` tools using deterministic filler.

    Raises if `n` is smaller than the core -- silently dropping core tools would
    invalidate the gold labels.
    """
    if n < len(core):
        raise ValueError(
            f"catalog size {n} is below the core size {len(core)}; "
            "gold-labelled tools must always be present"
        )
    out = list(core)
    seen = {s.name for s in core}
    rng = random.Random(seed)

    combos = [
        (sysname, syslabel, action, obj)
        for sysname, syslabel in _FILLER_SYSTEMS.items()
        for action in _FILLER_ACTIONS
        for obj in _FILLER_OBJECTS
    ]
    rng.shuffle(combos)

    for i, (sysname, syslabel, action, obj) in enumerate(combos):
        if len(out) >= n:
            break
        spec = _filler_spec(sysname, syslabel, action, obj, i)
        if spec.name in seen:
            continue
        seen.add(spec.name)
        out.append(spec)

    if len(out) < n:
        raise ValueError(
            f"filler vocabulary exhausted at {len(out)} tools; cannot reach {n}. "
            "Add systems or objects to _FILLER_SYSTEMS / _FILLER_OBJECTS."
        )
    return out


def load_catalog(size: int | None = None, seed: int = 0) -> list[ToolSpec]:
    """Return the catalog at a given size.

    Args:
        size: Total tool count. None or 50 returns the hand-written core only.
        seed: Seed for deterministic filler generation.
    """
    core = list(ALL_SPECS)
    if size is None or size == len(core):
        return core
    return pad_to(core, size, seed=seed)
