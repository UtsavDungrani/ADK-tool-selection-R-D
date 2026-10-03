"""pagerduty tools.

Incident response and on-call: triggering and resolving incidents, paging
responders, rotation schedules, services, and snoozing.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="pagerduty", confusable_with=["zendesk_create_ticket", "sentry_create_alert_rule"])
def pagerduty_trigger_incident(
    service_id: str,
    title: str,
    urgency: Optional[Literal['low', 'high']] = None,
) -> dict:
    """Trigger a new PagerDuty incident to page the on-call responder immediately.

    Args:
        service_id: Identifier of the affected PagerDuty service.
        title: Short incident title.
        urgency: Incident urgency. One of: low, high.
    """
    return {"status": "stub", "tool": "pagerduty_trigger_incident", "args": locals()}


@tool(domain="pagerduty")
def pagerduty_acknowledge_incident(incident_id: str) -> dict:
    """Acknowledge a PagerDuty incident to signal that someone is working on it.

    Args:
        incident_id: Identifier of the incident.
    """
    return {"status": "stub", "tool": "pagerduty_acknowledge_incident", "args": locals()}


@tool(domain="pagerduty", confusable_with=["sentry_resolve_issue", "jira_transition_issue"])
def pagerduty_resolve_incident(
    incident_id: str,
    resolution: Optional[str] = None,
) -> dict:
    """Mark a PagerDuty incident as resolved once the outage is over.

    Args:
        incident_id: Identifier of the incident.
        resolution: Note describing the resolution.
    """
    return {"status": "stub", "tool": "pagerduty_resolve_incident", "args": locals()}


@tool(domain="pagerduty")
def pagerduty_list_incidents(
    status: Optional[Literal['triggered', 'acknowledged', 'resolved']] = None,
    service_id: Optional[str] = None,
    limit: Optional[int] = None,
) -> dict:
    """List PagerDuty incidents, optionally filtered by status or service.

    Args:
        status: Filter by incident status. One of: triggered, acknowledged, resolved.
        service_id: Restrict to one service.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "pagerduty_list_incidents", "args": locals()}


@tool(domain="pagerduty", confusable_with=["zendesk_list_agents"])
def pagerduty_get_oncall(
    schedule_id: Optional[str] = None,
    at: Optional[str] = None,
) -> dict:
    """Find out which person is currently on call for a PagerDuty schedule.

    Args:
        schedule_id: Identifier of the on-call schedule.
        at: ISO 8601 time to check, defaulting to now.
    """
    return {"status": "stub", "tool": "pagerduty_get_oncall", "args": locals()}


@tool(domain="pagerduty", confusable_with=["gcalendar_create_recurring_event"])
def pagerduty_create_schedule(
    name: str,
    users: list[str],
    rotation: Optional[str] = None,
) -> dict:
    """Create a new PagerDuty on-call rotation schedule.

    Args:
        name: Schedule name.
        users: User identifiers in rotation order.
        rotation: Rotation length, for example weekly.
    """
    return {"status": "stub", "tool": "pagerduty_create_schedule", "args": locals()}


@tool(domain="pagerduty", confusable_with=["slack_invite_to_channel", "gcalendar_invite_attendees"])
def pagerduty_add_responder(incident_id: str, user_id: str) -> dict:
    """Add another responder to an active PagerDuty incident.

    Args:
        incident_id: Identifier of the incident.
        user_id: Identifier of the responder to add.
    """
    return {"status": "stub", "tool": "pagerduty_add_responder", "args": locals()}


@tool(domain="pagerduty", confusable_with=["jira_add_comment", "zendesk_add_comment"])
def pagerduty_add_note(incident_id: str, content: str) -> dict:
    """Add a timeline note to a PagerDuty incident.

    Args:
        incident_id: Identifier of the incident.
        content: Note text.
    """
    return {"status": "stub", "tool": "pagerduty_add_note", "args": locals()}


@tool(domain="pagerduty")
def pagerduty_list_services(limit: Optional[int] = None) -> dict:
    """List the PagerDuty services that incidents can be raised against.

    Args:
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "pagerduty_list_services", "args": locals()}


@tool(domain="pagerduty", confusable_with=["sentry_ignore_issue"])
def pagerduty_snooze_incident(incident_id: str, duration_minutes: int) -> dict:
    """Snooze a PagerDuty incident so it stops paging for a set duration.

    Args:
        incident_id: Identifier of the incident.
        duration_minutes: How long to snooze for, in minutes.
    """
    return {"status": "stub", "tool": "pagerduty_snooze_incident", "args": locals()}
