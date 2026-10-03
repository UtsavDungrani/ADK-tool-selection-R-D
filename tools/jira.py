"""jira tools.

Project and issue tracking: tickets, subtasks, workflow transitions,
assignees, sprints, boards, and worklogs.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="jira", confusable_with=["github_create_issue", "jira_create_subtask"])
def jira_create_issue(
    project: str,
    summary: str,
    issue_type: Literal['Bug', 'Story', 'Task', 'Epic'],
    description: Optional[str] = None,
) -> dict:
    """Create a new Jira ticket in a project, such as a bug, story, or task.

    Args:
        project: Jira project key, e.g. PLAT.
        summary: One-line ticket summary.
        issue_type: Type of ticket to create. One of: Bug, Story, Task, Epic.
        description: Full ticket description.
    """
    return {"status": "stub", "tool": "jira_create_issue", "args": locals()}


@tool(domain="jira", confusable_with=["github_search_issues"])
def jira_search_issues(jql: str, limit: Optional[int] = None) -> dict:
    """Search Jira tickets using JQL or free text, filtered by project, status, or assignee.

    Args:
        jql: JQL expression or free-text query.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "jira_search_issues", "args": locals()}


@tool(domain="jira", confusable_with=["github_add_comment"])
def jira_add_comment(issue_key: str, body: str) -> dict:
    """Add a comment to an existing Jira ticket.

    Args:
        issue_key: Jira issue key, e.g. PLAT-412.
        body: Comment text.
    """
    return {"status": "stub", "tool": "jira_add_comment", "args": locals()}


@tool(domain="jira")
def jira_transition_issue(issue_key: str, status: str) -> dict:
    """Move a Jira ticket to a different workflow status, such as In Progress or Done.

    Args:
        issue_key: Jira issue key, e.g. PLAT-412.
        status: Target workflow status.
    """
    return {"status": "stub", "tool": "jira_transition_issue", "args": locals()}


@tool(domain="jira")
def jira_assign_issue(issue_key: str, assignee: str) -> dict:
    """Assign a Jira ticket to a specific user.

    Args:
        issue_key: Jira issue key, e.g. PLAT-412.
        assignee: Username or account ID of the assignee.
    """
    return {"status": "stub", "tool": "jira_assign_issue", "args": locals()}


@tool(domain="jira")
def jira_list_sprints(
    board_id: int,
    state: Optional[Literal['active', 'future', 'closed']] = None,
) -> dict:
    """List sprints for a Jira board, including active, future, and closed sprints.

    Args:
        board_id: Numeric Jira board identifier.
        state: Filter by sprint state. One of: active, future, closed.
    """
    return {"status": "stub", "tool": "jira_list_sprints", "args": locals()}


@tool(domain="jira")
def jira_add_issue_to_sprint(issue_key: str, sprint_id: int) -> dict:
    """Move a Jira ticket into a sprint backlog for upcoming work.

    Args:
        issue_key: Jira issue key, e.g. PLAT-412.
        sprint_id: Numeric sprint identifier.
    """
    return {"status": "stub", "tool": "jira_add_issue_to_sprint", "args": locals()}


@tool(domain="jira", confusable_with=["slack_list_users"])
def jira_list_users(project: Optional[str] = None, limit: Optional[int] = None) -> dict:
    """List users in the Jira instance who can be assigned tickets.

    Args:
        project: Restrict to users with access to this project.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "jira_list_users", "args": locals()}


@tool(domain="jira")
def jira_log_work(
    issue_key: str,
    time_spent: str,
    comment: Optional[str] = None,
) -> dict:
    """Record time spent working on a Jira ticket as a worklog entry.

    Args:
        issue_key: Jira issue key, e.g. PLAT-412.
        time_spent: Duration in Jira format, e.g. 3h 30m.
        comment: Note describing the work done.
    """
    return {"status": "stub", "tool": "jira_log_work", "args": locals()}


@tool(domain="jira", confusable_with=["jira_create_issue"])
def jira_create_subtask(parent_key: str, summary: str) -> dict:
    """Create a subtask underneath an existing Jira ticket.

    Args:
        parent_key: Parent Jira issue key.
        summary: One-line subtask summary.
    """
    return {"status": "stub", "tool": "jira_create_subtask", "args": locals()}
