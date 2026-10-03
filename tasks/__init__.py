"""Task set, selectable by catalog profile.

A task is only answerable if its gold tool is in the catalog, so the task set
must track the profile. `tasks_for` is the single place that mapping lives --
never filter tasks ad hoc at a call site, or two runs will silently score
different question sets and their numbers will not be comparable.
"""

from __future__ import annotations

from .tasks import TASKS as TASKS_BASE
from .tasks import TIERS, Task
from .tasks_ext import TASKS_EXT

__all__ = [
    "TASKS",
    "TASKS_BASE",
    "TASKS_EXT",
    "TIERS",
    "Task",
    "tasks_for",
    "by_tier",
]

#: Every task across all profiles (120).
TASKS: list[Task] = list(TASKS_BASE) + list(TASKS_EXT)

_BY_PROFILE: dict[str, list[Task]] = {
    "base": list(TASKS_BASE),  # 60  -- answerable with the 50-tool core
    "full": list(TASKS),       # 120 -- answerable with the 100-tool core
}


def tasks_for(profile: str = "full") -> list[Task]:
    if profile not in _BY_PROFILE:
        raise ValueError(
            f"unknown profile {profile!r}; choose from {sorted(_BY_PROFILE)}"
        )
    return list(_BY_PROFILE[profile])


def by_tier(tier: str, profile: str = "full") -> list[Task]:
    return [t for t in tasks_for(profile) if t.tier == tier]
