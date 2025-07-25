"""Tests for account (user) commands"""

from unittest.mock import patch, MagicMock, call
import pytest
from hprsctool.comm.remote_system_controller import RedfishError
from hprsctool.models.account import User
from hprsctool.commands.account import (
    get_parameters,
    list_accounts,
    create_account,
    change_password,
    get_account,
    delete_account
)

@pytest.fixture
def mock_rsc():
    return MagicMock()

@pytest.fixture
def mock_args(mock_rsc):
    args = MagicMock()
    args.rsc = mock_rsc
    args.new_username = "testuser"
    args.new_password = "testpass"
    args.role_id = "ReadOnly"
    args.account_id = "testuser"
    return args

@patch('hprsctool.commands.account.account_ops.create_account')
def test_create_account_success(mock_create_account, mock_args, capsys):
    user = User({
        "Id": "testuser",
        "UserName": "testuser",
        "RoleId": "ReadOnly",
        "Enabled": True,
        "AccountTypes": ["Redfish"]
    })
    mock_create_account.return_value = user
    create_account(mock_args)
    captured = capsys.readouterr()
    assert "User created successfully:" in captured.out
    assert "ID: testuser" in captured.out

@patch('hprsctool.commands.account.account_ops.create_account')
def test_create_account_error(mock_create_account, mock_args, capsys):
    mock_create_account.side_effect = RedfishError("Role 'Invalid' not found")
    create_account(mock_args)
    captured = capsys.readouterr()
    assert "Error creating account:" in captured.out

@patch('hprsctool.commands.account.account_ops.change_account_password')
def test_change_password_success(mock_change_password, mock_args, capsys):
    user = User({
        "Id": "testuser",
        "UserName": "testuser",
        "RoleId": "ReadOnly"
    })
    mock_change_password.return_value = user
    change_password(mock_args)
    captured = capsys.readouterr()
    assert "Password changed successfully for account: testuser" in captured.out

@patch('hprsctool.commands.account.account_ops.change_account_password')
def test_change_password_error(mock_change_password, mock_args, capsys):
    mock_change_password.side_effect = RedfishError("Account not found")
    change_password(mock_args)
    captured = capsys.readouterr()
    assert "Error changing password:" in captured.out

@patch('hprsctool.commands.account.account_ops.get_accounts')
def test_list_accounts(mock_get_accounts, mock_args, capsys):
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
    mock_get_accounts.return_value = users
    list_accounts(mock_args)
    captured = capsys.readouterr()
    assert "User accounts:" in captured.out
    assert "admin" in captured.out
    assert "testuser" in captured.out

@patch('hprsctool.commands.account.account_ops.get_account')
def test_get_account_success(mock_get_account, mock_args, capsys):
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
    mock_get_account.return_value = user
    get_account(mock_args)
    captured = capsys.readouterr()
    assert "User account details:" in captured.out
    assert "ID: testuser" in captured.out
    assert "Username: testuser" in captured.out

def test_create_account_missing_params(mock_rsc, capsys):
    args = MagicMock()
    args.rsc = mock_rsc
    args.new_username = ""
    args.new_password = "pass"
    args.role_id = "ReadOnly"
    create_account(args)
    captured = capsys.readouterr()
    assert "Error: Username is required" in captured.out

def test_change_password_missing_params(mock_rsc, capsys):
    args = MagicMock()
    args.rsc = mock_rsc
    args.account_id = ""
    args.new_password = "newpass"
    change_password(args)
    captured = capsys.readouterr()
    assert "Error: Account ID is required" in captured.out

@patch('hprsctool.commands.account.account_ops.delete_account')
def test_delete_account_success(mock_delete_account, mock_args, capsys):
    mock_delete_account.return_value = None
    delete_account(mock_args)
    captured = capsys.readouterr()
    assert "User account deleted successfully: testuser" in captured.out
    mock_delete_account.assert_called_once_with(mock_args.rsc, "testuser")

@patch('hprsctool.commands.account.account_ops.delete_account')
def test_delete_account_error(mock_delete_account, mock_args, capsys):
    mock_delete_account.side_effect = RedfishError("Account not found")
    delete_account(mock_args)
    captured = capsys.readouterr()
    assert "Error deleting account: Account not found" in captured.out

def test_delete_account_missing_params(mock_rsc, capsys):
    args = MagicMock()
    args.rsc = mock_rsc
    args.account_id = ""
    delete_account(args)
    captured = capsys.readouterr()
    assert "Error: Account ID is required" in captured.out

