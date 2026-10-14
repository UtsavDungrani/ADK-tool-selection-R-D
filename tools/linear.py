"""linear tools.

Issue and project tracking: issues, cycles, projects, triage,
labels, assignees, workflow states, and sub-issues.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="linear", confusable_with=["jira_create_issue", "github_create_issue"])
def linear_create_issue(
    team: str,
    title: str,
    description: Optional[str] = None,
    priority: Optional[Literal['urgent', 'high', 'medium', 'low', 'none']] = None,
) -> dict:
    """Create a new issue in a Linear team with a title, description, and priority level.

    Args:
        team: Linear team identifier or key, e.g. ENG or OPS.
        title: Short title describing the issue.
        description: Markdown description and context for the issue.
        priority: Issue priority. One of: urgent, high, medium, low, none.
    """
    return {"status": "stub", "tool": "linear_create_issue", "args": locals()}


@tool(domain="linear", confusable_with=["jira_search_issues", "github_search_issues"])
def linear_search_issues(
    query: str,
    team: Optional[str] = None,
    status: Optional[Literal['backlog', 'unstarted', 'started', 'completed', 'canceled']] = None,
    limit: Optional[int] = None,
) -> dict:
    """Search Linear issues using text keywords, team filter, or issue state.

    Args:
        query: Free-text search query across title and description.
        team: Optional team identifier to filter issues.
        status: Filter by issue status. One of: backlog, unstarted, started, completed, canceled.
        limit: Maximum number of issues to return.
    """
    return {"status": "stub", "tool": "linear_search_issues", "args": locals()}


@tool(domain="linear", confusable_with=["jira_transition_issue"])
def linear_update_issue_status(
    issue_id: str,
    state: Literal['backlog', 'todo', 'in_progress', 'in_review', 'done', 'canceled'],
) -> dict:
    """Update the workflow state or status of an existing Linear issue.

    Args:
        issue_id: Linear issue identifier, e.g. ENG-404.
        state: New workflow state. One of: backlog, todo, in_progress, in_review, done, canceled.
    """
    return {"status": "stub", "tool": "linear_update_issue_status", "args": locals()}


@tool(domain="linear", confusable_with=["jira_add_comment", "github_add_comment", "notion_add_comment"])
def linear_add_comment(issue_id: str, body: str) -> dict:
    """Post a comment or discussion note to an existing Linear issue.

    Args:
        issue_id: Linear issue identifier, e.g. ENG-404.
        body: Comment content formatted in markdown.
    """
    return {"status": "stub", "tool": "linear_add_comment", "args": locals()}


@tool(domain="linear", confusable_with=["jira_assign_issue"])
def linear_assign_issue(issue_id: str, assignee: str) -> dict:
    """Assign an existing Linear issue to a specific team member.

    Args:
        issue_id: Linear issue identifier, e.g. ENG-404.
        assignee: Name, username, or email of the assignee.
    """
    return {"status": "stub", "tool": "linear_assign_issue", "args": locals()}


@tool(domain="linear", confusable_with=["jira_list_sprints"])
def linear_list_cycles(
    team: str,
    state: Optional[Literal['current', 'next', 'previous', 'all']] = None,
) -> dict:
    """List timeboxed development cycles for a team in Linear.

    Args:
        team: Linear team identifier, e.g. ENG.
        state: Cycle filter. One of: current, next, previous, all.
    """
    return {"status": "stub", "tool": "linear_list_cycles", "args": locals()}


@tool(domain="linear", confusable_with=["jira_add_issue_to_sprint"])
def linear_add_issue_to_cycle(issue_id: str, cycle_id: str) -> dict:
    """Assign an existing Linear issue into a planned work cycle.

    Args:
        issue_id: Linear issue identifier, e.g. ENG-404.
        cycle_id: Identifier of the target Linear cycle.
    """
    return {"status": "stub", "tool": "linear_add_issue_to_cycle", "args": locals()}


@tool(domain="linear", confusable_with=["jira_create_issue"])
def linear_create_project(
    team: str,
    name: str,
    description: Optional[str] = None,
) -> dict:
    """Create a new multi-issue roadmap project or initiative in Linear.

    Args:
        team: Linear team key responsible for the project.
        name: Project title or initiative name.
        description: Overview of the project scope and goals.
    """
    return {"status": "stub", "tool": "linear_create_project", "args": locals()}


@tool(domain="linear")
def linear_list_projects(
    team: Optional[str] = None,
    state: Optional[Literal['planned', 'started', 'paused', 'completed', 'canceled']] = None,
) -> dict:
    """List Linear roadmap projects optionally filtered by team or project state.

    Args:
        team: Optional team key to restrict results.
        state: Filter by state. One of: planned, started, paused, completed, canceled.
    """
    return {"status": "stub", "tool": "linear_list_projects", "args": locals()}


@tool(domain="linear", confusable_with=["jira_create_subtask"])
def linear_create_sub_issue(
    parent_id: str,
    title: str,
    description: Optional[str] = None,
) -> dict:
    """Create a sub-issue or child task underneath an existing Linear issue.

    Args:
        parent_id: Identifier of the parent Linear issue, e.g. ENG-404.
        title: Title for the sub-issue.
        description: Details and checklist items for the child issue.
    """
    return {"status": "stub", "tool": "linear_create_sub_issue", "args": locals()}
