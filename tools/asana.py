"""asana tools.

Work management: tasks, subtasks, projects, assignees, due dates, followers,
and project status updates.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="asana", confusable_with=["jira_create_issue", "linear_create_issue", "trello_create_card"])
def asana_create_task(
    project: str,
    name: str,
    notes: Optional[str] = None,
    assignee: Optional[str] = None,
    due_on: Optional[str] = None,
) -> dict:
    """Create a task in an Asana project with optional assignee and due date.

    Args:
        project: Asana project name or identifier.
        name: Short task name.
        notes: Longer description of the work.
        assignee: Email or user identifier to assign the task to.
        due_on: Due date in YYYY-MM-DD form.
    """
    return {"status": "stub", "tool": "asana_create_task", "args": locals()}


@tool(domain="asana", confusable_with=["jira_search_issues", "linear_search_issues"])
def asana_search_tasks(
    query: str,
    project: Optional[str] = None,
    completed: Optional[bool] = None,
    limit: Optional[int] = None,
) -> dict:
    """Search Asana tasks by free text, optionally scoped to one project.

    Args:
        query: Free-text search query.
        project: Restrict the search to this project.
        completed: Include only completed or only open tasks.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "asana_search_tasks", "args": locals()}


@tool(domain="asana", confusable_with=["jira_transition_issue", "linear_update_issue_status"])
def asana_complete_task(task_id: str, completed: Optional[bool] = None) -> dict:
    """Mark an Asana task as complete, or reopen one that was completed.

    Args:
        task_id: Identifier of the task.
        completed: True to complete the task, False to reopen it.
    """
    return {"status": "stub", "tool": "asana_complete_task", "args": locals()}


@tool(domain="asana", confusable_with=["jira_assign_issue", "linear_assign_issue"])
def asana_assign_task(task_id: str, assignee: str) -> dict:
    """Reassign an existing Asana task to a different team member.

    Args:
        task_id: Identifier of the task.
        assignee: Email or user identifier of the new owner.
    """
    return {"status": "stub", "tool": "asana_assign_task", "args": locals()}


@tool(domain="asana", confusable_with=["jira_add_comment", "trello_add_comment"])
def asana_add_comment(task_id: str, text: str) -> dict:
    """Post a comment onto an Asana task's activity feed.

    Args:
        task_id: Identifier of the task.
        text: Comment body.
    """
    return {"status": "stub", "tool": "asana_add_comment", "args": locals()}


@tool(domain="asana", confusable_with=["linear_create_project"])
def asana_create_project(
    name: str,
    team: Optional[str] = None,
    privacy: Optional[Literal['public', 'private_to_team', 'private']] = None,
) -> dict:
    """Create a new Asana project to group related tasks under a team.

    Args:
        name: Name of the new project.
        team: Team the project belongs to.
        privacy: Visibility. One of: public, private_to_team, private.
    """
    return {"status": "stub", "tool": "asana_create_project", "args": locals()}


@tool(domain="asana")
def asana_add_subtask(parent_task_id: str, name: str, assignee: Optional[str] = None) -> dict:
    """Break an Asana task down by adding a subtask beneath it.

    Args:
        parent_task_id: Identifier of the parent task.
        name: Name of the subtask.
        assignee: Email or user identifier to assign the subtask to.
    """
    return {"status": "stub", "tool": "asana_add_subtask", "args": locals()}


@tool(domain="asana", confusable_with=["trello_set_due_date", "gcalendar_update_event"])
def asana_set_due_date(task_id: str, due_on: str, start_on: Optional[str] = None) -> dict:
    """Change the deadline on an Asana task.

    Args:
        task_id: Identifier of the task.
        due_on: New due date in YYYY-MM-DD form.
        start_on: Optional start date in YYYY-MM-DD form.
    """
    return {"status": "stub", "tool": "asana_set_due_date", "args": locals()}


@tool(domain="asana", confusable_with=["slack_invite_to_channel"])
def asana_add_task_follower(task_id: str, follower: str) -> dict:
    """Subscribe someone to an Asana task so they receive its notifications.

    Args:
        task_id: Identifier of the task.
        follower: Email or user identifier to add as a follower.
    """
    return {"status": "stub", "tool": "asana_add_task_follower", "args": locals()}


@tool(domain="asana", confusable_with=["linear_list_cycles", "jira_list_sprints"])
def asana_post_project_status(
    project: str,
    text: str,
    status: Optional[Literal['on_track', 'at_risk', 'off_track', 'complete']] = None,
) -> dict:
    """Publish a progress update on an Asana project for stakeholders to read.

    Args:
        project: Asana project name or identifier.
        text: Body of the status update.
        status: Health signal. One of: on_track, at_risk, off_track, complete.
    """
    return {"status": "stub", "tool": "asana_post_project_status", "args": locals()}
