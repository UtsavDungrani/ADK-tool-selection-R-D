"""slack tools.

Team chat: channel and direct messages, channel management, message search,
reactions, file uploads, and user status.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="slack", confusable_with=["slack_send_dm", "github_add_comment"])
def slack_post_message(
    channel: str,
    text: str,
    thread_ts: Optional[str] = None,
) -> dict:
    """Post a message to a public or private Slack channel.

    Args:
        channel: Channel name or ID, e.g. engineering.
        text: Message body.
        thread_ts: Timestamp of a parent message to reply in-thread.
    """
    return {"status": "stub", "tool": "slack_post_message", "args": locals()}


@tool(domain="slack", confusable_with=["slack_post_message"])
def slack_send_dm(user: str, text: str) -> dict:
    """Send a direct private message to a single Slack user.

    Args:
        user: Slack username or user ID.
        text: Message body.
    """
    return {"status": "stub", "tool": "slack_send_dm", "args": locals()}


@tool(domain="slack")
def slack_create_channel(name: str, is_private: Optional[bool] = None) -> dict:
    """Create a new Slack channel, public or private.

    Args:
        name: Channel name without the leading hash.
        is_private: Whether the channel should be private.
    """
    return {"status": "stub", "tool": "slack_create_channel", "args": locals()}


@tool(domain="slack")
def slack_list_channels(
    types: Optional[Literal['public', 'private', 'all']] = None,
    limit: Optional[int] = None,
) -> dict:
    """List Slack channels in the workspace that the caller can see.

    Args:
        types: Channel visibility filter. One of: public, private, all.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "slack_list_channels", "args": locals()}


@tool(domain="slack")
def slack_search_messages(
    query: str,
    channel: Optional[str] = None,
    limit: Optional[int] = None,
) -> dict:
    """Search the Slack message history across channels for text.

    Args:
        query: Free-text search query.
        channel: Restrict the search to one channel.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "slack_search_messages", "args": locals()}


@tool(domain="slack", confusable_with=["gdrive_share_file"])
def slack_invite_to_channel(channel: str, users: list[str]) -> dict:
    """Invite one or more Slack users into an existing channel.

    Args:
        channel: Channel name or ID.
        users: Slack user IDs to invite.
    """
    return {"status": "stub", "tool": "slack_invite_to_channel", "args": locals()}


@tool(domain="slack", confusable_with=["jira_list_users"])
def slack_list_users(limit: Optional[int] = None) -> dict:
    """List members of the Slack workspace with their display names.

    Args:
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "slack_list_users", "args": locals()}


@tool(domain="slack", confusable_with=["gcalendar_set_out_of_office"])
def slack_set_status(
    text: str,
    emoji: Optional[str] = None,
    expires_at: Optional[str] = None,
) -> dict:
    """Set the caller's Slack status text, emoji, and expiry.

    Args:
        text: Status text to display.
        emoji: Status emoji shortcode.
        expires_at: ISO 8601 timestamp when the status clears.
    """
    return {"status": "stub", "tool": "slack_set_status", "args": locals()}


@tool(domain="slack", confusable_with=["gdrive_upload_file"])
def slack_upload_file(
    channel: str,
    file_path: str,
    title: Optional[str] = None,
) -> dict:
    """Upload a file attachment into a Slack channel or conversation.

    Args:
        channel: Destination channel name or ID.
        file_path: Local path of the file to upload.
        title: Display title for the file.
    """
    return {"status": "stub", "tool": "slack_upload_file", "args": locals()}


@tool(domain="slack")
def slack_add_reaction(channel: str, timestamp: str, emoji: str) -> dict:
    """Add an emoji reaction to an existing Slack message.

    Args:
        channel: Channel containing the message.
        timestamp: Timestamp identifying the message.
        emoji: Emoji shortcode to add.
    """
    return {"status": "stub", "tool": "slack_add_reaction", "args": locals()}
