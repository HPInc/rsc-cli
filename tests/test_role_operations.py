"""Tests for role operations"""

from unittest.mock import MagicMock
import pytest
from hprsctool.models.role import Role
from hprsctool.comm.operations.role import get_roles, get_role_ids

@pytest.fixture
def mock_rsc():
    return MagicMock()

def test_get_roles(mock_rsc):
    roles_response = MagicMock()
    roles_response.dict = {
        "Members": [
            {"@odata.id": "/redfish/v1/AccountService/Roles/Administrator"},
            {"@odata.id": "/redfish/v1/AccountService/Roles/Operator"},
            {"@odata.id": "/redfish/v1/AccountService/Roles/ReadOnly"}
        ]
    }
    admin_response = MagicMock()
    admin_response.dict = {
        "RoleId": "Administrator",
        "Name": "Administrator Role",
        "Description": "Administrator privileges"
    }
    operator_response = MagicMock()
    operator_response.dict = {
        "RoleId": "Operator",
        "Name": "Operator Role",
        "Description": "Operator privileges"
    }
    readonly_response = MagicMock()
    readonly_response.dict = {
        "RoleId": "ReadOnly",
        "Name": "ReadOnly Role",
        "Description": "ReadOnly privileges"
    }
    mock_rsc.perform_redfish_get.side_effect = [
        roles_response,
        admin_response,
        operator_response,
        readonly_response
    ]
    roles = get_roles(mock_rsc)
    assert len(roles) == 3
    assert roles[0].role_id == "Administrator"
    assert roles[1].role_id == "Operator"
    assert roles[2].role_id == "ReadOnly"

def test_get_role_ids(mock_rsc):
    roles_response = MagicMock()
    roles_response.dict = {
        "Members": [
            {"@odata.id": "/redfish/v1/AccountService/Roles/Administrator"},
            {"@odata.id": "/redfish/v1/AccountService/Roles/ReadOnly"}
        ]
    }
    admin_response = MagicMock()
    admin_response.dict = {"RoleId": "Administrator"}
    readonly_response = MagicMock()
    readonly_response.dict = {"RoleId": "ReadOnly"}
    mock_rsc.perform_redfish_get.side_effect = [
        roles_response,
        admin_response,
        readonly_response
    ]
    role_ids = get_role_ids(mock_rsc)
    assert role_ids == ["Administrator", "ReadOnly"]
    assert mock_rsc.perform_redfish_get.call_count == 3