@patch('argparse._SubParsersAction')
def test_get_parameters_creates_subparsers(mock_subparsers):
    mock_action = MagicMock()
    mock_subparsers.return_value = mock_action
    get_parameters(mock_action)
    assert mock_action.required is True
    expected = [
        'list', 'get', 'create', 'change-password', 'delete'
    ]
    added = [call[0][0] for call in mock_action.add_parser.call_args_list]
    for cmd in expected:
        assert cmd in added

@patch('argparse._SubParsersAction')
def test_get_parameters_sets_defaults(mock_subparsers):
    mock_action = MagicMock()
    parser_map = {}
    def add_parser_side_effect(name, **kwargs):
        parser = MagicMock()
        parser_map[name] = parser
        return parser
    mock_action.add_parser.side_effect = add_parser_side_effect
    mock_subparsers.return_value = mock_action
    get_parameters(mock_action)
    for cmd in ['list', 'get', 'create', 'change-password', 'delete']:
        assert parser_map[cmd].set_defaults.called

@patch('hprsctool.commands.account.account_ops.get_accounts', return_value=[])
def test_list_accounts_no_users(mock_get_accounts, mock_args, capsys):
    list_accounts(mock_args)
    captured = capsys.readouterr()
    assert "No user accounts found." in captured.out

@patch('hprsctool.commands.account.account_ops.get_accounts', side_effect=RedfishError("fail"))
def test_list_accounts_redfish_error(mock_get_accounts, mock_args, capsys):
    list_accounts(mock_args)
    captured = capsys.readouterr()
    assert "Error listing accounts: fail" in captured.out

@patch('hprsctool.commands.account.account_ops.get_account')
def test_get_account_missing_id(mock_get_account, mock_args, capsys):
    mock_args.account_id = ""
    get_account(mock_args)
    captured = capsys.readouterr()
    assert "Error: Account ID is required" in captured.out
    mock_get_account.assert_not_called()

@patch('hprsctool.commands.account.account_ops.get_account', side_effect=RedfishError("fail"))
def test_get_account_redfish_error(mock_get_account, mock_args, capsys):
    get_account(mock_args)
    captured = capsys.readouterr()
    assert "Error getting account: fail" in captured.out

@patch('hprsctool.commands.account.account_ops.create_account')
def test_create_account_missing_username(mock_create_account, mock_args, capsys):
    mock_args.new_username = ""
    create_account(mock_args)
    captured = capsys.readouterr()
    assert "Error: Username is required" in captured.out
    mock_create_account.assert_not_called()

@patch('hprsctool.commands.account.account_ops.create_account')
def test_create_account_missing_password(mock_create_account, mock_args, capsys):
    mock_args.new_password = ""
    create_account(mock_args)
    captured = capsys.readouterr()
    assert "Error: Password is required" in captured.out
    mock_create_account.assert_not_called()

@patch('hprsctool.commands.account.account_ops.create_account')
def test_create_account_missing_role_id(mock_create_account, mock_args, capsys):
    mock_args.role_id = ""
    create_account(mock_args)
    captured = capsys.readouterr()
    assert "Error: Role ID is required" in captured.out
    mock_create_account.assert_not_called()

@patch('hprsctool.commands.account.account_ops.create_account', side_effect=RedfishError("fail"))
def test_create_account_redfish_error(mock_create_account, mock_args, capsys):
    create_account(mock_args)
    captured = capsys.readouterr()
    assert "Error creating account: fail" in captured.out

@patch('hprsctool.commands.account.account_ops.change_account_password')
def test_change_password_missing_account_id(mock_change_password, mock_args, capsys):
    mock_args.account_id = ""
    change_password(mock_args)
    captured = capsys.readouterr()
    assert "Error: Account ID is required" in captured.out
    mock_change_password.assert_not_called()

@patch('hprsctool.commands.account.account_ops.change_account_password')
def test_change_password_missing_new_password(mock_change_password, mock_args, capsys):
    mock_args.new_password = ""
    change_password(mock_args)
    captured = capsys.readouterr()
    assert "Error: New password is required" in captured.out
    mock_change_password.assert_not_called()

@patch('hprsctool.commands.account.account_ops.change_account_password', side_effect=RedfishError("fail"))
def test_change_password_redfish_error(mock_change_password, mock_args, capsys):
    change_password(mock_args)
    captured = capsys.readouterr()
    assert "Error changing password: fail" in captured.out
