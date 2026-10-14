"""okta tools.

Okta identity and access: user lifecycle, group membership, application
assignments, credential resets, MFA policy, and access review.

Eight tools rather than ten. Domains are not required to be the same size --
`github` carries twelve -- and padding this one out with invented operations
would add vocabulary nobody would write a query against.

Every function here is a real Python function. Its docstring is the tool
description the model sees, its Args block supplies per-parameter
descriptions, and its signature supplies the schema. Bodies are stubs:
this project measures which tool gets chosen, not what it would do.
"""

from __future__ import annotations

from typing import Literal, Optional

from ._registry import tool


@tool(domain="okta", confusable_with=["slack_list_users", "jira_list_users"])
def okta_create_user(
    email: str,
    first_name: str,
    last_name: str,
    department: Optional[str] = None,
    activate: Optional[bool] = None,
) -> dict:
    """Provision a new user account in Okta for someone joining.

    Args:
        email: Email address, used as the login.
        first_name: User's given name.
        last_name: User's surname.
        department: Department to record on the profile.
        activate: Activate the account immediately rather than leaving it staged.
    """
    return {"status": "stub", "tool": "okta_create_user", "args": locals()}


@tool(domain="okta", confusable_with=["github_add_collaborator"])
def okta_deactivate_user(email: str, reason: Optional[str] = None) -> dict:
    """Deactivate an Okta account so the person loses access to every connected app.

    Args:
        email: Email address of the user to deactivate.
        reason: Why the account is being deactivated, e.g. offboarding.
    """
    return {"status": "stub", "tool": "okta_deactivate_user", "args": locals()}


@tool(domain="okta", confusable_with=["github_add_collaborator", "gdrive_share_file"])
def okta_assign_app(
    email: str,
    application: str,
    role: Optional[str] = None,
) -> dict:
    """Grant an Okta user access to a connected application.

    Args:
        email: Email address of the user.
        application: Name of the application to assign.
        role: Role to grant them within that application.
    """
    return {"status": "stub", "tool": "okta_assign_app", "args": locals()}


@tool(domain="okta", confusable_with=["slack_invite_to_channel", "teams_add_channel_member"])
def okta_add_user_to_group(email: str, group: str) -> dict:
    """Add an Okta user to a group so they inherit its application access.

    Args:
        email: Email address of the user.
        group: Name of the group to add them to.
    """
    return {"status": "stub", "tool": "okta_add_user_to_group", "args": locals()}


@tool(domain="okta")
def okta_reset_password(email: str, send_email: Optional[bool] = None, temporary: Optional[bool] = None) -> dict:
    """Trigger a password reset for an Okta user who has been locked out.

    Args:
        email: Email address of the user.
        send_email: Email the reset link to the user.
        temporary: Issue a one-time temporary password instead of a reset link.
    """
    return {"status": "stub", "tool": "okta_reset_password", "args": locals()}


@tool(domain="okta", confusable_with=["slack_list_users", "intercom_list_teammates"])
def okta_list_users(
    group: Optional[str] = None,
    status: Optional[Literal['active', 'staged', 'suspended', 'deprovisioned']] = None,
    limit: Optional[int] = None,
) -> dict:
    """List the user accounts held in Okta and their status.

    Args:
        group: Restrict results to members of this group.
        status: Filter by account status. One of: active, staged, suspended, deprovisioned.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "okta_list_users", "args": locals()}


@tool(domain="okta", confusable_with=["gdrive_get_file_permissions", "onedrive_get_item_permissions"])
def okta_list_app_assignments(application: str, limit: Optional[int] = None) -> dict:
    """List who currently has access to an application through Okta.

    Args:
        application: Name of the application to audit.
        limit: Maximum number of results to return.
    """
    return {"status": "stub", "tool": "okta_list_app_assignments", "args": locals()}


@tool(domain="okta")
def okta_enforce_mfa(
    group: str,
    factor: Literal['push', 'totp', 'webauthn', 'sms'],
    grace_period_days: Optional[int] = None,
) -> dict:
    """Require a second authentication factor for everyone in an Okta group.

    Args:
        group: Group the policy should apply to.
        factor: Required factor type. One of: push, totp, webauthn, sms.
        grace_period_days: Days users have to enrol before the rule is enforced.
    """
    return {"status": "stub", "tool": "okta_enforce_mfa", "args": locals()}
