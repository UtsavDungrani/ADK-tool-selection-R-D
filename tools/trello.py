"""trello tools.

Kanban boards: boards, lists, cards, card movement between lists, checklists,
members, due dates, and archiving.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="trello", confusable_with=["asana_create_task", "jira_create_issue"])
def trello_create_card(
    board: str,
    list_name: str,
    name: str,
    description: Optional[str] = None,
    due: Optional[str] = None,
) -> dict:
    """Add a card to a list on a Trello board.

    Args:
        board: Board name or identifier.
        list_name: List on the board to add the card to, e.g. Backlog.
        name: Short card title.
        description: Longer card description.
        due: Due date in YYYY-MM-DD form.
    """
    return {"status": "stub", "tool": "trello_create_card", "args": locals()}


@tool(domain="trello", confusable_with=["jira_transition_issue", "linear_update_issue_status"])
def trello_move_card(
    card_id: str,
    target_list: str,
    position: Optional[Literal['top', 'bottom']] = None,
) -> dict:
    """Move a Trello card from its current list into another list on the board.

    Args:
        card_id: Identifier of the card to move.
        target_list: Name of the destination list, e.g. In Progress.
        position: Where in the destination list to place it. One of: top, bottom.
    """
    return {"status": "stub", "tool": "trello_move_card", "args": locals()}


@tool(domain="trello", confusable_with=["asana_search_tasks", "jira_search_issues"])
def trello_search_cards(query: str, board: Optional[str] = None, limit: Optional[int] = None) -> dict:
    """Search Trello cards by free text across one board or the whole workspace.

    Args:
        query: Free-text search query.
        board: Restrict the search to this board.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "trello_search_cards", "args": locals()}


@tool(domain="trello")
def trello_add_checklist(card_id: str, name: str, items: Optional[list[str]] = None) -> dict:
    """Attach a checklist of sub-items to a Trello card.

    Args:
        card_id: Identifier of the card.
        name: Name of the checklist.
        items: Checklist item texts to create.
    """
    return {"status": "stub", "tool": "trello_add_checklist", "args": locals()}


@tool(domain="trello", confusable_with=["asana_add_comment", "jira_add_comment"])
def trello_add_comment(card_id: str, text: str) -> dict:
    """Post a comment onto a Trello card.

    Args:
        card_id: Identifier of the card.
        text: Comment body.
    """
    return {"status": "stub", "tool": "trello_add_comment", "args": locals()}


@tool(domain="trello")
def trello_create_board(name: str, description: Optional[str] = None, template: Optional[str] = None) -> dict:
    """Create a new Trello board, optionally copied from an existing template.

    Args:
        name: Name of the new board.
        description: Short description of the board's purpose.
        template: Template board to copy the structure from.
    """
    return {"status": "stub", "tool": "trello_create_board", "args": locals()}


@tool(domain="trello")
def trello_create_list(board: str, name: str, position: Optional[Literal['top', 'bottom']] = None) -> dict:
    """Add a new column list to an existing Trello board.

    Args:
        board: Board name or identifier.
        name: Name of the new list, e.g. In Review.
        position: Where to place the list. One of: top, bottom.
    """
    return {"status": "stub", "tool": "trello_create_list", "args": locals()}


@tool(domain="trello", confusable_with=["asana_assign_task", "jira_assign_issue"])
def trello_assign_member(card_id: str, member: str) -> dict:
    """Put a board member on a Trello card to make them its owner.

    Args:
        card_id: Identifier of the card.
        member: Username or email of the member to assign.
    """
    return {"status": "stub", "tool": "trello_assign_member", "args": locals()}


@tool(domain="trello", confusable_with=["asana_set_due_date"])
def trello_set_due_date(card_id: str, due: str, reminder_minutes: Optional[int] = None) -> dict:
    """Set or change the due date on a Trello card.

    Args:
        card_id: Identifier of the card.
        due: Due date in YYYY-MM-DD form.
        reminder_minutes: Minutes before the due date to send a reminder.
    """
    return {"status": "stub", "tool": "trello_set_due_date", "args": locals()}


@tool(domain="trello", confusable_with=["notion_archive_page", "confluence_archive_page"])
def trello_archive_card(card_id: str) -> dict:
    """Archive a Trello card so it leaves the board without being deleted.

    Args:
        card_id: Identifier of the card to archive.
    """
    return {"status": "stub", "tool": "trello_archive_card", "args": locals()}
