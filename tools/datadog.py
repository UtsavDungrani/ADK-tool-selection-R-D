"""datadog tools.

Datadog observability: log search, metric queries, monitors and muting,
dashboards, distributed traces, service level objectives, and host inventory.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="datadog", confusable_with=["sentry_list_events", "newrelic_search_errors"])
def datadog_search_logs(
    query: str,
    service: Optional[str] = None,
    from_time: Optional[str] = None,
    limit: Optional[int] = None,
) -> dict:
    """Search ingested application logs in Datadog for matching entries.

    Args:
        query: Datadog log search query, e.g. status:error service:api.
        service: Restrict the search to this service.
        from_time: Earliest timestamp in ISO 8601 form.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "datadog_search_logs", "args": locals()}


@tool(domain="datadog", confusable_with=["newrelic_query_nrql", "grafana_query_datasource"])
def datadog_query_metrics(
    metric_query: str,
    from_time: Optional[str] = None,
    to_time: Optional[str] = None,
) -> dict:
    """Run a Datadog metric query and return the resulting time series.

    Args:
        metric_query: Metric query, e.g. avg:system.cpu.user{service:api}.
        from_time: Start of the window in ISO 8601 form.
        to_time: End of the window in ISO 8601 form.
    """
    return {"status": "stub", "tool": "datadog_query_metrics", "args": locals()}


@tool(domain="datadog", confusable_with=["sentry_create_alert_rule", "grafana_create_alert_rule"])
def datadog_create_monitor(
    name: str,
    query: str,
    threshold: Optional[float] = None,
    notify: Optional[list[str]] = None,
) -> dict:
    """Create a Datadog monitor that alerts when a metric crosses a threshold.

    Args:
        name: Name of the monitor.
        query: Metric query the monitor evaluates.
        threshold: Value above which the monitor should alert.
        notify: Handles or emails to notify when it triggers.
    """
    return {"status": "stub", "tool": "datadog_create_monitor", "args": locals()}


@tool(domain="datadog", confusable_with=["pagerduty_snooze_incident", "grafana_silence_alert"])
def datadog_mute_monitor(monitor_id: str, until: Optional[str] = None, reason: Optional[str] = None) -> dict:
    """Silence a noisy Datadog monitor so it stops paging, temporarily or indefinitely.

    Args:
        monitor_id: Identifier of the monitor to mute.
        until: ISO 8601 time when muting should end.
        reason: Why the monitor is being muted.
    """
    return {"status": "stub", "tool": "datadog_mute_monitor", "args": locals()}


@tool(domain="datadog", confusable_with=["grafana_list_alerts", "pagerduty_list_incidents"])
def datadog_list_monitors(
    status: Optional[Literal['alert', 'warn', 'ok', 'no_data']] = None,
    tag: Optional[str] = None,
    limit: Optional[int] = None,
) -> dict:
    """List Datadog monitors and the state each one is currently in.

    Args:
        status: Filter by monitor state. One of: alert, warn, ok, no_data.
        tag: Restrict results to monitors carrying this tag.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "datadog_list_monitors", "args": locals()}


@tool(domain="datadog", confusable_with=["grafana_create_dashboard", "newrelic_create_dashboard"])
def datadog_create_dashboard(title: str, description: Optional[str] = None, widgets: Optional[list[str]] = None) -> dict:
    """Create a Datadog dashboard to display metrics on one screen.

    Args:
        title: Title of the dashboard.
        description: Short description of what it shows.
        widgets: Widget definitions to add, as metric query strings.
    """
    return {"status": "stub", "tool": "datadog_create_dashboard", "args": locals()}


@tool(domain="datadog", confusable_with=["sentry_get_issue_details", "newrelic_get_transaction_trace"])
def datadog_get_trace(trace_id: str, service: Optional[str] = None) -> dict:
    """Fetch a distributed trace in Datadog APM to see where a request spent its time.

    Args:
        trace_id: Identifier of the trace to fetch.
        service: Service the trace started in.
    """
    return {"status": "stub", "tool": "datadog_get_trace", "args": locals()}


@tool(domain="datadog")
def datadog_create_slo(
    name: str,
    target_percent: float,
    monitor_ids: Optional[list[str]] = None,
    timeframe: Optional[Literal['7d', '30d', '90d']] = None,
) -> dict:
    """Define a Datadog service level objective and its error budget.

    Args:
        name: Name of the objective.
        target_percent: Target availability, e.g. 99.9.
        monitor_ids: Monitors whose results the objective is calculated from.
        timeframe: Rolling window. One of: 7d, 30d, 90d.
    """
    return {"status": "stub", "tool": "datadog_create_slo", "args": locals()}


@tool(domain="datadog", confusable_with=["grafana_create_annotation", "newrelic_deploy_marker"])
def datadog_post_event(title: str, text: str, tags: Optional[list[str]] = None) -> dict:
    """Post an event onto the Datadog event stream to mark something that happened.

    Args:
        title: Short event title.
        text: Body describing the event.
        tags: Tags to attach so the event can be correlated with metrics.
    """
    return {"status": "stub", "tool": "datadog_post_event", "args": locals()}


@tool(domain="datadog", confusable_with=["newrelic_list_applications"])
def datadog_list_hosts(tag: Optional[str] = None, muted: Optional[bool] = None, limit: Optional[int] = None) -> dict:
    """List the hosts reporting into Datadog and their last-seen status.

    Args:
        tag: Restrict results to hosts carrying this tag.
        muted: Return only muted or only unmuted hosts.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "datadog_list_hosts", "args": locals()}
