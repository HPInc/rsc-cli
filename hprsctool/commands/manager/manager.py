"""Manager commands"""

import argparse

from ...comm.remote_system_controller import RedfishError, Rsc
from ...comm.operations import manager as manager_ops
from . import network, cert, trusted_cert, time


def get_parameters(subparsers: argparse._SubParsersAction) -> None:
    """Get the parameters for the manager command"""
    subparsers.required = True

    cert_parser = subparsers.add_parser("cert", help="RSC certificate management")
    cert.get_parameters(cert_parser)

    change_password_parser = subparsers.add_parser(
        "change_password", help="Change the RSC password"
    )
    change_password_parser.add_argument(
        "new_password", help="New password", action="store"
    )
    change_password_parser.set_defaults(func=change_password)

    get_subparser = subparsers.add_parser(
        "factory_reset", help="Factory-resets the RSC"
    )
    get_subparser.set_defaults(func=factory_reset_manager)

    get_subparser = subparsers.add_parser("get", help="Get the RSC information")
    get_subparser.set_defaults(func=print_manager)

    network_parser = subparsers.add_parser("network", help="RSC network settings")
    network.get_parameters(network_parser)

    get_subparser = subparsers.add_parser("restart", help="Restarts the RSC")
    get_subparser.set_defaults(func=restart_manager)

    time_parser = subparsers.add_parser("time", help="RSC time settings")
    time.get_parameters(time_parser)

    trusted_cert_parser = subparsers.add_parser(
        "trusted_cert", help="RSC trusted certificates management"
    )
    trusted_cert.get_parameters(trusted_cert_parser)

    update_parser = subparsers.add_parser("update", help="RSC firmware update")
    update_parser.add_argument("fw_file_path", help="Firmware file", action="store")
    update_parser.set_defaults(func=update_firmware)


def print_manager(args: argparse.Namespace):
    """Print the RSC information"""
    manager = manager_ops.get_manager(args.rsc)

    print(f"Model: {manager.model}")
    print(f"Serial number: {manager.serial_number}")
    print(f"Firmware version: {manager.firmware_version}")
    if manager.kvm_settings is not None:
        print("KVM settings:")
        print(
            f"  Disable video on KVM idle: {manager.kvm_settings.disable_video_on_kvm_idle}"
        )
        print(f"  Disable collaboration: {manager.kvm_settings.disable_collaboration}")
        print(
            "  Disable collaboration authorization: "
            f"{manager.kvm_settings.disable_collaboration_authorization}"
        )
        print(f"  Port range begin: {manager.kvm_settings.port_range_begin}")
        print(f"  Port range end: {manager.kvm_settings.port_range_end}")
    if manager.rsm_status is not None:
        print("RSM status:")
        print(f"  Binding status: {manager.rsm_status.binding_status}")
        print(f"  Organization: {manager.rsm_status.organization}")
    print(f"Date and time: {manager.date_time}")
    print(f"Date and time offset: {manager.date_time_offset}")


def change_password(args: argparse.Namespace):
    """Change the RSC password"""
    rsc: Rsc = args.rsc
    try:
        manager_ops.change_admin_password(rsc, args.new_password)
    except RedfishError as e:
        # Sometimes the password change will succeed, but
        # the session will be deleted before the response is received
        if "Failed to delete session" not in str(e):
            raise e

    # Verify if the password was changed by trying to login
    # with the new password
    config = rsc.config
    config.password = args.new_password

    try:
        rsc2 = Rsc(config)
        rsc2.login()
        manager_ops.get_manager(rsc2)
    except Exception as e:
        ex = Exception(f"Failed to login with the new password: {e}")
        raise ex from e
    print("Password changed")


def update_firmware(args: argparse.Namespace):
    """Update the RSC firmware"""
    manager_ops.update_rsc_firmware(args.rsc, args.fw_file_path)
    print("Firmware updated")


def restart_manager(args: argparse.Namespace):
    """Restart the RSC"""
    rsc: Rsc = args.rsc
    manager_ops.restart(rsc)
    print("RSC restarted")


def factory_reset_manager(args: argparse.Namespace):
    """Factory-reset the RSC"""
    rsc: Rsc = args.rsc
    manager_ops.factory_reset(rsc)
    print("RSC factory-reset")
