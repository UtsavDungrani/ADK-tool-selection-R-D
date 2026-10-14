"""gitlab tools.

DevOps and source code hosting: repositories, merge requests, issues,
branches, CI/CD pipelines, code search, and project members.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="gitlab", confusable_with=["github_create_issue", "jira_create_issue"])
def gitlab_create_issue(
    project: str,
    title: str,
    description: Optional[str] = None,
    labels: Optional[list[str]] = None,
) -> dict:
    """Create a new issue in a GitLab project to track bugs or feature tasks.

    Args:
        project: Project path with namespace, e.g. acme-org/backend-service.
        title: Title of the issue.
        description: Markdown description and context for the issue.
        labels: Optional labels or tags to assign to the issue.
    """
    return {"status": "stub", "tool": "gitlab_create_issue", "args": locals()}


@tool(domain="gitlab", confusable_with=["github_search_issues"])
def gitlab_search_issues(
    project: str,
    query: str,
    state: Optional[Literal["opened", "closed", "all"]] = None,
    limit: Optional[int] = None,
) -> dict:
    """Search issues within a GitLab project by keyword text, state, or author.

    Args:
        project: Project path with namespace, e.g. acme-org/backend-service.
        query: Free-text search query across titles and descriptions.
        state: Issue state filter. One of: opened, closed, all.
        limit: Maximum number of issues to return.
    """
    return {"status": "stub", "tool": "gitlab_search_issues", "args": locals()}


@tool(domain="gitlab", confusable_with=["github_list_pull_requests"])
def gitlab_create_merge_request(
    project: str,
    source_branch: str,
    target_branch: str,
    title: str,
    description: Optional[str] = None,
) -> dict:
    """Create a new merge request in a GitLab project proposing changes from a source branch.

    Args:
        project: Project path with namespace, e.g. acme-org/backend-service.
        source_branch: Name of the feature or bugfix branch containing new commits.
        target_branch: Name of the branch to merge into, such as main or master.
        title: Title summarizing the proposed changes.
        description: Markdown description with details and review instructions.
    """
    return {"status": "stub", "tool": "gitlab_create_merge_request", "args": locals()}


@tool(domain="gitlab", confusable_with=["github_search_pull_requests"])
def gitlab_search_merge_requests(
    project: str,
    query: Optional[str] = None,
    state: Optional[Literal["opened", "closed", "merged", "all"]] = None,
    limit: Optional[int] = None,
) -> dict:
    """Search or list merge requests in a GitLab project matching query and status filters.

    Args:
        project: Project path with namespace, e.g. acme-org/backend-service.
        query: Free-text query matching merge request titles or descriptions.
        state: Merge request state. One of: opened, closed, merged, all.
        limit: Maximum number of merge requests to return.
    """
    return {"status": "stub", "tool": "gitlab_search_merge_requests", "args": locals()}


@tool(domain="gitlab", confusable_with=["github_merge_pull_request"])
def gitlab_merge_merge_request(
    project: str,
    mr_iid: int,
    squash: bool = False,
    should_remove_source_branch: bool = False,
) -> dict:
    """Accept and merge an open merge request into its target branch in GitLab.

    Args:
        project: Project path with namespace, e.g. acme-org/backend-service.
        mr_iid: Internal project-scoped identifier of the merge request.
        squash: Whether to squash commits into a single commit upon merge.
        should_remove_source_branch: Whether to delete the source branch after merging.
    """
    return {"status": "stub", "tool": "gitlab_merge_merge_request", "args": locals()}


@tool(domain="gitlab", confusable_with=["github_add_comment", "jira_add_comment"])
def gitlab_add_note(
    project: str,
    target_type: Literal["issue", "merge_request"],
    target_iid: int,
    body: str,
) -> dict:
    """Post a comment or discussion note on a GitLab issue or merge request.

    Args:
        project: Project path with namespace, e.g. acme-org/backend-service.
        target_type: Target object type. One of: issue, merge_request.
        target_iid: Internal identifier (IID) of the issue or merge request.
        body: Comment body text in Markdown format.
    """
    return {"status": "stub", "tool": "gitlab_add_note", "args": locals()}


@tool(domain="gitlab", confusable_with=["github_search_code"])
def gitlab_search_code(
    project: str,
    query: str,
    ref: Optional[str] = None,
) -> dict:
    """Search repository source code files in a GitLab project for matching text.

    Args:
        project: Project path with namespace, e.g. acme-org/backend-service.
        query: Search term or code snippet.
        ref: Optional branch or tag name to search within.
    """
    return {"status": "stub", "tool": "gitlab_search_code", "args": locals()}


@tool(domain="gitlab", confusable_with=["github_create_branch"])
def gitlab_create_branch(
    project: str,
    branch: str,
    ref: str = "main",
) -> dict:
    """Create a new git branch in a GitLab repository off an existing branch or commit ref.

    Args:
        project: Project path with namespace, e.g. acme-org/backend-service.
        branch: Name of the new branch to create.
        ref: Existing commit hash, branch name, or tag to branch from.
    """
    return {"status": "stub", "tool": "gitlab_create_branch", "args": locals()}


@tool(domain="gitlab", confusable_with=["github_get_workflow_runs"])
def gitlab_get_pipeline_status(
    project: str,
    ref: Optional[str] = None,
    limit: Optional[int] = None,
) -> dict:
    """Retrieve recent CI/CD pipeline execution status and stages for a GitLab project.

    Args:
        project: Project path with namespace, e.g. acme-org/backend-service.
        ref: Optional branch or tag to filter pipeline runs.
        limit: Maximum number of recent pipeline runs to return.
    """
    return {"status": "stub", "tool": "gitlab_get_pipeline_status", "args": locals()}


@tool(domain="gitlab", confusable_with=["github_add_collaborator"])
def gitlab_add_project_member(
    project: str,
    username: str,
    access_level: Literal["guest", "reporter", "developer", "maintainer"] = "developer",
) -> dict:
    """Add a user and assign role permissions to a GitLab project.

    Args:
        project: Project path with namespace, e.g. acme-org/backend-service.
        username: GitLab username of the person to add.
        access_level: Permission tier to assign. One of: guest, reporter, developer, maintainer.
    """
    return {"status": "stub", "tool": "gitlab_add_project_member", "args": locals()}
