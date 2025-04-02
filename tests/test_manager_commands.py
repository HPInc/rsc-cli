"""Tests for manager commands"""

from unittest.mock import patch, MagicMock
import pytest
from hprsctool.commands.manager.manager import (
    print_manager,
    change_password,
    update_firmware,
    restart_manager,
    factory_reset_manager,
)


@pytest.fixture
def mock_rsc():
    return MagicMock()


@pytest.fixture
def mock_args():
    return MagicMock()


def test_print_manager(mock_args):
    mock_manager = MagicMock()
    mock_manager.model = "Model X"
    mock_manager.serial_number = "123456"
    mock_manager.firmware_version = "1.0.0"
    mock_manager.kvm_settings = None
    mock_manager.rsm_status = None
    mock_manager.date_time = "2025-02-28T12:00:00Z"
    mock_manager.date_time_offset = "+00:00"

    with patch(
        "hprsctool.commands.manager.manager.manager_ops.get_manager",
        return_value=mock_manager,
    ):
        print_manager(mock_args)


def test_change_password(mock_args, mock_rsc):
    mock_args.rsc = mock_rsc
    mock_args.new_password = "new_password"

    with patch(
        "hprsctool.commands.manager.manager.manager_ops.change_admin_password"
    ) as mock_change_password, patch(
        "hprsctool.commands.manager.manager.Rsc"
    ) as mock_rsc_class, patch(
        "hprsctool.commands.manager.manager.manager_ops.get_manager"
    ):
        mock_rsc_class.return_value = mock_rsc
        change_password(mock_args)
        mock_change_password.assert_called_once_with(mock_rsc, "new_password")


def test_update_firmware(mock_args, mock_rsc):
    mock_args.rsc = mock_rsc
    mock_args.fw_file_path = "path/to/firmware"

    with patch(
        "hprsctool.commands.manager.manager.manager_ops.update_rsc_firmware"
    ) as mock_update_firmware:
        update_firmware(mock_args)
        mock_update_firmware.assert_called_once_with(mock_rsc, "path/to/firmware")


def test_restart_manager(mock_args, mock_rsc):
    mock_args.rsc = mock_rsc

    with patch(
        "hprsctool.commands.manager.manager.manager_ops.restart"
    ) as mock_restart:
        restart_manager(mock_args)
        mock_restart.assert_called_once_with(mock_rsc)


def test_factory_reset_manager(mock_args, mock_rsc):
    mock_args.rsc = mock_rsc

    with patch(
        "hprsctool.commands.manager.manager.manager_ops.factory_reset"
    ) as mock_factory_reset:
        factory_reset_manager(mock_args)
        mock_factory_reset.assert_called_once_with(mock_rsc)
