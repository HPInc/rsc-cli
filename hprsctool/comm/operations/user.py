"""User management operations"""

from typing import List

from ...comm.remote_system_controller import RedfishError, Rsc
from ...models.user import Role, RoleCollection, User, UserCollection


def get_roles(rsc: Rsc) -> List[Role]:
    """Get all available roles from the system"""
    
    role_collection = RoleCollection(
        rsc.perform_redfish_get("/redfish/v1/AccountService/Roles").dict
    )
    
    roles = []
    
    for role_url in role_collection.members:
        roles.append(Role(rsc.perform_redfish_get(role_url).dict))
    
    return roles


def get_role_ids(rsc: Rsc) -> List[str]:
    """Get all available role IDs from the system"""
    roles = get_roles(rsc)
    return [role.role_id for role in roles]


def create_user(rsc: Rsc, username: str, password: str, role_id: str) -> User:
    """Create a new user account"""
    # First validate that the role exists
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


def change_user_password(rsc: Rsc, account_id: str, new_password: str) -> User:
    """Change user password"""
    body = {"Password": new_password}
    
    rsc.perform_redfish_patch(f"/redfish/v1/AccountService/Accounts/{account_id}", body)
    
    return get_user(rsc, account_id)


def delete_user(rsc: Rsc, account_id: str) -> None:
    """Delete a user account"""
    rsc.perform_redfish_delete(f"/redfish/v1/AccountService/Accounts/{account_id}")


def get_user(rsc: Rsc, account_id: str) -> User:
    """Get a specific user account"""
    
    return User(
        rsc.perform_redfish_get(f"/redfish/v1/AccountService/Accounts/{account_id}").dict
    )


def get_users(rsc: Rsc) -> List[User]:
    """Get all user accounts"""
    
    user_collection = UserCollection(
        rsc.perform_redfish_get("/redfish/v1/AccountService/Accounts").dict
    )
    
    users = []
    
    for user_url in user_collection.members:
        users.append(User(rsc.perform_redfish_get(user_url).dict))
    
    return users
