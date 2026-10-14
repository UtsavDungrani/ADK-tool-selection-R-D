"""bitbucket tools.

Repository hosting on Atlassian: repositories, branches, commits, pull
requests, inline review comments, pipelines, and repository access.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(
    domain="bitbucket",
    confusable_with=["github_create_pull_request", "gitlab_create_merge_request"],
)
def bitbucket_create_pull_request(
    repo: str,
    title: str,
    source_branch: str,
    destination_branch: Optional[str] = None,
    description: Optional[str] = None,
    reviewers: Optional[list[str]] = None,
) -> dict:
    """Open a pull request in a Bitbucket repository for review before merge.

    Args:
        repo: Repository in workspace/slug form, e.g. acme/web-app.
        title: Short pull request title.
        source_branch: Branch holding the changes.
        destination_branch: Branch the changes should land on.
        description: Markdown summary of the change.
        reviewers: Bitbucket usernames to request review from.
    """
    return {"status": "stub", "tool": "bitbucket_create_pull_request", "args": locals()}


@tool(domain="bitbucket", confusable_with=["github_list_pull_requests"])
def bitbucket_list_pull_requests(
    repo: str,
    state: Optional[Literal['open', 'merged', 'declined', 'all']] = None,
    author: Optional[str] = None,
    limit: Optional[int] = None,
) -> dict:
    """List pull requests open against a Bitbucket repository, newest first.

    Args:
        repo: Repository in workspace/slug form, e.g. acme/web-app.
        state: Filter by pull request state. One of: open, merged, declined, all.
        author: Restrict to pull requests opened by this username.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "bitbucket_list_pull_requests", "args": locals()}


@tool(domain="bitbucket", confusable_with=["github_merge_pull_request", "gitlab_merge_merge_request"])
def bitbucket_merge_pull_request(
    repo: str,
    pr_id: int,
    strategy: Optional[Literal['merge_commit', 'squash', 'fast_forward']] = None,
    close_source_branch: Optional[bool] = None,
) -> dict:
    """Merge an approved Bitbucket pull request into its destination branch.

    Args:
        repo: Repository in workspace/slug form, e.g. acme/web-app.
        pr_id: Pull request identifier to merge.
        strategy: Merge strategy. One of: merge_commit, squash, fast_forward.
        close_source_branch: Delete the source branch once merged.
    """
    return {"status": "stub", "tool": "bitbucket_merge_pull_request", "args": locals()}


@tool(domain="bitbucket", confusable_with=["github_create_branch", "gitlab_create_branch"])
def bitbucket_create_branch(repo: str, branch: str, from_ref: Optional[str] = None) -> dict:
    """Create a git branch in a Bitbucket repository from an existing ref.

    Args:
        repo: Repository in workspace/slug form, e.g. acme/web-app.
        branch: Name of the branch to create.
        from_ref: Base branch name or commit hash.
    """
    return {"status": "stub", "tool": "bitbucket_create_branch", "args": locals()}


@tool(domain="bitbucket", confusable_with=["github_create_commit"])
def bitbucket_create_commit(
    repo: str,
    branch: str,
    message: str,
    paths: Optional[list[str]] = None,
) -> dict:
    """Commit file changes onto a branch in a Bitbucket repository.

    Args:
        repo: Repository in workspace/slug form, e.g. acme/web-app.
        branch: Branch to commit onto.
        message: Commit message.
        paths: Files to include; all changed files when omitted.
    """
    return {"status": "stub", "tool": "bitbucket_create_commit", "args": locals()}


@tool(domain="bitbucket", confusable_with=["github_create_issue", "jira_create_issue"])
def bitbucket_create_issue(
    repo: str,
    title: str,
    content: Optional[str] = None,
    kind: Optional[Literal['bug', 'enhancement', 'proposal', 'task']] = None,
) -> dict:
    """Raise an issue on a Bitbucket repository's built-in issue tracker.

    Args:
        repo: Repository in workspace/slug form, e.g. acme/web-app.
        title: Short issue title.
        content: Markdown description of the issue.
        kind: Issue kind. One of: bug, enhancement, proposal, task.
    """
    return {"status": "stub", "tool": "bitbucket_create_issue", "args": locals()}


@tool(domain="bitbucket", confusable_with=["github_search_code", "gitlab_search_code"])
def bitbucket_search_code(repo: str, query: str, extension: Optional[str] = None) -> dict:
    """Search source file contents across a Bitbucket repository.

    Args:
        repo: Repository in workspace/slug form, e.g. acme/web-app.
        query: Free-text search query.
        extension: Restrict results to files with this extension.
    """
    return {"status": "stub", "tool": "bitbucket_search_code", "args": locals()}


@tool(domain="bitbucket", confusable_with=["github_add_comment", "gitlab_add_note"])
def bitbucket_add_comment(
    repo: str,
    pr_id: int,
    body: str,
    file_path: Optional[str] = None,
    line: Optional[int] = None,
) -> dict:
    """Leave a review comment on a Bitbucket pull request, optionally on a specific line.

    Args:
        repo: Repository in workspace/slug form, e.g. acme/web-app.
        pr_id: Pull request identifier.
        body: Markdown comment text.
        file_path: File to anchor an inline comment to.
        line: Line number within that file.
    """
    return {"status": "stub", "tool": "bitbucket_add_comment", "args": locals()}


@tool(domain="bitbucket", confusable_with=["github_get_workflow_runs", "gitlab_get_pipeline_status"])
def bitbucket_get_pipeline_status(
    repo: str,
    branch: Optional[str] = None,
    status: Optional[Literal['successful', 'failed', 'in_progress']] = None,
    limit: Optional[int] = None,
) -> dict:
    """Check the pass or fail status of recent Bitbucket Pipelines CI builds.

    Args:
        repo: Repository in workspace/slug form, e.g. acme/web-app.
        branch: Restrict to pipelines run on this branch.
        status: Filter by result. One of: successful, failed, in_progress.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "bitbucket_get_pipeline_status", "args": locals()}


@tool(domain="bitbucket", confusable_with=["github_add_collaborator", "gitlab_add_project_member"])
def bitbucket_add_repository_member(
    repo: str,
    username: str,
    permission: Optional[Literal['read', 'write', 'admin']] = None,
) -> dict:
    """Grant a Bitbucket user access to a repository at a given permission level.

    Args:
        repo: Repository in workspace/slug form, e.g. acme/web-app.
        username: Bitbucket username to grant access to.
        permission: Access level. One of: read, write, admin.
    """
    return {"status": "stub", "tool": "bitbucket_add_repository_member", "args": locals()}
