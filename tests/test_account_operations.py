"""Tests for account (user) operations"""

from unittest.mock import MagicMock
import pytest
from hprsctool.comm.remote_system_controller import RedfishError
from hprsctool.models.account import User
from hprsctool.comm.operations.account import (
    create_account,
    change_account_password,
    get_account,
    delete_account
)

@pytest.fixture
def mock_rsc():
    return MagicMock()

def test_create_account_success(mock_rsc):
    mock_rsc.perform_redfish_get.side_effect = [
        MagicMock(dict={
            "Members": [
                {"@odata.id": "/redfish/v1/AccountService/Roles/ReadOnly"}
            ]
        }),
        MagicMock(dict={"RoleId": "ReadOnly"})
    ]
    create_response = MagicMock()
    create_response.dict = {
        "Id": "testuser",
        "UserName": "testuser",
        "RoleId": "ReadOnly",
        "Enabled": True,
        "AccountTypes": ["Redfish"]
    }
    mock_rsc.perform_redfish_post.return_value = create_response
    result = create_account(mock_rsc, "testuser", "password123", "ReadOnly")
    assert isinstance(result, User)
    assert result.user_id == "testuser"
    assert result.username == "testuser"
    assert result.role_id == "ReadOnly"

def test_create_account_invalid_role(mock_rsc):
    mock_rsc.perform_redfish_get.side_effect = [
        MagicMock(dict={
            "Members": [
                {"@odata.id": "/redfish/v1/AccountService/Roles/ReadOnly"}
            ]
        }),
        MagicMock(dict={"RoleId": "ReadOnly"})
    ]
    with pytest.raises(RedfishError) as exc_info:
        create_account(mock_rsc, "testuser", "password123", "InvalidRole")
    assert "Role 'InvalidRole' not found" in str(exc_info.value)
    assert "ReadOnly" in str(exc_info.value)

def test_change_account_password(mock_rsc):
    patch_response = MagicMock()
    patch_response.dict = {
        "Id": "testuser",
        "UserName": "testuser",
        "RoleId": "ReadOnly"
    }
    mock_rsc.perform_redfish_patch.return_value = patch_response
    get_response = MagicMock()
    get_response.dict = {
        "Id": "testuser",
        "UserName": "testuser",
        "RoleId": "ReadOnly"
    }
    mock_rsc.perform_redfish_get.return_value = get_response
    result = change_account_password(mock_rsc, "testuser", "newpassword")
    assert isinstance(result, User)
    assert result.user_id == "testuser"
    mock_rsc.perform_redfish_patch.assert_called_once_with(
        "/redfish/v1/AccountService/Accounts/testuser",
        {"Password": "newpassword"}
    )
    mock_rsc.perform_redfish_get.assert_called_once_with(
        "/redfish/v1/AccountService/Accounts/testuser"
    )

def test_get_account(mock_rsc):
    user_response = MagicMock()
    user_response.dict = {
        "Id": "testuser",
        "UserName": "testuser",
        "RoleId": "ReadOnly",
        "Enabled": True
    }
    mock_rsc.perform_redfish_get.return_value = user_response
    result = get_account(mock_rsc, "testuser")
    assert isinstance(result, User)
    assert result.user_id == "testuser"
    mock_rsc.perform_redfish_get.assert_called_once_with(
        "/redfish/v1/AccountService/Accounts/testuser"
    )

def test_delete_account_success(mock_rsc):
    delete_response = MagicMock()
    delete_response.dict = None
    mock_rsc.perform_redfish_delete.return_value = delete_response
    delete_account(mock_rsc, "testuser")
    mock_rsc.perform_redfish_delete.assert_called_once_with(
        "/redfish/v1/AccountService/Accounts/testuser"
    )

def test_delete_account_error(mock_rsc):
    mock_rsc.perform_redfish_delete.side_effect = RedfishError("Account not found")
    with pytest.raises(RedfishError) as exc_info:
        delete_account(mock_rsc, "testuser")
    assert "Account not found" in str(exc_info.value)
    mock_rsc.perform_redfish_delete.assert_called_once_with(
        "/redfish/v1/AccountService/Accounts/testuser"
    )
