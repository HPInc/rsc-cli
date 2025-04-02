"""Commands for system management."""

import argparse

from hprsctool.comm.remote_system_controller import RedfishError, Rsc

from ..comm.operations import system as system_ops
from ..comm import redfish_messages


def get_parameters(subparsers: argparse._SubParsersAction) -> None:
    """Get the parameters for the system command"""
    subparsers.required = True
    get_subparser = subparsers.add_parser("get", help="Get the system information")
    get_subparser.set_defaults(func=print_system)
    power_subparser = subparsers.add_parser("power", help="Power commands")
    power_subparser.add_argument(
        "state",
        help="Power state",
        choices=[
            "On",
            "GracefulShutdown",
            "ForceOff",
            "GracefulRestart",
            "ForceRestart",
        ],
        action="store",
    )
    power_subparser.set_defaults(func=power_system)


def print_system(args):
    """Print the system information"""
    system = system_ops.get_system(args.rsc)

    print("Model:", system.model)
    print("Serial number:", system.serial_number)
    print("Power state:", system.power_state)
    print("Indicator LED:", system.indicator_led)
    print("Boot source override:", system.boot_source_override_target)
    print("Health:", system.health)
    if system.main_board_adapter_state is not None:
        print("Main board adapter state:", system.main_board_adapter_state)
    if system.boot_state is not None:
        print("Boot state:", system.boot_state)
    if system.processor_summary is not None:
        print("Processor summary:")
        print(f"  Model: {system.processor_summary.model}")
        print(f"  Core count: {system.processor_summary.core_count}")
        print(f"  Count: {system.processor_summary.count}")
    if system.memory_summary is not None:
        print("Memory summary:")
        print(
            f"  Total system memory GiB: {system.memory_summary.total_system_memory_gib}"
        )
    if system.blink_code_state is not None:
        print("Blink code state:")
        print(f"  Type: {system.blink_code_state.type}")
        print(f"  Major: {system.blink_code_state.major}")
        print(f"  Minor: {system.blink_code_state.minor}")
        print(
            f"  Message: {redfish_messages.get_redfish_message(
                args.rsc.config.base_url,
                system.blink_code_state.message_id, [])}"
        )


def power_system(args):
    """Power the system on or off"""
    print("Sending power command and monitoring response...", flush=True)
    rsc: Rsc = args.rsc
    response = rsc.monitor_task(system_ops.set_system_power(rsc, args.state))
    if response.status < 200 or response.status >= 300:
        error_msg = redfish_messages.get_error_message(response.dict)
        error_msg = error_msg if error_msg else "No error message"
        raise RedfishError(f"Power command '{args.state}' failed: {error_msg}")
    print(f"Power command '{args.state}' succeeded.")
