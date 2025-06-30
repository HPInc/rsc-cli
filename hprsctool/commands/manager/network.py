"""network related commands"""

import argparse

from hprsctool.comm import redfish_messages

from ...models import ethernet_interface
from ...comm.remote_system_controller import RedfishError, Rsc
from ...comm.operations import network as network_ops


def get_parameters(parser: argparse.ArgumentParser) -> None:
    subparsers = parser.add_subparsers(help="Network commands")
    subparsers.required = True
    get_parser = subparsers.add_parser("get", help="Get the Ethernet settings")
    get_parser.set_defaults(func=print_network_settings)

    set_network_parser = subparsers.add_parser(
        "set", help="Change the Ethernet settings"
    )
    set_network_parser.add_argument(
        "--static_address", help="Static IP address", action="store"
    )
    set_network_parser.add_argument(
        "--gateway", help="Static gateway setting", action="store"
    )
    set_network_parser.add_argument(
        "--subnet_mask", help="static IP subnet mask", action="store"
    )
    set_network_parser.add_argument(
        "--name_server",
        help="Static DNS server. May be specified more than once",
        action="append",
    )
    set_network_parser.add_argument(
        "--dhcp",
        help="Enable or disable DHCP",
        choices=["enable", "disable"],
        action="store",
        required=False,
    )
    set_network_parser.add_argument(
        "--use-dhcp-dns",
        help="Use DHCP DNS servers",
        choices=["enable", "disable"],
        action="store",
        required=False,
    )
    set_network_parser.add_argument(
        "--proxyserver", help="Proxy server", action="store", required=False
    )
    set_network_parser.add_argument(
        "--proxy",
        help="Enable or disable proxy",
        choices=["enable", "disable"],
        action="store",
        required=False,
    )
    set_network_parser.add_argument(
        "--proxyexclude",
        help="Proxy exclude address. May be specified more than once",
        action="append",
        required=False,
    )
    set_network_parser.add_argument(
        "--mdns",
        help="Enable or disable mDNS discovery protocol (default: enable)",
        choices=["enable", "disable"],
        action="store",
        required=False,
    )
    set_network_parser.set_defaults(func=set_network_settings)


def print_network_settings(args: argparse.Namespace):
    rsc: Rsc = args.rsc
    current_network_settings = network_ops.get_manager_ethernet_interface(rsc)
    print(f"Hostname: {current_network_settings.hostname}")
    print(f"MAC address: {current_network_settings.mac_address}")

    print(f"DHCP enabled: {current_network_settings.dhcp}")
    print("IP addresses:")
    for ip in current_network_settings.ips:
        print(f"  Address: {ip.address}")
        print(f"  Subnet mask: {ip.subnet_mask}")
        print(f"  Gateway: {ip.gateway}")
        print(f"  Origin: {ip.origin}")

    print("\nName servers:")
    for ns in current_network_settings.name_servers:
        print(f"  {ns}")

    manager_network_protocol = network_ops.get_manager_network_protocol(rsc)
    print("\nmDNS Discovery Protocol:")
    print(f"  Enabled: {manager_network_protocol.mdns_protocol_enabled}")
    print("\nProxy settings:")
    print(f"  Enabled: {manager_network_protocol.proxy.proxy_enabled}")
    print(f"  Proxy server URI: {manager_network_protocol.proxy.proxy_server_uri}")
    print("  Exclude addresses:")
    for exclude in manager_network_protocol.proxy.exclude_addresses:
        print(f"    {exclude}")


def set_network_settings(args: argparse.Namespace):
    rsc: Rsc = args.rsc
    current_network_settings = network_ops.get_manager_ethernet_interface(rsc)
    new_settings_body = {}

    dhcp_is_or_will_be_enabled = update_dhcp(
        args, current_network_settings, new_settings_body
    )
    update_static_addresses(args, new_settings_body, dhcp_is_or_will_be_enabled)
    update_use_dns_servers(args, new_settings_body, dhcp_is_or_will_be_enabled)

    response = rsc.monitor_task(network_ops.set_manager_ethernet_interface(rsc, new_settings_body))
    if response.status < 200 or response.status >= 300:
        raise RedfishError(
            f"Failed to update network settings: "
            f"{redfish_messages.get_error_message(response.dict)}")
    
    update_mdns_settings(args)
    update_proxy_settings(args)

    print("Network settings updated")


