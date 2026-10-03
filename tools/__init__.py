"""Tool catalog: 100 real Python functions across 10 domains.

Importing this package imports every domain module, which runs the @tool
decorators and populates the registry. `ALL_SPECS` is the introspected view
that the selection strategies consume.
"""

from __future__ import annotations

# Imported for their decorator side effects: each module registers its tools.
from . import gcalendar as gcalendar  # noqa: F401
from . import gdrive as gdrive  # noqa: F401
from . import github as github  # noqa: F401
from . import jira as jira  # noqa: F401
from . import notion as notion  # noqa: F401
from . import pagerduty as pagerduty  # noqa: F401
from . import sentry as sentry  # noqa: F401
from . import slack as slack  # noqa: F401
from . import stripe as stripe  # noqa: F401
from . import zendesk as zendesk  # noqa: F401
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
