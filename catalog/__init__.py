"""Catalog assembly: profiles, scaling, and filler generation.

The tools themselves live in `tools/` as real Python functions. This package
only decides *which* of them (plus how much generated filler) forms the catalog
for a given run.

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

Filler generation is seeded and deterministic, so runs are reproducible. Filler
tools are built as real functions by `tools._filler`, introspected through the
same code path as hand-written ones -- a parallel spec-only path would mean the
thing being scaled is not the thing being measured.
"""

from __future__ import annotations

import random

from tools import ALL_SPECS as _ALL_SPECS
from tools import DOMAINS as _DOMAINS
from tools._adk import FunctionBackedTool, build_tools
from tools._domains import DOMAIN_DESCRIPTIONS
from tools._filler import make_filler_spec
from tools._spec import Param, ToolSpec

__all__ = [
    "ALL_SPECS",
    "DOMAINS",
    "DOMAIN_DESCRIPTIONS",
    "PROFILES",
    "BASE_DOMAINS",
    "EXT_DOMAINS",
    "Param",
    "ToolSpec",
    "FunctionBackedTool",
    "build_tools",
    "load_catalog",
    "core_names",
    "CORE_NAMES",
]

#: The 5 domains the study started with, and the 5 added when it scaled to 100.
BASE_DOMAINS = ("github", "jira", "slack", "gcalendar", "gdrive")
EXT_DOMAINS = ("notion", "zendesk", "pagerduty", "stripe", "sentry")

# Canonical order: base domains first, then extended, each in the order the
# study introduced them. `tools/` imports its modules alphabetically, but
# catalog order is not cosmetic -- BM25 breaks score ties by catalog index, so
# a reordering would shift results for a reason unrelated to the experiment.
_DOMAIN_ORDER = BASE_DOMAINS + EXT_DOMAINS

ALL_SPECS: list[ToolSpec] = [s for d in _DOMAIN_ORDER for s in _DOMAINS[d]]
DOMAINS: dict[str, list[ToolSpec]] = {d: list(_DOMAINS[d]) for d in _DOMAIN_ORDER}

assert len(ALL_SPECS) == len(_ALL_SPECS), (
    "a domain is missing from _DOMAIN_ORDER; every registered domain must be listed"
)

PROFILES: dict[str, list[ToolSpec]] = {
    "base": [s for s in ALL_SPECS if s.domain in BASE_DOMAINS],   # 50
    "full": list(ALL_SPECS),                                      # 100
}

#: Names of every hand-written tool. Used by task validation to confirm no gold
#: label points at generated filler.
CORE_NAMES: frozenset[str] = frozenset(s.name for s in ALL_SPECS)


def core_names(profile: str = "full") -> frozenset[str]:
    return frozenset(s.name for s in PROFILES[profile])


# Filler vocabulary. Deliberately chosen to be plausible *neighbours* of the
# core domains. Padding with obviously unrelated tools (weather, horoscopes)
# would make the scaling curve look far better than reality, because a
# retriever rejects them trivially.
#
# Systems promoted into the hand-written core (notion, zendesk, pagerduty,
# stripe, sentry) are deliberately absent. Leaving them would generate filler
# sharing a namespace with real tools, so a hierarchical router that correctly
# picked "sentry" would be handed a mix of real and junk tools and scored as if
# it had failed.
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

_FILLER_ACTIONS: list[tuple[str, str]] = [
    ("create", "Create a new {obj} record in {sys}."),
    ("update", "Update the fields of an existing {obj} record in {sys}."),
    ("delete", "Delete a {obj} record from {sys}."),
    ("list", "List {obj} records available in {sys}."),
    ("search", "Search {obj} records in {sys} by free-text query."),
    ("get", "Fetch a single {obj} record from {sys} by identifier."),
    ("archive", "Archive a {obj} record in {sys} without deleting it."),
    ("assign", "Assign an owner to a {obj} record in {sys}."),
    ("export", "Export a {obj} report from {sys} to a downloadable file."),
    ("audit", "List recent {obj} activity events recorded in {sys}."),
]

_FILLER_OBJECTS = [
    "page", "ticket", "task", "comment", "attachment", "label",
    "webhook", "template", "dashboard", "notification",
]


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
        (sysname, syslabel, verb, template, obj)
        for sysname, syslabel in _FILLER_SYSTEMS.items()
        for verb, template in _FILLER_ACTIONS
        for obj in _FILLER_OBJECTS
    ]
    rng.shuffle(combos)

    for sysname, syslabel, verb, template, obj in combos:
        if len(out) >= n:
            break
        name = f"{sysname}_{verb}_{obj}"
        if name in seen:
            continue
        seen.add(name)
        out.append(
            make_filler_spec(
                name=name,
                domain=sysname,
                description=template.format(sys=syslabel, obj=obj),
                obj=obj,
            )
        )

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
