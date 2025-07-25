"""User models"""

from typing import List


class Role:
    """Class defining a Role"""

    def __init__(self, data: dict):
        if data is None:
            raise ValueError("data is required")
        self.data = data

    @property
    def role_id(self) -> str:
        return self.data.get("RoleId", "N/A")

    @property
    def name(self) -> str:
        return self.data.get("Name", "N/A")

    @property
    def description(self) -> str:
        return self.data.get("Description", "N/A")

    @property
    def assigned_privileges(self) -> List[str]:
        return self.data.get("AssignedPrivileges", [])

    @property
    def oem_privileges(self) -> List[str]:
        return self.data.get("OemPrivileges", [])


class User:
    """Class defining a User (ManagerAccount)"""

    def __init__(self, data: dict):
        if data is None:
            raise ValueError("data is required")
        self.data = data

    @property
    def user_id(self) -> str:
        return self.data.get("Id", "N/A")

    @property
    def username(self) -> str:
        return self.data.get("UserName", "N/A")

    @property
    def role_id(self) -> str:
        return self.data.get("RoleId", "N/A")

    @property
    def name(self) -> str:
        return self.data.get("Name", "N/A")

    @property
    def password_change_required(self) -> bool:
        return self.data.get("PasswordChangeRequired", False)

    @property
    def account_types(self) -> List[str]:
        return self.data.get("AccountTypes", [])

    @property
    def role_links(self) -> List[str]:
        if "Links" in self.data and "Roles" in self.data["Links"]:
            return [role.get("@odata.id", "") for role in self.data["Links"]["Roles"]]
        return []

    @property
    def odata_id(self) -> str:
        return self.data.get("@odata.id", "N/A")

    @property
    def odata_type(self) -> str:
        return self.data.get("@odata.type", "N/A")


class UserCollection:
    """Class defining a collection of Users"""

    def __init__(self, data: dict):
        if data is None:
            raise ValueError("data is required")
        self.data = data

    @property
    def name(self) -> str:
        return self.data.get("Name", "N/A")

    @property
    def members_count(self) -> int:
        return self.data.get("Members@odata.count", 0)

    @property
    def members(self) -> List[str]:
        if "Members" in self.data:
            return [member.get("@odata.id", "") for member in self.data["Members"]]
        return []

    @property
    def odata_id(self) -> str:
        return self.data.get("@odata.id", "N/A")

    @property
    def odata_type(self) -> str:
        return self.data.get("@odata.type", "N/A")


class RoleCollection:
    """Class defining a collection of Roles"""

    def __init__(self, data: dict):
        if data is None:
            raise ValueError("data is required")
        self.data = data

    @property
    def name(self) -> str:
        return self.data.get("Name", "N/A")

    @property
    def members_count(self) -> int:
        return self.data.get("Members@odata.count", 0)

    @property
    def members(self) -> List[str]:
        if "Members" in self.data:
            return [member.get("@odata.id", "") for member in self.data["Members"]]
        return []

    @property
    def odata_id(self) -> str:
        return self.data.get("@odata.id", "N/A")

    @property
    def odata_type(self) -> str:
        return self.data.get("@odata.type", "N/A")
