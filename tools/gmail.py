"""gmail tools.

Gmail mailbox: sending and searching mail, replies and forwards, drafts,
labels, archiving, filters, attachments, and vacation responders.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Optional

from ._registry import tool


@tool(domain="gmail", confusable_with=["outlook_send_email", "slack_send_dm"])
def gmail_send_email(
    to: list[str],
    subject: str,
    body: str,
    cc: Optional[list[str]] = None,
    bcc: Optional[list[str]] = None,
) -> dict:
    """Send an email message from a Gmail account.

    Args:
        to: Recipient email addresses.
        subject: Subject line.
        body: Message body.
        cc: Addresses to copy on the message.
        bcc: Addresses to blind copy on the message.
    """
    return {"status": "stub", "tool": "gmail_send_email", "args": locals()}


@tool(domain="gmail", confusable_with=["outlook_search_email"])
def gmail_search_messages(
    query: str,
    label: Optional[str] = None,
    unread_only: Optional[bool] = None,
    limit: Optional[int] = None,
) -> dict:
    """Search a Gmail mailbox for messages matching a query.

    Args:
        query: Gmail search query, e.g. from:ops subject:deploy.
        label: Restrict the search to messages carrying this label.
        unread_only: Return only unread messages.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "gmail_search_messages", "args": locals()}


@tool(domain="gmail", confusable_with=["outlook_reply_to_email"])
def gmail_reply_to_message(message_id: str, body: str, reply_all: Optional[bool] = None) -> dict:
    """Reply to a message in a Gmail thread.

    Args:
        message_id: Identifier of the message to reply to.
        body: Reply body.
        reply_all: Reply to every recipient rather than only the sender.
    """
    return {"status": "stub", "tool": "gmail_reply_to_message", "args": locals()}


@tool(domain="gmail", confusable_with=["outlook_forward_email"])
def gmail_forward_message(message_id: str, to: list[str], comment: Optional[str] = None) -> dict:
    """Forward an existing Gmail message on to other recipients.

    Args:
        message_id: Identifier of the message to forward.
        to: Recipient email addresses.
        comment: Note to add above the forwarded content.
    """
    return {"status": "stub", "tool": "gmail_forward_message", "args": locals()}


@tool(domain="gmail", confusable_with=["outlook_create_draft"])
def gmail_create_draft(to: list[str], subject: str, body: Optional[str] = None) -> dict:
    """Save an unsent Gmail message as a draft for later review.

    Args:
        to: Intended recipient email addresses.
        subject: Subject line.
        body: Draft message body.
    """
    return {"status": "stub", "tool": "gmail_create_draft", "args": locals()}


@tool(domain="gmail", confusable_with=["zendesk_add_tag"])
def gmail_add_label(message_id: str, label: str) -> dict:
    """Apply a label to a Gmail message so it can be grouped and found later.

    Args:
        message_id: Identifier of the message to label.
        label: Name of the label to apply.
    """
    return {"status": "stub", "tool": "gmail_add_label", "args": locals()}


@tool(domain="gmail", confusable_with=["outlook_move_to_folder", "trello_archive_card"])
def gmail_archive_message(message_id: str) -> dict:
    """Remove a Gmail message from the inbox without deleting it.

    Args:
        message_id: Identifier of the message to archive.
    """
    return {"status": "stub", "tool": "gmail_archive_message", "args": locals()}


@tool(domain="gmail", confusable_with=["outlook_create_inbox_rule"])
def gmail_create_filter(
    from_address: Optional[str] = None,
    subject_contains: Optional[str] = None,
    apply_label: Optional[str] = None,
    skip_inbox: Optional[bool] = None,
) -> dict:
    """Create a standing Gmail filter that labels or sorts future mail automatically.

    Args:
        from_address: Apply the filter to mail from this sender.
        subject_contains: Apply the filter when the subject contains this text.
        apply_label: Label to attach to matching mail.
        skip_inbox: Archive matching mail instead of leaving it in the inbox.
    """
    return {"status": "stub", "tool": "gmail_create_filter", "args": locals()}


@tool(domain="gmail", confusable_with=["outlook_set_automatic_replies", "gcalendar_set_out_of_office"])
def gmail_set_vacation_responder(
    message: str,
    subject: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> dict:
    """Turn on the Gmail vacation auto-responder for a date range.

    Args:
        message: Auto-reply body sent to people who write in.
        subject: Subject line for the auto-reply.
        start_date: First day of the vacation, in YYYY-MM-DD form.
        end_date: Last day of the vacation, in YYYY-MM-DD form.
    """
    return {"status": "stub", "tool": "gmail_set_vacation_responder", "args": locals()}


@tool(domain="gmail", confusable_with=["gdrive_export_file"])
def gmail_download_attachment(message_id: str, filename: Optional[str] = None) -> dict:
    """Save a file attached to a Gmail message.

    Args:
        message_id: Identifier of the message holding the attachment.
        filename: Name of the attachment to save; all attachments when omitted.
    """
    return {"status": "stub", "tool": "gmail_download_attachment", "args": locals()}
