"""One-line blurb per domain, used as the hierarchical router's menu.

Kept roughly uniform in length so the level-1 routing choice is not biased
by one domain simply having more text than another.
"""

from __future__ import annotations

DOMAIN_DESCRIPTIONS: dict[str, str] = {
    "github": (
        "Source code hosting: repositories, branches, issues, pull requests, "
        "code search, CI workflow runs, and collaborator access."
    ),
    "jira": (
        "Project and issue tracking: tickets, subtasks, workflow transitions, "
        "assignees, sprints, boards, and worklogs."
    ),
    "linear": (
        "Issue and project tracking: issues, cycles, projects, triage, "
        "labels, assignees, workflow states, and sub-issues."
    ),
    "slack": (
        "Team chat: channel and direct messages, channel management, message "
        "search, reactions, file uploads, and user status."
    ),
    "gcalendar": (
        "Scheduling: calendar events, recurring meetings, availability "
        "lookup, attendee invitations, meeting rooms, and out-of-office."
    ),
    "gdrive": (
        "Cloud file storage: file and folder search, listing, upload, move, "
        "copy, export, deletion, and sharing permissions."
    ),
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
    "confluence": (
        "Team workspace and wiki: spaces, pages, blog posts, attachments, "
        "page comments, exports, version history, and archiving."
    ),
    "gitlab": (
        "DevOps and code hosting: repositories, merge requests, issues, "
        "branches, CI/CD pipelines, code search, and project members."
    ),
    "bitbucket": (
        "Atlassian code hosting: repositories, branches, commits, pull "
        "requests, inline review comments, pipelines, and repository "
        "access."
    ),
    "asana": (
        "Work management: tasks and subtasks, projects, assignees, due "
        "dates, followers, completion, and project status updates."
    ),
    "trello": (
        "Kanban boards: boards, lists and cards, moving cards between "
        "lists, checklists, members, due dates, and archiving."
    ),
    "teams": (
        "Microsoft Teams: channel posts, private chats, channel creation "
        "and membership, message search, file sharing, and presence."
    ),
    "zoom": (
        "Video conferencing: scheduled meetings and webinars, invitations, "
        "cancellations, cloud recordings, transcripts, and attendance."
    ),
    "outlook": (
        "Outlook mail and calendar: sending and searching mail, replies, "
        "drafts, folders, inbox rules, events, and automatic replies."
    ),
    "gmail": (
        "Gmail mailbox: sending and searching mail, replies and forwards, "
        "drafts, labels, archiving, filters, and vacation responders."
    ),
    "dropbox": (
        "Dropbox storage: uploads, search, folders, moves, deletion, shared "
        "links, shared-folder members, and revision restore."
    ),
    "box": (
        "Box content management: uploads, search, folders, moves, deletion, "
        "shared links, collaborators, file locking, and comments."
    ),
    "onedrive": (
        "OneDrive storage: uploads, search, folders, moves and copies, "
        "deletion, sharing links, permissions, and version history."
    ),
    "sharepoint": (
        "SharePoint intranet: team sites, pages and news posts, document "
        "libraries, custom lists, check-out, and permissions."
    ),
    "salesforce": (
        "Salesforce CRM: leads and contacts, opportunities and pipeline "
        "stages, activity logging, tasks, cases, and reports."
    ),
    "hubspot": (
        "HubSpot CRM and marketing: contacts, deals and pipeline stages, "
        "activity logging, marketing email, lists, and forms."
    ),
    "intercom": (
        "Intercom customer messaging: live conversations, replies and "
        "internal notes, assignment, snoozing, tags, and articles."
    ),
    "freshdesk": (
        "Freshdesk support desk: customer tickets, public replies and "
        "private notes, assignment, priority, merging, and escalation."
    ),
    "datadog": (
        "Datadog observability: log search, metric queries, monitors and "
        "muting, dashboards, traces, service objectives, and hosts."
    ),
    "grafana": (
        "Grafana dashboards: dashboards and panels, datasource queries, "
        "alert rules and silences, annotations, and exports."
    ),
    "newrelic": (
        "New Relic performance monitoring: error inboxes, NRQL queries, "
        "traces, alert conditions, Apdex, and deployment markers."
    ),
    "opsgenie": (
        "Opsgenie alerting and on-call: raising and closing alerts, "
        "acknowledgement, rotations, responders, snoozing, and escalation."
    ),
    "figma": (
        "Figma design files: files and pages, design comments, frame "
        "exports, component libraries, branches, sharing, and versions."
    ),
    "airtable": (
        "Airtable bases: records, tables and fields, filtered views, "
        "querying, updates and deletion, attachments, and CSV export."
    ),
    "okta": (
        "Okta identity and access: user lifecycle, group membership, "
        "application assignments, credential resets, and MFA policy."
    ),
}
