"""Tests for role commands"""

from unittest.mock import patch, MagicMock
import pytest
from hprsctool.comm.remote_system_controller import RedfishError
from hprsctool.models.role import Role
from hprsctool.commands.role import list_roles

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
