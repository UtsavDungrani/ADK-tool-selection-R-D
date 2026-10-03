"""Extended catalog: 5 more domains, 50 more hand-written tools (core 50 -> 100).

WHY THESE FIVE

The first five domains (github, jira, slack, gcalendar, gdrive) produce mostly
*pairwise* collisions. Real tool catalogs get harder than that: once an org runs
an issue tracker, a support desk, an on-call system and an error tracker, the
phrase "file a ticket for this" has four defensible destinations.

These domains are picked to manufacture exactly that:

  FOUR-WAY "create a ticket":
      github_create_issue      a code defect, tracked with the code
      jira_create_issue        planned engineering work
      zendesk_create_ticket    a customer-reported problem
      sentry_search_issues     an error the system already recorded itself
    plus pagerduty_trigger_incident for "page someone now".
  Disambiguation depends entirely on *who reported it and what happens next* --
  which is the realistic hard case, and the one flat retrieval handles worst.

  FIVE-WAY "add a comment":
      github_add_comment / jira_add_comment / zendesk_add_comment /
      pagerduty_add_note / sentry_add_comment   (+ notion_add_comment)

  THREE-WAY "mark it done":
      jira_transition_issue / pagerduty_resolve_incident / sentry_resolve_issue

  stripe is the control domain. It overlaps almost nothing -- payments
  vocabulary is distinct. If a retriever starts pulling stripe tools for
  engineering queries, that is pure noise and a sign the index is broken.

A note on `confusable_with`: it is directional and not exhaustive. Entries here
point into the original 50 where relevant, but the original tools were not
retrofitted to point back. It drives error *analysis* only -- no strategy reads
it -- so asymmetry costs nothing.
"""

from __future__ import annotations

from .schema import Param as P
from .schema import ToolSpec


def _t(name, domain, description, params=(), confusable=()):
    return ToolSpec(
        name=name,
        domain=domain,
        description=description,
        params=tuple(params),
        confusable_with=tuple(confusable),
    )


_query = P("query", "string", "Free-text search query.")
_limit = P("limit", "integer", "Maximum number of results to return.", required=False)

NOTION = [
    _t("notion_create_page", "notion",
       "Create a new page in a Notion workspace, optionally inside a parent page.",
       [P("title", "string", "Page title."),
        P("parent_id", "string", "Identifier of the parent page or database.", required=False),
        P("content", "string", "Initial page body in Markdown.", required=False)],
       ["gdrive_create_folder"]),
    _t("notion_search_pages", "notion",
       "Search Notion pages and databases by text in their title or content.",
       [_query, _limit],
       ["gdrive_search_files"]),
    _t("notion_update_page", "notion",
       "Update the title or properties of an existing Notion page.",
       [P("page_id", "string", "Identifier of the page."),
        P("title", "string", "New page title.", required=False)]),
    _t("notion_append_block", "notion",
       "Append a block of content to the end of an existing Notion page.",
       [P("page_id", "string", "Identifier of the page."),
        P("content", "string", "Markdown content to append.")],
       ["notion_add_comment"]),
    _t("notion_create_database", "notion",
       "Create a new Notion database with typed properties for structured records.",
       [P("title", "string", "Database title."),
        P("parent_id", "string", "Identifier of the parent page."),
        P("properties", "array", "Property names to define on the database.", required=False)]),
    _t("notion_query_database", "notion",
       "Query rows in a Notion database with filters and sorting.",
       [P("database_id", "string", "Identifier of the database."),
        P("filter", "string", "Filter expression.", required=False),
        _limit],
       ["notion_search_pages"]),
    _t("notion_share_page", "notion",
       "Share a Notion page with a person and set their permission level.",
       [P("page_id", "string", "Identifier of the page."),
        P("email", "string", "Email address of the recipient."),
        P("role", "string", "Permission level.", required=False,
          enum=("reader", "commenter", "editor"))],
       ["gdrive_share_file"]),
    _t("notion_duplicate_page", "notion",
       "Create a duplicate copy of an existing Notion page.",
       [P("page_id", "string", "Identifier of the page to duplicate."),
        P("new_title", "string", "Title for the copy.", required=False)],
       ["gdrive_copy_file"]),
    _t("notion_archive_page", "notion",
       "Archive a Notion page, removing it from navigation without deleting it.",
       [P("page_id", "string", "Identifier of the page to archive.")],
       ["gdrive_delete_file"]),
    _t("notion_add_comment", "notion",
       "Add a comment to a Notion page.",
       [P("page_id", "string", "Identifier of the page."),
        P("body", "string", "Comment text.")],
       ["jira_add_comment", "github_add_comment"]),
]

