"""Commands for role management."""

import argparse
from hprsctool.comm.remote_system_controller import RedfishError, Rsc
from ..comm.operations import role as role_ops
from ..comm import redfish_messages

def get_parameters(subparsers: argparse._SubParsersAction) -> None:
    """Get the parameters for the role command"""
    subparsers.required = True

    # List roles command
    list_roles_parser = subparsers.add_parser("list", help="List all available roles")
    list_roles_parser.set_defaults(func=list_roles)


def list_roles(args):
    """List all available roles"""
    try:
        roles = role_ops.get_roles(args.rsc)
        print("Available roles:")
        for role in roles:
            print(f"  - {role.role_id}")
            if role.description != "N/A":
                print(f"    Description: {role.description}")
    except RedfishError as e:
        error_msg = str(e)
        print(f"Error listing roles: {error_msg}")
