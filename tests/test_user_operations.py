"""Tests for user operations"""

from unittest.mock import MagicMock
import pytest
from hprsctool.comm.remote_system_controller import RedfishError
from hprsctool.models.user import Role, User
from hprsctool.comm.operations.user import(
    get_roles,
    get_role_ids,
    create_user,
    change_user_password,
    get_user,
    get_users,
    delete_user
)


@pytest.fixture
def mock_rsc():
    return MagicMock()


def test_get_roles(mock_rsc):
    """Test getting roles"""
    # Mock the roles collection response
    roles_response = MagicMock()
    roles_response.dict = {
        "Members": [
            {"@odata.id": "/redfish/v1/AccountService/Roles/Administrator"},
            {"@odata.id": "/redfish/v1/AccountService/Roles/Operator"},
            {"@odata.id": "/redfish/v1/AccountService/Roles/ReadOnly"}
        ]
    }
    
    # Mock individual role responses
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
    
    # Configure the mock RSC to return appropriate responses
    mock_rsc.perform_redfish_get.side_effect = [
        roles_response,
        admin_response,
        operator_response,
        readonly_response
    ]
    
    roles = get_roles(mock_rsc)
    
    assert len(roles) == 3
def test_get_role_ids(mock_rsc):
    """Test getting role IDs"""
    # Mock the roles collection response
    roles_response = MagicMock()
    roles_response.dict = {
        "Members": [
            {"@odata.id": "/redfish/v1/AccountService/Roles/Administrator"},
            {"@odata.id": "/redfish/v1/AccountService/Roles/ReadOnly"}
        ]
    }
    
    # Mock individual role responses
    admin_response = MagicMock()
    admin_response.dict = {"RoleId": "Administrator"}
    
    readonly_response = MagicMock()
    readonly_response.dict = {"RoleId": "ReadOnly"}
    
    # Configure the mock RSC to return appropriate responses
    mock_rsc.perform_redfish_get.side_effect = [
        roles_response,
        admin_response,
        readonly_response
    ]
    
    role_ids = get_role_ids(mock_rsc)
    
    assert role_ids == ["Administrator", "ReadOnly"]
    assert mock_rsc.perform_redfish_get.call_count == 3


def test_create_user_success(mock_rsc):
    """Test successful user creation"""
    # Mock get_role_ids to return available roles
    mock_rsc.perform_redfish_get.side_effect = [
        # Mock roles collection response
        MagicMock(dict={
            "Members": [
                {"@odata.id": "/redfish/v1/AccountService/Roles/ReadOnly"}
            ]
        }),
        # Mock individual role response
        MagicMock(dict={"RoleId": "ReadOnly"})
    ]
    
    # Mock create user response
    create_response = MagicMock()
    create_response.dict = {
        "Id": "testuser",
        "UserName": "testuser",
        "RoleId": "ReadOnly",
        "Enabled": True,
        "AccountTypes": ["Redfish"]
    }
    mock_rsc.perform_redfish_post.return_value = create_response
    
    result = create_user(mock_rsc, "testuser", "password123", "ReadOnly")
    
    assert isinstance(result, User)
    assert result.user_id == "testuser"
    assert result.username == "testuser"
    assert result.role_id == "ReadOnly"


def test_create_user_invalid_role(mock_rsc):
    """Test user creation with invalid role"""
    # Mock get_role_ids to return available roles
    mock_rsc.perform_redfish_get.side_effect = [
        # Mock roles collection response
        MagicMock(dict={
            "Members": [
                {"@odata.id": "/redfish/v1/AccountService/Roles/ReadOnly"}
            ]
        }),
        # Mock individual role response
        MagicMock(dict={"RoleId": "ReadOnly"})
    ]
    
    with pytest.raises(RedfishError) as exc_info:
        create_user(mock_rsc, "testuser", "password123", "InvalidRole")
    
    assert "Role 'InvalidRole' not found" in str(exc_info.value)
    assert "ReadOnly" in str(exc_info.value)


