"""Tests for the manager network commands."""

from unittest.mock import patch, MagicMock
import pytest
from hprsctool.models import ethernet_interface
from hprsctool.commands.manager.network import (
    get_parameters,
    print_network_settings,
    set_network_settings,
    update_proxy_settings,
    update_dhcp,
    update_static_addresses,
    update_use_dns_servers,
    update_static_name_servers,
    update_mdns_settings,
)


@pytest.fixture(name="mock_rsc")
def fixture_mock_rsc():
    return MagicMock()


@pytest.fixture(name="mock_args")
def fixture_mock_args():
    return MagicMock()


def test_get_parameters():
    parser = MagicMock()
    get_parameters(parser)
    parser.add_subparsers.assert_called_once_with(help="Network commands")


def test_print_network_settings(mock_args, mock_rsc):
    mock_args.rsc = mock_rsc
    mock_network_settings = MagicMock()
    mock_network_settings.hostname = "test-host"
    mock_network_settings.mac_address = "00:11:22:33:44:55"
    mock_network_settings.dhcp = True
    mock_network_settings.ips = [
        MagicMock(
            address="192.168.1.100",
            subnet_mask="255.255.255.0",
            gateway="192.168.1.1",
            origin="DHCP",
        )
    ]
    mock_network_settings.name_servers = ["8.8.8.8", "8.8.4.4"]

    mock_manager_network_protocol = MagicMock()
    mock_manager_network_protocol.proxy.proxy_enabled = True
    mock_manager_network_protocol.proxy.proxy_server_uri = "http://proxy.example.com"
    mock_manager_network_protocol.proxy.exclude_addresses = ["localhost", "127.0.0.1"]

    with patch(
        "hprsctool.commands.manager.network.network_ops.get_manager_ethernet_interface",
        return_value=mock_network_settings,
    ), patch(
        "hprsctool.commands.manager.network.network_ops.get_manager_network_protocol",
        return_value=mock_manager_network_protocol,
    ):
        print_network_settings(mock_args)


def test_set_network_settings_dhcp_enable(mock_args, mock_rsc):
    mock_args.rsc = mock_rsc
    mock_args.dhcp = "enable"
    mock_args.static_address = None
    mock_args.subnet_mask = None
    mock_args.gateway = None
    mock_args.name_server = ["8.8.8.8", "8.8.4.4"]
    mock_args.use_dhcp_dns = "disable"
    mock_args.proxy = "enable"
    mock_args.proxyserver = "http://proxy.example.com"
    mock_args.proxyexclude = ["localhost", "127.0.0.1"]

    mock_network_settings = MagicMock()
    mock_network_settings.dhcp = True

    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.dict = {}

    with patch(
        "hprsctool.commands.manager.network.network_ops.get_manager_ethernet_interface",
        return_value=mock_network_settings,
    ), patch(
        "hprsctool.commands.manager.network.network_ops.set_manager_ethernet_interface",
        return_value=MagicMock()
    ) as mock_set_ethernet, patch(
        "hprsctool.commands.manager.network.network_ops.set_manager_network_protocol",
        return_value=MagicMock()
    ) as mock_set_protocol, patch.object(mock_args.rsc, "monitor_task", return_value=mock_response):
        set_network_settings(mock_args)
        mock_set_ethernet.assert_called_once()
        assert mock_set_protocol.call_count == 2


def test_set_network_settings_dhcp_disable(mock_args, mock_rsc):
    mock_args.rsc = mock_rsc
    mock_args.dhcp = "disable"
    mock_args.static_address = "1.1.1.1"
    mock_args.subnet_mask = "255.255.255.0"
    mock_args.gateway = "1.1.1.2"
    mock_args.name_server = ["8.8.8.8", "8.8.4.4"]
    mock_args.use_dhcp_dns = None
    mock_args.proxy = "enable"
    mock_args.proxyserver = "http://proxy.example.com"
    mock_args.proxyexclude = ["localhost", "127.0.0.1"]

    mock_network_settings = MagicMock()
    mock_network_settings.dhcp = True

    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.dict = {}

    with patch(
        "hprsctool.commands.manager.network.network_ops.get_manager_ethernet_interface",
        return_value=mock_network_settings,
    ), patch(
        "hprsctool.commands.manager.network.network_ops.set_manager_ethernet_interface",
        return_value=MagicMock()
    ) as mock_set_ethernet, patch(
        "hprsctool.commands.manager.network.network_ops.set_manager_network_protocol",
        return_value=MagicMock()
    ) as mock_set_protocol, patch.object(mock_args.rsc, "monitor_task", return_value=mock_response):
        set_network_settings(mock_args)
        mock_set_ethernet.assert_called_once()
        assert mock_set_protocol.call_count == 2