ZENDESK = [
    _t("zendesk_create_ticket", "zendesk",
       "Open a new customer support ticket in Zendesk on behalf of a requester.",
       [P("subject", "string", "Ticket subject line."),
        P("requester_email", "string", "Email address of the customer reporting the issue."),
        P("description", "string", "Full description of the customer's problem."),
        P("priority", "string", "Ticket priority.", required=False,
          enum=("low", "normal", "high", "urgent"))],
       ["github_create_issue", "jira_create_issue"]),
    _t("zendesk_search_tickets", "zendesk",
       "Search Zendesk support tickets by text, status, requester, or tag.",
       [_query,
        P("status", "string", "Filter by ticket status.", required=False,
          enum=("new", "open", "pending", "solved", "closed")),
        _limit],
       ["jira_search_issues", "github_search_issues"]),
    _t("zendesk_add_comment", "zendesk",
       "Add a public reply or internal note to a Zendesk support ticket.",
       [P("ticket_id", "integer", "Numeric Zendesk ticket identifier."),
        P("body", "string", "Comment text."),
        P("public", "boolean", "True for a customer-visible reply, false for an internal note.",
          required=False)],
       ["jira_add_comment", "github_add_comment"]),
    _t("zendesk_assign_ticket", "zendesk",
       "Assign a Zendesk support ticket to a support agent.",
       [P("ticket_id", "integer", "Numeric Zendesk ticket identifier."),
        P("assignee", "string", "Agent email or identifier.")],
       ["jira_assign_issue"]),
    _t("zendesk_update_ticket_status", "zendesk",
       "Change the status of a Zendesk ticket, for example to pending or solved.",
       [P("ticket_id", "integer", "Numeric Zendesk ticket identifier."),
        P("status", "string", "New ticket status.",
          enum=("new", "open", "pending", "solved", "closed"))],
       ["jira_transition_issue"]),
    _t("zendesk_list_views", "zendesk",
       "List the saved Zendesk views that group tickets into queues.",
       [_limit]),
    _t("zendesk_merge_tickets", "zendesk",
       "Merge a duplicate Zendesk ticket into another ticket.",
       [P("source_ticket_id", "integer", "Ticket to merge from."),
        P("target_ticket_id", "integer", "Ticket to merge into.")]),
    _t("zendesk_add_tag", "zendesk",
       "Add one or more tags to a Zendesk support ticket.",
       [P("ticket_id", "integer", "Numeric Zendesk ticket identifier."),
        P("tags", "array", "Tags to add.")]),
    _t("zendesk_list_agents", "zendesk",
       "List Zendesk support agents who can be assigned tickets.",
       [_limit],
       ["jira_list_users", "slack_list_users"]),
    _t("zendesk_escalate_ticket", "zendesk",
       "Escalate a Zendesk ticket to a higher support tier or to engineering.",
       [P("ticket_id", "integer", "Numeric Zendesk ticket identifier."),
        P("tier", "string", "Target escalation tier.", required=False),
        P("reason", "string", "Why the ticket is being escalated.", required=False)],
       ["pagerduty_trigger_incident"]),
]

