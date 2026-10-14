"""airtable tools.

Airtable bases: records, tables and fields, filtered views, search, updates
and deletion, attachments, CSV export, and bases.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="airtable", confusable_with=["notion_query_database", "sharepoint_add_list_item"])
def airtable_create_record(base: str, table: str, fields: list[str]) -> dict:
    """Add a row to an Airtable table.

    Args:
        base: Airtable base name or identifier.
        table: Table to add the record to.
        fields: Field values as name=value strings.
    """
    return {"status": "stub", "tool": "airtable_create_record", "args": locals()}


@tool(domain="airtable", confusable_with=["notion_query_database"])
def airtable_search_records(
    base: str,
    table: str,
    formula: Optional[str] = None,
    view: Optional[str] = None,
    limit: Optional[int] = None,
) -> dict:
    """Query rows in an Airtable table, optionally filtered by formula or view.

    Args:
        base: Airtable base name or identifier.
        table: Table to query.
        formula: Airtable filter formula, e.g. {Status}='Open'.
        view: Restrict results to rows visible in this view.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "airtable_search_records", "args": locals()}


@tool(domain="airtable", confusable_with=["notion_update_page"])
def airtable_update_record(base: str, table: str, record_id: str, fields: list[str]) -> dict:
    """Change field values on an existing Airtable record.

    Args:
        base: Airtable base name or identifier.
        table: Table holding the record.
        record_id: Identifier of the record to update.
        fields: Field values to set, as name=value strings.
    """
    return {"status": "stub", "tool": "airtable_update_record", "args": locals()}


@tool(domain="airtable", confusable_with=["gdrive_delete_file"])
def airtable_delete_record(base: str, table: str, record_id: str) -> dict:
    """Delete a row from an Airtable table.

    Args:
        base: Airtable base name or identifier.
        table: Table holding the record.
        record_id: Identifier of the record to delete.
    """
    return {"status": "stub", "tool": "airtable_delete_record", "args": locals()}


@tool(domain="airtable", confusable_with=["notion_create_database", "sharepoint_create_list"])
def airtable_create_table(base: str, name: str, fields: Optional[list[str]] = None) -> dict:
    """Create a new table inside an Airtable base.

    Args:
        base: Airtable base name or identifier.
        name: Name of the new table.
        fields: Field definitions as name:type strings.
    """
    return {"status": "stub", "tool": "airtable_create_table", "args": locals()}


@tool(domain="airtable", confusable_with=["notion_search_pages"])
def airtable_list_bases(workspace: Optional[str] = None, limit: Optional[int] = None) -> dict:
    """List the Airtable bases available in a workspace.

    Args:
        workspace: Restrict results to this workspace.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "airtable_list_bases", "args": locals()}


@tool(domain="airtable", confusable_with=["zendesk_list_views"])
def airtable_create_view(
    base: str,
    table: str,
    name: str,
    view_type: Optional[Literal['grid', 'kanban', 'calendar', 'gallery']] = None,
    filter_formula: Optional[str] = None,
) -> dict:
    """Create a saved, filtered view over an Airtable table.

    Args:
        base: Airtable base name or identifier.
        table: Table the view belongs to.
        name: Name of the new view.
        view_type: Presentation style. One of: grid, kanban, calendar, gallery.
        filter_formula: Formula restricting which rows appear.
    """
    return {"status": "stub", "tool": "airtable_create_view", "args": locals()}


@tool(domain="airtable")
def airtable_add_field(
    base: str,
    table: str,
    name: str,
    field_type: Literal['text', 'number', 'date', 'select', 'checkbox', 'link'],
) -> dict:
    """Add a new column to an Airtable table.

    Args:
        base: Airtable base name or identifier.
        table: Table to add the column to.
        name: Name of the new field.
        field_type: Column type. One of: text, number, date, select, checkbox, link.
    """
    return {"status": "stub", "tool": "airtable_add_field", "args": locals()}


@tool(domain="airtable", confusable_with=["gdrive_export_file", "salesforce_run_report"])
def airtable_export_csv(base: str, table: str, view: Optional[str] = None) -> dict:
    """Export an Airtable table or view as a CSV file.

    Args:
        base: Airtable base name or identifier.
        table: Table to export.
        view: Export only the rows visible in this view.
    """
    return {"status": "stub", "tool": "airtable_export_csv", "args": locals()}


@tool(domain="airtable", confusable_with=["confluence_attach_file", "box_upload_file"])
def airtable_add_attachment(base: str, table: str, record_id: str, file_url: str) -> dict:
    """Attach a file to an attachment field on an Airtable record.

    Args:
        base: Airtable base name or identifier.
        table: Table holding the record.
        record_id: Identifier of the record.
        file_url: Publicly reachable URL of the file to attach.
    """
    return {"status": "stub", "tool": "airtable_add_attachment", "args": locals()}
