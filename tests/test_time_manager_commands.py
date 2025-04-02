"""Tests for the manager time commands."""

from unittest.mock import MagicMock, patch
import pytest
from hprsctool.commands.manager.time import get_parameters, set_time


@pytest.fixture(name="mock_parser")
def fixture_mock_parser():
    return MagicMock()


def test_get_parameters(mock_parser):
    get_parameters(mock_parser)
    mock_parser.add_subparsers.assert_called_once_with(help="Time commands")
    assert mock_parser.add_subparsers().required is True

    set_time_parser = mock_parser.add_subparsers().add_parser(
        "set", help="Set the RSC time settings"
    )
    set_time_parser.add_argument.assert_any_call(
        "--time",
        help=(
            "Time in the format YYYY-MM-DDTHH:MM:SS+HH:MM, or YYYY-MM-DDTHH:MM:SSZ."
            " Example: 2024-06-07T12:29:01-03:00"
        ),
        action="store",
    )
    set_time_parser.add_argument.assert_any_call(
        "--offset", help="Time offset in format [+-]HH:MM", action="store"
    )
    set_time_parser.add_argument.assert_any_call(
        "--ntp",
        help="Enable or disable NTP",
        action="store",
        choices=["enable", "disable"],
    )
    set_time_parser.add_argument.assert_any_call(
        "--ntpserver",
        help="NTP server to add. Can be specified multiple times.",
        action="append",
    )
    set_time_parser.set_defaults.assert_called_with(
        func=set_time_parser.set_defaults.call_args[1]["func"]
    )

    get_time_parser = mock_parser.add_subparsers().add_parser(
        "get", help="Get the RSC time settings"
    )
    get_time_parser.set_defaults.assert_called_with(
        func=get_time_parser.set_defaults.call_args[1]["func"]
    )


@pytest.fixture(name="mock_rsc")
def fixture_mock_rsc():
    return MagicMock()


@pytest.fixture(name="mock_args")
def fixture_mock_args():
    return MagicMock()


def test_set_time_ntp_enable(mock_args, mock_rsc):
    mock_args.rsc = mock_rsc
    mock_args.ntp = "enable"
    mock_args.ntpserver = ["ntp1.example.com", "ntp2.example.com"]
    mock_args.time = None
    mock_args.offset = None

    with patch(
        "hprsctool.commands.manager.network.network_ops.get_manager_network_protocol"
    ) as mock_get_protocol, patch(
        "hprsctool.commands.manager.network.network_ops.set_manager_network_protocol"
    ) as mock_set_protocol:
        mock_protocol = MagicMock()
        mock_protocol.ntp.ntp_protocol_enabled = False
        mock_get_protocol.return_value = mock_protocol

        set_time(mock_args)

        mock_set_protocol.assert_called_once_with(
            mock_rsc,
            {
                "NTP": {
                    "ProtocolEnabled": True,
                    "NTPServers": ["ntp1.example.com", "ntp2.example.com"],
                }
            },
        )


def test_set_time_ntp_disable(mock_args, mock_rsc):
    mock_args.rsc = mock_rsc
    mock_args.ntp = "disable"
    mock_args.ntpserver = None
    mock_args.time = None
    mock_args.offset = None

    with patch(
        "hprsctool.commands.manager.network.network_ops.get_manager_network_protocol"
    ) as mock_get_protocol, patch(
        "hprsctool.commands.manager.network.network_ops.set_manager_network_protocol"
    ) as mock_set_protocol:
        mock_protocol = MagicMock()
        mock_protocol.ntp.ntp_protocol_enabled = True
        mock_get_protocol.return_value = mock_protocol

        set_time(mock_args)

        mock_set_protocol.assert_called_once_with(
            mock_rsc,
            {"NTP": {"ProtocolEnabled": False}},
        )


def test_set_time_manual_time_ntp_disabled(mock_args, mock_rsc):
    mock_args.rsc = mock_rsc
    mock_args.ntp = "disable"
    mock_args.ntpserver = None
    mock_args.time = "2024-06-07T12:29:01-03:00"
    mock_args.offset = "+03:00"

    with patch(
        "hprsctool.commands.manager.network.network_ops.get_manager_network_protocol"
    ) as mock_get_protocol, patch(
        "hprsctool.commands.manager.network.network_ops.set_manager_network_protocol"
    ), patch(
        "hprsctool.comm.operations.manager.update_manager"
    ) as mock_update_manager:
        mock_protocol = MagicMock()
        mock_protocol.ntp.ntp_protocol_enabled = False
        mock_get_protocol.return_value = mock_protocol

        set_time(mock_args)

        mock_update_manager.assert_called_once_with(
            mock_rsc,
            {
                "DateTime": "2024-06-07T12:29:01-03:00",
                "DateTimeOffset": "+03:00",
            },
        )


def test_set_time_manual_time_ntp_enabled_raises_error(mock_args, mock_rsc):
    mock_args.rsc = mock_rsc
    mock_args.ntp = "enable"
    mock_args.ntpserver = None
    mock_args.time = "2024-06-07T12:29:01-03:00"
    mock_args.offset = "+03:00"

    with patch(
        "hprsctool.commands.manager.network.network_ops.get_manager_network_protocol"
    ) as mock_get_protocol:
        mock_protocol = MagicMock()
        mock_protocol.ntp.ntp_protocol_enabled = True
        mock_get_protocol.return_value = mock_protocol

        with pytest.raises(
            ValueError, match="Can't manually set time when NTP is or will be enabled"
        ):
            set_time(mock_args)
