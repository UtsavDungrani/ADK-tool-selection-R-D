"""sentry tools.

Application error tracking: recorded exceptions, stack traces, resolution and
assignment, alert rules, releases, and tracker links.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="sentry", confusable_with=["github_search_issues", "jira_search_issues"])
def sentry_search_issues(
    query: str,
    project: Optional[str] = None,
    status: Optional[Literal['unresolved', 'resolved', 'ignored']] = None,
    limit: Optional[int] = None,
) -> dict:
    """Search Sentry for recorded application errors matching a query.

    Args:
        query: Free-text search query.
        project: Sentry project slug.
        status: Filter by issue status. One of: unresolved, resolved, ignored.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "sentry_search_issues", "args": locals()}


@tool(domain="sentry")
def sentry_get_issue_details(issue_id: str) -> dict:
    """Retrieve the stack trace and metadata for one Sentry error issue.

    Args:
        issue_id: Identifier of the Sentry issue.
    """
    return {"status": "stub", "tool": "sentry_get_issue_details", "args": locals()}


@tool(domain="sentry", confusable_with=["pagerduty_resolve_incident", "jira_transition_issue"])
def sentry_resolve_issue(issue_id: str, in_release: Optional[str] = None) -> dict:
    """Mark a Sentry error issue as resolved.

    Args:
        issue_id: Identifier of the Sentry issue.
        in_release: Release version the fix ships in.
    """
    return {"status": "stub", "tool": "sentry_resolve_issue", "args": locals()}


@tool(domain="sentry", confusable_with=["jira_assign_issue", "zendesk_assign_ticket"])
def sentry_assign_issue(issue_id: str, assignee: str) -> dict:
    """Assign a Sentry error issue to a developer to investigate.

    Args:
        issue_id: Identifier of the Sentry issue.
        assignee: Username or email of the assignee.
    """
    return {"status": "stub", "tool": "sentry_assign_issue", "args": locals()}


@tool(domain="sentry", confusable_with=["pagerduty_snooze_incident"])
def sentry_ignore_issue(issue_id: str, duration_minutes: Optional[int] = None) -> dict:
    """Ignore a Sentry error issue so it stops appearing in the unresolved feed.

    Args:
        issue_id: Identifier of the Sentry issue.
        duration_minutes: Ignore for this long, or omit for forever.
    """
    return {"status": "stub", "tool": "sentry_ignore_issue", "args": locals()}


@tool(domain="sentry")
def sentry_list_events(issue_id: str, limit: Optional[int] = None) -> dict:
    """List individual error events recorded under a Sentry issue.

    Args:
        issue_id: Identifier of the Sentry issue.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "sentry_list_events", "args": locals()}


@tool(domain="sentry", confusable_with=["pagerduty_trigger_incident"])
def sentry_create_alert_rule(project: str, name: str, threshold: int) -> dict:
    """Create a Sentry alert rule that notifies a channel when error rates spike.

    Args:
        project: Sentry project slug.
        name: Alert rule name.
        threshold: Event count that triggers the alert.
    """
    return {"status": "stub", "tool": "sentry_create_alert_rule", "args": locals()}


@tool(domain="sentry", confusable_with=["jira_create_issue", "github_create_issue"])
def sentry_link_to_tracker(issue_id: str, external_key: str) -> dict:
    """Link a Sentry error issue to an existing ticket in an external issue tracker.

    Args:
        issue_id: Identifier of the Sentry issue.
        external_key: Key or URL of the external ticket.
    """
    return {"status": "stub", "tool": "sentry_link_to_tracker", "args": locals()}


@tool(domain="sentry")
def sentry_list_releases(project: str, limit: Optional[int] = None) -> dict:
    """List deployed releases tracked in Sentry with their error counts.

    Args:
        project: Sentry project slug.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "sentry_list_releases", "args": locals()}


@tool(domain="sentry", confusable_with=["jira_add_comment", "github_add_comment", "pagerduty_add_note"])
def sentry_add_comment(issue_id: str, body: str) -> dict:
    """Add a comment to a Sentry error issue.

    Args:
        issue_id: Identifier of the Sentry issue.
        body: Comment text.
    """
    return {"status": "stub", "tool": "sentry_add_comment", "args": locals()}
