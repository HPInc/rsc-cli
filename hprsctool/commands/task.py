"""Task Commands"""

import argparse

from ..comm.remote_system_controller import Rsc
from ..comm.operations import task as task_ops

def get_parameters(subparser: argparse.ArgumentParser):
    """Get the parameters for the task command"""
    subparser.required = True

    list_parser = subparser.add_parser("list", help="list tasks")
    list_parser.add_argument(
        "--running", help="Only print running tasks", action="store_true"
    )
    list_parser.set_defaults(func=list_tasks)

    get_parser = subparser.add_parser("get", help="get a task")
    get_parser.add_argument("task_id", help="Task ID", action="store")
    get_parser.set_defaults(func=print_task)

    delete_parser = subparser.add_parser("cancel", help="cancel a running task")
    delete_parser.add_argument("task_id", help="Task ID", action="store")
    delete_parser.set_defaults(func=cancel_task)


def list_tasks(args: argparse.Namespace):
    """List the tasks"""
    rsc: Rsc = args.rsc
    tasks = task_ops.get_task_collection(rsc)
    for task_uri in tasks:
        task = task_ops.get_task(rsc, task_uri.split("/")[-1])
        if args.running and task.task_state != "Running":
            continue
        print(task)


def print_task(args: argparse.Namespace):
    """Get a task"""
    rsc: Rsc = args.rsc
    task = task_ops.get_task(rsc, args.task_id)
    print(task)


def cancel_task(args: argparse.Namespace):
    """Cancel a task"""
    rsc: Rsc = args.rsc
    task_ops.delete_task(rsc, args.task_id)
    print("Task deleted")
