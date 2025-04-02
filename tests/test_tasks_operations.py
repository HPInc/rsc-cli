"""Tests for the task operations module."""

from unittest.mock import MagicMock, patch

import pytest

from hprsctool.comm.operations.task import get_task, delete_task, get_task_collection


@pytest.fixture(name="mock_rsc")
def fixture_mock_rsc():
    return MagicMock()


def test_get_task_collection_no_elements(mock_rsc):
    mock_response = MagicMock()
    mock_response.dict = {"Members": []}
    mock_rsc.perform_redfish_get.return_value = mock_response

    with patch(
        "hprsctool.comm.operations.task.TaskCollection", return_value=MagicMock()
    ) as mock_task_collection:
        result = get_task_collection(mock_rsc)
        mock_rsc.perform_redfish_get.assert_called_once_with(
            "/redfish/v1/TaskService/Tasks"
        )
        mock_task_collection.assert_called_once_with(mock_response.dict)
        assert len(result.members) == 0


def test_get_task_collection_not_empty(mock_rsc):
    mock_response = MagicMock()

    task_id_list = [
        {"@odata.id": "/redfish/v1/TaskService/Tasks/12345"},
        {"@odata.id": "/redfish/v1/TaskService/Tasks/67890"},
    ]

    mock_response.dict = {"Members": task_id_list}
    mock_rsc.perform_redfish_get.return_value = mock_response

    result = get_task_collection(mock_rsc)
    mock_rsc.perform_redfish_get.assert_called_once_with(
        "/redfish/v1/TaskService/Tasks"
    )
    assert len(result.members) == len(task_id_list)
    assert result.members == [task["@odata.id"] for task in task_id_list]


def test_get_task(mock_rsc):
    task_id = "12345"
    mock_response = MagicMock()
    mock_response.dict = {"Id": task_id, "Name": "Test Task"}
    mock_rsc.perform_redfish_get.return_value = mock_response

    task = get_task(mock_rsc, task_id)
    mock_rsc.perform_redfish_get.assert_called_once_with(
        f"/redfish/v1/TaskService/Tasks/{task_id}"
    )

    assert task.task_id == task_id


def test_delete_task(mock_rsc):
    task_id = "12345"

    with patch.object(mock_rsc, "perform_redfish_delete") as mock_delete:
        delete_task(mock_rsc, task_id)
        mock_delete.assert_called_once_with(
            f"/redfish/v1/TaskService/Tasks/{task_id}/Monitor"
        )
