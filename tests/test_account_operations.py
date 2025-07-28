"""Tests for account (user) operations"""

from unittest.mock import MagicMock
import pytest
from hprsctool.comm.remote_system_controller import RedfishError
from hprsctool.models.account import User
from hprsctool.comm.operations.account import (
    create_account,
    change_account_role,
    change_account_password,
    get_account,
    delete_account,
    get_accounts
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

def test_change_account_role_success(mock_rsc):
    # Mock role validation - get available roles
    mock_rsc.perform_redfish_get.side_effect = [
        MagicMock(dict={
            "Members": [
                {"@odata.id": "/redfish/v1/AccountService/Roles/Administrator"},
                {"@odata.id": "/redfish/v1/AccountService/Roles/ReadOnly"}
            ]
        }),
        MagicMock(dict={"RoleId": "Administrator"}),
        MagicMock(dict={"RoleId": "ReadOnly"}),
        # Mock get_account response after role change
        MagicMock(dict={
            "Id": "testuser",
            "UserName": "testuser",
            "RoleId": "Administrator"
        })
    ]

    result = change_account_role(mock_rsc, "testuser", "Administrator")

    assert isinstance(result, User)
    assert result.role_id == "Administrator"
    mock_rsc.perform_redfish_patch.assert_called_once_with(
        "/redfish/v1/AccountService/Accounts/testuser",
        {"RoleId": "Administrator"}
    )

def test_change_account_role_invalid_role(mock_rsc):
    # Mock role validation - get available roles
    mock_rsc.perform_redfish_get.side_effect = [
        MagicMock(dict={
            "Members": [
                {"@odata.id": "/redfish/v1/AccountService/Roles/ReadOnly"}
            ]
        }),
        MagicMock(dict={"RoleId": "ReadOnly"})
    ]

    with pytest.raises(RedfishError) as exc_info:
        change_account_role(mock_rsc, "testuser", "InvalidRole")
    assert "Role 'InvalidRole' not found" in str(exc_info.value)
    assert "ReadOnly" in str(exc_info.value)

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

def test_get_accounts_success(mock_rsc):
    # Mock UserCollection with two members
    user_collection_response = MagicMock()
    user_collection_response.dict = {
        "Members": [
            {"@odata.id": "/redfish/v1/AccountService/Accounts/user1"},
            {"@odata.id": "/redfish/v1/AccountService/Accounts/user2"}
        ]
    }
    user1_response = MagicMock()
    user1_response.dict = {
        "Id": "user1",
        "UserName": "user1",
        "RoleId": "ReadOnly"
    }
    user2_response = MagicMock()
    user2_response.dict = {
        "Id": "user2",
        "UserName": "user2",
        "RoleId": "Administrator"
    }
    mock_rsc.perform_redfish_get.side_effect = [user_collection_response, user1_response, user2_response]
    users = get_accounts(mock_rsc)
    assert len(users) == 2
    assert users[0].user_id == "user1"
    assert users[1].user_id == "user2"


def test_get_accounts_empty(mock_rsc):
    user_collection_response = MagicMock()
    user_collection_response.dict = {"Members": []}
    mock_rsc.perform_redfish_get.return_value = user_collection_response
    users = get_accounts(mock_rsc)
    assert users == []


def test_get_accounts_redfish_error(mock_rsc):
    mock_rsc.perform_redfish_get.side_effect = RedfishError("fail")
    with pytest.raises(RedfishError) as exc_info:
        get_accounts(mock_rsc)
    assert "fail" in str(exc_info.value)
