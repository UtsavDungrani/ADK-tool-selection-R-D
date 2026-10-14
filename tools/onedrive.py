"""onedrive tools.

OneDrive file storage: uploads, search, folders, moves and copies, deletion,
sharing links, permissions, and version history.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="onedrive", confusable_with=["gdrive_upload_file", "dropbox_upload_file", "box_upload_file"])
def onedrive_upload_file(local_path: str, folder_path: str, conflict: Optional[Literal['rename', 'replace', 'fail']] = None) -> dict:
    """Upload a file from disk into a OneDrive folder.

    Args:
        local_path: Path of the file to upload.
        folder_path: Destination folder path inside OneDrive.
        conflict: What to do if the name is taken. One of: rename, replace, fail.
    """
    return {"status": "stub", "tool": "onedrive_upload_file", "args": locals()}


@tool(domain="onedrive", confusable_with=["gdrive_search_files", "sharepoint_search_documents"])
def onedrive_search_files(query: str, folder_path: Optional[str] = None, limit: Optional[int] = None) -> dict:
    """Search OneDrive for files matching a query.

    Args:
        query: Free-text search query.
        folder_path: Restrict the search to this folder.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "onedrive_search_files", "args": locals()}


@tool(domain="onedrive", confusable_with=["gdrive_list_files", "box_list_folder_items"])
def onedrive_list_items(folder_path: str, limit: Optional[int] = None) -> dict:
    """List the files and folders inside a OneDrive folder.

    Args:
        folder_path: Folder path inside OneDrive.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "onedrive_list_items", "args": locals()}


@tool(domain="onedrive", confusable_with=["gdrive_share_file", "dropbox_create_shared_link"])
def onedrive_create_sharing_link(
    item_path: str,
    link_type: Optional[Literal['view', 'edit', 'embed']] = None,
    scope: Optional[Literal['anonymous', 'organization']] = None,
    expires_at: Optional[str] = None,
) -> dict:
    """Generate a OneDrive sharing link for a file or folder.

    Args:
        item_path: Path of the item to share.
        link_type: What the link permits. One of: view, edit, embed.
        scope: Who may use the link. One of: anonymous, organization.
        expires_at: ISO 8601 time when the link should stop working.
    """
    return {"status": "stub", "tool": "onedrive_create_sharing_link", "args": locals()}


@tool(domain="onedrive", confusable_with=["gdrive_create_folder", "box_create_folder"])
def onedrive_create_folder(name: str, parent_path: Optional[str] = None) -> dict:
    """Create a new folder in OneDrive.

    Args:
        name: Name of the folder to create.
        parent_path: Folder to create it inside; the root when omitted.
    """
    return {"status": "stub", "tool": "onedrive_create_folder", "args": locals()}


@tool(domain="onedrive", confusable_with=["gdrive_move_file", "dropbox_move_file"])
def onedrive_move_item(item_path: str, target_folder_path: str, new_name: Optional[str] = None) -> dict:
    """Move a OneDrive file or folder somewhere else in the drive.

    Args:
        item_path: Current path of the item.
        target_folder_path: Destination folder path.
        new_name: New name for the item.
    """
    return {"status": "stub", "tool": "onedrive_move_item", "args": locals()}


@tool(domain="onedrive", confusable_with=["gdrive_copy_file"])
def onedrive_copy_item(item_path: str, target_folder_path: str, new_name: Optional[str] = None) -> dict:
    """Duplicate a OneDrive file or folder into another location.

    Args:
        item_path: Path of the item to copy.
        target_folder_path: Folder the copy should land in.
        new_name: Name for the copy.
    """
    return {"status": "stub", "tool": "onedrive_copy_item", "args": locals()}


@tool(domain="onedrive", confusable_with=["gdrive_delete_file", "box_delete_file"])
def onedrive_delete_item(item_path: str) -> dict:
    """Delete a file or folder from OneDrive.

    Args:
        item_path: Path of the item to delete.
    """
    return {"status": "stub", "tool": "onedrive_delete_item", "args": locals()}


@tool(domain="onedrive", confusable_with=["dropbox_restore_file", "confluence_export_page"])
def onedrive_restore_version(item_path: str, version_id: Optional[str] = None) -> dict:
    """Roll a OneDrive file back to an earlier version from its history.

    Args:
        item_path: Path of the file to restore.
        version_id: Version to restore; the previous one when omitted.
    """
    return {"status": "stub", "tool": "onedrive_restore_version", "args": locals()}


@tool(domain="onedrive", confusable_with=["gdrive_get_file_permissions"])
def onedrive_get_item_permissions(item_path: str) -> dict:
    """List who currently has access to a OneDrive file or folder and at what level.

    Args:
        item_path: Path of the item to inspect.
    """
    return {"status": "stub", "tool": "onedrive_get_item_permissions", "args": locals()}
