"""hubspot tools.

HubSpot CRM and marketing: contacts, companies, deals and pipeline stages,
activity logging, marketing emails, lists, forms, and pipeline reporting.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="hubspot", confusable_with=["salesforce_create_lead", "stripe_create_customer"])
def hubspot_create_contact(
    email: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    company: Optional[str] = None,
    lifecycle_stage: Optional[Literal['subscriber', 'lead', 'opportunity', 'customer']] = None,
) -> dict:
    """Create a contact record in the HubSpot CRM.

    Args:
        email: Contact email address, used as the unique key.
        first_name: Contact's given name.
        last_name: Contact's surname.
        company: Company the contact works for.
        lifecycle_stage: Where they sit in the funnel. One of: subscriber, lead, opportunity, customer.
    """
    return {"status": "stub", "tool": "hubspot_create_contact", "args": locals()}


@tool(domain="hubspot", confusable_with=["salesforce_search_contacts", "stripe_search_customers"])
def hubspot_search_contacts(query: str, lifecycle_stage: Optional[str] = None, limit: Optional[int] = None) -> dict:
    """Search HubSpot contacts by name, email, or company.

    Args:
        query: Free-text search query.
        lifecycle_stage: Restrict results to this lifecycle stage.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "hubspot_search_contacts", "args": locals()}


@tool(domain="hubspot", confusable_with=["salesforce_create_opportunity"])
def hubspot_create_deal(
    name: str,
    amount: Optional[float] = None,
    pipeline: Optional[str] = None,
    close_date: Optional[str] = None,
    associated_contact: Optional[str] = None,
) -> dict:
    """Create a deal in a HubSpot sales pipeline.

    Args:
        name: Name of the deal.
        amount: Expected deal value.
        pipeline: Pipeline the deal belongs to.
        close_date: Expected close date in YYYY-MM-DD form.
        associated_contact: Email of the contact the deal is with.
    """
    return {"status": "stub", "tool": "hubspot_create_deal", "args": locals()}


@tool(domain="hubspot", confusable_with=["salesforce_update_opportunity_stage"])
def hubspot_update_deal_stage(deal_id: str, stage: str, amount: Optional[float] = None) -> dict:
    """Move a HubSpot deal to a different stage of its pipeline.

    Args:
        deal_id: Identifier of the deal.
        stage: Name of the stage to move the deal into.
        amount: Revised deal value.
    """
    return {"status": "stub", "tool": "hubspot_update_deal_stage", "args": locals()}


@tool(domain="hubspot", confusable_with=["salesforce_log_activity"])
def hubspot_log_activity(
    contact_email: str,
    activity_type: Literal['call', 'email', 'meeting', 'note'],
    summary: Optional[str] = None,
) -> dict:
    """Record an interaction with a HubSpot contact on their timeline.

    Args:
        contact_email: Email of the contact the activity relates to.
        activity_type: Kind of activity. One of: call, email, meeting, note.
        summary: Short description of what happened.
    """
    return {"status": "stub", "tool": "hubspot_log_activity", "args": locals()}


@tool(domain="hubspot", confusable_with=["gmail_send_email", "outlook_send_email"])
def hubspot_send_marketing_email(
    campaign: str,
    list_name: str,
    subject: Optional[str] = None,
    send_at: Optional[str] = None,
) -> dict:
    """Send or schedule a HubSpot marketing email campaign to a contact list.

    Args:
        campaign: Name of the marketing email campaign.
        list_name: Contact list to send the campaign to.
        subject: Subject line of the email.
        send_at: ISO 8601 time to send; immediately when omitted.
    """
    return {"status": "stub", "tool": "hubspot_send_marketing_email", "args": locals()}


@tool(domain="hubspot", confusable_with=["salesforce_run_report"])
def hubspot_get_pipeline_report(
    pipeline: Optional[str] = None,
    date_range: Optional[str] = None,
    group_by: Optional[Literal['stage', 'owner', 'source']] = None,
) -> dict:
    """Summarise deal value and count across a HubSpot sales pipeline.

    Args:
        pipeline: Pipeline to report on; all pipelines when omitted.
        date_range: Period to report over, e.g. last_quarter.
        group_by: How to break the figures down. One of: stage, owner, source.
    """
    return {"status": "stub", "tool": "hubspot_get_pipeline_report", "args": locals()}


@tool(domain="hubspot")
def hubspot_add_contact_to_list(contact_email: str, list_name: str) -> dict:
    """Add a HubSpot contact to a static marketing list.

    Args:
        contact_email: Email of the contact to add.
        list_name: Name of the list to add them to.
    """
    return {"status": "stub", "tool": "hubspot_add_contact_to_list", "args": locals()}


@tool(domain="hubspot", confusable_with=["salesforce_create_task", "asana_create_task"])
def hubspot_create_task(
    title: str,
    due_date: Optional[str] = None,
    associated_contact: Optional[str] = None,
    owner: Optional[str] = None,
) -> dict:
    """Create a follow-up task in HubSpot against a contact or deal.

    Args:
        title: What the task is.
        due_date: Due date in YYYY-MM-DD form.
        associated_contact: Email of the contact the task relates to.
        owner: User the task should be assigned to.
    """
    return {"status": "stub", "tool": "hubspot_create_task", "args": locals()}


@tool(domain="hubspot")
def hubspot_list_form_submissions(form_name: str, since: Optional[str] = None, limit: Optional[int] = None) -> dict:
    """Retrieve the submissions captured by a HubSpot marketing form.

    Args:
        form_name: Name of the form.
        since: Only return submissions after this date, in YYYY-MM-DD form.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "hubspot_list_form_submissions", "args": locals()}
