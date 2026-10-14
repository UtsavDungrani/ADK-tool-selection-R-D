"""opsgenie tools.

Opsgenie alerting and on-call: raising and closing alerts, acknowledgement,
on-call lookup, rotation schedules, responders, notes, snoozing, and escalation.

Deliberately close to `pagerduty`: the two are near drop-in replacements for
each other, which makes "page the on-call engineer" a query with two defensible
destinations. That collision is the point.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="opsgenie", confusable_with=["pagerduty_trigger_incident", "sentry_create_alert_rule"])
def opsgenie_create_alert(
    message: str,
    priority: Optional[Literal['P1', 'P2', 'P3', 'P4', 'P5']] = None,
    team: Optional[str] = None,
    description: Optional[str] = None,
) -> dict:
    """Raise an Opsgenie alert that pages whoever is currently on call.

    Args:
        message: Short alert message shown on the page.
        priority: Alert priority. One of: P1, P2, P3, P4, P5.
        team: Team the alert should be routed to.
        description: Longer description of what is wrong.
    """
    return {"status": "stub", "tool": "opsgenie_create_alert", "args": locals()}


@tool(domain="opsgenie", confusable_with=["pagerduty_acknowledge_incident", "newrelic_acknowledge_violation"])
def opsgenie_acknowledge_alert(alert_id: str, note: Optional[str] = None) -> dict:
    """Acknowledge an Opsgenie alert to stop it escalating while you investigate.

    Args:
        alert_id: Identifier of the alert.
        note: Note about who picked it up.
    """
    return {"status": "stub", "tool": "opsgenie_acknowledge_alert", "args": locals()}


@tool(domain="opsgenie", confusable_with=["pagerduty_resolve_incident", "sentry_resolve_issue"])
def opsgenie_close_alert(alert_id: str, note: Optional[str] = None) -> dict:
    """Close a resolved Opsgenie alert.

    Args:
        alert_id: Identifier of the alert to close.
        note: Note on how it was resolved.
    """
    return {"status": "stub", "tool": "opsgenie_close_alert", "args": locals()}


@tool(domain="opsgenie", confusable_with=["pagerduty_list_incidents", "datadog_list_monitors"])
def opsgenie_list_alerts(
    status: Optional[Literal['open', 'acknowledged', 'closed']] = None,
    team: Optional[str] = None,
    limit: Optional[int] = None,
) -> dict:
    """List Opsgenie alerts and the state each one is in.

    Args:
        status: Filter by alert status. One of: open, acknowledged, closed.
        team: Restrict results to alerts routed to this team.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "opsgenie_list_alerts", "args": locals()}


@tool(domain="opsgenie", confusable_with=["pagerduty_get_oncall"])
def opsgenie_get_on_call(schedule: Optional[str] = None, at_time: Optional[str] = None) -> dict:
    """Look up who is on call in Opsgenie right now or at a given time.

    Args:
        schedule: Rotation schedule to check.
        at_time: ISO 8601 time to check; now when omitted.
    """
    return {"status": "stub", "tool": "opsgenie_get_on_call", "args": locals()}


@tool(domain="opsgenie", confusable_with=["pagerduty_create_schedule"])
def opsgenie_create_schedule(
    name: str,
    participants: list[str],
    rotation_length: Optional[Literal['daily', 'weekly', 'custom']] = None,
    timezone: Optional[str] = None,
) -> dict:
    """Create an Opsgenie on-call rotation schedule.

    Args:
        name: Name of the schedule.
        participants: Users taking part in the rotation.
        rotation_length: How often the rotation turns over. One of: daily, weekly, custom.
        timezone: Timezone the rotation is anchored to.
    """
    return {"status": "stub", "tool": "opsgenie_create_schedule", "args": locals()}


@tool(domain="opsgenie", confusable_with=["pagerduty_add_responder"])
def opsgenie_add_responder(alert_id: str, responder: str, note: Optional[str] = None) -> dict:
    """Pull another person into an Opsgenie alert as an additional responder.

    Args:
        alert_id: Identifier of the alert.
        responder: User or team to add.
        note: Why they are being brought in.
    """
    return {"status": "stub", "tool": "opsgenie_add_responder", "args": locals()}


@tool(domain="opsgenie", confusable_with=["pagerduty_add_note", "intercom_add_note"])
def opsgenie_add_note(alert_id: str, note: str) -> dict:
    """Append a timeline note to an Opsgenie alert.

    Args:
        alert_id: Identifier of the alert.
        note: Note text to append.
    """
    return {"status": "stub", "tool": "opsgenie_add_note", "args": locals()}


@tool(domain="opsgenie", confusable_with=["pagerduty_snooze_incident", "datadog_mute_monitor"])
def opsgenie_snooze_alert(alert_id: str, until: str, note: Optional[str] = None) -> dict:
    """Snooze an Opsgenie alert so it stops notifying until a given time.

    Args:
        alert_id: Identifier of the alert.
        until: ISO 8601 time when notifications should resume.
        note: Why the alert is being snoozed.
    """
    return {"status": "stub", "tool": "opsgenie_snooze_alert", "args": locals()}


@tool(domain="opsgenie", confusable_with=["zendesk_escalate_ticket", "freshdesk_escalate_ticket"])
def opsgenie_escalate_alert(alert_id: str, escalation: str, reason: Optional[str] = None) -> dict:
    """Push an unanswered Opsgenie alert up its escalation chain.

    Args:
        alert_id: Identifier of the alert to escalate.
        escalation: Escalation policy or team to escalate to.
        reason: Why the alert is being escalated.
    """
    return {"status": "stub", "tool": "opsgenie_escalate_alert", "args": locals()}
