"""zoom tools.

Video conferencing: scheduled meetings, invitations, cancellations, cloud
recordings, transcripts, participant reports, and webinars.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="zoom", confusable_with=["gcalendar_create_event", "teams_schedule_meeting"])
def zoom_create_meeting(
    topic: str,
    start_time: str,
    duration_minutes: Optional[int] = None,
    passcode: Optional[str] = None,
    waiting_room: Optional[bool] = None,
) -> dict:
    """Schedule a Zoom meeting and generate its join link.

    Args:
        topic: Meeting topic shown to participants.
        start_time: Start time in ISO 8601 form.
        duration_minutes: Meeting length in minutes.
        passcode: Passcode participants must enter to join.
        waiting_room: Hold participants in a waiting room until admitted.
    """
    return {"status": "stub", "tool": "zoom_create_meeting", "args": locals()}


@tool(domain="zoom", confusable_with=["gcalendar_list_events"])
def zoom_list_meetings(
    user: Optional[str] = None,
    meeting_type: Optional[Literal['scheduled', 'live', 'upcoming']] = None,
    limit: Optional[int] = None,
) -> dict:
    """List Zoom meetings scheduled on an account.

    Args:
        user: Email of the host whose meetings to list.
        meeting_type: Which meetings to return. One of: scheduled, live, upcoming.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "zoom_list_meetings", "args": locals()}


@tool(domain="zoom", confusable_with=["gcalendar_update_event"])
def zoom_update_meeting(
    meeting_id: str,
    topic: Optional[str] = None,
    start_time: Optional[str] = None,
    duration_minutes: Optional[int] = None,
) -> dict:
    """Change the time or topic of an already scheduled Zoom meeting.

    Args:
        meeting_id: Identifier of the meeting to update.
        topic: New meeting topic.
        start_time: New start time in ISO 8601 form.
        duration_minutes: New meeting length in minutes.
    """
    return {"status": "stub", "tool": "zoom_update_meeting", "args": locals()}


@tool(domain="zoom", confusable_with=["gcalendar_cancel_event"])
def zoom_cancel_meeting(meeting_id: str, notify_participants: Optional[bool] = None) -> dict:
    """Cancel a scheduled Zoom meeting and invalidate its join link.

    Args:
        meeting_id: Identifier of the meeting to cancel.
        notify_participants: Email registered participants about the cancellation.
    """
    return {"status": "stub", "tool": "zoom_cancel_meeting", "args": locals()}


@tool(domain="zoom", confusable_with=["gcalendar_invite_attendees"])
def zoom_invite_participants(meeting_id: str, emails: list[str], message: Optional[str] = None) -> dict:
    """Send Zoom meeting invitations to additional people.

    Args:
        meeting_id: Identifier of the meeting.
        emails: Email addresses to invite.
        message: Note to include in the invitation.
    """
    return {"status": "stub", "tool": "zoom_invite_participants", "args": locals()}


@tool(domain="zoom", confusable_with=["gdrive_list_files"])
def zoom_list_recordings(
    user: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
) -> dict:
    """List Zoom cloud recordings saved for past meetings.

    Args:
        user: Email of the host whose recordings to list.
        from_date: Earliest meeting date in YYYY-MM-DD form.
        to_date: Latest meeting date in YYYY-MM-DD form.
    """
    return {"status": "stub", "tool": "zoom_list_recordings", "args": locals()}


@tool(domain="zoom")
def zoom_get_meeting_transcript(meeting_id: str, language: Optional[str] = None) -> dict:
    """Retrieve the automatic speech transcript of a recorded Zoom meeting.

    Args:
        meeting_id: Identifier of the recorded meeting.
        language: Language code of the transcript to fetch.
    """
    return {"status": "stub", "tool": "zoom_get_meeting_transcript", "args": locals()}


@tool(domain="zoom")
def zoom_get_meeting_participants(meeting_id: str, limit: Optional[int] = None) -> dict:
    """Report who actually attended a past Zoom meeting and for how long.

    Args:
        meeting_id: Identifier of the past meeting.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "zoom_get_meeting_participants", "args": locals()}


@tool(domain="zoom", confusable_with=["zoom_create_meeting"])
def zoom_create_webinar(
    topic: str,
    start_time: str,
    panelists: Optional[list[str]] = None,
    registration_required: Optional[bool] = None,
) -> dict:
    """Schedule a Zoom webinar for a large broadcast audience rather than a meeting.

    Args:
        topic: Webinar topic shown to attendees.
        start_time: Start time in ISO 8601 form.
        panelists: Email addresses of panelists who may speak.
        registration_required: Require attendees to register in advance.
    """
    return {"status": "stub", "tool": "zoom_create_webinar", "args": locals()}


@tool(domain="zoom")
def zoom_add_webinar_registrant(webinar_id: str, email: str, full_name: Optional[str] = None) -> dict:
    """Register an attendee for an upcoming Zoom webinar.

    Args:
        webinar_id: Identifier of the webinar.
        email: Email address of the registrant.
        full_name: Registrant's display name.
    """
    return {"status": "stub", "tool": "zoom_add_webinar_registrant", "args": locals()}
