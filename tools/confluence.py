"""confluence tools.

Team workspace and wiki: spaces, pages, blog posts, attachments,
page comments, exports, version history, and archiving.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="confluence", confusable_with=["notion_create_page", "jira_create_issue"])
def confluence_create_page(
    space_key: str,
    title: str,
    body: str,
    parent_id: Optional[str] = None,
) -> dict:
    """Create a new page in a Confluence space, optionally nested under a parent page.

    Args:
        space_key: Key of the Confluence space, e.g. ENG, HR, or PRODUCT.
        title: Title of the new page.
        body: Page content formatted in storage format or Markdown.
        parent_id: Optional identifier of the parent page to nest under.
    """
    return {"status": "stub", "tool": "confluence_create_page", "args": locals()}


@tool(domain="confluence", confusable_with=["notion_search_pages", "gdrive_search_files"])
def confluence_search_pages(
    query: str,
    space_key: Optional[str] = None,
    limit: Optional[int] = None,
) -> dict:
    """Search Confluence wiki pages and documentation by keyword or CQL query.

    Args:
        query: Search keywords or Confluence Query Language (CQL) expression.
        space_key: Optional space key to constrain the search.
        limit: Maximum number of pages to return.
    """
    return {"status": "stub", "tool": "confluence_search_pages", "args": locals()}


@tool(domain="confluence", confusable_with=["notion_search_pages"])
def confluence_get_page(page_id: str) -> dict:
    """Retrieve the content, version metadata, and author of a Confluence page.

    Args:
        page_id: Unique identifier of the Confluence page.
    """
    return {"status": "stub", "tool": "confluence_get_page", "args": locals()}


@tool(domain="confluence", confusable_with=["notion_update_page"])
def confluence_update_page(
    page_id: str,
    title: Optional[str] = None,
    body: Optional[str] = None,
    version_comment: Optional[str] = None,
) -> dict:
    """Update the title or body content of an existing Confluence page.

    Args:
        page_id: Unique identifier of the Confluence page to update.
        title: Updated page title.
        body: Updated page body content.
        version_comment: Optional summary of edits for page history.
    """
    return {"status": "stub", "tool": "confluence_update_page", "args": locals()}


@tool(domain="confluence", confusable_with=["notion_add_comment", "jira_add_comment"])
def confluence_add_comment(page_id: str, body: str) -> dict:
    """Post a discussion comment on an existing Confluence page.

    Args:
        page_id: Unique identifier of the Confluence page.
        body: Comment text formatted in Markdown or rich text.
    """
    return {"status": "stub", "tool": "confluence_add_comment", "args": locals()}


@tool(domain="confluence", confusable_with=["notion_archive_page"])
def confluence_archive_page(page_id: str) -> dict:
    """Archive an outdated Confluence page to hide it from standard space navigation.

    Args:
        page_id: Unique identifier of the Confluence page to archive.
    """
    return {"status": "stub", "tool": "confluence_archive_page", "args": locals()}


@tool(domain="confluence", confusable_with=["notion_create_database"])
def confluence_create_space(
    key: str,
    name: str,
    description: Optional[str] = None,
) -> dict:
    """Create a new team collaboration space in Confluence.

    Args:
        key: Short uppercase key identifying the space, e.g. DESIGN or INFRA.
        name: Human-readable display name for the space.
        description: Purpose and overview of the new space.
    """
    return {"status": "stub", "tool": "confluence_create_space", "args": locals()}


@tool(domain="confluence", confusable_with=["jira_list_users"])
def confluence_list_spaces(
    type: Optional[Literal["global", "personal"]] = None,
    limit: Optional[int] = None,
) -> dict:
    """List Confluence spaces available in the workspace.

    Args:
        type: Space category filter. One of: global, personal.
        limit: Maximum number of spaces to return.
    """
    return {"status": "stub", "tool": "confluence_list_spaces", "args": locals()}


@tool(domain="confluence", confusable_with=["gdrive_upload_file", "slack_upload_file"])
def confluence_attach_file(
    page_id: str,
    filename: str,
    comment: Optional[str] = None,
) -> dict:
    """Upload a file or document attachment to a Confluence page.

    Args:
        page_id: Unique identifier of the Confluence page.
        filename: Name of the file being attached, e.g. diagram.png or architecture.pdf.
        comment: Optional note describing the attached file.
    """
    return {"status": "stub", "tool": "confluence_attach_file", "args": locals()}


@tool(domain="confluence", confusable_with=["gdrive_search_files"])
def confluence_export_page(
    page_id: str,
    format: Literal["pdf", "word"] = "pdf",
) -> dict:
    """Export a Confluence page to a downloadable PDF or Word document.

    Args:
        page_id: Unique identifier of the Confluence page.
        format: Export file format. One of: pdf, word.
    """
    return {"status": "stub", "tool": "confluence_export_page", "args": locals()}
