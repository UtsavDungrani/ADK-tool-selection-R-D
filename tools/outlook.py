"""outlook tools.

Microsoft Outlook mail and calendar: sending and searching mail, replies and
forwards, drafts, folders, inbox rules, calendar events, and automatic replies.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="outlook", confusable_with=["gmail_send_email", "slack_send_dm"])
def outlook_send_email(
    to: list[str],
    subject: str,
    body: str,
    cc: Optional[list[str]] = None,
    importance: Optional[Literal['low', 'normal', 'high']] = None,
) -> dict:
    """Send an email message from an Outlook mailbox.

    Args:
        to: Recipient email addresses.
        subject: Subject line.
        body: Message body.
        cc: Addresses to copy on the message.
        importance: Message importance. One of: low, normal, high.
    """
    return {"status": "stub", "tool": "outlook_send_email", "args": locals()}


@tool(domain="outlook", confusable_with=["gmail_search_messages"])
def outlook_search_email(
    query: str,
    folder: Optional[str] = None,
    unread_only: Optional[bool] = None,
    limit: Optional[int] = None,
) -> dict:
    """Search an Outlook mailbox for messages matching a text query.

    Args:
        query: Free-text search query.
        folder: Restrict the search to this mail folder.
        unread_only: Return only unread messages.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "outlook_search_email", "args": locals()}


@tool(domain="outlook", confusable_with=["gmail_reply_to_message"])
def outlook_reply_to_email(message_id: str, body: str, reply_all: Optional[bool] = None) -> dict:
    """Reply to a message already in an Outlook mailbox.

    Args:
        message_id: Identifier of the message to reply to.
        body: Reply body.
        reply_all: Reply to every recipient rather than only the sender.
    """
    return {"status": "stub", "tool": "outlook_reply_to_email", "args": locals()}


@tool(domain="outlook", confusable_with=["gmail_forward_message"])
def outlook_forward_email(message_id: str, to: list[str], comment: Optional[str] = None) -> dict:
    """Forward an existing Outlook message on to other recipients.

    Args:
        message_id: Identifier of the message to forward.
        to: Recipient email addresses.
        comment: Note to add above the forwarded content.
    """
    return {"status": "stub", "tool": "outlook_forward_email", "args": locals()}


@tool(domain="outlook", confusable_with=["gmail_create_draft"])
def outlook_create_draft(to: list[str], subject: str, body: Optional[str] = None) -> dict:
    """Save an unsent Outlook message as a draft for later review.

    Args:
        to: Intended recipient email addresses.
        subject: Subject line.
        body: Draft message body.
    """
    return {"status": "stub", "tool": "outlook_create_draft", "args": locals()}


@tool(domain="outlook", confusable_with=["gcalendar_create_event", "zoom_create_meeting"])
def outlook_create_event(
    subject: str,
    start_time: str,
    end_time: Optional[str] = None,
    attendees: Optional[list[str]] = None,
    location: Optional[str] = None,
) -> dict:
    """Put a new appointment on an Outlook calendar and invite attendees.

    Args:
        subject: Event title.
        start_time: Start time in ISO 8601 form.
        end_time: End time in ISO 8601 form.
        attendees: Email addresses to invite.
        location: Meeting room or place.
    """
    return {"status": "stub", "tool": "outlook_create_event", "args": locals()}


@tool(domain="outlook", confusable_with=["gcalendar_list_events"])
def outlook_list_events(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: Optional[int] = None,
) -> dict:
    """List appointments booked on an Outlook calendar over a date range.

    Args:
        start_date: Earliest date in YYYY-MM-DD form.
        end_date: Latest date in YYYY-MM-DD form.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "outlook_list_events", "args": locals()}


@tool(domain="outlook", confusable_with=["gmail_archive_message"])
def outlook_move_to_folder(message_id: str, folder: str) -> dict:
    """File an Outlook message into a different mail folder.

    Args:
        message_id: Identifier of the message to move.
        folder: Destination folder name.
    """
    return {"status": "stub", "tool": "outlook_move_to_folder", "args": locals()}


@tool(domain="outlook", confusable_with=["gmail_create_filter"])
def outlook_create_inbox_rule(
    name: str,
    from_address: Optional[str] = None,
    subject_contains: Optional[str] = None,
    move_to_folder: Optional[str] = None,
) -> dict:
    """Create a standing Outlook inbox rule that files future mail automatically.

    Args:
        name: Name of the rule.
        from_address: Apply the rule to mail from this sender.
        subject_contains: Apply the rule when the subject contains this text.
        move_to_folder: Folder matching mail should be moved into.
    """
    return {"status": "stub", "tool": "outlook_create_inbox_rule", "args": locals()}


@tool(domain="outlook", confusable_with=["gcalendar_set_out_of_office", "gmail_set_vacation_responder"])
def outlook_set_automatic_replies(
    message: str,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    external_message: Optional[str] = None,
) -> dict:
    """Turn on an Outlook out-of-office automatic reply for a date range.

    Args:
        message: Reply text sent to colleagues inside the organisation.
        start_time: When automatic replies begin, in ISO 8601 form.
        end_time: When automatic replies stop, in ISO 8601 form.
        external_message: Alternative reply text for senders outside the organisation.
    """
    return {"status": "stub", "tool": "outlook_set_automatic_replies", "args": locals()}
