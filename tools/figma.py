"""figma tools.

Figma design files: files and pages, design comments, frame exports, component
libraries, branches, sharing, version history, and prototype links.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="figma", confusable_with=["notion_create_page"])
def figma_create_file(name: str, team: Optional[str] = None, template: Optional[str] = None) -> dict:
    """Create a new Figma design file in a team project.

    Args:
        name: Name of the new design file.
        team: Team project to create it in.
        template: Template file to start from.
    """
    return {"status": "stub", "tool": "figma_create_file", "args": locals()}


@tool(domain="figma", confusable_with=["gdrive_search_files"])
def figma_search_files(query: str, team: Optional[str] = None, limit: Optional[int] = None) -> dict:
    """Search Figma for design files by name.

    Args:
        query: Free-text search query.
        team: Restrict the search to this team.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "figma_search_files", "args": locals()}


@tool(domain="figma", confusable_with=["notion_add_comment", "github_add_comment"])
def figma_add_comment(file_key: str, message: str, node_id: Optional[str] = None) -> dict:
    """Leave a comment on a Figma design, optionally pinned to a specific element.

    Args:
        file_key: Key of the Figma file.
        message: Comment text.
        node_id: Identifier of the layer or frame to pin the comment to.
    """
    return {"status": "stub", "tool": "figma_add_comment", "args": locals()}


@tool(domain="figma", confusable_with=["gdrive_export_file", "grafana_export_dashboard"])
def figma_export_frame(
    file_key: str,
    node_id: str,
    export_format: Optional[Literal['png', 'svg', 'pdf', 'jpg']] = None,
    scale: Optional[float] = None,
) -> dict:
    """Export a Figma frame or component as an image asset for engineering handoff.

    Args:
        file_key: Key of the Figma file.
        node_id: Identifier of the frame to export.
        export_format: Output format. One of: png, svg, pdf, jpg.
        scale: Export scale factor, e.g. 2 for 2x assets.
    """
    return {"status": "stub", "tool": "figma_export_frame", "args": locals()}


@tool(domain="figma")
def figma_list_components(file_key: str, published_only: Optional[bool] = None) -> dict:
    """List the reusable components defined in a Figma file.

    Args:
        file_key: Key of the Figma file.
        published_only: Return only components published to a library.
    """
    return {"status": "stub", "tool": "figma_list_components", "args": locals()}


@tool(domain="figma", confusable_with=["github_create_branch", "gitlab_create_branch"])
def figma_create_branch(file_key: str, branch_name: str, description: Optional[str] = None) -> dict:
    """Create a branch of a Figma design file so changes can be reviewed before merging.

    Args:
        file_key: Key of the Figma file to branch.
        branch_name: Name of the new branch.
        description: What the branch is for.
    """
    return {"status": "stub", "tool": "figma_create_branch", "args": locals()}


@tool(domain="figma", confusable_with=["gdrive_share_file", "notion_share_page"])
def figma_share_file(
    file_key: str,
    email: str,
    role: Optional[Literal['viewer', 'editor', 'owner']] = None,
) -> dict:
    """Invite someone to a Figma design file at a given permission level.

    Args:
        file_key: Key of the Figma file.
        email: Email address of the person to invite.
        role: Permission to grant. One of: viewer, editor, owner.
    """
    return {"status": "stub", "tool": "figma_share_file", "args": locals()}


@tool(domain="figma", confusable_with=["onedrive_restore_version"])
def figma_list_versions(file_key: str, limit: Optional[int] = None) -> dict:
    """List the saved version history of a Figma file.

    Args:
        file_key: Key of the Figma file.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "figma_list_versions", "args": locals()}


@tool(domain="figma", confusable_with=["sentry_list_releases"])
def figma_publish_library(file_key: str, description: Optional[str] = None) -> dict:
    """Publish a Figma file's components and styles as a shared team library.

    Args:
        file_key: Key of the Figma file to publish.
        description: Changelog note describing what changed.
    """
    return {"status": "stub", "tool": "figma_publish_library", "args": locals()}


@tool(domain="figma")
def figma_create_prototype_link(file_key: str, start_node_id: str, device: Optional[str] = None) -> dict:
    """Generate a shareable Figma prototype link that starts at a given frame.

    Args:
        file_key: Key of the Figma file.
        start_node_id: Frame the prototype should open on.
        device: Device frame to present the prototype in.
    """
    return {"status": "stub", "tool": "figma_create_prototype_link", "args": locals()}
