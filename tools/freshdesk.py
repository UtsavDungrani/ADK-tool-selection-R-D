"""freshdesk tools.

Freshdesk support desk: customer tickets, public replies and private notes,
assignment, priority, merging, escalation, agents, and solution articles.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="freshdesk", confusable_with=["zendesk_create_ticket", "salesforce_create_case", "jira_create_issue"])
def freshdesk_create_ticket(
    subject: str,
    description: str,
    requester_email: Optional[str] = None,
    priority: Optional[Literal['low', 'medium', 'high', 'urgent']] = None,
) -> dict:
    """Raise a Freshdesk support ticket on behalf of a customer who reported a problem.

    Args:
        subject: Short summary of the customer's problem.
        description: Full description of what the customer reported.
        requester_email: Email of the customer who reported it.
        priority: Ticket priority. One of: low, medium, high, urgent.
    """
    return {"status": "stub", "tool": "freshdesk_create_ticket", "args": locals()}


@tool(domain="freshdesk", confusable_with=["zendesk_search_tickets", "intercom_search_conversations"])
def freshdesk_search_tickets(
    query: str,
    status: Optional[Literal['open', 'pending', 'resolved', 'closed']] = None,
    agent: Optional[str] = None,
    limit: Optional[int] = None,
) -> dict:
    """Search Freshdesk tickets by text, status, or assigned agent.

    Args:
        query: Free-text search query.
        status: Filter by ticket status. One of: open, pending, resolved, closed.
        agent: Restrict to tickets assigned to this agent.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "freshdesk_search_tickets", "args": locals()}


@tool(domain="freshdesk", confusable_with=["zendesk_add_comment", "intercom_reply_to_conversation"])
def freshdesk_reply_to_ticket(ticket_id: int, body: str, cc_emails: Optional[list[str]] = None) -> dict:
    """Send a public reply on a Freshdesk ticket that the customer will receive.

    Args:
        ticket_id: Identifier of the ticket.
        body: Reply text the customer will see.
        cc_emails: Additional addresses to copy on the reply.
    """
    return {"status": "stub", "tool": "freshdesk_reply_to_ticket", "args": locals()}


@tool(domain="freshdesk", confusable_with=["zendesk_add_comment", "intercom_add_note"])
def freshdesk_add_private_note(ticket_id: int, body: str, notify_agents: Optional[list[str]] = None) -> dict:
    """Add an internal note to a Freshdesk ticket that the customer cannot see.

    Args:
        ticket_id: Identifier of the ticket.
        body: Note text, visible only to agents.
        notify_agents: Agent emails to notify about the note.
    """
    return {"status": "stub", "tool": "freshdesk_add_private_note", "args": locals()}


@tool(domain="freshdesk", confusable_with=["zendesk_assign_ticket", "intercom_assign_conversation"])
def freshdesk_assign_ticket(ticket_id: int, agent: str, group: Optional[str] = None) -> dict:
    """Assign a Freshdesk ticket to a support agent or group.

    Args:
        ticket_id: Identifier of the ticket.
        agent: Email or identifier of the agent to assign it to.
        group: Support group to assign it to instead of an individual.
    """
    return {"status": "stub", "tool": "freshdesk_assign_ticket", "args": locals()}


@tool(domain="freshdesk", confusable_with=["zendesk_update_ticket_status", "jira_transition_issue"])
def freshdesk_update_ticket_priority(
    ticket_id: int,
    priority: Literal['low', 'medium', 'high', 'urgent'],
    status: Optional[Literal['open', 'pending', 'resolved', 'closed']] = None,
) -> dict:
    """Change the priority, and optionally the status, of a Freshdesk ticket.

    Args:
        ticket_id: Identifier of the ticket.
        priority: New priority. One of: low, medium, high, urgent.
        status: New status. One of: open, pending, resolved, closed.
    """
    return {"status": "stub", "tool": "freshdesk_update_ticket_priority", "args": locals()}


@tool(domain="freshdesk", confusable_with=["zendesk_merge_tickets"])
def freshdesk_merge_tickets(primary_ticket_id: int, duplicate_ticket_ids: list[int], note: Optional[str] = None) -> dict:
    """Merge duplicate Freshdesk tickets into one primary ticket.

    Args:
        primary_ticket_id: Ticket that should survive the merge.
        duplicate_ticket_ids: Tickets to fold into the primary one.
        note: Note explaining the merge.
    """
    return {"status": "stub", "tool": "freshdesk_merge_tickets", "args": locals()}


@tool(domain="freshdesk", confusable_with=["zendesk_escalate_ticket", "pagerduty_trigger_incident"])
def freshdesk_escalate_ticket(ticket_id: int, escalate_to: str, reason: Optional[str] = None) -> dict:
    """Escalate a Freshdesk ticket to a senior agent or manager.

    Args:
        ticket_id: Identifier of the ticket to escalate.
        escalate_to: Email or group to escalate the ticket to.
        reason: Why the ticket needs escalating.
    """
    return {"status": "stub", "tool": "freshdesk_escalate_ticket", "args": locals()}


@tool(domain="freshdesk", confusable_with=["zendesk_list_agents", "intercom_list_teammates"])
def freshdesk_list_agents(group: Optional[str] = None, limit: Optional[int] = None) -> dict:
    """List the Freshdesk support agents available to take tickets.

    Args:
        group: Restrict results to agents in this support group.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "freshdesk_list_agents", "args": locals()}


@tool(domain="freshdesk", confusable_with=["intercom_create_article", "confluence_create_page"])
def freshdesk_create_solution_article(
    title: str,
    description: str,
    folder: Optional[str] = None,
    status: Optional[Literal['draft', 'published']] = None,
) -> dict:
    """Write a Freshdesk knowledge-base solution article for customers to self-serve.

    Args:
        title: Title of the article.
        description: Article content.
        folder: Solution folder to file it under.
        status: Publication state. One of: draft, published.
    """
    return {"status": "stub", "tool": "freshdesk_create_solution_article", "args": locals()}
