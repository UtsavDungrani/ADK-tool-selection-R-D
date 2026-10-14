"""salesforce tools.

Salesforce CRM: leads, contacts and accounts, opportunities and pipeline
stages, activity logging, tasks, reports, and case escalation.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="salesforce", confusable_with=["hubspot_create_contact", "stripe_create_customer"])
def salesforce_create_lead(
    last_name: str,
    company: str,
    email: Optional[str] = None,
    lead_source: Optional[str] = None,
) -> dict:
    """Create a new sales lead record in Salesforce.

    Args:
        last_name: Surname of the prospect.
        company: Company the prospect works for.
        email: Contact email address.
        lead_source: Where the lead came from, e.g. Web or Referral.
    """
    return {"status": "stub", "tool": "salesforce_create_lead", "args": locals()}


@tool(domain="salesforce", confusable_with=["hubspot_search_contacts", "stripe_search_customers"])
def salesforce_search_contacts(query: str, account: Optional[str] = None, limit: Optional[int] = None) -> dict:
    """Search Salesforce contacts by name, email, or account.

    Args:
        query: Free-text search query.
        account: Restrict results to contacts under this account.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "salesforce_search_contacts", "args": locals()}


@tool(domain="salesforce", confusable_with=["hubspot_create_deal"])
def salesforce_create_opportunity(
    name: str,
    account: str,
    amount: Optional[float] = None,
    close_date: Optional[str] = None,
    stage: Optional[Literal['prospecting', 'qualification', 'proposal', 'negotiation', 'closed_won', 'closed_lost']] = None,
) -> dict:
    """Open a new sales opportunity against a Salesforce account.

    Args:
        name: Name of the opportunity.
        account: Account the opportunity belongs to.
        amount: Expected deal value.
        close_date: Expected close date in YYYY-MM-DD form.
        stage: Pipeline stage. One of: prospecting, qualification, proposal, negotiation, closed_won, closed_lost.
    """
    return {"status": "stub", "tool": "salesforce_create_opportunity", "args": locals()}


@tool(domain="salesforce", confusable_with=["hubspot_update_deal_stage", "jira_transition_issue"])
def salesforce_update_opportunity_stage(
    opportunity_id: str,
    stage: Literal['prospecting', 'qualification', 'proposal', 'negotiation', 'closed_won', 'closed_lost'],
    close_date: Optional[str] = None,
) -> dict:
    """Advance a Salesforce opportunity to a different pipeline stage.

    Args:
        opportunity_id: Identifier of the opportunity.
        stage: New stage. One of: prospecting, qualification, proposal, negotiation, closed_won, closed_lost.
        close_date: Revised close date in YYYY-MM-DD form.
    """
    return {"status": "stub", "tool": "salesforce_update_opportunity_stage", "args": locals()}


@tool(domain="salesforce", confusable_with=["hubspot_log_activity", "jira_log_work"])
def salesforce_log_activity(
    record_id: str,
    subject: str,
    activity_type: Optional[Literal['call', 'email', 'meeting', 'note']] = None,
    notes: Optional[str] = None,
) -> dict:
    """Record a call, email, or meeting against a Salesforce record.

    Args:
        record_id: Identifier of the lead, contact, or opportunity.
        subject: Short summary of the interaction.
        activity_type: Kind of activity. One of: call, email, meeting, note.
        notes: Longer notes about what was discussed.
    """
    return {"status": "stub", "tool": "salesforce_log_activity", "args": locals()}


@tool(domain="salesforce", confusable_with=["asana_create_task", "jira_create_issue"])
def salesforce_create_task(
    subject: str,
    related_to: Optional[str] = None,
    due_date: Optional[str] = None,
    assigned_to: Optional[str] = None,
) -> dict:
    """Create a follow-up task in Salesforce linked to a CRM record.

    Args:
        subject: What the task is.
        related_to: Identifier of the record the task relates to.
        due_date: Due date in YYYY-MM-DD form.
        assigned_to: User the task should be assigned to.
    """
    return {"status": "stub", "tool": "salesforce_create_task", "args": locals()}


@tool(domain="salesforce", confusable_with=["zendesk_create_ticket", "freshdesk_create_ticket"])
def salesforce_create_case(
    subject: str,
    contact: Optional[str] = None,
    priority: Optional[Literal['low', 'medium', 'high']] = None,
    origin: Optional[Literal['phone', 'email', 'web']] = None,
) -> dict:
    """Open a Salesforce Service Cloud case for a customer problem.

    Args:
        subject: Short description of the customer's problem.
        contact: Contact who reported it.
        priority: Case priority. One of: low, medium, high.
        origin: How the case arrived. One of: phone, email, web.
    """
    return {"status": "stub", "tool": "salesforce_create_case", "args": locals()}


@tool(domain="salesforce", confusable_with=["hubspot_get_pipeline_report"])
def salesforce_run_report(report_name: str, filters: Optional[list[str]] = None, export_format: Optional[Literal['csv', 'xlsx', 'pdf']] = None) -> dict:
    """Run a saved Salesforce report and return its rows.

    Args:
        report_name: Name of the saved report to run.
        filters: Filter expressions as field=value strings.
        export_format: Format to export the results in. One of: csv, xlsx, pdf.
    """
    return {"status": "stub", "tool": "salesforce_run_report", "args": locals()}


@tool(domain="salesforce", confusable_with=["hubspot_create_contact"])
def salesforce_convert_lead(
    lead_id: str,
    create_opportunity: Optional[bool] = None,
    account_name: Optional[str] = None,
) -> dict:
    """Convert a qualified Salesforce lead into a contact, account, and opportunity.

    Args:
        lead_id: Identifier of the lead to convert.
        create_opportunity: Also create an opportunity during conversion.
        account_name: Account name to attach the converted contact to.
    """
    return {"status": "stub", "tool": "salesforce_convert_lead", "args": locals()}


@tool(domain="salesforce", confusable_with=["jira_assign_issue", "zendesk_assign_ticket"])
def salesforce_assign_record_owner(record_id: str, owner: str, send_notification: Optional[bool] = None) -> dict:
    """Transfer ownership of a Salesforce record to a different user.

    Args:
        record_id: Identifier of the record to reassign.
        owner: Username or email of the new owner.
        send_notification: Email the new owner about the handover.
    """
    return {"status": "stub", "tool": "salesforce_assign_record_owner", "args": locals()}
