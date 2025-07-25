"""Tests for role commands"""

from unittest.mock import patch, MagicMock
import pytest
from hprsctool.comm.remote_system_controller import RedfishError
from hprsctool.models.role import Role
from hprsctool.commands.role import (
    list_roles,
    get_role,
    create_role,
    delete_role,
    list_privileges
)

@pytest.fixture
def mock_rsc():
    return MagicMock()

@pytest.fixture
def mock_args(mock_rsc):
    args = MagicMock()
    args.rsc = mock_rsc
    return args

@patch('hprsctool.commands.role.role_ops.get_roles')
def test_list_roles(mock_get_roles, mock_args, capsys):
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


@patch('hprsctool.commands.role.role_ops.get_role_privileges')
def test_get_role(mock_get_role_privileges, mock_args, capsys):
    mock_args.role_id = "Administrator"
    role = Role({
        "RoleId": "Administrator",
        "Name": "Administrator Role",
        "Description": "Administrator privileges",
        "IsPredefined": True,
        "AssignedPrivileges": [
            "Login",
            "ConfigureManager",
            "ConfigureUsers",
            "ConfigureSelf",
            "ConfigureComponents",
            "AdministrateSystems",
            "OperateSystems"
        ],
        "OemPrivileges": [
            "KVM",
            "ConfigureRSM",
            "ClearAuditLogs",
            "VirtualMedia"
        ]
    })
    mock_get_role_privileges.return_value = role
    
    get_role(mock_args)
    
    captured = capsys.readouterr()
    assert "Role Information for 'Administrator':" in captured.out
    assert "Name: Administrator Role" in captured.out
    assert "RoleId: Administrator" in captured.out
    assert "IsPredefined: True" in captured.out
    assert "Assigned Privileges:" in captured.out
    assert "Login" in captured.out
    assert "ConfigureManager" in captured.out
    assert "OEM Privileges:" in captured.out
    assert "KVM" in captured.out
    assert "ConfigureRSM" in captured.out
    mock_get_role_privileges.assert_called_once_with(mock_args.rsc, "Administrator")


@patch('hprsctool.commands.role.role_ops.get_role_privileges')
def test_get_role_no_role_id(mock_get_role_privileges, mock_args, capsys):
    mock_args.role_id = None
    
    get_role(mock_args)
    
    captured = capsys.readouterr()
    assert "Error: Role ID is required" in captured.out
    mock_get_role_privileges.assert_not_called()


@patch('hprsctool.commands.role.role_ops.get_role_privileges')
def test_get_role_with_error(mock_get_role_privileges, mock_args, capsys):
    mock_args.role_id = "InvalidRole"
    mock_get_role_privileges.side_effect = RedfishError("Role not found")
    
    get_role(mock_args)
    
    captured = capsys.readouterr()
    assert "Error getting role: Role not found" in captured.out


@patch('hprsctool.commands.role.role_ops.create_role')
def test_create_role(mock_create_role, mock_args, capsys):
    mock_args.role_id = "ReadOnlyWithKVM"
    mock_args.assigned_privileges = ["Login", "ConfigureSelf"]
    mock_args.oem_privileges = ["KVM"]
    
    create_role(mock_args)
    
    captured = capsys.readouterr()
    assert "Role 'ReadOnlyWithKVM' created successfully" in captured.out
    mock_create_role.assert_called_once_with(
        mock_args.rsc, 
        "ReadOnlyWithKVM", 
        ["Login", "ConfigureSelf"], 
        ["KVM"]
    )


@patch('hprsctool.commands.role.role_ops.create_role')
def test_create_role_missing_role_id(mock_create_role, mock_args, capsys):
    mock_args.role_id = None
    mock_args.assigned_privileges = ["Login"]
    mock_args.oem_privileges = ["KVM"]
    
    create_role(mock_args)
    
    captured = capsys.readouterr()
    assert "Error: Role ID is required" in captured.out
    mock_create_role.assert_not_called()


