"""Catalog loading, with catalog size as a first-class experimental parameter.

The headline question of this study is how selection behaves as the catalog
grows. That requires growing the catalog *without* changing the task set --
otherwise accuracy changes are confounded by the tasks getting easier or harder.

TWO KNOBS, DELIBERATELY SEPARATE

  profile   WHICH hand-written tools form the core, and therefore which tasks
            are answerable. Growing the core changes the question set.
              "base" -> 50 tools, the original 5 domains
              "full" -> 100 tools, all 10 domains  (default)

  size      TOTAL catalog size. The core is kept intact and padded with
            generated filler from plausible neighbouring SaaS systems. Filler
            is never a gold answer, so this varies exactly one thing: the
            number of wrong answers the selector has to reject.

Keeping these apart is what makes results comparable. Sweeping `size` at a
fixed `profile` isolates distractor pressure. Changing `profile` is a different
experiment and its numbers are not directly comparable to the other profile's,
because the questions changed -- say so if you report both.

`size` below the core raises rather than truncating. Silently dropping core
tools would invalidate gold labels and produce a quietly meaningless number,
which is worse than a crash.

Filler generation is seeded and deterministic, so runs are reproducible.
"""

from __future__ import annotations

import random

from .domains import ALL_SPECS as BASE_SPECS
from .domains import DOMAIN_DESCRIPTIONS as BASE_DOMAIN_DESCRIPTIONS
from .domains import DOMAINS as BASE_DOMAINS
from .domains_ext import DOMAIN_DESCRIPTIONS_EXT, DOMAINS_EXT, EXT_SPECS
from .schema import Param, StubTool, ToolSpec, build_tools

__all__ = [
    "ALL_SPECS",
    "BASE_SPECS",
    "EXT_SPECS",
    "DOMAINS",
    "DOMAIN_DESCRIPTIONS",
    "PROFILES",
    "Param",
    "ToolSpec",
    "StubTool",
    "build_tools",
    "load_catalog",
    "core_names",
    "CORE_NAMES",
]

# The full 100-tool core: 10 domains x 10 tools.
ALL_SPECS: list[ToolSpec] = list(BASE_SPECS) + list(EXT_SPECS)

DOMAINS: dict[str, list[ToolSpec]] = {**BASE_DOMAINS, **DOMAINS_EXT}

DOMAIN_DESCRIPTIONS: dict[str, str] = {
    **BASE_DOMAIN_DESCRIPTIONS,
    **DOMAIN_DESCRIPTIONS_EXT,
}

PROFILES: dict[str, list[ToolSpec]] = {
    "base": list(BASE_SPECS),   # 50  -- original 5 domains
    "full": list(ALL_SPECS),    # 100 -- all 10 domains
}

#: Names of every hand-written tool across all profiles. Used by task
#: validation to confirm no gold label points at generated filler.
CORE_NAMES: frozenset[str] = frozenset(s.name for s in ALL_SPECS)


def core_names(profile: str = "full") -> frozenset[str]:
    return frozenset(s.name for s in PROFILES[profile])


# Filler vocabulary. Deliberately chosen to be plausible *neighbours* of the
# core domains. Padding with obviously unrelated tools (weather, horoscopes)
# would make the scaling curve look far better than reality, because a
# retriever rejects them trivially.
#
# Systems promoted into the hand-written core (notion, zendesk, pagerduty,
# stripe, sentry) were REMOVED from this list. Leaving them would generate
# filler sharing a namespace with real tools, so a hierarchical router that
# correctly picked "sentry" would be handed a mix of real and junk tools and
# scored as if it had failed.
_FILLER_SYSTEMS: dict[str, str] = {
    "confluence": "Confluence wiki",
    "linear": "Linear issue tracker",
    "asana": "Asana project tracker",
    "gitlab": "GitLab repository host",
    "salesforce": "Salesforce CRM",
    "hubspot": "HubSpot CRM",
    "datadog": "Datadog observability platform",
    "figma": "Figma design tool",
    "zoom": "Zoom meeting platform",
    "onedrive": "OneDrive file storage",
    "dropbox": "Dropbox file storage",
    "outlook": "Outlook mail client",
    "teams": "Microsoft Teams chat",
    "trello": "Trello kanban board",
    "bitbucket": "Bitbucket repository host",
    "intercom": "Intercom messaging platform",
    "airtable": "Airtable database",
    "miro": "Miro whiteboard",
    "box": "Box file storage",
    "monday": "Monday work tracker",
    "clickup": "ClickUp work tracker",
    "freshdesk": "Freshdesk support desk",
    "opsgenie": "Opsgenie alerting platform",
    "grafana": "Grafana dashboards",
    "newrelic": "New Relic observability platform",
}

# (verb, slot, description template) triples.
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


def _filler_spec(system: str, sys_label: str, action, obj: str) -> ToolSpec:
    verb, _slot, template = action
    return ToolSpec(
        name=f"{system}_{verb}_{obj}",
        domain=system,
        description=template.format(sys=sys_label, obj=obj),
        params=(
            Param("id", "string", f"Identifier of the {obj}.", required=False),
            Param("query", "string", "Free-text filter.", required=False),
            Param("limit", "integer", "Maximum number of results.", required=False),
        ),
    )


def pad_to(core: list[ToolSpec], n: int, seed: int = 0) -> list[ToolSpec]:
    """Grow `core` to exactly `n` tools using deterministic filler."""
    if n < len(core):
        raise ValueError(
            f"catalog size {n} is below the core size {len(core)}. Gold-labelled "
            f"tools must always be present -- use a smaller profile instead "
            f"(profiles: {', '.join(f'{k}={len(v)}' for k, v in PROFILES.items())})."
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

    for sysname, syslabel, action, obj in combos:
        if len(out) >= n:
            break
        spec = _filler_spec(sysname, syslabel, action, obj)
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


def load_catalog(
    size: int | None = None, seed: int = 0, profile: str = "full"
) -> list[ToolSpec]:
    """Return the catalog at a given size.

    Args:
        size: Total tool count. None returns the profile's core unpadded.
        seed: Seed for deterministic filler generation.
        profile: Which hand-written core to use -- "base" (50) or "full" (100).
    """
    if profile not in PROFILES:
        raise ValueError(f"unknown profile {profile!r}; choose from {sorted(PROFILES)}")
    core = list(PROFILES[profile])
    if size is None or size == len(core):
        return core
    return pad_to(core, size, seed=seed)
