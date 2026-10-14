"""intercom tools.

Intercom customer messaging: live conversations with users, replies and
internal notes, assignment, snoozing, tags, help-centre articles, and teammates.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="intercom", confusable_with=["slack_send_dm", "gmail_send_email"])
def intercom_send_message(
    user_email: str,
    body: str,
    message_type: Optional[Literal['in_app', 'email']] = None,
    subject: Optional[str] = None,
) -> dict:
    """Start a new outbound Intercom conversation with a customer.

    Args:
        user_email: Email of the customer to message.
        body: Message body.
        message_type: Delivery channel. One of: in_app, email.
        subject: Subject line, used for email messages.
    """
    return {"status": "stub", "tool": "intercom_send_message", "args": locals()}


@tool(domain="intercom", confusable_with=["zendesk_add_comment", "freshdesk_reply_to_ticket"])
def intercom_reply_to_conversation(conversation_id: str, body: str, attachment_urls: Optional[list[str]] = None) -> dict:
    """Reply to a customer in an open Intercom conversation.

    Args:
        conversation_id: Identifier of the conversation.
        body: Reply text the customer will see.
        attachment_urls: URLs of files to attach to the reply.
    """
    return {"status": "stub", "tool": "intercom_reply_to_conversation", "args": locals()}


@tool(domain="intercom", confusable_with=["zendesk_search_tickets", "freshdesk_search_tickets"])
def intercom_search_conversations(
    query: str,
    state: Optional[Literal['open', 'closed', 'snoozed']] = None,
    assignee: Optional[str] = None,
    limit: Optional[int] = None,
) -> dict:
    """Search Intercom conversations by text, state, or assignee.

    Args:
        query: Free-text search query.
        state: Filter by conversation state. One of: open, closed, snoozed.
        assignee: Restrict to conversations assigned to this teammate.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "intercom_search_conversations", "args": locals()}


@tool(domain="intercom", confusable_with=["zendesk_assign_ticket", "freshdesk_assign_ticket"])
def intercom_assign_conversation(conversation_id: str, assignee: str, team: Optional[str] = None) -> dict:
    """Hand an Intercom conversation to a specific teammate or team.

    Args:
        conversation_id: Identifier of the conversation.
        assignee: Email or identifier of the teammate to assign it to.
        team: Team to assign it to instead of an individual.
    """
    return {"status": "stub", "tool": "intercom_assign_conversation", "args": locals()}


@tool(domain="intercom", confusable_with=["zendesk_update_ticket_status"])
def intercom_close_conversation(conversation_id: str, reason: Optional[str] = None) -> dict:
    """Close an Intercom conversation once the customer's issue is resolved.

    Args:
        conversation_id: Identifier of the conversation to close.
        reason: Short note on why it was closed.
    """
    return {"status": "stub", "tool": "intercom_close_conversation", "args": locals()}


@tool(domain="intercom", confusable_with=["zendesk_add_comment", "pagerduty_add_note"])
def intercom_add_note(conversation_id: str, body: str) -> dict:
    """Add an internal note to an Intercom conversation that the customer cannot see.

    Args:
        conversation_id: Identifier of the conversation.
        body: Note text, visible only to teammates.
    """
    return {"status": "stub", "tool": "intercom_add_note", "args": locals()}


@tool(domain="intercom", confusable_with=["zendesk_add_tag", "gmail_add_label"])
def intercom_tag_conversation(conversation_id: str, tag: str) -> dict:
    """Apply a tag to an Intercom conversation for later reporting.

    Args:
        conversation_id: Identifier of the conversation.
        tag: Name of the tag to apply.
    """
    return {"status": "stub", "tool": "intercom_tag_conversation", "args": locals()}


@tool(domain="intercom", confusable_with=["pagerduty_snooze_incident"])
def intercom_snooze_conversation(conversation_id: str, until: str) -> dict:
    """Snooze an Intercom conversation so it reopens later instead of sitting in the inbox.

    Args:
        conversation_id: Identifier of the conversation.
        until: ISO 8601 time when it should reopen.
    """
    return {"status": "stub", "tool": "intercom_snooze_conversation", "args": locals()}


@tool(domain="intercom", confusable_with=["confluence_create_page", "freshdesk_create_solution_article"])
def intercom_create_article(
    title: str,
    body: str,
    collection: Optional[str] = None,
    state: Optional[Literal['draft', 'published']] = None,
) -> dict:
    """Write a help-centre article in Intercom for customers to self-serve.

    Args:
        title: Title of the article.
        body: Article content.
        collection: Help-centre collection to file it under.
        state: Publication state. One of: draft, published.
    """
    return {"status": "stub", "tool": "intercom_create_article", "args": locals()}


@tool(domain="intercom", confusable_with=["zendesk_list_agents", "slack_list_users"])
def intercom_list_teammates(team: Optional[str] = None, limit: Optional[int] = None) -> dict:
    """List the Intercom teammates who can be assigned conversations.

    Args:
        team: Restrict results to members of this team.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "intercom_list_teammates", "args": locals()}
