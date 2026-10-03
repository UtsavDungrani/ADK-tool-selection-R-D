"""zendesk tools.

Customer support desk: tickets raised by customers, replies and internal
notes, assignment, status, tags, views, and escalation.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="zendesk", confusable_with=["github_create_issue", "jira_create_issue"])
def zendesk_create_ticket(
    subject: str,
    requester_email: str,
    description: str,
    priority: Optional[Literal['low', 'normal', 'high', 'urgent']] = None,
) -> dict:
    """Open a new customer support ticket in Zendesk on behalf of a requester.

    Args:
        subject: Ticket subject line.
        requester_email: Email address of the customer reporting the issue.
        description: Full description of the customer's problem.
        priority: Ticket priority. One of: low, normal, high, urgent.
    """
    return {"status": "stub", "tool": "zendesk_create_ticket", "args": locals()}


@tool(domain="zendesk", confusable_with=["jira_search_issues", "github_search_issues"])
def zendesk_search_tickets(
    query: str,
    status: Optional[Literal['new', 'open', 'pending', 'solved', 'closed']] = None,
    limit: Optional[int] = None,
) -> dict:
    """Search Zendesk support tickets by text, status, requester, or tag.

    Args:
        query: Free-text search query.
        status: Filter by ticket status. One of: new, open, pending, solved, closed.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "zendesk_search_tickets", "args": locals()}


@tool(domain="zendesk", confusable_with=["jira_add_comment", "github_add_comment"])
def zendesk_add_comment(
    ticket_id: int,
    body: str,
    public: Optional[bool] = None,
) -> dict:
    """Add a public reply or internal note to a Zendesk support ticket.

    Args:
        ticket_id: Numeric Zendesk ticket identifier.
        body: Comment text.
        public: True for a customer-visible reply, false for an internal note.
    """
    return {"status": "stub", "tool": "zendesk_add_comment", "args": locals()}


@tool(domain="zendesk", confusable_with=["jira_assign_issue"])
def zendesk_assign_ticket(ticket_id: int, assignee: str) -> dict:
    """Assign a Zendesk support ticket to a support agent.

    Args:
        ticket_id: Numeric Zendesk ticket identifier.
        assignee: Agent email or identifier.
    """
    return {"status": "stub", "tool": "zendesk_assign_ticket", "args": locals()}


@tool(domain="zendesk", confusable_with=["jira_transition_issue"])
def zendesk_update_ticket_status(
    ticket_id: int,
    status: Literal['new', 'open', 'pending', 'solved', 'closed'],
) -> dict:
    """Change the status of a Zendesk ticket, for example to pending or solved.

    Args:
        ticket_id: Numeric Zendesk ticket identifier.
        status: New ticket status. One of: new, open, pending, solved, closed.
    """
    return {"status": "stub", "tool": "zendesk_update_ticket_status", "args": locals()}


@tool(domain="zendesk")
def zendesk_list_views(limit: Optional[int] = None) -> dict:
    """List the saved Zendesk views that group tickets into queues.

    Args:
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "zendesk_list_views", "args": locals()}


@tool(domain="zendesk")
def zendesk_merge_tickets(source_ticket_id: int, target_ticket_id: int) -> dict:
    """Merge a duplicate Zendesk ticket into another ticket.

    Args:
        source_ticket_id: Ticket to merge from.
        target_ticket_id: Ticket to merge into.
    """
    return {"status": "stub", "tool": "zendesk_merge_tickets", "args": locals()}


@tool(domain="zendesk")
def zendesk_add_tag(ticket_id: int, tags: list[str]) -> dict:
    """Add one or more tags to a Zendesk support ticket.

    Args:
        ticket_id: Numeric Zendesk ticket identifier.
        tags: Tags to add.
    """
    return {"status": "stub", "tool": "zendesk_add_tag", "args": locals()}


@tool(domain="zendesk", confusable_with=["jira_list_users", "slack_list_users"])
def zendesk_list_agents(limit: Optional[int] = None) -> dict:
    """List Zendesk support agents who can be assigned tickets.

    Args:
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "zendesk_list_agents", "args": locals()}


@tool(domain="zendesk", confusable_with=["pagerduty_trigger_incident"])
def zendesk_escalate_ticket(
    ticket_id: int,
    tier: Optional[str] = None,
    reason: Optional[str] = None,
) -> dict:
    """Escalate a Zendesk ticket to a higher support tier or to engineering.

    Args:
        ticket_id: Numeric Zendesk ticket identifier.
        tier: Target escalation tier.
        reason: Why the ticket is being escalated.
    """
    return {"status": "stub", "tool": "zendesk_escalate_ticket", "args": locals()}
