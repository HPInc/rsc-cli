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
