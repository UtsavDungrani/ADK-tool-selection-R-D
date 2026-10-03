"""gcalendar tools.

Scheduling: calendar events, recurring meetings, availability lookup, attendee
invitations, meeting rooms, and out-of-office.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Optional

from ._registry import tool


@tool(domain="gcalendar", confusable_with=["gcalendar_create_recurring_event"])
def gcalendar_create_event(
    title: str,
    start: str,
    end: str,
    attendees: Optional[list[str]] = None,
) -> dict:
    """Create a new calendar event at a fixed date and time.

    Args:
        title: Event title.
        start: ISO 8601 start datetime.
        end: ISO 8601 end datetime.
        attendees: Email addresses to invite.
    """
    return {"status": "stub", "tool": "gcalendar_create_event", "args": locals()}


@tool(domain="gcalendar", confusable_with=["gcalendar_find_free_slots"])
def gcalendar_list_events(
    start_date: str,
    end_date: str,
    limit: Optional[int] = None,
) -> dict:
    """List calendar events occurring within a date range.

    Args:
        start_date: ISO 8601 range start.
        end_date: ISO 8601 range end.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "gcalendar_list_events", "args": locals()}


@tool(domain="gcalendar", confusable_with=["gcalendar_list_events", "gcalendar_check_room_availability"])
def gcalendar_find_free_slots(
    attendees: list[str],
    duration_minutes: int,
    search_until: Optional[str] = None,
) -> dict:
    """Find open time slots when all listed people are available to meet.

    Args:
        attendees: Email addresses to check availability for.
        duration_minutes: Required meeting length in minutes.
        search_until: ISO 8601 date to search up to.
    """
    return {"status": "stub", "tool": "gcalendar_find_free_slots", "args": locals()}


@tool(domain="gcalendar")
def gcalendar_update_event(
    event_id: str,
    start: Optional[str] = None,
    title: Optional[str] = None,
) -> dict:
    """Change the time, title, or location of an existing calendar event.

    Args:
        event_id: Identifier of the event to update.
        start: New ISO 8601 start datetime.
        title: New event title.
    """
    return {"status": "stub", "tool": "gcalendar_update_event", "args": locals()}


@tool(domain="gcalendar")
def gcalendar_cancel_event(event_id: str, notify: Optional[bool] = None) -> dict:
    """Cancel a calendar event and notify its attendees.

    Args:
        event_id: Identifier of the event to cancel.
        notify: Whether to email attendees.
    """
    return {"status": "stub", "tool": "gcalendar_cancel_event", "args": locals()}


@tool(domain="gcalendar", confusable_with=["slack_invite_to_channel"])
def gcalendar_invite_attendees(event_id: str, attendees: list[str]) -> dict:
    """Add additional attendees to an existing calendar event.

    Args:
        event_id: Identifier of the event.
        attendees: Email addresses to add.
    """
    return {"status": "stub", "tool": "gcalendar_invite_attendees", "args": locals()}


@tool(domain="gcalendar", confusable_with=["gcalendar_create_event"])
def gcalendar_create_recurring_event(title: str, start: str, recurrence: str) -> dict:
    """Create a repeating calendar event such as a weekly standup.

    Args:
        title: Event title.
        start: ISO 8601 start datetime of the first occurrence.
        recurrence: Recurrence rule, e.g. RRULE:FREQ=WEEKLY;BYDAY=MO.
    """
    return {"status": "stub", "tool": "gcalendar_create_recurring_event", "args": locals()}


@tool(domain="gcalendar")
def gcalendar_get_event_details(event_id: str) -> dict:
    """Retrieve the full details of one calendar event by its identifier.

    Args:
        event_id: Identifier of the event.
    """
    return {"status": "stub", "tool": "gcalendar_get_event_details", "args": locals()}


@tool(domain="gcalendar", confusable_with=["slack_set_status"])
def gcalendar_set_out_of_office(
    start_date: str,
    end_date: str,
    message: Optional[str] = None,
) -> dict:
    """Mark a date range as out of office and auto-decline meeting invitations.

    Args:
        start_date: ISO 8601 first day out.
        end_date: ISO 8601 last day out.
        message: Auto-decline message.
    """
    return {"status": "stub", "tool": "gcalendar_set_out_of_office", "args": locals()}


@tool(domain="gcalendar", confusable_with=["gcalendar_find_free_slots"])
def gcalendar_check_room_availability(room: str, start: str, end: str) -> dict:
    """Check whether a bookable meeting room is free during a time window.

    Args:
        room: Room name or resource ID.
        start: ISO 8601 window start.
        end: ISO 8601 window end.
    """
    return {"status": "stub", "tool": "gcalendar_check_room_availability", "args": locals()}
