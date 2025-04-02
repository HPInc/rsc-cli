"""Task Commands"""

from ...models.task import Task, TaskCollection
from ..remote_system_controller import Rsc

def get_task_collection(rsc: Rsc) -> TaskCollection:
    """Get the task collection information"""
    return TaskCollection(rsc.perform_redfish_get("/redfish/v1/TaskService/Tasks").dict)


def get_task(rsc: Rsc, task_id: str) -> Task:
    """Get the task information"""
    return Task(
        rsc.perform_redfish_get(f"/redfish/v1/TaskService/Tasks/{task_id}").dict
    )


def delete_task(rsc: Rsc, task_id: str):
    """Delete (cancel) a task"""
    rsc.perform_redfish_delete(f"/redfish/v1/TaskService/Tasks/{task_id}/Monitor")
