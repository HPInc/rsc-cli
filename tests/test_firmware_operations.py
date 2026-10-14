"""Tests for UpdateService firmware upload endpoint discovery."""

import json
from pathlib import Path
from unittest.mock import MagicMock, call, patch
from urllib.parse import urljoin

import pytest

from hprsctool.comm.operations.manager import update_rsc_firmware
from hprsctool.comm.remote_system_controller import RedfishError, Rsc


@pytest.fixture(name="mock_rsc")
def fixture_mock_rsc():
    rsc = MagicMock(spec=Rsc)
    rsc.address = "https://rsc.example:8443"
    rsc.client = MagicMock()
    rsc.client.get_session_key.return_value = "session-token"
    rsc.monitor_task.return_value = MagicMock(status=200)
    return rsc


@pytest.fixture(name="firmware_file")
def fixture_firmware_file(tmp_path):
    firmware_file = tmp_path / "firmware.bin"
    firmware_file.write_bytes(b"firmware")
    return str(firmware_file)


@pytest.mark.parametrize(
    "upload_uri",
    [
        "/redfish/v1/UpdateService/MultipartUpdate",
        "/redfish/v1/UpdateService/update-multipart",
        "/custom/firmware-upload",
        "https://other-host.example/redfish/v1/UpdateService/update-multipart",
    ],
)
def test_upload_uses_advertised_endpoint(mock_rsc, firmware_file, upload_uri):
    mock_rsc.perform_redfish_get.side_effect = [
        MagicMock(dict={"MultipartHttpPushUri": upload_uri}),
    ]
    expected_url = urljoin(mock_rsc.address, upload_uri)
    task_response = MagicMock()
    with patch("hprsctool.comm.operations.manager.requests.post") as mock_post, patch(
        "hprsctool.comm.operations.manager.RedfishRestResponse",
        return_value=task_response,
    ):
        update_rsc_firmware(mock_rsc, firmware_file)

    assert mock_rsc.perform_redfish_get.call_args_list == [
        call("/redfish/v1/UpdateService"),
    ]
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert args == (expected_url,)
    assert kwargs["headers"] == {"X-Auth-Token": "session-token"}
    assert kwargs["timeout"] == 3600
    assert kwargs["verify"] is False
    assert list(kwargs["files"]) == ["UpdateParameters", "UpdateFile"]
    assert json.loads(kwargs["files"]["UpdateParameters"][1]) == {}
    update_file_name, update_file, update_file_type = kwargs["files"]["UpdateFile"]
    assert update_file_name == Path(firmware_file).name
    assert update_file.name == firmware_file
    assert update_file.closed
    assert update_file_type == "application/octet-stream"
    mock_post.return_value.raise_for_status.assert_called_once_with()
    mock_rsc.monitor_task.assert_called_once_with(task_response)


@pytest.mark.parametrize(
    "data",
    [
        None,
        {},
        {"MultipartHttpPushUri": None},
        {"MultipartHttpPushUri": 1},
        {"MultipartHttpPushUri": ""},
        {"MultipartHttpPushUri": " "},
    ],
)
def test_missing_endpoint_uses_legacy_fallback(mock_rsc, firmware_file, data):
    mock_rsc.perform_redfish_get.side_effect = [
        MagicMock(dict=data),
    ]
    with patch("hprsctool.comm.operations.manager.requests.post") as mock_post, patch(
        "hprsctool.comm.operations.manager.RedfishRestResponse"
    ):
        update_rsc_firmware(mock_rsc, firmware_file)

    assert mock_rsc.perform_redfish_get.call_args_list == [
        call("/redfish/v1/UpdateService"),
    ]
    mock_post.assert_called_once()
    assert mock_post.call_args.args == (
        urljoin(mock_rsc.address, "/redfish/v1/UpdateService/MultipartUpdate"),
    )
    mock_rsc.monitor_task.assert_called_once()


def test_update_service_error_prevents_upload(mock_rsc, firmware_file):
    mock_rsc.perform_redfish_get.side_effect = RedfishError("GET failed")
    with patch("hprsctool.comm.operations.manager.requests.post") as mock_post:
        with pytest.raises(RedfishError, match="GET failed"):
            update_rsc_firmware(mock_rsc, firmware_file)

    mock_post.assert_not_called()
    mock_rsc.monitor_task.assert_not_called()


def test_missing_firmware_prevents_discovery(mock_rsc, tmp_path):
    with pytest.raises(ValueError, match="not found"):
        update_rsc_firmware(mock_rsc, str(tmp_path / "missing.bin"))

    mock_rsc.perform_redfish_get.assert_not_called()
