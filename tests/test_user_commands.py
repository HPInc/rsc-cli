"""Tests for user commands"""

from unittest.mock import patch, MagicMock
import pytest
from hprsctool.comm.remote_system_controller import RedfishError
from hprsctool.models.user import Role, User
from hprsctool.commands.user import (
    list_roles,
    create_user,
    change_password,
    list_users,
    get_user,
    delete_user
)


@pytest.fixture
def mock_rsc():
    return MagicMock()


@pytest.fixture
def mock_args():
    args = MagicMock()
    args.username = "testuser"
    args.password = "testpass"
    args.role_id = "ReadOnly"
    args.account_id = "testuser"
    args.new_password = "newpass"
    return args


@patch('hprsctool.commands.user.user_ops.get_roles')
def test_list_roles(mock_get_roles, mock_args, mock_rsc, capsys):
    """Test listing roles"""
    mock_args.rsc = mock_rsc
    # Create mock Role objects
    roles = [
        Role({"RoleId": "Administrator", "Description": "Admin role"}),
        Role({"RoleId": "Operator", "Description": "Operator role"}),
        Role({"RoleId": "ReadOnly", "Description": "Read-only role"})
    ]
    mock_get_roles.return_value = roles
    
    list_roles(mock_args)
    
    captured = capsys.readouterr()
    assert "Available roles:" in captured.out
    assert "Administrator" in captured.out
    assert "Operator" in captured.out
    assert "ReadOnly" in captured.out


@patch('hprsctool.commands.user.user_ops.create_user')
def test_create_user_success(mock_create_user, mock_args, mock_rsc, capsys):
    """Test successful user creation"""
    mock_args.rsc = mock_rsc
    # Create mock User object
    user = User({
        "Id": "testuser",
        "UserName": "testuser", 
        "RoleId": "ReadOnly",
        "Enabled": True,
        "AccountTypes": ["Redfish"]
    })
    mock_create_user.return_value = user
    
    create_user(mock_args)
    
    captured = capsys.readouterr()
    assert "User created successfully:" in captured.out
    assert "ID: testuser" in captured.out


@patch('hprsctool.commands.user.user_ops.create_user')
def test_create_user_error(mock_create_user, mock_args, mock_rsc, capsys):
    """Test user creation with error"""
    mock_args.rsc = mock_rsc
    mock_create_user.side_effect = RedfishError("Role 'Invalid' not found")
    
    create_user(mock_args)
    
    captured = capsys.readouterr()
    assert "Error creating user:" in captured.out


@patch('hprsctool.commands.user.user_ops.change_user_password')
def test_change_password_success(mock_change_password, mock_args, mock_rsc, capsys):
    """Test successful password change"""
    mock_args.rsc = mock_rsc
    # Create mock User object
    user = User({
        "Id": "testuser",
        "UserName": "testuser", 
        "RoleId": "ReadOnly"
    })
    mock_change_password.return_value = user
    
    change_password(mock_args)
    
    captured = capsys.readouterr()
    assert "Password changed successfully for account: testuser" in captured.out


@patch('hprsctool.commands.user.user_ops.change_user_password')
def test_change_password_error(mock_change_password, mock_args, mock_rsc, capsys):
    """Test password change with error"""
    mock_args.rsc = mock_rsc
    mock_change_password.side_effect = RedfishError("Account not found")
    
    change_password(mock_args)
    
    captured = capsys.readouterr()
    assert "Error changing password:" in captured.out


@patch('hprsctool.commands.user.user_ops.get_users')
def test_list_users(mock_get_users, mock_args, mock_rsc, capsys):
    """Test listing users"""
    mock_args.rsc = mock_rsc
    # Create mock User objects
    users = [
        User({
            "Id": "admin",
            "UserName": "admin", 
            "RoleId": "Administrator",
            "Enabled": True,
            "Locked": False,
            "AccountTypes": ["Redfish"]
        }),
        User({
            "Id": "testuser",
            "UserName": "testuser", 
            "RoleId": "ReadOnly",
            "Enabled": True,
            "Locked": False,
            "AccountTypes": ["Redfish"]
        })
    ]
    mock_get_users.return_value = users
    
    list_users(mock_args)
    
    captured = capsys.readouterr()
    assert "User accounts:" in captured.out
    assert "admin" in captured.out
    assert "testuser" in captured.out


@patch('hprsctool.commands.user.user_ops.get_user')
def test_get_user_success(mock_get_user, mock_args, mock_rsc, capsys):
    """Test getting a specific user"""
    mock_args.rsc = mock_rsc
    # Create mock User object
    user = User({
        "Id": "testuser",
        "UserName": "testuser", 
        "Name": "Test User",
        "RoleId": "ReadOnly",
        "Enabled": True,
        "Locked": False,
        "PasswordChangeRequired": False,
        "AccountTypes": ["Redfish"],
        "@odata.id": "/redfish/v1/AccountService/Accounts/testuser",
        "@odata.type": "#ManagerAccount.v1_13_0.ManagerAccount"
    })
    mock_get_user.return_value = user
    
    get_user(mock_args)
    
    captured = capsys.readouterr()
    assert "User account details:" in captured.out
    assert "ID: testuser" in captured.out
    assert "Username: testuser" in captured.out


def test_create_user_missing_params(mock_rsc, capsys):
    """Test create user with missing parameters"""
    args = MagicMock()
    args.rsc = mock_rsc
    args.username = ""
    args.password = "pass"
    args.role_id = "ReadOnly"
    
    create_user(args)
    
    captured = capsys.readouterr()
    assert "Error: Username is required" in captured.out


def test_change_password_missing_params(mock_rsc, capsys):
    """Test change password with missing parameters"""
    args = MagicMock()
    args.rsc = mock_rsc
    args.account_id = ""
    args.new_password = "newpass"
    
    change_password(args)
    
    captured = capsys.readouterr()
    assert "Error: Account ID is required" in captured.out


@patch('hprsctool.commands.user.user_ops.delete_user')
def test_delete_user_success(mock_delete_user, mock_args, mock_rsc, capsys):
    """Test successful user deletion"""
    mock_args.rsc = mock_rsc
    # delete_user operation returns None on success
    mock_delete_user.return_value = None
    
    delete_user(mock_args)
    
    captured = capsys.readouterr()
    assert "User account deleted successfully: testuser" in captured.out
    mock_delete_user.assert_called_once_with(mock_rsc, "testuser")


@patch('hprsctool.commands.user.user_ops.delete_user')
def test_delete_user_error(mock_delete_user, mock_args, mock_rsc, capsys):
    """Test user deletion with error"""
    mock_args.rsc = mock_rsc
    mock_delete_user.side_effect = RedfishError("Account not found")
    
    delete_user(mock_args)
    
    captured = capsys.readouterr()
    assert "Error deleting user: Account not found" in captured.out


def test_delete_user_missing_params(mock_rsc, capsys):
    """Test delete user with missing parameters"""
    args = MagicMock()
    args.rsc = mock_rsc
    args.account_id = ""
    
    delete_user(args)
    
    captured = capsys.readouterr()
    assert "Error: Account ID is required" in captured.out
