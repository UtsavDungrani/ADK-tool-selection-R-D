"""One-line blurb per domain, used as the hierarchical router's menu.

Kept roughly uniform in length so the level-1 routing choice is not biased
by one domain simply having more text than another.
"""

from __future__ import annotations

DOMAIN_DESCRIPTIONS: dict[str, str] = {
    "github": (
        "Source code hosting: repositories, branches, issues, pull requests, "
        "code search, CI workflow runs, and collaborator access."
    ),
    "jira": (
        "Project and issue tracking: tickets, subtasks, workflow transitions, "
        "assignees, sprints, boards, and worklogs."
    ),
    "slack": (
        "Team chat: channel and direct messages, channel management, message "
        "search, reactions, file uploads, and user status."
    ),
    "gcalendar": (
        "Scheduling: calendar events, recurring meetings, availability "
        "lookup, attendee invitations, meeting rooms, and out-of-office."
    ),
    "gdrive": (
        "Cloud file storage: file and folder search, listing, upload, move, "
        "copy, export, deletion, and sharing permissions."
    ),
    "notion": (
        "Workspace docs and wikis: pages, databases, blocks, comments, "
        "duplication, archiving, and sharing permissions."
    ),
    "zendesk": (
        "Customer support desk: tickets raised by customers, replies and "
        "internal notes, assignment, status, tags, views, and escalation."
    ),
    "pagerduty": (
        "Incident response and on-call: triggering and resolving incidents, "
        "paging responders, rotation schedules, services, and snoozing."
    ),
    "stripe": (
        "Payments and billing: customers, invoices, charges, refunds, "
        "subscriptions, payment links, and account balance."
    ),
    "sentry": (
        "Application error tracking: recorded exceptions, stack traces, "
        "resolution and assignment, alert rules, releases, and tracker links."
    ),
}