PAGERDUTY = [
    _t("pagerduty_trigger_incident", "pagerduty",
       "Trigger a new PagerDuty incident to page the on-call responder immediately.",
       [P("service_id", "string", "Identifier of the affected PagerDuty service."),
        P("title", "string", "Short incident title."),
        P("urgency", "string", "Incident urgency.", required=False, enum=("low", "high"))],
       ["zendesk_create_ticket", "sentry_create_alert_rule"]),
    _t("pagerduty_acknowledge_incident", "pagerduty",
       "Acknowledge a PagerDuty incident to signal that someone is working on it.",
       [P("incident_id", "string", "Identifier of the incident.")]),
    _t("pagerduty_resolve_incident", "pagerduty",
       "Mark a PagerDuty incident as resolved once the outage is over.",
       [P("incident_id", "string", "Identifier of the incident."),
        P("resolution", "string", "Note describing the resolution.", required=False)],
       ["sentry_resolve_issue", "jira_transition_issue"]),
    _t("pagerduty_list_incidents", "pagerduty",
       "List PagerDuty incidents, optionally filtered by status or service.",
       [P("status", "string", "Filter by incident status.", required=False,
          enum=("triggered", "acknowledged", "resolved")),
        P("service_id", "string", "Restrict to one service.", required=False),
        _limit]),
    _t("pagerduty_get_oncall", "pagerduty",
       "Find out which person is currently on call for a PagerDuty schedule.",
       [P("schedule_id", "string", "Identifier of the on-call schedule.", required=False),
        P("at", "string", "ISO 8601 time to check, defaulting to now.", required=False)],
       ["zendesk_list_agents"]),
    _t("pagerduty_create_schedule", "pagerduty",
       "Create a new PagerDuty on-call rotation schedule.",
       [P("name", "string", "Schedule name."),
        P("users", "array", "User identifiers in rotation order."),
        P("rotation", "string", "Rotation length, for example weekly.", required=False)],
       ["gcalendar_create_recurring_event"]),
    _t("pagerduty_add_responder", "pagerduty",
       "Add another responder to an active PagerDuty incident.",
       [P("incident_id", "string", "Identifier of the incident."),
        P("user_id", "string", "Identifier of the responder to add.")],
       ["slack_invite_to_channel", "gcalendar_invite_attendees"]),
    _t("pagerduty_add_note", "pagerduty",
       "Add a timeline note to a PagerDuty incident.",
       [P("incident_id", "string", "Identifier of the incident."),
        P("content", "string", "Note text.")],
       ["jira_add_comment", "zendesk_add_comment"]),
    _t("pagerduty_list_services", "pagerduty",
       "List the PagerDuty services that incidents can be raised against.",
       [_limit]),
    _t("pagerduty_snooze_incident", "pagerduty",
       "Snooze a PagerDuty incident so it stops paging for a set duration.",
       [P("incident_id", "string", "Identifier of the incident."),
        P("duration_minutes", "integer", "How long to snooze for, in minutes.")],
       ["sentry_ignore_issue"]),
]

STRIPE = [
    _t("stripe_create_customer", "stripe",
       "Create a new customer record in Stripe for billing.",
       [P("email", "string", "Customer email address."),
        P("name", "string", "Customer display name.", required=False)]),
    _t("stripe_search_customers", "stripe",
       "Search Stripe customers by email, name, or metadata.",
       [_query, _limit]),
    _t("stripe_create_invoice", "stripe",
       "Create and optionally send a Stripe invoice to a customer.",
       [P("customer_id", "string", "Identifier of the Stripe customer."),
        P("amount_cents", "integer", "Invoice amount in the smallest currency unit."),
        P("send", "boolean", "Whether to email the invoice immediately.", required=False)]),
    _t("stripe_refund_payment", "stripe",
       "Issue a full or partial refund for a Stripe payment.",
       [P("charge_id", "string", "Identifier of the charge to refund."),
        P("amount_cents", "integer", "Amount to refund; omit for a full refund.",
          required=False)]),
    _t("stripe_list_subscriptions", "stripe",
       "List Stripe subscriptions, optionally filtered by customer or status.",
       [P("customer_id", "string", "Restrict to one customer.", required=False),
        P("status", "string", "Filter by subscription status.", required=False,
          enum=("active", "past_due", "canceled", "trialing")),
        _limit]),
    _t("stripe_cancel_subscription", "stripe",
       "Cancel a Stripe subscription, immediately or at the end of the billing period.",
       [P("subscription_id", "string", "Identifier of the subscription."),
        P("at_period_end", "boolean", "Cancel at period end rather than immediately.",
          required=False)]),
    _t("stripe_list_charges", "stripe",
       "List recent Stripe charges with their amounts and outcomes.",
       [P("customer_id", "string", "Restrict to one customer.", required=False), _limit]),
    _t("stripe_create_payment_link", "stripe",
       "Create a shareable Stripe payment link for a product or amount.",
       [P("amount_cents", "integer", "Amount in the smallest currency unit."),
        P("description", "string", "What the payment is for.", required=False)]),
    _t("stripe_update_subscription", "stripe",
       "Change the plan or quantity on an existing Stripe subscription.",
       [P("subscription_id", "string", "Identifier of the subscription."),
        P("price_id", "string", "Identifier of the new price.", required=False),
        P("quantity", "integer", "New seat or unit quantity.", required=False)]),
    _t("stripe_get_balance", "stripe",
       "Retrieve the current available and pending balance in the Stripe account.",
       []),
]

