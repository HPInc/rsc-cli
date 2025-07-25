"""Commands for account management (user accounts)."""

import argparse
from hprsctool.comm.remote_system_controller import RedfishError, Rsc
from ..comm.operations import account as account_ops
from ..comm import redfish_messages

def get_parameters(subparsers: argparse._SubParsersAction) -> None:
    """Get the parameters for the account command"""
    subparsers.required = True

    # List accounts command
    list_accounts_parser = subparsers.add_parser("list", help="List all user accounts")
    list_accounts_parser.set_defaults(func=list_accounts)

    # Get account command
    get_account_parser = subparsers.add_parser("get", help="Get details of a specific user account")
    get_account_parser.add_argument("account_id", help="Account ID to get details for", action="store")
    get_account_parser.set_defaults(func=get_account)

    # Create account command
    create_account_parser = subparsers.add_parser("create", help="Create a new user account")
    create_account_parser.add_argument("new_username", help="Username for the new account", action="store")
    create_account_parser.add_argument("new_password", help="Password for the new account", action="store")
    create_account_parser.add_argument("role_id", help="Role ID for the new account", action="store")
    create_account_parser.set_defaults(func=create_account)

    # Change password command
    change_password_parser = subparsers.add_parser("change-password", help="Change user password")
    change_password_parser.add_argument("account_id", help="Account ID to change password for", action="store")
    change_password_parser.add_argument("new_password", help="New password", action="store")
    change_password_parser.set_defaults(func=change_password)

    # Delete account command
    delete_account_parser = subparsers.add_parser("delete", help="Delete a user account")
    delete_account_parser.add_argument("account_id", help="Account ID to delete", action="store")
    delete_account_parser.set_defaults(func=delete_account)


def list_accounts(args):
    """List all user accounts"""
    try:
        users = account_ops.get_accounts(args.rsc)
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
        print(f"Error listing accounts: {error_msg}")


def get_account(args):
    """Get details of a specific user account"""
    if not args.account_id:
        print("Error: Account ID is required")
        return
    try:
        user = account_ops.get_account(args.rsc, args.account_id)
        print(f"User account details:")
        print(f"  ID: {user.user_id}")
        print(f"  Username: {user.username}")
        print(f"  Name: {user.name}")
        print(f"  Role ID: {user.role_id}")
        print(f"  Password Change Required: {user.password_change_required}")
    except RedfishError as e:
        error_msg = str(e)
        print(f"Error getting account: {error_msg}")


def create_account(args):
    """Create a new user account"""
    if not args.new_username:
        print("Error: Username is required")
        return
    if not args.new_password:
        print("Error: Password is required")
        return
    if not args.role_id:
        print("Error: Role ID is required")
        return
    try:
        user = account_ops.create_account(args.rsc, args.new_username, args.new_password, args.role_id)
        print(f"User created successfully:")
        print(f"  ID: {user.user_id}")
        print(f"  Username: {user.username}")
        print(f"  Role ID: {user.role_id}")
    except RedfishError as e:
        error_msg = str(e)
        print(f"Error creating account: {error_msg}")


def change_password(args):
    """Change user password"""
    if not args.account_id:
        print("Error: Account ID is required")
        return
    if not args.new_password:
        print("Error: New password is required")
        return
    try:
        user = account_ops.change_account_password(args.rsc, args.account_id, args.new_password)
        print(f"Password changed successfully for account: {args.account_id}")
        print(f"  Username: {user.username}")
        print(f"  Role ID: {user.role_id}")
        if user.password_change_required:
            print(f"  Password change required: {user.password_change_required}")
    except RedfishError as e:
        error_msg = str(e)
        print(f"Error changing password: {error_msg}")


def delete_account(args):
    """Delete a user account"""
    if not args.account_id:
        print("Error: Account ID is required")
        return
    try:
        account_ops.delete_account(args.rsc, args.account_id)
        print(f"User account deleted successfully: {args.account_id}")
    except RedfishError as e:
        error_msg = str(e)
        print(f"Error deleting account: {error_msg}")