def update_proxy_settings(args: argparse.Namespace) -> None:
    """Updates the proxy settings based on the provided arguments."""

    rsc: Rsc = args.rsc

    manager_network_protocol = {}
    if args.proxy is not None:
        manager_network_protocol.setdefault("Proxy", {})
        manager_network_protocol["Proxy"]["Enabled"] = args.proxy == "enable"
        if (manager_network_protocol["Proxy"]["Enabled"] and
            args.proxyserver is None):
            raise ValueError("Cannot enable proxy without specifying a proxy server")

    if args.proxyserver is not None:
        manager_network_protocol.setdefault("Proxy", {})
        manager_network_protocol["Proxy"]["ProxyServerURI"] = args.proxyserver
    if args.proxyexclude is not None:
        manager_network_protocol.setdefault("Proxy", {})
        manager_network_protocol["Proxy"]["ExcludeAddresses"] = args.proxyexclude

    if manager_network_protocol:
        response = rsc.monitor_task(
            network_ops.set_manager_network_protocol(rsc, manager_network_protocol))
        if response.status < 200 or response.status >= 300:
            raise RedfishError(
                f"Failed to update proxy settings: "
                f"{redfish_messages.get_error_message(response.dict)}")

def update_mdns_settings(args: argparse.Namespace) -> None:
    """Updates the mDNS discovery protocol setting based on the provided arguments."""
    if not hasattr(args, "mdns") or args.mdns is None:
        return  # Do not change mDNS if not specified
    
    rsc: Rsc = args.rsc
    mdns_enabled = args.mdns == "enable"
    manager_network_protocol = {}
    manager_network_protocol.setdefault("Oem", {})
    manager_network_protocol["Oem"].setdefault("HP", {})
    manager_network_protocol["Oem"]["HP"]["mDNSDiscoveryProtocol"] = {"ProtocolEnabled": mdns_enabled}
    response = rsc.monitor_task(
        network_ops.set_manager_network_protocol(rsc, manager_network_protocol))
    if response.status < 200 or response.status >= 300:
        raise RedfishError(
            f"Failed to update mDNS settings: "
            f"{redfish_messages.get_error_message(response.dict)}")

def update_dhcp(
    args: argparse.Namespace,
    current_network_settings: ethernet_interface.EthernetInterface,
    new_settings_body: dict,
) -> bool:
    """Validates configuration for DHCP and updates the new settings body.
    Returns True if DHCP is or will be enabled."""

    if args.dhcp is not None:
        new_settings_body.update(
            {
                ethernet_interface.DHCPV4_KEY: {
                    ethernet_interface.DHCP_ENABLED_KEY: args.dhcp == "enable"
                }
            }
        )

        if args.dhcp == "disable" and current_network_settings.dhcp:
            if not args.static_address or not args.subnet_mask:
                raise ValueError("Cannot disable DHCP without setting a static address")

    dhcp_is_or_will_be_enabled = False
    if ethernet_interface.DHCPV4_KEY in new_settings_body:
        dhcp_is_or_will_be_enabled = new_settings_body[ethernet_interface.DHCPV4_KEY][
            ethernet_interface.DHCP_ENABLED_KEY
        ]
    else:
        dhcp_is_or_will_be_enabled = current_network_settings.dhcp

    return dhcp_is_or_will_be_enabled


def update_static_addresses(
    args: argparse.Namespace, new_settings_body: dict, dhcp_is_or_will_be_enabled: bool
) -> None:
    """Validates configuration for static addresses and updates the new settings body
    accordingly."""

    if args.static_address is not None:
        if dhcp_is_or_will_be_enabled:
            raise ValueError("Cannot set a static address when DHCP is enabled")

        if not args.subnet_mask:
            raise ValueError("Static address requires a subnet mask")

        new_settings_body[ethernet_interface.STATIC_IPV4_ADDRESSES_KEY] = [
            {
                ethernet_interface.ADDRESS_KEY: args.static_address,
                ethernet_interface.SUBNET_MASK_KEY: args.subnet_mask,
            }
        ]

        if "gateway" in args:
            new_settings_body[ethernet_interface.STATIC_IPV4_ADDRESSES_KEY][0][
                ethernet_interface.GATEWAY_KEY
            ] = args.gateway


def update_use_dns_servers(
    args: argparse.Namespace, new_settings_body: dict, dhcp_is_or_will_be_enabled: bool
) -> None:
    """Validates configuration for using DHCP DNS servers and updates the new settings
    body accordingly."""

    if args.use_dhcp_dns is not None:
        if dhcp_is_or_will_be_enabled:
            if ethernet_interface.DHCPV4_KEY not in new_settings_body:
                new_settings_body[ethernet_interface.DHCPV4_KEY] = {}
            new_settings_body[ethernet_interface.DHCPV4_KEY][
                ethernet_interface.USE_DNS_SERVERS_KEY
            ] = args.use_dhcp_dns == "enable"
        else:
            raise ValueError("Cannot use DHCP DNS servers when DHCP is disabled")

def update_static_name_servers(args: argparse.Namespace, new_settings_body: dict) -> None:
    """Validates configuration for static name servers and updates the new settings body
    accordingly."""

    if args.name_server is not None:
        new_settings_body[ethernet_interface.STATIC_NAME_SERVERS_KEY] = []
        for ns in args.name_server:
            new_settings_body[ethernet_interface.STATIC_NAME_SERVERS_KEY].append(ns)
