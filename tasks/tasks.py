"""Labelled evaluation tasks: 60 queries, one gold tool each.

TIERS -- report accuracy per tier, never blended only.

  easy    The query names the system explicitly ("Open a GitHub issue...").
          Tests basic retrieval. A keyword baseline should do well here.

  medium  The system is implied but not named ("Where is validate_jwt
          defined?"). Tests semantic matching.

  hard    The query sits on a seeded trap: a plausible wrong tool exists and is
          lexically closer than the right one, or the query uses the vocabulary
          of a neighbouring system. Tests actual disambiguation.

Every hard task still has a single defensible answer -- disambiguation requires
care, not guessing. If you cannot justify the gold label in one sentence, the
task is broken; fix it rather than tolerating a noisy label.

`trap` names the tool we expect a weak selector to pick instead. Scoring uses
it to split errors into "fell into the designed trap" vs "picked something
unrelated". The first number tells you the selector is lexically fooled; the
second tells you it has no idea.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    id: str
    query: str
    gold: str
    tier: str  # "easy" | "medium" | "hard"
    trap: str | None = None


TASKS: list[Task] = [
    # ---------------- github ----------------
    Task("gh01", "Open a GitHub issue in acme/web-app titled 'Login button unresponsive on Safari'.",
         "github_create_issue", "easy"),
    Task("gh02", "Merge pull request 482 in acme/web-app using squash.",
         "github_merge_pull_request", "easy"),
    Task("gh03", "Create a branch called hotfix/session-timeout in acme/api off main.",
         "github_create_branch", "easy"),
    Task("gh04", "Did the latest CI workflow run pass on acme/web-app?",
         "github_get_workflow_runs", "easy"),
    Task("gh05", "Find every open bug report in the acme/web-app repository mentioning timeout.",
         "github_search_issues", "medium"),
    Task("gh06", "Show me all the pull requests waiting for review on acme/api.",
         "github_list_pull_requests", "medium"),
    Task("gh07", "Where in acme/api is the function validate_jwt defined?",
         "github_search_code", "medium"),
    Task("gh08", "Give maya push access to the acme/infra repo.",
         "github_add_collaborator", "medium"),
    Task("gh09", "We use GitHub for code and Jira for planning. A user reported the CSV export is "
                 "broken - file that against the repo acme/web-app.",
         "github_create_issue", "hard", trap="jira_create_issue"),
    Task("gh10", "Reply on pull request 71 in acme/api that the migration needs a rollback plan.",
         "github_add_comment", "hard", trap="slack_post_message"),
    Task("gh11", "Which PRs in acme/web-app did dmitri open that mention caching?",
         "github_search_pull_requests", "hard", trap="github_list_pull_requests"),
    Task("gh12", "Our repo acme/infra needs sam to be able to merge - sort out their access.",
         "github_add_collaborator", "hard", trap="gdrive_share_file"),

    # ---------------- jira ----------------
    Task("jr01", "Create a Jira bug in project PLAT titled 'Checkout total miscalculated with coupons'.",
         "jira_create_issue", "easy"),
    Task("jr02", "Move PLAT-412 to In Progress.",
         "jira_transition_issue", "easy"),
    Task("jr03", "Assign PLAT-388 to ravi.",
         "jira_assign_issue", "easy"),
    Task("jr04", "List the active sprints on Jira board 17.",
         "jira_list_sprints", "easy"),
    Task("jr05", "Which Jira tickets in PLAT are still unresolved and assigned to me?",
         "jira_search_issues", "medium"),
    Task("jr06", "Pull PLAT-501 into sprint 42.",
         "jira_add_issue_to_sprint", "medium"),
    Task("jr07", "I spent 3 hours and 30 minutes on PLAT-412 this afternoon - record that.",
         "jira_log_work", "medium"),
    Task("jr08", "Break PLAT-500 down - add a subtask for the database migration.",
         "jira_create_subtask", "medium"),
    Task("jr09", "Planning lives in Jira. The design review turned up a button spacing bug - "
                 "raise a ticket for it in PLAT.",
         "jira_create_issue", "hard", trap="github_create_issue"),
    Task("jr10", "Add a note to PLAT-412 explaining we are blocked on the vendor.",
         "jira_add_comment", "hard", trap="github_add_comment"),
    Task("jr11", "Who can I assign PLAT tickets to?",
         "jira_list_users", "hard", trap="slack_list_users"),
    Task("jr12", "Our tracker is Jira. Find everything tagged payments that is still open.",
         "jira_search_issues", "hard", trap="github_search_issues"),

    # ---------------- slack ----------------
    Task("sl01", "Post in the engineering Slack channel that the deploy is done.",
         "slack_post_message", "easy"),
    Task("sl02", "Create a private Slack channel called incident-2026-10-03.",
         "slack_create_channel", "easy"),
    Task("sl03", "React with the eyes emoji to the Slack message at 1727950000.123 in ops.",
         "slack_add_reaction", "easy"),
    Task("sl04", "Set my Slack status to 'In deep work' until 5pm.",
         "slack_set_status", "easy"),
    Task("sl05", "Message priya directly to ask if she has reviewed the RFC.",
         "slack_send_dm", "medium"),
    Task("sl06", "Which Slack channels exist in the workspace?",
         "slack_list_channels", "medium"),
    Task("sl07", "Search Slack for where we discussed the Redis migration.",
         "slack_search_messages", "medium"),
    Task("sl08", "Add tom and lena to the incident-response Slack channel.",
         "slack_invite_to_channel", "medium"),
    Task("sl09", "Drop the build log file into the ci-alerts Slack channel so the team can see it.",
         "slack_upload_file", "hard", trap="gdrive_upload_file"),
    Task("sl10", "Tell the team in the engineering channel that PLAT-412 is blocked.",
         "slack_post_message", "hard", trap="jira_add_comment"),
    Task("sl11", "Quietly ask ravi about the outage - do not put it in a channel.",
         "slack_send_dm", "hard", trap="slack_post_message"),
    Task("sl12", "Who is in our Slack workspace?",
         "slack_list_users", "hard", trap="jira_list_users"),

    # ---------------- gcalendar ----------------
    Task("cal01", "Create a calendar event called 'Arch review' on 2026-10-09 from 14:00 to 15:00.",
         "gcalendar_create_event", "easy"),
    Task("cal02", "Cancel the calendar event with id evt_8812 and let the attendees know.",
         "gcalendar_cancel_event", "easy"),
    Task("cal03", "Set up a weekly standup on the calendar every Monday at 9:30am.",
         "gcalendar_create_recurring_event", "easy"),
    Task("cal04", "What is on my calendar between October 6 and October 10?",
         "gcalendar_list_events", "easy"),
    Task("cal05", "When are priya, tom and I all free for 45 minutes this week?",
         "gcalendar_find_free_slots", "medium"),
    Task("cal06", "Push the arch review event evt_8812 back to 16:00.",
         "gcalendar_update_event", "medium"),
    Task("cal07", "Add lena to the calendar event evt_8812.",
         "gcalendar_invite_attendees", "medium"),
    Task("cal08", "Is the Oak meeting room free tomorrow from 10 to 11am?",
         "gcalendar_check_room_availability", "medium"),
    Task("cal09", "I am on leave October 14 to 18 - block it off and auto-decline anything "
                  "that comes in.",
         "gcalendar_set_out_of_office", "hard", trap="slack_set_status"),
    Task("cal10", "Find a slot for the retro - everyone on the team needs to be there, one hour.",
         "gcalendar_find_free_slots", "hard", trap="gcalendar_list_events"),
    Task("cal11", "Pull up everything about calendar event evt_8812.",
         "gcalendar_get_event_details", "hard", trap="gcalendar_list_events"),
    Task("cal12", "Loop maya into the arch review meeting evt_8812.",
         "gcalendar_invite_attendees", "hard", trap="slack_invite_to_channel"),

    # ---------------- gdrive ----------------
    Task("dr01", "Create a Google Drive folder called Q4 Planning.",
         "gdrive_create_folder", "easy"),
    Task("dr02", "Delete the Drive file with id 1aBc.",
         "gdrive_delete_file", "easy"),
    Task("dr03", "Export the Drive doc 1xYz as a PDF.",
         "gdrive_export_file", "easy"),
    Task("dr04", "Upload ./report.xlsx to the Drive folder 1QQQ.",
         "gdrive_upload_file", "easy"),
    Task("dr05", "Find the Drive doc about the 2026 pricing model.",
         "gdrive_search_files", "medium"),
    Task("dr06", "What is inside the Drive folder 1QQQ?",
         "gdrive_list_files", "medium"),
    Task("dr07", "Give maya@acme.com edit access to the Drive file 1xYz.",
         "gdrive_share_file", "medium"),
    Task("dr08", "Move the Drive file 1aBc into folder 1QQQ.",
         "gdrive_move_file", "medium"),
    Task("dr09", "Make a duplicate of the budget sheet 1xYz in Drive before I edit it.",
         "gdrive_copy_file", "hard", trap="gdrive_move_file"),
    Task("dr10", "Who currently has access to the Drive file 1xYz?",
         "gdrive_get_file_permissions", "hard", trap="gdrive_share_file"),
    Task("dr11", "Put the quarterly deck into Drive under folder 1QQQ.",
         "gdrive_upload_file", "hard", trap="slack_upload_file"),
    Task("dr12", "I need the pricing doc - search Drive, I do not know which folder it is in.",
         "gdrive_search_files", "hard", trap="gdrive_list_files"),
]


def by_tier(tier: str) -> list[Task]:
    return [t for t in TASKS if t.tier == tier]


TIERS = ("easy", "medium", "hard")
