"""github tools.

Source code hosting: repositories, branches, issues, pull requests, code
search, CI workflow runs, and collaborator access.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="github", confusable_with=["jira_create_issue"])
def github_create_issue(
    repo: str,
    title: str,
    body: Optional[str] = None,
    labels: Optional[list[str]] = None,
) -> dict:
    """Open a new issue on a GitHub repository to report a bug or request a feature.

    Args:
        repo: Repository in owner/name form, e.g. acme/web-app.
        title: Short issue title.
        body: Markdown description of the issue.
        labels: Labels to apply to the new issue.
    """
    return {"status": "stub", "tool": "github_create_issue", "args": locals()}


@tool(domain="github", confusable_with=["jira_search_issues", "github_search_pull_requests"])
def github_search_issues(
    repo: str,
    query: str,
    state: Optional[Literal['open', 'closed', 'all']] = None,
    limit: Optional[int] = None,
) -> dict:
    """Search issues in a GitHub repository by text, label, state, or author.

    Args:
        repo: Repository in owner/name form, e.g. acme/web-app.
        query: Free-text search query.
        state: Filter by issue state. One of: open, closed, all.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "github_search_issues", "args": locals()}


@tool(domain="github", confusable_with=["github_search_pull_requests"])
def github_list_pull_requests(
    repo: str,
    state: Optional[Literal['open', 'closed', 'merged', 'all']] = None,
    limit: Optional[int] = None,
) -> dict:
    """List pull requests on a GitHub repository, optionally filtered by state.

    Args:
        repo: Repository in owner/name form, e.g. acme/web-app.
        state: Filter by PR state. One of: open, closed, merged, all.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "github_list_pull_requests", "args": locals()}


@tool(domain="github", confusable_with=["github_list_pull_requests", "github_search_issues"])
def github_search_pull_requests(
    repo: str,
    query: str,
    author: Optional[str] = None,
    limit: Optional[int] = None,
) -> dict:
    """Search pull requests in a GitHub repository by title text, author, or review status.

    Args:
        repo: Repository in owner/name form, e.g. acme/web-app.
        query: Free-text search query.
        author: Filter to PRs opened by this user.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "github_search_pull_requests", "args": locals()}


@tool(domain="github")
def github_merge_pull_request(
    repo: str,
    pr_number: int,
    method: Optional[Literal['merge', 'squash', 'rebase']] = None,
) -> dict:
    """Merge an open pull request into its base branch on GitHub.

    Args:
        repo: Repository in owner/name form, e.g. acme/web-app.
        pr_number: Pull request number to merge.
        method: Merge strategy. One of: merge, squash, rebase.
    """
    return {"status": "stub", "tool": "github_merge_pull_request", "args": locals()}


@tool(domain="github", confusable_with=["jira_add_comment", "slack_post_message"])
def github_add_comment(repo: str, number: int, body: str) -> dict:
    """Post a comment on an existing GitHub issue or pull request.

    Args:
        repo: Repository in owner/name form, e.g. acme/web-app.
        number: Issue or pull request number.
        body: Markdown comment text.
    """
    return {"status": "stub", "tool": "github_add_comment", "args": locals()}


@tool(domain="github", confusable_with=["gdrive_search_files"])
def github_search_code(repo: str, query: str, language: Optional[str] = None) -> dict:
    """Search source code contents across a GitHub repository for a string or pattern.

    Args:
        repo: Repository in owner/name form, e.g. acme/web-app.
        query: Free-text search query.
        language: Restrict results to this language.
    """
    return {"status": "stub", "tool": "github_search_code", "args": locals()}


@tool(domain="github", confusable_with=["gdrive_share_file"])
def github_add_collaborator(
    repo: str,
    username: str,
    permission: Optional[Literal['read', 'write', 'admin']] = None,
) -> dict:
    """Grant a GitHub user push or admin access to a repository.

    Args:
        repo: Repository in owner/name form, e.g. acme/web-app.
        username: GitHub username to add.
        permission: Access level to grant. One of: read, write, admin.
    """
    return {"status": "stub", "tool": "github_add_collaborator", "args": locals()}


@tool(domain="github")
def github_create_branch(
    repo: str,
    branch: str,
    from_ref: Optional[str] = None,
) -> dict:
    """Create a new git branch in a GitHub repository from an existing ref.

    Args:
        repo: Repository in owner/name form, e.g. acme/web-app.
        branch: Name of the branch to create.
        from_ref: Base branch or commit SHA.
    """
    return {"status": "stub", "tool": "github_create_branch", "args": locals()}


@tool(domain="github")
def github_get_workflow_runs(
    repo: str,
    workflow: Optional[str] = None,
    status: Optional[Literal['success', 'failure', 'in_progress']] = None,
    limit: Optional[int] = None,
) -> dict:
    """Retrieve recent GitHub Actions CI workflow runs and their pass or fail status.

    Args:
        repo: Repository in owner/name form, e.g. acme/web-app.
        workflow: Workflow file name to filter by.
        status: Filter by run status. One of: success, failure, in_progress.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "github_get_workflow_runs", "args": locals()}
