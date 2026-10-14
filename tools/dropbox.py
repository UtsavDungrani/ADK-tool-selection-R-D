"""dropbox tools.

Dropbox file storage: uploads, search, folders, moves, deletion, shared
links, shared-folder membership, and version restore.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="dropbox", confusable_with=["gdrive_upload_file", "box_upload_file", "onedrive_upload_file"])
def dropbox_upload_file(
    local_path: str,
    dropbox_path: str,
    overwrite: Optional[bool] = None,
) -> dict:
    """Upload a file from disk into a Dropbox folder.

    Args:
        local_path: Path of the file to upload.
        dropbox_path: Destination path inside Dropbox.
        overwrite: Replace any existing file at that path.
    """
    return {"status": "stub", "tool": "dropbox_upload_file", "args": locals()}


@tool(domain="dropbox", confusable_with=["gdrive_search_files", "box_search_files"])
def dropbox_search_files(
    query: str,
    path: Optional[str] = None,
    file_extension: Optional[str] = None,
    limit: Optional[int] = None,
) -> dict:
    """Search Dropbox for files whose name or contents match a query.

    Args:
        query: Free-text search query.
        path: Restrict the search to this folder path.
        file_extension: Restrict results to this file extension.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "dropbox_search_files", "args": locals()}


@tool(domain="dropbox", confusable_with=["gdrive_list_files", "box_list_folder_items"])
def dropbox_list_folder(path: str, recursive: Optional[bool] = None, limit: Optional[int] = None) -> dict:
    """List the files and folders inside a Dropbox folder.

    Args:
        path: Folder path inside Dropbox.
        recursive: Descend into subfolders as well.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "dropbox_list_folder", "args": locals()}


@tool(domain="dropbox", confusable_with=["gdrive_share_file", "box_share_file"])
def dropbox_create_shared_link(
    path: str,
    access: Optional[Literal['viewer', 'editor']] = None,
    expires_at: Optional[str] = None,
    password: Optional[str] = None,
) -> dict:
    """Generate a shareable Dropbox link to a file or folder.

    Args:
        path: Path of the file or folder to share.
        access: Permission the link grants. One of: viewer, editor.
        expires_at: ISO 8601 time when the link should stop working.
        password: Require this password before the link opens.
    """
    return {"status": "stub", "tool": "dropbox_create_shared_link", "args": locals()}


@tool(domain="dropbox", confusable_with=["gdrive_create_folder"])
def dropbox_create_folder(path: str) -> dict:
    """Create a new folder in Dropbox.

    Args:
        path: Full path of the folder to create.
    """
    return {"status": "stub", "tool": "dropbox_create_folder", "args": locals()}


@tool(domain="dropbox", confusable_with=["gdrive_move_file", "onedrive_move_item"])
def dropbox_move_file(from_path: str, to_path: str) -> dict:
    """Move or rename a file within Dropbox.

    Args:
        from_path: Current path of the file.
        to_path: New path for the file.
    """
    return {"status": "stub", "tool": "dropbox_move_file", "args": locals()}


@tool(domain="dropbox", confusable_with=["gdrive_delete_file"])
def dropbox_delete_file(path: str) -> dict:
    """Delete a file or folder from Dropbox.

    Args:
        path: Path of the file or folder to delete.
    """
    return {"status": "stub", "tool": "dropbox_delete_file", "args": locals()}


@tool(domain="dropbox", confusable_with=["onedrive_restore_version", "confluence_export_page"])
def dropbox_restore_file(path: str, revision: Optional[str] = None) -> dict:
    """Roll a Dropbox file back to an earlier saved revision.

    Args:
        path: Path of the file to restore.
        revision: Revision identifier to restore; the previous one when omitted.
    """
    return {"status": "stub", "tool": "dropbox_restore_file", "args": locals()}


@tool(domain="dropbox", confusable_with=["gdrive_get_file_permissions"])
def dropbox_get_file_metadata(path: str, include_deleted: Optional[bool] = None) -> dict:
    """Fetch size, modification time and revision details for a Dropbox file.

    Args:
        path: Path of the file to inspect.
        include_deleted: Return metadata even if the file was deleted.
    """
    return {"status": "stub", "tool": "dropbox_get_file_metadata", "args": locals()}


@tool(domain="dropbox", confusable_with=["box_add_collaborator", "gdrive_share_file"])
def dropbox_invite_to_shared_folder(
    path: str,
    email: str,
    access: Optional[Literal['viewer', 'editor', 'owner']] = None,
) -> dict:
    """Invite someone to collaborate on a Dropbox shared folder.

    Args:
        path: Path of the shared folder.
        email: Email address of the person to invite.
        access: Permission to grant. One of: viewer, editor, owner.
    """
    return {"status": "stub", "tool": "dropbox_invite_to_shared_folder", "args": locals()}
