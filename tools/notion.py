"""notion tools.

Workspace docs and wikis: pages, databases, blocks, comments, duplication,
archiving, and sharing permissions.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="notion", confusable_with=["gdrive_create_folder"])
def notion_create_page(
    title: str,
    parent_id: Optional[str] = None,
    content: Optional[str] = None,
) -> dict:
    """Create a new page in a Notion workspace, optionally inside a parent page.

    Args:
        title: Page title.
        parent_id: Identifier of the parent page or database.
        content: Initial page body in Markdown.
    """
    return {"status": "stub", "tool": "notion_create_page", "args": locals()}


@tool(domain="notion", confusable_with=["gdrive_search_files"])
def notion_search_pages(query: str, limit: Optional[int] = None) -> dict:
    """Search Notion pages and databases by text in their title or content.

    Args:
        query: Free-text search query.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "notion_search_pages", "args": locals()}


@tool(domain="notion")
def notion_update_page(page_id: str, title: Optional[str] = None) -> dict:
    """Update the title or properties of an existing Notion page.

    Args:
        page_id: Identifier of the page.
        title: New page title.
    """
    return {"status": "stub", "tool": "notion_update_page", "args": locals()}


@tool(domain="notion", confusable_with=["notion_add_comment"])
def notion_append_block(page_id: str, content: str) -> dict:
    """Append a block of content to the end of an existing Notion page.

    Args:
        page_id: Identifier of the page.
        content: Markdown content to append.
    """
    return {"status": "stub", "tool": "notion_append_block", "args": locals()}


@tool(domain="notion")
def notion_create_database(
    title: str,
    parent_id: str,
    properties: Optional[list[str]] = None,
) -> dict:
    """Create a new Notion database with typed properties for structured records.

    Args:
        title: Database title.
        parent_id: Identifier of the parent page.
        properties: Property names to define on the database.
    """
    return {"status": "stub", "tool": "notion_create_database", "args": locals()}


@tool(domain="notion", confusable_with=["notion_search_pages"])
def notion_query_database(
    database_id: str,
    filter: Optional[str] = None,
    limit: Optional[int] = None,
) -> dict:
    """Query rows in a Notion database with filters and sorting.

    Args:
        database_id: Identifier of the database.
        filter: Filter expression.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "notion_query_database", "args": locals()}


@tool(domain="notion", confusable_with=["gdrive_share_file"])
def notion_share_page(
    page_id: str,
    email: str,
    role: Optional[Literal['reader', 'commenter', 'editor']] = None,
) -> dict:
    """Share a Notion page with a person and set their permission level.

    Args:
        page_id: Identifier of the page.
        email: Email address of the recipient.
        role: Permission level. One of: reader, commenter, editor.
    """
    return {"status": "stub", "tool": "notion_share_page", "args": locals()}


@tool(domain="notion", confusable_with=["gdrive_copy_file"])
def notion_duplicate_page(page_id: str, new_title: Optional[str] = None) -> dict:
    """Create a duplicate copy of an existing Notion page.

    Args:
        page_id: Identifier of the page to duplicate.
        new_title: Title for the copy.
    """
    return {"status": "stub", "tool": "notion_duplicate_page", "args": locals()}


@tool(domain="notion", confusable_with=["gdrive_delete_file"])
def notion_archive_page(page_id: str) -> dict:
    """Archive a Notion page, removing it from navigation without deleting it.

    Args:
        page_id: Identifier of the page to archive.
    """
    return {"status": "stub", "tool": "notion_archive_page", "args": locals()}


@tool(domain="notion", confusable_with=["jira_add_comment", "github_add_comment"])
def notion_add_comment(page_id: str, body: str) -> dict:
    """Add a comment to a Notion page.

    Args:
        page_id: Identifier of the page.
        body: Comment text.
    """
    return {"status": "stub", "tool": "notion_add_comment", "args": locals()}