def test_cannot_use_static_address_when_dhcp_is_enabled(mock_args, mock_rsc):
    mock_args.rsc = mock_rsc
    mock_args.dhcp = "enable"
    mock_args.static_address = "1.1.1.1"
    mock_args.subnet_mask = "255.255.255.0"
    mock_args.gateway = ".1.1.1.2"

    mock_network_settings = MagicMock()
    mock_network_settings.dhcp = True

    with patch(
        "hprsctool.commands.manager.network.network_ops.get_manager_ethernet_interface",
        return_value=mock_network_settings,
    ):
        with pytest.raises(ValueError):
            set_network_settings(mock_args)


def test_cannot_set_use_dns_when_dhcp_is_disabled(mock_args, mock_rsc):
    mock_args.rsc = mock_rsc
    mock_args.dhcp = "disable"
    mock_args.use_dhcp_dns = "enable"

    mock_network_settings = MagicMock()
    mock_network_settings.dhcp = False

    with patch(
        "hprsctool.commands.manager.network.network_ops.get_manager_ethernet_interface",
        return_value=mock_network_settings,
    ):
        with pytest.raises(ValueError):
            set_network_settings(mock_args)


def test_update_proxy_settings(mock_args):
    mock_args.proxy = "enable"
    mock_args.proxyserver = "http://proxy.example.com"
    mock_args.proxyexclude = ["localhost", "127.0.0.1"]

    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.dict = {}

    mock_rsc = MagicMock()
    mock_args.rsc = mock_rsc
    mock_rsc.monitor_task.return_value = mock_response

    with patch(
        "hprsctool.commands.manager.network.network_ops.set_manager_network_protocol"
    ) as mock_set_protocol:
        update_proxy_settings(mock_args)
        mock_set_protocol.assert_called_once()


def test_update_dhcp(mock_args):
    mock_args.dhcp = "disable"
    mock_args.static_address = "192.168.1.100"
    mock_args.subnet_mask = "255.255.255.0"
    mock_network_settings = MagicMock()
    mock_network_settings.dhcp = True
    new_settings_body = {}

    dhcp_is_or_will_be_enabled = update_dhcp(
        mock_args, mock_network_settings, new_settings_body
    )
    assert not dhcp_is_or_will_be_enabled


def test_update_static_addresses(mock_args):
    mock_args.static_address = "192.168.1.100"
    mock_args.subnet_mask = "255.255.255.0"
    mock_args.gateway = "192.168.1.1"
    new_settings_body = {}

    update_static_addresses(mock_args, new_settings_body, False)
    assert ethernet_interface.STATIC_IPV4_ADDRESSES_KEY in new_settings_body


def test_update_use_dns_servers(mock_args):
    mock_args.use_dhcp_dns = "enable"
    mock_args.dhcp = "enable"
    new_settings_body = {}
    dhcp_is_or_will_be_enabled = True

    update_use_dns_servers(mock_args, new_settings_body, dhcp_is_or_will_be_enabled)
    assert ethernet_interface.DHCPV4_KEY in new_settings_body


def test_update_static_name_servers(mock_args):
    mock_args.name_server = ["8.8.8.8", "8.8.4.4"]
    new_settings_body = {}

    update_static_name_servers(mock_args, new_settings_body)
    assert ethernet_interface.STATIC_NAME_SERVERS_KEY in new_settings_body


def test_update_mdns_settings_enable(mock_args):
    mock_args.mdns = "enable"

    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.dict = {}

    mock_rsc = MagicMock()
    mock_args.rsc = mock_rsc
    mock_rsc.monitor_task.return_value = mock_response

    with patch(
        "hprsctool.commands.manager.network.network_ops.set_manager_network_protocol"
    ) as mock_set_protocol:
        update_mdns_settings(mock_args)
        mock_set_protocol.assert_called_once_with(
            mock_args.rsc, {
                "Oem": {
                    "HP": {
                        "mDNSDiscoveryProtocol": {"ProtocolEnabled": True}
                    }
                }
            }
        )


def test_update_mdns_settings_disable(mock_args):
    mock_args.mdns = "disable"

    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.dict = {}

    mock_rsc = MagicMock()
    mock_args.rsc = mock_rsc
    mock_rsc.monitor_task.return_value = mock_response
    
    with patch(
        "hprsctool.commands.manager.network.network_ops.set_manager_network_protocol"
    ) as mock_set_protocol:
        update_mdns_settings(mock_args)
        mock_set_protocol.assert_called_once_with(
            mock_args.rsc, {
                "Oem": {
                    "HP": {
                        "mDNSDiscoveryProtocol": {"ProtocolEnabled": False}
                    }
                }
            }
        )


def test_update_mdns_settings_not_specified(mock_args):
    mock_args.mdns = None
    mock_args.rsc = MagicMock()
    with patch(
        "hprsctool.commands.manager.network.network_ops.set_manager_network_protocol"
    ) as mock_set_protocol:
        update_mdns_settings(mock_args)
        mock_set_protocol.assert_not_called()
