"""60 more labelled tasks covering the 5 extended domains (120 total).

Same tier contract as `tasks.py`: easy names the system, medium implies it,
hard sits on a seeded trap.

The hard tier here is genuinely harder than in the base set, because the
extended domains manufacture multi-way collisions rather than pairs. Several
hard tasks are only resolvable from *who reported the problem and what happens
next*:

    "A customer emailed saying the CSV export is broken"  -> zendesk  (customer)
    "Checkout is down and nobody is looking at it"        -> pagerduty (page now)
    "The app is throwing errors in production"            -> sentry   (recorded)
    "The design review turned up a bug"                   -> jira     (planned)

All four are "something is broken, record it somewhere". A retriever matching
on surface words cannot separate them; that is the point of including them.
"""

from __future__ import annotations

from .tasks import Task

TASKS_EXT: list[Task] = [
    # ---------------- notion ----------------
    Task("nt01", "Create a Notion page called Q4 Roadmap.",
         "notion_create_page", "easy"),
    Task("nt02", "Archive the Notion page abc123.",
         "notion_archive_page", "easy"),
    Task("nt03", "Create a Notion database called Vendor Tracker under page abc123.",
         "notion_create_database", "easy"),
    Task("nt04", "Search Notion for the onboarding checklist.",
         "notion_search_pages", "easy"),
    Task("nt05", "Add a paragraph to the end of Notion page abc123 about the new SLA.",
         "notion_append_block", "medium"),
    Task("nt06", "Give maya@acme.com edit access to the Notion page abc123.",
         "notion_share_page", "medium"),
    Task("nt07", "Which rows in Notion database db77 are marked blocked?",
         "notion_query_database", "medium"),
    Task("nt08", "Rename the Notion page abc123 to 'Q4 Roadmap (final)'.",
         "notion_update_page", "medium"),
    Task("nt09", "Make a copy of the Notion page abc123 before I restructure it.",
         "notion_duplicate_page", "hard", trap="gdrive_copy_file"),
    Task("nt10", "Leave a note on the Notion page abc123 asking who owns this.",
         "notion_add_comment", "hard", trap="jira_add_comment"),
    Task("nt11", "Find the pricing doc - it is in Notion somewhere, not Drive.",
         "notion_search_pages", "hard", trap="gdrive_search_files"),
    Task("nt12", "Share the Notion runbook page abc123 with ravi@acme.com as a reader.",
         "notion_share_page", "hard", trap="gdrive_share_file"),

    # ---------------- zendesk ----------------
    Task("zd01", "Open a Zendesk ticket for customer sam@buyer.com about a failed checkout.",
         "zendesk_create_ticket", "easy"),
    Task("zd02", "Mark Zendesk ticket 4412 as solved.",
         "zendesk_update_ticket_status", "easy"),
    Task("zd03", "Assign Zendesk ticket 4412 to priya.",
         "zendesk_assign_ticket", "easy"),
    Task("zd04", "List the saved Zendesk views.",
         "zendesk_list_views", "easy"),
    Task("zd05", "Search Zendesk for open tickets mentioning refund.",
         "zendesk_search_tickets", "medium"),
    Task("zd06", "Add an internal note on Zendesk ticket 4412 that we are waiting on engineering.",
         "zendesk_add_comment", "medium"),
    Task("zd07", "Tag Zendesk ticket 4412 as billing and urgent.",
         "zendesk_add_tag", "medium"),
    Task("zd08", "Ticket 4499 is a duplicate of 4412 - combine them.",
         "zendesk_merge_tickets", "medium"),
    Task("zd09", "A customer emailed saying the CSV export is broken. Log it in our support desk.",
         "zendesk_create_ticket", "hard", trap="github_create_issue"),
    Task("zd10", "Who on the support team can I hand this ticket to?",
         "zendesk_list_agents", "hard", trap="jira_list_users"),
    Task("zd11", "Ticket 4412 is beyond tier 1 - push it up to engineering.",
         "zendesk_escalate_ticket", "hard", trap="pagerduty_trigger_incident"),
    Task("zd12", "Reply to the customer on Zendesk ticket 4412 that the fix ships Friday.",
         "zendesk_add_comment", "hard", trap="jira_add_comment"),

    # ---------------- pagerduty ----------------
    Task("pd01", "Trigger a PagerDuty incident on service svc_api titled 'Checkout 500s'.",
         "pagerduty_trigger_incident", "easy"),
    Task("pd02", "Acknowledge PagerDuty incident inc_991.",
         "pagerduty_acknowledge_incident", "easy"),
    Task("pd03", "List all triggered PagerDuty incidents.",
         "pagerduty_list_incidents", "easy"),
    Task("pd04", "Which PagerDuty services exist?",
         "pagerduty_list_services", "easy"),
    Task("pd05", "Who is on call right now for schedule sch_12?",
         "pagerduty_get_oncall", "medium"),
    Task("pd06", "Set up a weekly PagerDuty on-call rotation for the platform team.",
         "pagerduty_create_schedule", "medium"),
    Task("pd07", "Snooze PagerDuty incident inc_991 for 30 minutes.",
         "pagerduty_snooze_incident", "medium"),
    Task("pd08", "Pull ravi into PagerDuty incident inc_991 as another responder.",
         "pagerduty_add_responder", "medium"),
    Task("pd09", "The outage is over - close out incident inc_991.",
         "pagerduty_resolve_incident", "hard", trap="jira_transition_issue"),
    Task("pd10", "Record on incident inc_991 that we rolled back the deploy at 14:20.",
         "pagerduty_add_note", "hard", trap="jira_add_comment"),
    Task("pd11", "Checkout is down and nobody is looking at it. Page whoever is on call.",
         "pagerduty_trigger_incident", "hard", trap="zendesk_create_ticket"),
    Task("pd12", "Add lena to the active incident inc_991 so she gets the alerts.",
         "pagerduty_add_responder", "hard", trap="slack_invite_to_channel"),

    # ---------------- stripe ----------------
    Task("st01", "Create a Stripe customer for lena@buyer.com.",
         "stripe_create_customer", "easy"),
    Task("st02", "Refund Stripe charge ch_8891.",
         "stripe_refund_payment", "easy"),
    Task("st03", "What is the current Stripe account balance?",
         "stripe_get_balance", "easy"),
    Task("st04", "List Stripe subscriptions with status past_due.",
         "stripe_list_subscriptions", "easy"),
    Task("st05", "Invoice Stripe customer cus_44 for 250 dollars and send it.",
         "stripe_create_invoice", "medium"),
    Task("st06", "Find the Stripe customer with email sam@buyer.com.",
         "stripe_search_customers", "medium"),
    Task("st07", "Cancel Stripe subscription sub_77 at the end of the billing period.",
         "stripe_cancel_subscription", "medium"),
    Task("st08", "Show me recent Stripe charges for customer cus_44.",
         "stripe_list_charges", "medium"),
    Task("st09", "Bump customer cus_44 from 5 seats to 12 on their Stripe plan.",
         "stripe_update_subscription", "hard", trap="stripe_create_invoice"),
    Task("st10", "Make a Stripe link I can send a client to pay 500 dollars.",
         "stripe_create_payment_link", "hard", trap="stripe_create_invoice"),
    Task("st11", "The customer was double charged on ch_8891 - give them their money back.",
         "stripe_refund_payment", "hard", trap="stripe_cancel_subscription"),
    Task("st12", "Stop billing Stripe subscription sub_77 right now, not at period end.",
         "stripe_cancel_subscription", "hard", trap="stripe_update_subscription"),

    # ---------------- sentry ----------------
    Task("se01", "Search Sentry for unresolved errors mentioning NullPointer.",
         "sentry_search_issues", "easy"),
    Task("se02", "Show the stack trace for Sentry issue iss_55.",
         "sentry_get_issue_details", "easy"),
    Task("se03", "List the releases tracked in Sentry for project web.",
         "sentry_list_releases", "easy"),
    Task("se04", "Assign Sentry issue iss_55 to dmitri.",
         "sentry_assign_issue", "easy"),
    Task("se05", "Mark Sentry issue iss_55 resolved in release 4.2.0.",
         "sentry_resolve_issue", "medium"),
    Task("se06", "Ignore Sentry issue iss_55 for 2 hours.",
         "sentry_ignore_issue", "medium"),
    Task("se07", "Show the individual error events under Sentry issue iss_55.",
         "sentry_list_events", "medium"),
    Task("se08", "Alert us in Sentry when project web goes over 500 errors.",
         "sentry_create_alert_rule", "medium"),
    Task("se09", "We already have PLAT-412 for this crash - connect Sentry issue iss_55 to it.",
         "sentry_link_to_tracker", "hard", trap="jira_create_issue"),
    Task("se10", "The app is throwing errors in production - find out what is breaking.",
         "sentry_search_issues", "hard", trap="github_search_issues"),
    Task("se11", "Note on Sentry issue iss_55 that this only reproduces on Safari.",
         "sentry_add_comment", "hard", trap="jira_add_comment"),
    Task("se12", "That crash is fixed and shipped - clear it from the unresolved list.",
         "sentry_resolve_issue", "hard", trap="pagerduty_resolve_incident"),
]