def test_change_user_password(mock_rsc):
    """Test changing user password with full response"""
    patch_response = MagicMock()
    patch_response.dict = {
        "Id": "testuser",
        "UserName": "testuser",
        "RoleId": "ReadOnly"
    }
    mock_rsc.perform_redfish_patch.return_value = patch_response
    
    # Mock the GET request that get_user makes
    get_response = MagicMock()
    get_response.dict = {
        "Id": "testuser",
        "UserName": "testuser",
        "RoleId": "ReadOnly"
    }
    mock_rsc.perform_redfish_get.return_value = get_response
    
    result = change_user_password(mock_rsc, "testuser", "newpassword")
    
    assert isinstance(result, User)
    assert result.user_id == "testuser"
    mock_rsc.perform_redfish_patch.assert_called_once_with(
        "/redfish/v1/AccountService/Accounts/testuser",
        {"Password": "newpassword"}
    )
    # Should also call GET to fetch updated user info
    mock_rsc.perform_redfish_get.assert_called_once_with(
        "/redfish/v1/AccountService/Accounts/testuser"
    )


def test_change_user_password_empty_response(mock_rsc):
    """Test changing user password with empty response (success case)"""
    # Mock empty response from PATCH operation
    patch_response = MagicMock()
    patch_response.dict = None  # Empty response
    mock_rsc.perform_redfish_patch.return_value = patch_response
    
    # Mock GET response to fetch updated user info
    get_response = MagicMock()
    get_response.dict = {
        "Id": "testuser",
        "UserName": "testuser", 
        "RoleId": "ReadOnly"
    }
    mock_rsc.perform_redfish_get.return_value = get_response
    
    result = change_user_password(mock_rsc, "testuser", "newpassword")
    
    assert isinstance(result, User)
    assert result.user_id == "testuser"
    mock_rsc.perform_redfish_patch.assert_called_once_with(
        "/redfish/v1/AccountService/Accounts/testuser",
        {"Password": "newpassword"}
    )
    # Should also call GET to fetch updated user info
    mock_rsc.perform_redfish_get.assert_called_once_with(
        "/redfish/v1/AccountService/Accounts/testuser"
    )


def test_get_user(mock_rsc):
    """Test getting a specific user"""
    user_response = MagicMock()
    user_response.dict = {
        "Id": "testuser",
        "UserName": "testuser",
        "RoleId": "ReadOnly",
        "Enabled": True
    }
    mock_rsc.perform_redfish_get.return_value = user_response
    
    result = get_user(mock_rsc, "testuser")
    
    assert isinstance(result, User)
    assert result.user_id == "testuser"
    mock_rsc.perform_redfish_get.assert_called_once_with(
        "/redfish/v1/AccountService/Accounts/testuser"
    )


def test_get_users(mock_rsc):
    """Test getting all users"""
    # Mock users collection response
    users_response = MagicMock()
    users_response.dict = {
        "Members": [
            {"@odata.id": "/redfish/v1/AccountService/Accounts/admin"},
            {"@odata.id": "/redfish/v1/AccountService/Accounts/testuser"}
        ]
    }
    
    # Mock individual user responses
    admin_response = MagicMock()
    admin_response.dict = {
        "Id": "admin",
        "UserName": "admin",
        "RoleId": "Administrator"
    }
    
    user_response = MagicMock()
    user_response.dict = {
        "Id": "testuser",
        "UserName": "testuser",
        "RoleId": "ReadOnly"
    }
    
    mock_rsc.perform_redfish_get.side_effect = [
        users_response,
        admin_response,
        user_response
    ]
    
    results = get_users(mock_rsc)
    
    assert len(results) == 2
    assert all(isinstance(user, User) for user in results)
    assert results[0].user_id == "admin"
    assert results[1].user_id == "testuser"
    assert mock_rsc.perform_redfish_get.call_count == 3


def test_delete_user_success(mock_rsc):
    """Test successful user deletion"""
    # Mock the DELETE response (should be empty/None for success)
    delete_response = MagicMock()
    delete_response.dict = None  # Empty response indicates success
    mock_rsc.perform_redfish_delete.return_value = delete_response
    
    # Should not raise any exception
    delete_user(mock_rsc, "testuser")
    
    mock_rsc.perform_redfish_delete.assert_called_once_with(
        "/redfish/v1/AccountService/Accounts/testuser"
    )


def test_delete_user_error(mock_rsc):
    """Test user deletion with error"""
    # Mock a RedfishError being raised
    mock_rsc.perform_redfish_delete.side_effect = RedfishError("Account not found")
    
    with pytest.raises(RedfishError) as exc_info:
        delete_user(mock_rsc, "testuser")
    
    assert "Account not found" in str(exc_info.value)
    mock_rsc.perform_redfish_delete.assert_called_once_with(
        "/redfish/v1/AccountService/Accounts/testuser"
    )
