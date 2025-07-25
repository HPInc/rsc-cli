"""Commands for user management."""

import argparse

from hprsctool.comm.remote_system_controller import RedfishError, Rsc
from ..comm.operations import user as user_ops
from ..comm import redfish_messages


def get_parameters(subparsers: argparse._SubParsersAction) -> None:
    """Get the parameters for the user command"""
    subparsers.required = True
    
    # List roles command
    list_roles_parser = subparsers.add_parser("list-roles", help="List all available roles")
    list_roles_parser.set_defaults(func=list_roles)
    
    # List users command
    list_users_parser = subparsers.add_parser("list-users", help="List all user accounts")
    list_users_parser.set_defaults(func=list_users)
    
    # Get user command
    get_user_parser = subparsers.add_parser("get-user", help="Get details of a specific user account")
    get_user_parser.add_argument("account_id", help="Account ID to get details for", action="store")
    get_user_parser.set_defaults(func=get_user)
    
    # Create user command
    create_user_parser = subparsers.add_parser("create", help="Create a new user account")
    create_user_parser.add_argument("new_username", help="Username for the new account", action="store")
    create_user_parser.add_argument("new_password", help="Password for the new account", action="store")
    create_user_parser.add_argument("role_id", help="Role ID for the new account", action="store")
    create_user_parser.set_defaults(func=create_user)
    
    # Change password command
    change_password_parser = subparsers.add_parser("change-password", help="Change user password")
    change_password_parser.add_argument("account_id", help="Account ID to change password for", action="store")
    change_password_parser.add_argument("new_password", help="New password", action="store")
    change_password_parser.set_defaults(func=change_password)


def list_roles(args):
    """List all available roles"""
    try:
        roles = user_ops.get_roles(args.rsc)
        print("Available roles:")
        for role in roles:
            print(f"  - {role.role_id}")
            if role.description != "N/A":
                print(f"    Description: {role.description}")
    except RedfishError as e:
        error_msg = str(e)
        print(f"Error listing roles: {error_msg}")


def create_user(args):
    """Create a new user account"""
    # Validate that all required parameters are provided
    if not args.username:
        print("Error: Username is required")
        return
    if not args.password:
        print("Error: Password is required")
        return
    if not args.role_id:
        print("Error: Role ID is required")
        return
    
    try:
        user = user_ops.create_user(args.rsc, args.new_username, args.new_password, args.role_id)
        print(f"User created successfully:")
        print(f"  ID: {user.user_id}")
        print(f"  Username: {user.username}")
        print(f"  Role ID: {user.role_id}")
        if user.account_types:
            print(f"  Account Types: {', '.join(user.account_types)}")
    except RedfishError as e:
        error_msg = str(e)
        print(f"Error creating user: {error_msg}")


def change_password(args):
    """Change user password"""
    # Validate that all required parameters are provided
    if not args.account_id:
        print("Error: Account ID is required")
        return
    if not args.new_password:
        print("Error: New password is required")
        return
    
    try:
        user = user_ops.change_user_password(args.rsc, args.account_id, args.new_password)
        print(f"Password changed successfully for account: {args.account_id}")
        print(f"  Username: {user.username}")
        print(f"  Role ID: {user.role_id}")
        if user.password_change_required:
            print(f"  Password change required: {user.password_change_required}")
    except RedfishError as e:
        error_msg = str(e)
        print(f"Error changing password: {error_msg}")


def list_users(args):
    """List all user accounts"""
    try:
        users = user_ops.get_users(args.rsc)
        if not users:
            print("No user accounts found.")
            return
            
        print("User accounts:")
        for user in users:
            print(f"  - ID: {user.user_id}")
            print(f"    Username: {user.username}")
            print(f"    Role ID: {user.role_id}")
            print()
    except RedfishError as e:
        error_msg = str(e)
        print(f"Error listing users: {error_msg}")


def get_user(args):
    """Get details of a specific user account"""
    # Validate that account ID is provided
    if not args.account_id:
        print("Error: Account ID is required")
        return
    
    try:
        user = user_ops.get_user(args.rsc, args.account_id)
        print(f"User account details:")
        print(f"  ID: {user.user_id}")
        print(f"  Username: {user.username}")
        print(f"  Name: {user.name}")
        print(f"  Role ID: {user.role_id}")
        print(f"  Password Change Required: {user.password_change_required}")
    except RedfishError as e:
        error_msg = str(e)
        print(f"Error getting user: {error_msg}")
