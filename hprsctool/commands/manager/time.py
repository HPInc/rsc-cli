"""RSC time settings"""

import argparse

from ...comm.remote_system_controller import Rsc
from ...comm.operations import (
    manager as manager_ops,
    network as network_ops,
)


def get_parameters(parser: argparse.ArgumentParser) -> None:
    """Get the parameters for the time command"""
    subparsers = parser.add_subparsers(help="Time commands")
    subparsers.required = True
    set_time_parser = subparsers.add_parser("set", help="Set the RSC time settings")
    set_time_parser.add_argument(
        "--time",
        help=(
            "Time in the format YYYY-MM-DDTHH:MM:SS+HH:MM, or YYYY-MM-DDTHH:MM:SSZ."
            " Example: 2024-06-07T12:29:01-03:00"
        ),
        action="store",
    )
    set_time_parser.add_argument(
        "--offset",
        help=("Time offset in format '[+-]HH:MM'. "
              "Please use '--offset=<value> if offset contains a minus sign"),
        action="store",
        type=str,
    )
    set_time_parser.add_argument(
        "--ntp",
        help="Enable or disable NTP",
        action="store",
        choices=["enable", "disable"],
    )
    set_time_parser.add_argument(
        "--ntpserver",
        help="NTP server to add. Can be specified multiple times.",
        action="append",
    )
    set_time_parser.set_defaults(func=set_time)

    get_time_parser = subparsers.add_parser("get", help="Get the RSC time settings")
    get_time_parser.set_defaults(func=get_time)


def set_time(args: argparse.Namespace):
    """Set the RSC time settings"""
    rsc: Rsc = args.rsc
    manager_net_protocol = network_ops.get_manager_network_protocol(rsc)
    time_settings = {}
    net_protocol_settings = {}

    ntp_is_or_will_be_enabled = manager_net_protocol.ntp.ntp_protocol_enabled

    if args.ntp is not None:
        ntp_is_or_will_be_enabled = args.ntp == "enable"
        net_protocol_settings = {"NTP": {"ProtocolEnabled": ntp_is_or_will_be_enabled}}
    if args.ntpserver is not None:
        net_protocol_settings.setdefault("NTP", {})
        net_protocol_settings["NTP"]["NTPServers"] = []
        for server in args.ntpserver:
            net_protocol_settings["NTP"]["NTPServers"].append(server)

    if args.time is not None or args.offset is not None:
        if ntp_is_or_will_be_enabled:
            raise ValueError("Can't manually set time when NTP is or will be enabled")
        if args.time is not None:
            time_settings["DateTime"] = args.time
        if args.offset is not None:
            time_settings["DateTimeLocalOffset"] = args.offset

    if net_protocol_settings:
        network_ops.set_manager_network_protocol(rsc, net_protocol_settings)
    if time_settings:
        manager_ops.update_manager(rsc, time_settings)

    print("Time settings updated")


def get_time(args: argparse.Namespace):
    """Get the RSC time settings"""
    rsc: Rsc = args.rsc
    mgr = manager_ops.get_manager(rsc)
    manager_net_protocol = network_ops.get_manager_network_protocol(rsc)

    print(f"Time: {mgr.date_time}")
    print(f"Offset: {mgr.date_time_offset}")
    print("NTP settings:")
    print(f"  NTP enabled: {manager_net_protocol.ntp.ntp_protocol_enabled}")
    print("  NTP servers:")
    for server in manager_net_protocol.ntp.ntp_servers:
        print(f"    {server}")