@patch('hprsctool.commands.role.role_ops.create_role')
def test_create_role_missing_assigned_privileges(mock_create_role, mock_args, capsys):
    mock_args.role_id = "TestRole"
    mock_args.assigned_privileges = None
    mock_args.oem_privileges = ["KVM"]
    
    create_role(mock_args)
    
    captured = capsys.readouterr()
    assert "Error: Assigned privileges are required" in captured.out
    mock_create_role.assert_not_called()


@patch('hprsctool.commands.role.role_ops.create_role')
def test_create_role_missing_oem_privileges(mock_create_role, mock_args, capsys):
    mock_args.role_id = "TestRole"
    mock_args.assigned_privileges = ["Login"]
    mock_args.oem_privileges = None
    
    create_role(mock_args)
    
    captured = capsys.readouterr()
    assert "Error: OEM privileges are required" in captured.out
    mock_create_role.assert_not_called()


@patch('hprsctool.commands.role.role_ops.create_role')
def test_create_role_with_error(mock_create_role, mock_args, capsys):
    mock_args.role_id = "TestRole"
    mock_args.assigned_privileges = ["Login"]
    mock_args.oem_privileges = ["KVM"]
    mock_create_role.side_effect = RedfishError("Role already exists")
    
    create_role(mock_args)
    
    captured = capsys.readouterr()
    assert "Error creating role: Role already exists" in captured.out


@patch('hprsctool.commands.role.role_ops.delete_role')
def test_delete_role(mock_delete_role, mock_args, capsys):
    mock_args.role_id = "TestRole"
    
    delete_role(mock_args)
    
    captured = capsys.readouterr()
    assert "Role 'TestRole' deleted successfully" in captured.out
    mock_delete_role.assert_called_once_with(mock_args.rsc, "TestRole")


@patch('hprsctool.commands.role.role_ops.delete_role')
def test_delete_role_missing_role_id(mock_delete_role, mock_args, capsys):
    mock_args.role_id = None
    
    delete_role(mock_args)
    
    captured = capsys.readouterr()
    assert "Error: Role ID is required" in captured.out
    mock_delete_role.assert_not_called()


@patch('hprsctool.commands.role.role_ops.delete_role')
def test_delete_role_with_error(mock_delete_role, mock_args, capsys):
    mock_args.role_id = "TestRole"
    mock_delete_role.side_effect = RedfishError("Role not found")
    
    delete_role(mock_args)
    
    captured = capsys.readouterr()
    assert "Error deleting role: Role not found" in captured.out


@patch('hprsctool.commands.role.role_ops.get_role_privileges')
def test_list_privileges(mock_get_role_privileges, mock_args, capsys):
    role = Role({
        "RoleId": "Administrator",
        "Name": "Administrator Role",
        "Description": "Administrator privileges",
        "AssignedPrivileges": [
            "Login",
            "ConfigureManager",
            "ConfigureUsers",
            "ConfigureSelf",
            "ConfigureComponents",
            "AdministrateSystems",
            "OperateSystems"
        ],
        "OemPrivileges": [
            "KVM",
            "ConfigureRSM",
            "ClearAuditLogs",
            "VirtualMedia"
        ]
    })
    mock_get_role_privileges.return_value = role

    list_privileges(mock_args)

    captured = capsys.readouterr()
    assert "Privileges:" in captured.out
    assert "Assigned Privileges:" in captured.out
    assert "Login" in captured.out
    assert "ConfigureManager" in captured.out
    assert "OEM Privileges:" in captured.out
    assert "KVM" in captured.out
    assert "ConfigureRSM" in captured.out
    mock_get_role_privileges.assert_called_once_with(mock_args.rsc, "Administrator")


@patch('hprsctool.commands.role.role_ops.get_role_privileges')
def test_list_privileges_with_error(mock_get_role_privileges, mock_args, capsys):
    mock_get_role_privileges.side_effect = RedfishError("Privileges not found")
    
    list_privileges(mock_args)

    captured = capsys.readouterr()
    assert "Error getting privileges: Privileges not found" in captured.out
