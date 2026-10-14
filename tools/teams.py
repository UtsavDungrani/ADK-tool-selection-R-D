"""teams tools.

Microsoft Teams collaboration: channel posts, private chats, channel
management, membership, message search, file sharing, and presence.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="teams", confusable_with=["slack_post_message"])
def teams_post_message(
    team: str,
    channel: str,
    content: str,
    importance: Optional[Literal['normal', 'high', 'urgent']] = None,
) -> dict:
    """Post a message to a channel in a Microsoft Teams team.

    Args:
        team: Name or identifier of the team.
        channel: Channel within that team, e.g. General.
        content: Message body.
        importance: Delivery emphasis. One of: normal, high, urgent.
    """
    return {"status": "stub", "tool": "teams_post_message", "args": locals()}


@tool(domain="teams", confusable_with=["slack_send_dm"])
def teams_send_chat_message(recipient: str, content: str) -> dict:
    """Send a private one-to-one chat message to a Microsoft Teams user.

    Args:
        recipient: Email or user identifier of the person to message.
        content: Message body.
    """
    return {"status": "stub", "tool": "teams_send_chat_message", "args": locals()}


@tool(domain="teams", confusable_with=["slack_create_channel"])
def teams_create_channel(
    team: str,
    name: str,
    description: Optional[str] = None,
    membership: Optional[Literal['standard', 'private', 'shared']] = None,
) -> dict:
    """Create a new channel inside an existing Microsoft Teams team.

    Args:
        team: Name or identifier of the team.
        name: Name of the new channel.
        description: Short description of the channel's purpose.
        membership: Channel type. One of: standard, private, shared.
    """
    return {"status": "stub", "tool": "teams_create_channel", "args": locals()}


@tool(domain="teams", confusable_with=["slack_list_channels"])
def teams_list_channels(team: str, limit: Optional[int] = None) -> dict:
    """List the channels available inside a Microsoft Teams team.

    Args:
        team: Name or identifier of the team.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "teams_list_channels", "args": locals()}


@tool(domain="teams", confusable_with=["slack_search_messages"])
def teams_search_messages(
    query: str,
    team: Optional[str] = None,
    channel: Optional[str] = None,
    limit: Optional[int] = None,
) -> dict:
    """Search the Microsoft Teams message history for text someone posted.

    Args:
        query: Free-text search query.
        team: Restrict the search to this team.
        channel: Restrict the search to this channel.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "teams_search_messages", "args": locals()}


@tool(domain="teams", confusable_with=["slack_invite_to_channel"])
def teams_add_channel_member(team: str, channel: str, user: str) -> dict:
    """Add a person to a Microsoft Teams channel so they can see its posts.

    Args:
        team: Name or identifier of the team.
        channel: Channel to add the member to.
        user: Email or user identifier of the person to add.
    """
    return {"status": "stub", "tool": "teams_add_channel_member", "args": locals()}


@tool(domain="teams", confusable_with=["gcalendar_create_event", "zoom_create_meeting"])
def teams_schedule_meeting(
    subject: str,
    start_time: str,
    attendees: Optional[list[str]] = None,
    duration_minutes: Optional[int] = None,
) -> dict:
    """Schedule a Microsoft Teams video meeting and send the join link to attendees.

    Args:
        subject: Meeting title.
        start_time: Start time in ISO 8601 form.
        attendees: Email addresses to invite.
        duration_minutes: Meeting length in minutes.
    """
    return {"status": "stub", "tool": "teams_schedule_meeting", "args": locals()}


@tool(domain="teams", confusable_with=["slack_upload_file", "gdrive_share_file"])
def teams_share_file(team: str, channel: str, file_path: str, message: Optional[str] = None) -> dict:
    """Upload a file into a Microsoft Teams channel's Files tab.

    Args:
        team: Name or identifier of the team.
        channel: Channel to share the file into.
        file_path: Path of the file to upload.
        message: Message to post alongside the file.
    """
    return {"status": "stub", "tool": "teams_share_file", "args": locals()}


@tool(domain="teams", confusable_with=["slack_set_status", "gcalendar_set_out_of_office"])
def teams_set_presence(
    availability: Literal['available', 'busy', 'do_not_disturb', 'away'],
    message: Optional[str] = None,
    expires_at: Optional[str] = None,
) -> dict:
    """Set your own availability indicator in Microsoft Teams.

    Args:
        availability: Presence to show. One of: available, busy, do_not_disturb, away.
        message: Status note shown alongside the presence.
        expires_at: ISO 8601 time when the presence should reset.
    """
    return {"status": "stub", "tool": "teams_set_presence", "args": locals()}


@tool(domain="teams")
def teams_pin_message(team: str, channel: str, message_id: str) -> dict:
    """Pin a message to the top of a Microsoft Teams channel.

    Args:
        team: Name or identifier of the team.
        channel: Channel the message is in.
        message_id: Identifier of the message to pin.
    """
    return {"status": "stub", "tool": "teams_pin_message", "args": locals()}
