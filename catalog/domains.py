"""The v1 catalog: 50 tools across 5 domains.

DESIGN INTENT -- read before adding tools.

Raw tool count is the *weak* independent variable. What actually degrades
selection accuracy is **distractor density**: how many tools in the catalog are
plausible-but-wrong answers for a given query. This catalog is therefore built
around deliberate collisions, documented per tool in `confusable_with`.

Three collision classes are seeded:

  1. CROSS-DOMAIN HOMONYMS -- same verb+noun, different system.
       github_create_issue  <-> jira_create_issue
       slack_upload_file    <-> gdrive_upload_file
     Resolving these requires the query to name the system, or the model to
     infer it from context. These are the hardest cases and the most realistic:
     any org running both GitHub and Jira has exactly this problem.

  2. WITHIN-DOMAIN NEAR-SYNONYMS -- list vs search vs get.
       gdrive_list_files <-> gdrive_search_files
       github_list_pull_requests <-> github_search_pull_requests
     Retrieval embeds these almost identically; the distinction lives in the
     *parameters*, not the description.

  3. SEMANTIC OVERLAP -- different surface form, overlapping intent.
       gdrive_share_file  <-> github_add_collaborator  ("give someone access")
       slack_post_message <-> github_add_comment       ("tell the team")

`confusable_with` is NEVER read by any selection strategy. It is used only in
scoring, to separate "model picked a random wrong tool" from "model fell into a
designed trap" -- the second is the interesting number.
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


# Frequently reused parameter shapes.
_repo = P("repo", "string", "Repository in owner/name form, e.g. acme/web-app.")
_query = P("query", "string", "Free-text search query.")
_limit = P("limit", "integer", "Maximum number of results to return.", required=False)

GITHUB = [
    _t("github_create_issue", "github",
       "Open a new issue on a GitHub repository to report a bug or request a feature.",
       [_repo,
        P("title", "string", "Short issue title."),
        P("body", "string", "Markdown description of the issue.", required=False),
        P("labels", "array", "Labels to apply to the new issue.", required=False)],
       ["jira_create_issue"]),
    _t("github_search_issues", "github",
       "Search issues in a GitHub repository by text, label, state, or author.",
       [_repo, _query,
        P("state", "string", "Filter by issue state.", required=False,
          enum=("open", "closed", "all")),
        _limit],
       ["jira_search_issues", "github_search_pull_requests"]),
    _t("github_list_pull_requests", "github",
       "List pull requests on a GitHub repository, optionally filtered by state.",
       [_repo,
        P("state", "string", "Filter by PR state.", required=False,
          enum=("open", "closed", "merged", "all")),
        _limit],
       ["github_search_pull_requests"]),
    _t("github_search_pull_requests", "github",
       "Search pull requests in a GitHub repository by title text, author, or review status.",
       [_repo, _query,
        P("author", "string", "Filter to PRs opened by this user.", required=False),
        _limit],
       ["github_list_pull_requests", "github_search_issues"]),
    _t("github_merge_pull_request", "github",
       "Merge an open pull request into its base branch on GitHub.",
       [_repo,
        P("pr_number", "integer", "Pull request number to merge."),
        P("method", "string", "Merge strategy.", required=False,
          enum=("merge", "squash", "rebase"))]),
    _t("github_add_comment", "github",
       "Post a comment on an existing GitHub issue or pull request.",
       [_repo,
        P("number", "integer", "Issue or pull request number."),
        P("body", "string", "Markdown comment text.")],
       ["jira_add_comment", "slack_post_message"]),
    _t("github_search_code", "github",
       "Search source code contents across a GitHub repository for a string or pattern.",
       [_repo, _query,
        P("language", "string", "Restrict results to this language.", required=False)],
       ["gdrive_search_files"]),
    _t("github_add_collaborator", "github",
       "Grant a GitHub user push or admin access to a repository.",
       [_repo,
        P("username", "string", "GitHub username to add."),
        P("permission", "string", "Access level to grant.", required=False,
          enum=("read", "write", "admin"))],
       ["gdrive_share_file"]),
    _t("github_create_branch", "github",
       "Create a new git branch in a GitHub repository from an existing ref.",
       [_repo,
        P("branch", "string", "Name of the branch to create."),
        P("from_ref", "string", "Base branch or commit SHA.", required=False)]),
    _t("github_get_workflow_runs", "github",
       "Retrieve recent GitHub Actions CI workflow runs and their pass or fail status.",
       [_repo,
        P("workflow", "string", "Workflow file name to filter by.", required=False),
        P("status", "string", "Filter by run status.", required=False,
          enum=("success", "failure", "in_progress")),
        _limit]),
]

JIRA = [
    _t("jira_create_issue", "jira",
       "Create a new Jira ticket in a project, such as a bug, story, or task.",
       [P("project", "string", "Jira project key, e.g. PLAT."),
        P("summary", "string", "One-line ticket summary."),
        P("issue_type", "string", "Type of ticket to create.",
          enum=("Bug", "Story", "Task", "Epic")),
        P("description", "string", "Full ticket description.", required=False)],
       ["github_create_issue", "jira_create_subtask"]),
    _t("jira_search_issues", "jira",
       "Search Jira tickets using JQL or free text, filtered by project, status, or assignee.",
       [P("jql", "string", "JQL expression or free-text query."), _limit],
       ["github_search_issues"]),
    _t("jira_add_comment", "jira",
       "Add a comment to an existing Jira ticket.",
       [P("issue_key", "string", "Jira issue key, e.g. PLAT-412."),
        P("body", "string", "Comment text.")],
       ["github_add_comment"]),
    _t("jira_transition_issue", "jira",
       "Move a Jira ticket to a different workflow status, such as In Progress or Done.",
       [P("issue_key", "string", "Jira issue key, e.g. PLAT-412."),
        P("status", "string", "Target workflow status.")]),
    _t("jira_assign_issue", "jira",
       "Assign a Jira ticket to a specific user.",
       [P("issue_key", "string", "Jira issue key, e.g. PLAT-412."),
        P("assignee", "string", "Username or account ID of the assignee.")]),
    _t("jira_list_sprints", "jira",
       "List sprints for a Jira board, including active, future, and closed sprints.",
       [P("board_id", "integer", "Numeric Jira board identifier."),
        P("state", "string", "Filter by sprint state.", required=False,
          enum=("active", "future", "closed"))]),
    _t("jira_add_issue_to_sprint", "jira",
       "Move a Jira ticket into a sprint backlog for upcoming work.",
       [P("issue_key", "string", "Jira issue key, e.g. PLAT-412."),
        P("sprint_id", "integer", "Numeric sprint identifier.")]),
    _t("jira_list_users", "jira",
       "List users in the Jira instance who can be assigned tickets.",
       [P("project", "string", "Restrict to users with access to this project.",
          required=False),
        _limit],
       ["slack_list_users"]),
    _t("jira_log_work", "jira",
       "Record time spent working on a Jira ticket as a worklog entry.",
       [P("issue_key", "string", "Jira issue key, e.g. PLAT-412."),
        P("time_spent", "string", "Duration in Jira format, e.g. 3h 30m."),
        P("comment", "string", "Note describing the work done.", required=False)]),
    _t("jira_create_subtask", "jira",
       "Create a subtask underneath an existing Jira ticket.",
       [P("parent_key", "string", "Parent Jira issue key."),
        P("summary", "string", "One-line subtask summary.")],
       ["jira_create_issue"]),
]

SLACK = [
    _t("slack_post_message", "slack",
       "Post a message to a public or private Slack channel.",
       [P("channel", "string", "Channel name or ID, e.g. engineering."),
        P("text", "string", "Message body."),
        P("thread_ts", "string", "Timestamp of a parent message to reply in-thread.",
          required=False)],
       ["slack_send_dm", "github_add_comment"]),
    _t("slack_send_dm", "slack",
       "Send a direct private message to a single Slack user.",
       [P("user", "string", "Slack username or user ID."),
        P("text", "string", "Message body.")],
       ["slack_post_message"]),
    _t("slack_create_channel", "slack",
       "Create a new Slack channel, public or private.",
       [P("name", "string", "Channel name without the leading hash."),
        P("is_private", "boolean", "Whether the channel should be private.",
          required=False)]),
    _t("slack_list_channels", "slack",
       "List Slack channels in the workspace that the caller can see.",
       [P("types", "string", "Channel visibility filter.", required=False,
          enum=("public", "private", "all")),
        _limit]),
    _t("slack_search_messages", "slack",
       "Search the Slack message history across channels for text.",
       [_query,
        P("channel", "string", "Restrict the search to one channel.", required=False),
        _limit]),
    _t("slack_invite_to_channel", "slack",
       "Invite one or more Slack users into an existing channel.",
       [P("channel", "string", "Channel name or ID."),
        P("users", "array", "Slack user IDs to invite.")],
       ["gdrive_share_file"]),
    _t("slack_list_users", "slack",
       "List members of the Slack workspace with their display names.",
       [_limit],
       ["jira_list_users"]),
    _t("slack_set_status", "slack",
       "Set the caller's Slack status text, emoji, and expiry.",
       [P("text", "string", "Status text to display."),
        P("emoji", "string", "Status emoji shortcode.", required=False),
        P("expires_at", "string", "ISO 8601 timestamp when the status clears.",
          required=False)],
       ["gcalendar_set_out_of_office"]),
    _t("slack_upload_file", "slack",
       "Upload a file attachment into a Slack channel or conversation.",
       [P("channel", "string", "Destination channel name or ID."),
        P("file_path", "string", "Local path of the file to upload."),
        P("title", "string", "Display title for the file.", required=False)],
       ["gdrive_upload_file"]),
    _t("slack_add_reaction", "slack",
       "Add an emoji reaction to an existing Slack message.",
       [P("channel", "string", "Channel containing the message."),
        P("timestamp", "string", "Timestamp identifying the message."),
        P("emoji", "string", "Emoji shortcode to add.")]),
]

GCALENDAR = [
    _t("gcalendar_create_event", "gcalendar",
       "Create a new calendar event at a fixed date and time.",
       [P("title", "string", "Event title."),
        P("start", "string", "ISO 8601 start datetime."),
        P("end", "string", "ISO 8601 end datetime."),
        P("attendees", "array", "Email addresses to invite.", required=False)],
       ["gcalendar_create_recurring_event"]),
    _t("gcalendar_list_events", "gcalendar",
       "List calendar events occurring within a date range.",
       [P("start_date", "string", "ISO 8601 range start."),
        P("end_date", "string", "ISO 8601 range end."),
        _limit],
       ["gcalendar_find_free_slots"]),
    _t("gcalendar_find_free_slots", "gcalendar",
       "Find open time slots when all listed people are available to meet.",
       [P("attendees", "array", "Email addresses to check availability for."),
        P("duration_minutes", "integer", "Required meeting length in minutes."),
        P("search_until", "string", "ISO 8601 date to search up to.", required=False)],
       ["gcalendar_list_events", "gcalendar_check_room_availability"]),
    _t("gcalendar_update_event", "gcalendar",
       "Change the time, title, or location of an existing calendar event.",
       [P("event_id", "string", "Identifier of the event to update."),
        P("start", "string", "New ISO 8601 start datetime.", required=False),
        P("title", "string", "New event title.", required=False)]),
    _t("gcalendar_cancel_event", "gcalendar",
       "Cancel a calendar event and notify its attendees.",
       [P("event_id", "string", "Identifier of the event to cancel."),
        P("notify", "boolean", "Whether to email attendees.", required=False)]),
    _t("gcalendar_invite_attendees", "gcalendar",
       "Add additional attendees to an existing calendar event.",
       [P("event_id", "string", "Identifier of the event."),
        P("attendees", "array", "Email addresses to add.")],
       ["slack_invite_to_channel"]),
    _t("gcalendar_create_recurring_event", "gcalendar",
       "Create a repeating calendar event such as a weekly standup.",
       [P("title", "string", "Event title."),
        P("start", "string", "ISO 8601 start datetime of the first occurrence."),
        P("recurrence", "string",
          "Recurrence rule, e.g. RRULE:FREQ=WEEKLY;BYDAY=MO.")],
       ["gcalendar_create_event"]),
    _t("gcalendar_get_event_details", "gcalendar",
       "Retrieve the full details of one calendar event by its identifier.",
       [P("event_id", "string", "Identifier of the event.")]),
    _t("gcalendar_set_out_of_office", "gcalendar",
       "Mark a date range as out of office and auto-decline meeting invitations.",
       [P("start_date", "string", "ISO 8601 first day out."),
        P("end_date", "string", "ISO 8601 last day out."),
        P("message", "string", "Auto-decline message.", required=False)],
       ["slack_set_status"]),
    _t("gcalendar_check_room_availability", "gcalendar",
       "Check whether a bookable meeting room is free during a time window.",
       [P("room", "string", "Room name or resource ID."),
        P("start", "string", "ISO 8601 window start."),
        P("end", "string", "ISO 8601 window end.")],
       ["gcalendar_find_free_slots"]),
]

GDRIVE = [
    _t("gdrive_search_files", "gdrive",
       "Search Google Drive for files matching text in their name or contents.",
       [_query,
        P("mime_type", "string", "Restrict to a MIME type.", required=False),
        _limit],
       ["gdrive_list_files", "github_search_code"]),
    _t("gdrive_list_files", "gdrive",
       "List the files inside a specific Google Drive folder.",
       [P("folder_id", "string", "Identifier of the folder to list."), _limit],
       ["gdrive_search_files"]),
    _t("gdrive_share_file", "gdrive",
       "Share a Google Drive file with a person and set their permission level.",
       [P("file_id", "string", "Identifier of the file to share."),
        P("email", "string", "Email address of the recipient."),
        P("role", "string", "Permission level to grant.", required=False,
          enum=("reader", "commenter", "writer"))],
       ["github_add_collaborator", "slack_invite_to_channel"]),
    _t("gdrive_create_folder", "gdrive",
       "Create a new folder in Google Drive.",
       [P("name", "string", "Folder name."),
        P("parent_id", "string", "Identifier of the parent folder.", required=False)]),
    _t("gdrive_move_file", "gdrive",
       "Move a Google Drive file into a different folder.",
       [P("file_id", "string", "Identifier of the file to move."),
        P("target_folder_id", "string", "Destination folder identifier.")],
       ["gdrive_copy_file"]),
    _t("gdrive_copy_file", "gdrive",
       "Create a duplicate copy of a Google Drive file.",
       [P("file_id", "string", "Identifier of the file to copy."),
        P("new_name", "string", "Name for the copy.", required=False)],
       ["gdrive_move_file"]),
    _t("gdrive_delete_file", "gdrive",
       "Move a Google Drive file to the trash.",
       [P("file_id", "string", "Identifier of the file to delete.")]),
    _t("gdrive_export_file", "gdrive",
       "Export a Google Doc or Sheet to another format such as PDF or XLSX.",
       [P("file_id", "string", "Identifier of the file to export."),
        P("format", "string", "Target export format.",
          enum=("pdf", "docx", "xlsx", "csv"))]),
    _t("gdrive_get_file_permissions", "gdrive",
       "List who currently has access to a Google Drive file and at what level.",
       [P("file_id", "string", "Identifier of the file.")]),
    _t("gdrive_upload_file", "gdrive",
       "Upload a local file into a Google Drive folder.",
       [P("file_path", "string", "Local path of the file to upload."),
        P("folder_id", "string", "Destination folder identifier.", required=False)],
       ["slack_upload_file"]),
]

DOMAINS: dict[str, list[ToolSpec]] = {
    "github": GITHUB,
    "jira": JIRA,
    "slack": SLACK,
    "gcalendar": GCALENDAR,
    "gdrive": GDRIVE,
}

ALL_SPECS: list[ToolSpec] = [s for specs in DOMAINS.values() for s in specs]

# Used by the hierarchical strategy as the first-level menu. Keep these
# descriptions roughly uniform in length so the level-1 choice is not biased by
# one domain simply having more text.
DOMAIN_DESCRIPTIONS: dict[str, str] = {
    "github": (
        "Source code hosting: repositories, branches, issues, pull requests, "
        "code search, CI workflow runs, and collaborator access."
    ),
    "jira": (
        "Project and issue tracking: tickets, subtasks, workflow transitions, "
        "assignees, sprints, boards, and worklogs."
    ),
    "slack": (
        "Team chat: channel and direct messages, channel management, message "
        "search, reactions, file uploads, and user status."
    ),
    "gcalendar": (
        "Scheduling: calendar events, recurring meetings, availability lookup, "
        "attendee invitations, meeting rooms, and out-of-office."
    ),
    "gdrive": (
        "Cloud file storage: file and folder search, listing, upload, move, "
        "copy, export, deletion, and sharing permissions."
    ),
}
