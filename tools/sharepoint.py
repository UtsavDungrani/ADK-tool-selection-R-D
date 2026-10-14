"""sharepoint tools.

SharePoint intranet: team sites, pages and news posts, document libraries,
custom lists, check-out, permissions, and version restore.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="sharepoint", confusable_with=["confluence_create_page", "notion_create_page"])
def sharepoint_create_page(site: str, title: str, content: Optional[str] = None) -> dict:
    """Create a content page on a SharePoint team site.

    Args:
        site: Name or URL of the SharePoint site.
        title: Title of the new page.
        content: HTML or Markdown body of the page.
    """
    return {"status": "stub", "tool": "sharepoint_create_page", "args": locals()}


@tool(domain="sharepoint", confusable_with=["confluence_search_pages", "onedrive_search_files"])
def sharepoint_search_documents(
    query: str,
    site: Optional[str] = None,
    file_type: Optional[str] = None,
    limit: Optional[int] = None,
) -> dict:
    """Search documents and pages stored across SharePoint sites.

    Args:
        query: Free-text search query.
        site: Restrict the search to this site.
        file_type: Restrict results to this file type.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "sharepoint_search_documents", "args": locals()}


@tool(domain="sharepoint", confusable_with=["onedrive_upload_file", "confluence_attach_file"])
def sharepoint_upload_document(site: str, library: str, local_path: str, overwrite: Optional[bool] = None) -> dict:
    """Upload a document into a SharePoint document library.

    Args:
        site: Name or URL of the SharePoint site.
        library: Document library to upload into, e.g. Shared Documents.
        local_path: Path of the file to upload.
        overwrite: Replace an existing document with the same name.
    """
    return {"status": "stub", "tool": "sharepoint_upload_document", "args": locals()}


@tool(domain="sharepoint", confusable_with=["confluence_create_space"])
def sharepoint_create_site(
    name: str,
    template: Optional[Literal['team', 'communication']] = None,
    owner: Optional[str] = None,
) -> dict:
    """Provision a new SharePoint site for a team or department.

    Args:
        name: Name of the new site.
        template: Site template. One of: team, communication.
        owner: Email of the person who should own the site.
    """
    return {"status": "stub", "tool": "sharepoint_create_site", "args": locals()}


@tool(domain="sharepoint", confusable_with=["notion_create_database", "airtable_create_table"])
def sharepoint_create_list(site: str, name: str, columns: Optional[list[str]] = None) -> dict:
    """Create a structured SharePoint list to hold tabular records on a site.

    Args:
        site: Name or URL of the SharePoint site.
        name: Name of the new list.
        columns: Column names to define on the list.
    """
    return {"status": "stub", "tool": "sharepoint_create_list", "args": locals()}


@tool(domain="sharepoint", confusable_with=["airtable_create_record", "notion_append_block"])
def sharepoint_add_list_item(site: str, list_name: str, title: str, fields: Optional[list[str]] = None) -> dict:
    """Add a row to an existing SharePoint list.

    Args:
        site: Name or URL of the SharePoint site.
        list_name: List to add the item to.
        title: Title of the new item.
        fields: Additional field values as name=value strings.
    """
    return {"status": "stub", "tool": "sharepoint_add_list_item", "args": locals()}


@tool(domain="sharepoint", confusable_with=["notion_share_page", "onedrive_get_item_permissions"])
def sharepoint_set_page_permissions(
    site: str,
    page: str,
    group: str,
    permission: Optional[Literal['read', 'contribute', 'full_control']] = None,
) -> dict:
    """Change who can read or edit a SharePoint page.

    Args:
        site: Name or URL of the SharePoint site.
        page: Title or path of the page.
        group: Security group or user to grant the permission to.
        permission: Access level. One of: read, contribute, full_control.
    """
    return {"status": "stub", "tool": "sharepoint_set_page_permissions", "args": locals()}


@tool(domain="sharepoint", confusable_with=["box_lock_file"])
def sharepoint_check_out_document(site: str, library: str, filename: str) -> dict:
    """Check out a SharePoint document so nobody else can edit it until you check it back in.

    Args:
        site: Name or URL of the SharePoint site.
        library: Document library holding the file.
        filename: Name of the document to check out.
    """
    return {"status": "stub", "tool": "sharepoint_check_out_document", "args": locals()}


@tool(domain="sharepoint", confusable_with=["confluence_create_page", "slack_post_message"])
def sharepoint_publish_news_post(site: str, title: str, body: str, audience: Optional[str] = None) -> dict:
    """Publish a news announcement on a SharePoint site for staff to read.

    Args:
        site: Name or URL of the SharePoint site.
        title: Headline of the news post.
        body: Body of the announcement.
        audience: Group the post should be targeted at.
    """
    return {"status": "stub", "tool": "sharepoint_publish_news_post", "args": locals()}


@tool(domain="sharepoint", confusable_with=["onedrive_restore_version", "dropbox_restore_file"])
def sharepoint_restore_document_version(
    site: str,
    library: str,
    filename: str,
    version: Optional[str] = None,
) -> dict:
    """Roll a SharePoint document back to an earlier version.

    Args:
        site: Name or URL of the SharePoint site.
        library: Document library holding the file.
        filename: Name of the document to restore.
        version: Version label to restore; the previous one when omitted.
    """
    return {"status": "stub", "tool": "sharepoint_restore_document_version", "args": locals()}
