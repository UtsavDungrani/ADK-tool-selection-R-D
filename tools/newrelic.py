"""newrelic tools.

New Relic application performance monitoring: error inboxes, NRQL queries,
transaction traces, alert conditions and violations, applications, Apdex,
dashboards, and deployment markers.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="newrelic", confusable_with=["sentry_search_issues", "datadog_search_logs"])
def newrelic_search_errors(
    application: str,
    query: Optional[str] = None,
    since: Optional[str] = None,
    limit: Optional[int] = None,
) -> dict:
    """Search the New Relic error inbox for exceptions thrown by an application.

    Args:
        application: Name of the monitored application.
        query: Free-text filter on the error message or class.
        since: Earliest timestamp in ISO 8601 form.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "newrelic_search_errors", "args": locals()}


@tool(domain="newrelic", confusable_with=["datadog_query_metrics", "grafana_query_datasource"])
def newrelic_query_nrql(nrql: str, account_id: Optional[str] = None) -> dict:
    """Run an NRQL query against New Relic telemetry and return the rows.

    Args:
        nrql: NRQL query, e.g. SELECT count(*) FROM Transaction.
        account_id: Account to run the query against.
    """
    return {"status": "stub", "tool": "newrelic_query_nrql", "args": locals()}


@tool(domain="newrelic", confusable_with=["datadog_get_trace", "sentry_get_issue_details"])
def newrelic_get_transaction_trace(application: str, transaction: str, trace_id: Optional[str] = None) -> dict:
    """Fetch a slow transaction trace in New Relic to see which calls dominated the time.

    Args:
        application: Name of the monitored application.
        transaction: Name of the transaction, e.g. WebTransaction/API/checkout.
        trace_id: Specific trace to fetch; the slowest recent one when omitted.
    """
    return {"status": "stub", "tool": "newrelic_get_transaction_trace", "args": locals()}


@tool(domain="newrelic", confusable_with=["datadog_create_monitor", "grafana_create_alert_rule"])
def newrelic_create_alert_condition(
    policy: str,
    name: str,
    nrql: str,
    threshold: Optional[float] = None,
) -> dict:
    """Add an alert condition to a New Relic alert policy.

    Args:
        policy: Alert policy the condition belongs to.
        name: Name of the condition.
        nrql: NRQL query the condition evaluates.
        threshold: Value above which the condition opens a violation.
    """
    return {"status": "stub", "tool": "newrelic_create_alert_condition", "args": locals()}


@tool(domain="newrelic", confusable_with=["pagerduty_acknowledge_incident", "datadog_mute_monitor"])
def newrelic_acknowledge_violation(violation_id: str, comment: Optional[str] = None) -> dict:
    """Acknowledge an open New Relic alert violation so responders know it is being handled.

    Args:
        violation_id: Identifier of the violation.
        comment: Note about who is handling it.
    """
    return {"status": "stub", "tool": "newrelic_acknowledge_violation", "args": locals()}


@tool(domain="newrelic", confusable_with=["datadog_list_hosts"])
def newrelic_list_applications(language: Optional[str] = None, reporting: Optional[bool] = None, limit: Optional[int] = None) -> dict:
    """List the applications reporting telemetry into New Relic.

    Args:
        language: Restrict results to applications in this language.
        reporting: Return only applications currently sending data.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "newrelic_list_applications", "args": locals()}


@tool(domain="newrelic")
def newrelic_get_apdex_score(application: str, since: Optional[str] = None) -> dict:
    """Report the Apdex user-satisfaction score for a New Relic application.

    Args:
        application: Name of the monitored application.
        since: Start of the window in ISO 8601 form.
    """
    return {"status": "stub", "tool": "newrelic_get_apdex_score", "args": locals()}


@tool(domain="newrelic", confusable_with=["grafana_create_dashboard", "datadog_create_dashboard"])
def newrelic_create_dashboard(name: str, widgets: Optional[list[str]] = None, permissions: Optional[Literal['private', 'public_read_only', 'public_read_write']] = None) -> dict:
    """Create a New Relic dashboard built from NRQL widgets.

    Args:
        name: Name of the dashboard.
        widgets: NRQL queries to render as widgets.
        permissions: Who may see it. One of: private, public_read_only, public_read_write.
    """
    return {"status": "stub", "tool": "newrelic_create_dashboard", "args": locals()}


@tool(domain="newrelic", confusable_with=["sentry_list_releases", "datadog_post_event"])
def newrelic_deploy_marker(application: str, revision: str, description: Optional[str] = None, user: Optional[str] = None) -> dict:
    """Record a deployment marker in New Relic so charts show when the release landed.

    Args:
        application: Name of the monitored application.
        revision: Version or commit SHA that was deployed.
        description: Short note about what shipped.
        user: Who performed the deployment.
    """
    return {"status": "stub", "tool": "newrelic_deploy_marker", "args": locals()}


@tool(domain="newrelic", confusable_with=["sentry_list_releases"])
def newrelic_list_deployments(application: str, limit: Optional[int] = None) -> dict:
    """List the deployments recorded against a New Relic application.

    Args:
        application: Name of the monitored application.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "newrelic_list_deployments", "args": locals()}
