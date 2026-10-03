"""stripe tools.

Payments and billing: customers, invoices, charges, refunds, subscriptions,
payment links, and account balance.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="stripe")
def stripe_create_customer(email: str, name: Optional[str] = None) -> dict:
    """Create a new customer record in Stripe for billing.

    Args:
        email: Customer email address.
        name: Customer display name.
    """
    return {"status": "stub", "tool": "stripe_create_customer", "args": locals()}


@tool(domain="stripe")
def stripe_search_customers(query: str, limit: Optional[int] = None) -> dict:
    """Search Stripe customers by email, name, or metadata.

    Args:
        query: Free-text search query.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "stripe_search_customers", "args": locals()}


@tool(domain="stripe")
def stripe_create_invoice(
    customer_id: str,
    amount_cents: int,
    send: Optional[bool] = None,
) -> dict:
    """Create and optionally send a Stripe invoice to a customer.

    Args:
        customer_id: Identifier of the Stripe customer.
        amount_cents: Invoice amount in the smallest currency unit.
        send: Whether to email the invoice immediately.
    """
    return {"status": "stub", "tool": "stripe_create_invoice", "args": locals()}


@tool(domain="stripe")
def stripe_refund_payment(charge_id: str, amount_cents: Optional[int] = None) -> dict:
    """Issue a full or partial refund for a Stripe payment.

    Args:
        charge_id: Identifier of the charge to refund.
        amount_cents: Amount to refund; omit for a full refund.
    """
    return {"status": "stub", "tool": "stripe_refund_payment", "args": locals()}


@tool(domain="stripe")
def stripe_list_subscriptions(
    customer_id: Optional[str] = None,
    status: Optional[Literal['active', 'past_due', 'canceled', 'trialing']] = None,
    limit: Optional[int] = None,
) -> dict:
    """List Stripe subscriptions, optionally filtered by customer or status.

    Args:
        customer_id: Restrict to one customer.
        status: Filter by subscription status. One of: active, past_due, canceled,
            trialing.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "stripe_list_subscriptions", "args": locals()}


@tool(domain="stripe")
def stripe_cancel_subscription(
    subscription_id: str,
    at_period_end: Optional[bool] = None,
) -> dict:
    """Cancel a Stripe subscription, immediately or at the end of the billing period.

    Args:
        subscription_id: Identifier of the subscription.
        at_period_end: Cancel at period end rather than immediately.
    """
    return {"status": "stub", "tool": "stripe_cancel_subscription", "args": locals()}


@tool(domain="stripe")
def stripe_list_charges(
    customer_id: Optional[str] = None,
    limit: Optional[int] = None,
) -> dict:
    """List recent Stripe charges with their amounts and outcomes.

    Args:
        customer_id: Restrict to one customer.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "stripe_list_charges", "args": locals()}


@tool(domain="stripe")
def stripe_create_payment_link(
    amount_cents: int,
    description: Optional[str] = None,
) -> dict:
    """Create a shareable Stripe payment link for a product or amount.

    Args:
        amount_cents: Amount in the smallest currency unit.
        description: What the payment is for.
    """
    return {"status": "stub", "tool": "stripe_create_payment_link", "args": locals()}


@tool(domain="stripe")
def stripe_update_subscription(
    subscription_id: str,
    price_id: Optional[str] = None,
    quantity: Optional[int] = None,
) -> dict:
    """Change the plan or quantity on an existing Stripe subscription.

    Args:
        subscription_id: Identifier of the subscription.
        price_id: Identifier of the new price.
        quantity: New seat or unit quantity.
    """
    return {"status": "stub", "tool": "stripe_update_subscription", "args": locals()}


@tool(domain="stripe")
def stripe_get_balance() -> dict:
    """Retrieve the current available and pending balance in the Stripe account.
    """
    return {"status": "stub", "tool": "stripe_get_balance", "args": locals()}
