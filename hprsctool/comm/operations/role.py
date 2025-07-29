"""Role management operations."""

from typing import List
from ...comm.remote_system_controller import RedfishError, Rsc
from ...models.role import Role, RoleCollection

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

def get_role_privileges(rsc: Rsc, role_id: str) -> Role:
    """Get privileges for a specific role"""
    role_url = f"/redfish/v1/AccountService/Roles/{role_id}"
    role_data = rsc.perform_redfish_get(role_url).dict
    return Role(role_data)

def create_role(rsc: Rsc, role_id: str, assigned_privileges: List[str], oem_privileges: List[str]) -> None:
    """Create a new role with specified privileges"""
    role_data = {
        "RoleId": role_id,
        "AssignedPrivileges": assigned_privileges,
        "OemPrivileges": oem_privileges
    }
    rsc.perform_redfish_post("/redfish/v1/AccountService/Roles", role_data)

def update_role_privileges(rsc: Rsc, role_id: str, assigned_privileges: List[str] = None, oem_privileges: List[str] = None) -> None:
    """Update an existing role's privileges"""
    role_data = {}
    if assigned_privileges is not None:
        role_data["AssignedPrivileges"] = assigned_privileges
    if oem_privileges is not None:
        role_data["OemPrivileges"] = oem_privileges

    role_url = f"/redfish/v1/AccountService/Roles/{role_id}"
    rsc.perform_redfish_patch(role_url, role_data)

def delete_role(rsc: Rsc, role_id: str) -> None:
    """Delete an existing role"""
    role_url = f"/redfish/v1/AccountService/Roles/{role_id}"
    rsc.perform_redfish_delete(role_url)