SENTRY = [
    _t("sentry_search_issues", "sentry",
       "Search Sentry for recorded application errors matching a query.",
       [_query,
        P("project", "string", "Sentry project slug.", required=False),
        P("status", "string", "Filter by issue status.", required=False,
          enum=("unresolved", "resolved", "ignored")),
        _limit],
       ["github_search_issues", "jira_search_issues"]),
    _t("sentry_get_issue_details", "sentry",
       "Retrieve the stack trace and metadata for one Sentry error issue.",
       [P("issue_id", "string", "Identifier of the Sentry issue.")]),
    _t("sentry_resolve_issue", "sentry",
       "Mark a Sentry error issue as resolved.",
       [P("issue_id", "string", "Identifier of the Sentry issue."),
        P("in_release", "string", "Release version the fix ships in.", required=False)],
       ["pagerduty_resolve_incident", "jira_transition_issue"]),
    _t("sentry_assign_issue", "sentry",
       "Assign a Sentry error issue to a developer to investigate.",
       [P("issue_id", "string", "Identifier of the Sentry issue."),
        P("assignee", "string", "Username or email of the assignee.")],
       ["jira_assign_issue", "zendesk_assign_ticket"]),
    _t("sentry_ignore_issue", "sentry",
       "Ignore a Sentry error issue so it stops appearing in the unresolved feed.",
       [P("issue_id", "string", "Identifier of the Sentry issue."),
        P("duration_minutes", "integer", "Ignore for this long, or omit for forever.",
          required=False)],
       ["pagerduty_snooze_incident"]),
    _t("sentry_list_events", "sentry",
       "List individual error events recorded under a Sentry issue.",
       [P("issue_id", "string", "Identifier of the Sentry issue."), _limit]),
    _t("sentry_create_alert_rule", "sentry",
       "Create a Sentry alert rule that notifies a channel when error rates spike.",
       [P("project", "string", "Sentry project slug."),
        P("name", "string", "Alert rule name."),
        P("threshold", "integer", "Event count that triggers the alert.")],
       ["pagerduty_trigger_incident"]),
    _t("sentry_link_to_tracker", "sentry",
       "Link a Sentry error issue to an existing ticket in an external issue tracker.",
       [P("issue_id", "string", "Identifier of the Sentry issue."),
        P("external_key", "string", "Key or URL of the external ticket.")],
       ["jira_create_issue", "github_create_issue"]),
    _t("sentry_list_releases", "sentry",
       "List deployed releases tracked in Sentry with their error counts.",
       [P("project", "string", "Sentry project slug."), _limit]),
    _t("sentry_add_comment", "sentry",
       "Add a comment to a Sentry error issue.",
       [P("issue_id", "string", "Identifier of the Sentry issue."),
        P("body", "string", "Comment text.")],
       ["jira_add_comment", "github_add_comment", "pagerduty_add_note"]),
]

DOMAINS_EXT: dict[str, list[ToolSpec]] = {
    "notion": NOTION,
    "zendesk": ZENDESK,
    "pagerduty": PAGERDUTY,
    "stripe": STRIPE,
    "sentry": SENTRY,
}

EXT_SPECS: list[ToolSpec] = [s for specs in DOMAINS_EXT.values() for s in specs]

DOMAIN_DESCRIPTIONS_EXT: dict[str, str] = {
    "notion": (
        "Workspace docs and wikis: pages, databases, blocks, comments, "
        "duplication, archiving, and sharing permissions."
    ),
    "zendesk": (
        "Customer support desk: tickets raised by customers, replies and "
        "internal notes, assignment, status, tags, views, and escalation."
    ),
    "pagerduty": (
        "Incident response and on-call: triggering and resolving incidents, "
        "paging responders, rotation schedules, services, and snoozing."
    ),
    "stripe": (
        "Payments and billing: customers, invoices, charges, refunds, "
        "subscriptions, payment links, and account balance."
    ),
    "sentry": (
        "Application error tracking: recorded exceptions, stack traces, "
        "resolution and assignment, alert rules, releases, and tracker links."
    ),
}
