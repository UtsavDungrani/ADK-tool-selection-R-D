"""Tool catalog: 350 real Python functions across 35 domains.

Importing this package imports every domain module, which runs the @tool
decorators and populates the registry. `ALL_SPECS` is the introspected view
that the selection strategies consume.
"""

from __future__ import annotations

# Imported for their decorator side effects: each module registers its tools.
from . import airtable as airtable  # noqa: F401
from . import asana as asana  # noqa: F401
from . import bitbucket as bitbucket  # noqa: F401
from . import box as box  # noqa: F401
from . import confluence as confluence  # noqa: F401
from . import datadog as datadog  # noqa: F401
from . import dropbox as dropbox  # noqa: F401
from . import figma as figma  # noqa: F401
from . import freshdesk as freshdesk  # noqa: F401
from . import gcalendar as gcalendar  # noqa: F401
from . import gdrive as gdrive  # noqa: F401
from . import github as github  # noqa: F401
from . import gitlab as gitlab  # noqa: F401
from . import gmail as gmail  # noqa: F401
from . import grafana as grafana  # noqa: F401
from . import hubspot as hubspot  # noqa: F401
from . import intercom as intercom  # noqa: F401
from . import jira as jira  # noqa: F401
from . import linear as linear  # noqa: F401
from . import newrelic as newrelic  # noqa: F401
from . import notion as notion  # noqa: F401
from . import okta as okta  # noqa: F401
from . import onedrive as onedrive  # noqa: F401
from . import opsgenie as opsgenie  # noqa: F401
from . import outlook as outlook  # noqa: F401
from . import pagerduty as pagerduty  # noqa: F401
from . import salesforce as salesforce  # noqa: F401
from . import sentry as sentry  # noqa: F401
from . import sharepoint as sharepoint  # noqa: F401
from . import slack as slack  # noqa: F401
from . import stripe as stripe  # noqa: F401
from . import teams as teams  # noqa: F401
from . import trello as trello  # noqa: F401
from . import zendesk as zendesk  # noqa: F401
from . import zoom as zoom  # noqa: F401
from ._registry import (
    registered_functions,
    registered_specs,
    spec_from_function,
    tool,
)
from ._spec import Param, ToolSpec

#: Every hand-written tool, as introspected specs.
ALL_SPECS: list[ToolSpec] = registered_specs()

#: Domain -> specs.
DOMAINS: dict[str, list[ToolSpec]] = {}
for _s in ALL_SPECS:
    DOMAINS.setdefault(_s.domain, []).append(_s)

# `confusable_with` is error-analysis metadata, never read by a strategy, so a
# typo in one would not fail a run -- it would quietly reclassify a designed
# trap as an unrelated miss. Catch it at import instead.
_NAMES = {_s.name for _s in ALL_SPECS}
_DANGLING = sorted(
    f"{_s.name} -> {_c}"
    for _s in ALL_SPECS
    for _c in _s.confusable_with
    if _c not in _NAMES
)
assert not _DANGLING, (
    "confusable_with points at tools that do not exist: " + ", ".join(_DANGLING)
)

__all__ = [
    "ALL_SPECS",
    "DOMAINS",
    "Param",
    "ToolSpec",
    "tool",
    "spec_from_function",
    "registered_functions",
    "registered_specs",
]
