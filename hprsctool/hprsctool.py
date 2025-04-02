"""Main module for hprsctool"""

import argparse
import sys

from .commands.manager import manager
from .commands import system
from .commands import task
from .comm import remote_system_controller

VERSION = "0.11.0"


def main():
    """Manager standalone command"""

    # Create a separate argument parser for the --version argument
    version_parser = argparse.ArgumentParser(add_help=False)
    add_version_argument(version_parser)

    # Parse the --version argument separately
    args, remaining_args = version_parser.parse_known_args()
    if args.version:
        print("hprsctool", VERSION)
        sys.exit(0)

    argparser = argparse.ArgumentParser(
        description="HP RSC tool",
        prog="hprsctool",
        epilog="For help on a specific command, use hprsctool <command> -h",
    )
    argparser.add_argument(
        "-u", "--username", help="Username for the RSC", required=True
    )
    argparser.add_argument(
        "-p", "--password", help="Password for the RSC", required=True
    )
    argparser.add_argument("-a", "--address", help="Address of the RSC", required=True)

    # Include version in the main argument parser so it shows up in the help text
    add_version_argument(argparser)

    top_level_subparsers = argparser.add_subparsers()
    subparser = top_level_subparsers.add_parser("manager", help="Manager commands")
    manager_subparsers = subparser.add_subparsers()

    manager.get_parameters(manager_subparsers)

    subparser = top_level_subparsers.add_parser("system", help="System commands")
    system_subparsers = subparser.add_subparsers()
    system.get_parameters(system_subparsers)

    subparser = top_level_subparsers.add_parser("tasks", help="Task commands")
    task_subparsers = subparser.add_subparsers()
    task.get_parameters(task_subparsers)

    args = argparser.parse_args(remaining_args)
    config = remote_system_controller.RedfishConfig(
        f"https://{args.address}", args.username, args.password
    )

    if "func" not in args:
        print("-- No action specified.")
        argparser.print_help()
        sys.exit(1)

    try:
        thersc = remote_system_controller.Rsc(config)
        thersc.login()
        args.rsc = thersc
        args.func(args)
    except ValueError as e:
        print(f"Invalid parameters: {e}")
        sys.exit(1)
    except remote_system_controller.RedfishError as e:
        print(e)
        sys.exit(1)

def add_version_argument(parser):
    """Add a --version argument to an argument parser"""
    parser.add_argument(
        "--version",
        help="Print the program version and exit.",
        required=False,
        action="store_true",
    )

if __name__ == "__main__":
    main()
