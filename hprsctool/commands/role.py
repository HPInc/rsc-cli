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

    # Get role command
    get_role_parser = subparsers.add_parser("get", help="Get detailed information for a role")
    get_role_parser.add_argument("role_id", help="Role ID to get information for")
    get_role_parser.set_defaults(func=get_role)

    # Create role command
    create_role_parser = subparsers.add_parser("create", help="Create a new role")
    create_role_parser.add_argument("role_id", help="Role ID for the new role")
    create_role_parser.add_argument("--assigned-privileges", nargs='+', required=True, 
                                   help="List of assigned privileges")
    create_role_parser.add_argument("--oem-privileges", nargs='+', required=True,
                                   help="List of OEM privileges")
    create_role_parser.set_defaults(func=create_role)

    # Update role command
    update_role_parser = subparsers.add_parser("update", help="Update role privileges")
    update_role_parser.add_argument("role_id", help="Role ID to update")
    update_role_parser.add_argument("--assigned-privileges", nargs='+', 
                                   help="List of assigned privileges (optional)")
    update_role_parser.add_argument("--oem-privileges", nargs='+',
                                   help="List of OEM privileges (optional)")
    update_role_parser.set_defaults(func=update_role)

    # Delete role command
    delete_role_parser = subparsers.add_parser("delete", help="Delete an existing role")
    delete_role_parser.add_argument("role_id", help="Role ID to delete")
    delete_role_parser.set_defaults(func=delete_role)

    # Get privileges command
    get_privileges_parser = subparsers.add_parser("list-privileges", help="List available privileges")
    get_privileges_parser.set_defaults(func=list_privileges)


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


def get_role(args):
    """Get detailed information for a specific role"""
    if not args.role_id:
        print("Error: Role ID is required")
        return
    try:
        role = role_ops.get_role_privileges(args.rsc, args.role_id)
        print(f"Role Information for '{args.role_id}':")
        print(f"  Name: {role.name}")
        print(f"  RoleId: {role.role_id}")
        print(f"  IsPredefined: {role.is_predefined}")
        
        # Display Assigned Privileges
        print_role_privileges(role)

    except RedfishError as e:
        error_msg = str(e)
        print(f"Error getting role: {error_msg}")


def create_role(args):
    """Create a new role"""
    try:
        # Validate that all required parameters are provided
        if not args.role_id:
            print("Error: Role ID is required")
            return

        assigned_privileges = getattr(args, 'assigned_privileges', None)
        oem_privileges = getattr(args, 'oem_privileges', None)

        # Remove empty strings from the privileges lists
        if assigned_privileges:
            assigned_privileges = [p for p in assigned_privileges if p]
        if oem_privileges:
            oem_privileges = [p for p in oem_privileges if p]

        if not assigned_privileges:
            print("Error: Assigned privileges are required")
            return
        if not oem_privileges:
            print("Error: OEM privileges are required")
            return

        role_ops.create_role(args.rsc, args.role_id, assigned_privileges, oem_privileges)
        print(f"Role '{args.role_id}' created successfully")
    except RedfishError as e:
        error_msg = str(e)
        print(f"Error creating role: {error_msg}")


def update_role(args):
    """Update role privileges"""
    try:
        if not args.role_id:
            print("Error: Role ID is required")
            return

        assigned_privileges = getattr(args, 'assigned_privileges', None)
        oem_privileges = getattr(args, 'oem_privileges', None)

        # Remove empty strings from the privileges lists
        if assigned_privileges:
            assigned_privileges = [p for p in assigned_privileges if p]
        if oem_privileges:
            oem_privileges = [p for p in oem_privileges if p]

        if assigned_privileges is None and oem_privileges is None:
            print("Error: At least one of --assigned-privileges or --oem-privileges must be provided")
            return

        role_ops.update_role_privileges(args.rsc, args.role_id, assigned_privileges, oem_privileges)
        print(f"Role '{args.role_id}' updated successfully")
    except RedfishError as e:
        error_msg = str(e)
        print(f"Error updating role: {error_msg}")


def delete_role(args):
    """Delete an existing role"""
    try:
        if not args.role_id:
            print("Error: Role ID is required")
            return
            
        role_ops.delete_role(args.rsc, args.role_id)
        print(f"Role '{args.role_id}' deleted successfully")
    except RedfishError as e:
        error_msg = str(e)
        print(f"Error deleting role: {error_msg}")


def list_privileges(args):
    """List all available privileges"""
    try:
        # Fetch the role with Administrator privileges to get its privileges
        # as Administrator role is a read-only role that has all privileges
        role = role_ops.get_role_privileges(args.rsc, "Administrator")
        print(f"Privileges:")

        print_role_privileges(role)

    except RedfishError as e:
        error_msg = str(e)
        print(f"Error getting privileges: {error_msg}")


# Helper function to print role privileges
def print_role_privileges(role):
    """Print the privileges of a role"""
    # Display Assigned Privileges
    if role.assigned_privileges:
        print("\nAssigned Privileges:")
        for privilege in role.assigned_privileges:
            print(f"  - {privilege}")
    else:
        print("\nAssigned Privileges: None")

    # Display OEM Privileges
    if role.oem_privileges:
        print("\nOEM Privileges:")
        for privilege in role.oem_privileges:
            print(f"  - {privilege}")
    else:
        print("\nOEM Privileges: None")
