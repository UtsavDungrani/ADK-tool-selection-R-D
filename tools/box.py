"""box tools.

Box content management: uploads, search, folders, moves, deletion, shared
links, collaborator access, file locking, comments, and retention.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="box", confusable_with=["gdrive_upload_file", "dropbox_upload_file", "onedrive_upload_file"])
def box_upload_file(local_path: str, folder_id: str, name: Optional[str] = None) -> dict:
    """Upload a file from disk into a Box folder.

    Args:
        local_path: Path of the file to upload.
        folder_id: Identifier of the destination Box folder.
        name: Name to store the file under; the local name when omitted.
    """
    return {"status": "stub", "tool": "box_upload_file", "args": locals()}


@tool(domain="box", confusable_with=["gdrive_search_files", "dropbox_search_files"])
def box_search_files(
    query: str,
    folder_id: Optional[str] = None,
    file_type: Optional[str] = None,
    limit: Optional[int] = None,
) -> dict:
    """Search Box for content matching a query.

    Args:
        query: Free-text search query.
        folder_id: Restrict the search to this folder.
        file_type: Restrict results to this file type.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "box_search_files", "args": locals()}


@tool(domain="box", confusable_with=["gdrive_list_files", "dropbox_list_folder"])
def box_list_folder_items(folder_id: str, limit: Optional[int] = None) -> dict:
    """List the files and subfolders contained in a Box folder.

    Args:
        folder_id: Identifier of the folder to list.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "box_list_folder_items", "args": locals()}


@tool(domain="box", confusable_with=["gdrive_share_file", "dropbox_create_shared_link"])
def box_share_file(
    file_id: str,
    access: Optional[Literal['open', 'company', 'collaborators']] = None,
    expires_at: Optional[str] = None,
) -> dict:
    """Create a shared link to a Box file so others can open it.

    Args:
        file_id: Identifier of the file to share.
        access: Who the link works for. One of: open, company, collaborators.
        expires_at: ISO 8601 time when the link should stop working.
    """
    return {"status": "stub", "tool": "box_share_file", "args": locals()}


@tool(domain="box", confusable_with=["gdrive_create_folder", "dropbox_create_folder"])
def box_create_folder(name: str, parent_folder_id: Optional[str] = None) -> dict:
    """Create a new folder in Box.

    Args:
        name: Name of the folder to create.
        parent_folder_id: Folder to create it inside; the root when omitted.
    """
    return {"status": "stub", "tool": "box_create_folder", "args": locals()}


@tool(domain="box", confusable_with=["gdrive_move_file", "dropbox_move_file"])
def box_move_file(file_id: str, target_folder_id: str, new_name: Optional[str] = None) -> dict:
    """Move a Box file into a different folder, optionally renaming it.

    Args:
        file_id: Identifier of the file to move.
        target_folder_id: Identifier of the destination folder.
        new_name: New name for the file.
    """
    return {"status": "stub", "tool": "box_move_file", "args": locals()}


@tool(domain="box", confusable_with=["gdrive_delete_file", "dropbox_delete_file"])
def box_delete_file(file_id: str, permanent: Optional[bool] = None) -> dict:
    """Send a Box file to the trash, or purge it outright.

    Args:
        file_id: Identifier of the file to delete.
        permanent: Purge immediately instead of moving to the trash.
    """
    return {"status": "stub", "tool": "box_delete_file", "args": locals()}


@tool(domain="box", confusable_with=["dropbox_invite_to_shared_folder", "gdrive_share_file"])
def box_add_collaborator(
    folder_id: str,
    email: str,
    role: Optional[Literal['viewer', 'editor', 'co_owner']] = None,
) -> dict:
    """Give someone standing access to a Box folder as a collaborator.

    Args:
        folder_id: Identifier of the folder to share.
        email: Email address of the person to add.
        role: Permission level. One of: viewer, editor, co_owner.
    """
    return {"status": "stub", "tool": "box_add_collaborator", "args": locals()}


@tool(domain="box")
def box_lock_file(file_id: str, expires_at: Optional[str] = None, prevent_download: Optional[bool] = None) -> dict:
    """Lock a Box file so other collaborators cannot edit it while you work.

    Args:
        file_id: Identifier of the file to lock.
        expires_at: ISO 8601 time when the lock should release.
        prevent_download: Block downloads as well as edits while locked.
    """
    return {"status": "stub", "tool": "box_lock_file", "args": locals()}


@tool(domain="box", confusable_with=["notion_add_comment", "gdrive_share_file"])
def box_add_file_comment(file_id: str, message: str, tagged_users: Optional[list[str]] = None) -> dict:
    """Leave a comment on a Box file for other collaborators.

    Args:
        file_id: Identifier of the file.
        message: Comment body.
        tagged_users: Email addresses to mention in the comment.
    """
    return {"status": "stub", "tool": "box_add_file_comment", "args": locals()}
