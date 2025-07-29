"""Account (user) management operations."""

from typing import List
from ...comm.remote_system_controller import RedfishError, Rsc
from ...models.account import User, UserCollection
from .role import get_role_ids

def create_account(rsc: Rsc, username: str, password: str, role_id: str) -> User:
    """Create a new user account"""
    available_role_ids = get_role_ids(rsc)
    if role_id not in available_role_ids:
        raise RedfishError(f"Role '{role_id}' not found. Available roles: {', '.join(available_role_ids)}")
    body = {
        "UserName": username,
        "Password": password,
        "RoleId": role_id
    }
    return User(
        rsc.perform_redfish_post("/redfish/v1/AccountService/Accounts", body).dict
    )

def change_account_password(rsc: Rsc, account_id: str, new_password: str) -> User:
    """Change user password"""
    body = {"Password": new_password}
    rsc.perform_redfish_patch(f"/redfish/v1/AccountService/Accounts/{account_id}", body)
    return get_account(rsc, account_id)

def change_account_role(rsc: Rsc, account_id: str, role_id: str) -> User:
    """Change user role"""
    available_role_ids = get_role_ids(rsc)
    if role_id not in available_role_ids:
        raise RedfishError(f"Role '{role_id}' not found. Available roles: {', '.join(available_role_ids)}")
    body = {"RoleId": role_id}
    rsc.perform_redfish_patch(f"/redfish/v1/AccountService/Accounts/{account_id}", body)
    return get_account(rsc, account_id)

def delete_account(rsc: Rsc, account_id: str) -> None:
    """Delete a user account"""
    rsc.perform_redfish_delete(f"/redfish/v1/AccountService/Accounts/{account_id}")

def get_account(rsc: Rsc, account_id: str) -> User:
    """Get a specific user account"""
    return User(
        rsc.perform_redfish_get(f"/redfish/v1/AccountService/Accounts/{account_id}").dict
    )

def get_accounts(rsc: Rsc) -> List[User]:
    """Get all user accounts"""
    user_collection = UserCollection(
        rsc.perform_redfish_get("/redfish/v1/AccountService/Accounts").dict
    )
    users = []
    for user_url in user_collection.members:
        users.append(User(rsc.perform_redfish_get(user_url).dict))
    return users
