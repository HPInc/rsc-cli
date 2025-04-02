"""Model for a task Redfish object"""


class Task:
    """Model for a task Redfish object"""

    def __init__(self, data: dict):
        if data is None:
            raise ValueError("data is required")
        self.data = data

    @property
    def task_id(self) -> str:
        return self.data.get("Id", "N/A")

    @property
    def task_monitor(self) -> str:
        return self.data.get("TaskMonitor", "N/A")

    @property
    def start_time(self) -> str:
        return self.data.get("StartTime", "N/A")

    @property
    def end_time(self) -> str:
        return self.data.get("EndTime", "N/A")

    @property
    def task_state(self) -> str:
        return self.data.get("TaskState", "N/A")

    @property
    def task_status(self) -> str:
        return self.data.get("TaskStatus", "N/A")

    @property
    def name(self) -> str:
        return self.data.get("Name", "N/A")

    def __str__(self):
        return (
            f"Task {self.task_id}:\n"
            f"\tName: {self.name}\n"
            f"\tState: {self.task_state}\n"
            f"\tStatus: {self.task_status}\n"
            f"\tStart time: {self.start_time}\n"
            f"\tEnd time: {self.end_time}\n"
            f"\tMonitor: {self.task_monitor}"
        )


class TaskCollection:
    """Model for a task collection Redfish object"""

    def __init__(self, data: dict):
        if data is None:
            raise ValueError("data is required")
        if data.get("Members") is None:
            data["Members"] = []
        self.members = [member["@odata.id"] for member in data["Members"]]

    def __str__(self):
        return f"TaskCollection with {len(self.members)} tasks"

    def __iter__(self):
        return iter(self.members)
