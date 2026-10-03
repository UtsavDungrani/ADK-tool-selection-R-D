"""gdrive tools.

Cloud file storage: file and folder search, listing, upload, move, copy,
export, deletion, and sharing permissions.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="gdrive", confusable_with=["gdrive_list_files", "github_search_code"])
def gdrive_search_files(
    query: str,
    mime_type: Optional[str] = None,
    limit: Optional[int] = None,
) -> dict:
    """Search Google Drive for files matching text in their name or contents.

    Args:
        query: Free-text search query.
        mime_type: Restrict to a MIME type.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "gdrive_search_files", "args": locals()}


@tool(domain="gdrive", confusable_with=["gdrive_search_files"])
def gdrive_list_files(folder_id: str, limit: Optional[int] = None) -> dict:
    """List the files inside a specific Google Drive folder.

    Args:
        folder_id: Identifier of the folder to list.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "gdrive_list_files", "args": locals()}


@tool(domain="gdrive", confusable_with=["github_add_collaborator", "slack_invite_to_channel"])
def gdrive_share_file(
    file_id: str,
    email: str,
    role: Optional[Literal['reader', 'commenter', 'writer']] = None,
) -> dict:
    """Share a Google Drive file with a person and set their permission level.

    Args:
        file_id: Identifier of the file to share.
        email: Email address of the recipient.
        role: Permission level to grant. One of: reader, commenter, writer.
    """
    return {"status": "stub", "tool": "gdrive_share_file", "args": locals()}


@tool(domain="gdrive")
def gdrive_create_folder(name: str, parent_id: Optional[str] = None) -> dict:
    """Create a new folder in Google Drive.

    Args:
        name: Folder name.
        parent_id: Identifier of the parent folder.
    """
    return {"status": "stub", "tool": "gdrive_create_folder", "args": locals()}


@tool(domain="gdrive", confusable_with=["gdrive_copy_file"])
def gdrive_move_file(file_id: str, target_folder_id: str) -> dict:
    """Move a Google Drive file into a different folder.

    Args:
        file_id: Identifier of the file to move.
        target_folder_id: Destination folder identifier.
    """
    return {"status": "stub", "tool": "gdrive_move_file", "args": locals()}


@tool(domain="gdrive", confusable_with=["gdrive_move_file"])
def gdrive_copy_file(file_id: str, new_name: Optional[str] = None) -> dict:
    """Create a duplicate copy of a Google Drive file.

    Args:
        file_id: Identifier of the file to copy.
        new_name: Name for the copy.
    """
    return {"status": "stub", "tool": "gdrive_copy_file", "args": locals()}


@tool(domain="gdrive")
def gdrive_delete_file(file_id: str) -> dict:
    """Move a Google Drive file to the trash.

    Args:
        file_id: Identifier of the file to delete.
    """
    return {"status": "stub", "tool": "gdrive_delete_file", "args": locals()}


@tool(domain="gdrive")
def gdrive_export_file(
    file_id: str,
    format: Literal['pdf', 'docx', 'xlsx', 'csv'],
) -> dict:
    """Export a Google Doc or Sheet to another format such as PDF or XLSX.

    Args:
        file_id: Identifier of the file to export.
        format: Target export format. One of: pdf, docx, xlsx, csv.
    """
    return {"status": "stub", "tool": "gdrive_export_file", "args": locals()}


@tool(domain="gdrive")
def gdrive_get_file_permissions(file_id: str) -> dict:
    """List who currently has access to a Google Drive file and at what level.

    Args:
        file_id: Identifier of the file.
    """
    return {"status": "stub", "tool": "gdrive_get_file_permissions", "args": locals()}


@tool(domain="gdrive", confusable_with=["slack_upload_file"])
def gdrive_upload_file(file_path: str, folder_id: Optional[str] = None) -> dict:
    """Upload a local file into a Google Drive folder.

    Args:
        file_path: Local path of the file to upload.
        folder_id: Destination folder identifier.
    """
    return {"status": "stub", "tool": "gdrive_upload_file", "args": locals()}
