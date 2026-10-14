"""grafana tools.

Grafana dashboards and alerting: dashboards and panels, datasource queries,
alert rules and silences, annotations, exports, and datasource configuration.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="grafana", confusable_with=["datadog_create_dashboard", "newrelic_create_dashboard"])
def grafana_create_dashboard(title: str, folder: Optional[str] = None, tags: Optional[list[str]] = None) -> dict:
    """Create a new Grafana dashboard to visualise metrics.

    Args:
        title: Title of the dashboard.
        folder: Folder to file the dashboard under.
        tags: Tags to attach for searching.
    """
    return {"status": "stub", "tool": "grafana_create_dashboard", "args": locals()}


@tool(domain="grafana", confusable_with=["datadog_list_monitors"])
def grafana_search_dashboards(query: str, folder: Optional[str] = None, limit: Optional[int] = None) -> dict:
    """Search existing Grafana dashboards by title or tag.

    Args:
        query: Free-text search query.
        folder: Restrict the search to this folder.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "grafana_search_dashboards", "args": locals()}


@tool(domain="grafana", confusable_with=["datadog_query_metrics", "newrelic_query_nrql"])
def grafana_query_datasource(
    datasource: str,
    query: str,
    from_time: Optional[str] = None,
    to_time: Optional[str] = None,
) -> dict:
    """Run a query against a Grafana datasource and return the series.

    Args:
        datasource: Name of the datasource to query, e.g. Prometheus.
        query: Query expression in that datasource's language.
        from_time: Start of the window in ISO 8601 form.
        to_time: End of the window in ISO 8601 form.
    """
    return {"status": "stub", "tool": "grafana_query_datasource", "args": locals()}


@tool(domain="grafana", confusable_with=["datadog_create_monitor", "sentry_create_alert_rule"])
def grafana_create_alert_rule(
    name: str,
    query: str,
    condition: Optional[str] = None,
    contact_point: Optional[str] = None,
) -> dict:
    """Create a Grafana alert rule that fires when a query breaches a condition.

    Args:
        name: Name of the alert rule.
        query: Query the rule evaluates.
        condition: Condition expression, e.g. avg() > 0.9.
        contact_point: Contact point to notify when the rule fires.
    """
    return {"status": "stub", "tool": "grafana_create_alert_rule", "args": locals()}


@tool(domain="grafana", confusable_with=["datadog_mute_monitor", "pagerduty_snooze_incident"])
def grafana_silence_alert(alert_rule: str, duration_minutes: int, comment: Optional[str] = None) -> dict:
    """Silence a firing Grafana alert for a period so it stops notifying.

    Args:
        alert_rule: Name or identifier of the alert rule to silence.
        duration_minutes: How long the silence should last.
        comment: Why the alert is being silenced.
    """
    return {"status": "stub", "tool": "grafana_silence_alert", "args": locals()}


@tool(domain="grafana", confusable_with=["datadog_list_monitors", "pagerduty_list_incidents"])
def grafana_list_alerts(
    state: Optional[Literal['firing', 'pending', 'normal']] = None,
    folder: Optional[str] = None,
    limit: Optional[int] = None,
) -> dict:
    """List Grafana alert rules and whether each is currently firing.

    Args:
        state: Filter by alert state. One of: firing, pending, normal.
        folder: Restrict results to rules in this folder.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "grafana_list_alerts", "args": locals()}


@tool(domain="grafana")
def grafana_add_panel(
    dashboard: str,
    title: str,
    query: str,
    visualization: Optional[Literal['timeseries', 'bar', 'gauge', 'table']] = None,
) -> dict:
    """Add a new panel to an existing Grafana dashboard.

    Args:
        dashboard: Title or identifier of the dashboard.
        title: Title of the new panel.
        query: Query the panel should plot.
        visualization: Panel type. One of: timeseries, bar, gauge, table.
    """
    return {"status": "stub", "tool": "grafana_add_panel", "args": locals()}


@tool(domain="grafana", confusable_with=["confluence_export_page", "gdrive_export_file"])
def grafana_export_dashboard(dashboard: str, export_format: Optional[Literal['json', 'pdf', 'png']] = None) -> dict:
    """Export a Grafana dashboard for sharing or version control.

    Args:
        dashboard: Title or identifier of the dashboard to export.
        export_format: Output format. One of: json, pdf, png.
    """
    return {"status": "stub", "tool": "grafana_export_dashboard", "args": locals()}


@tool(domain="grafana", confusable_with=["datadog_post_event", "newrelic_deploy_marker"])
def grafana_create_annotation(dashboard: str, text: str, time: Optional[str] = None, tags: Optional[list[str]] = None) -> dict:
    """Mark a point in time on a Grafana dashboard with an annotation.

    Args:
        dashboard: Dashboard to annotate.
        text: Annotation text, e.g. what changed.
        time: ISO 8601 time to place the marker at.
        tags: Tags to attach to the annotation.
    """
    return {"status": "stub", "tool": "grafana_create_annotation", "args": locals()}


@tool(domain="grafana")
def grafana_add_datasource(
    name: str,
    datasource_type: Literal['prometheus', 'loki', 'postgres', 'elasticsearch'],
    url: Optional[str] = None,
) -> dict:
    """Connect a new datasource to Grafana so dashboards can query it.

    Args:
        name: Name to give the datasource in Grafana.
        datasource_type: Backend type. One of: prometheus, loki, postgres, elasticsearch.
        url: Base URL the datasource is reachable at.
    """
    return {"status": "stub", "tool": "grafana_add_datasource", "args": locals()}
