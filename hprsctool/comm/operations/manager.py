"""Manager commands"""

import json
from pathlib import Path
from urllib.parse import urljoin

import requests
from redfish.rest.v1 import RestResponse as RedfishRestResponse

from ...comm.remote_system_controller import RedfishError, Rsc
from ...comm import redfish_messages
from ...models.manager import Manager
from .collection import get_first_uri


def get_manager(rsc: Rsc) -> Manager:
    """Get the RSC manager information"""
    manager_uri = get_first_uri(rsc, "/redfish/v1/Managers")
    return Manager(rsc.perform_redfish_get(manager_uri).dict)


def change_admin_password(rsc: Rsc, new_password: str):
    """Change the RSC password"""
    body = {"Password": new_password}
    rsc.perform_redfish_patch("/redfish/v1/AccountService/Accounts/1", body)


def restart(rsc: Rsc):
    """Restart the RSC"""
    manager_uri = get_first_uri(rsc, "/redfish/v1/Managers")
    rsc.perform_redfish_post(
        f"{manager_uri}/Actions/Manager.Reset",
        {"ResetType": "ForceRestart"},
    )


def factory_reset(rsc: Rsc):
    """Factory-reset the RSC"""
    manager_uri = get_first_uri(rsc, "/redfish/v1/Managers")
    rsc.perform_redfish_post(
        f"{manager_uri}/Actions/Manager.ResetToDefaults",
        {"ResetToDefaultsType": "ResetAll"},
    )


def update_rsc_firmware(rsc: Rsc, fw_file_path: str) -> RedfishRestResponse:
    """Update the RSC firmware"""

    if not Path(fw_file_path).exists():
        raise ValueError(f"Firmware file {fw_file_path} not found")

    update_service_uri = "/redfish/v1/UpdateService"
    update_service = rsc.perform_redfish_get(update_service_uri).dict
    upload_uri = (
        update_service.get("MultipartHttpPushUri")
        if isinstance(update_service, dict) else None
    )
    if not isinstance(upload_uri, str) or not upload_uri.strip():
        upload_uri = "/redfish/v1/UpdateService/MultipartUpdate"

    update_parameters = {}
    response = RedfishRestResponse(None, None)
    with open(fw_file_path, "rb") as firmware:
        print("Sending file...", flush=True)
        files = {
            "UpdateParameters": (
                None,
                json.dumps(update_parameters),
                "application/json",
            ),
            "UpdateFile": (
                Path(fw_file_path).name,
                firmware,
                "application/octet-stream",
            ),
        }
        headers = {"X-Auth-Token": rsc.client.get_session_key()}
        # Using the self.client.post method directly fails to upload the
        # firmware in very old RSC versions. The following code is a workaround
        # to upload the firmware file using requests.
        resp = requests.post(
            urljoin(rsc.address, upload_uri),
            files=files,
            headers=headers,
            verify=False,
            timeout=3600,
        )
        resp.raise_for_status()
        # Create a redfish lib RedfishRestResponse object to monitor the task
        response = RedfishRestResponse(None, resp)

    print("File sent, monitoring update:", flush=True)
    monitor_response = rsc.monitor_task(response)
    if monitor_response.status < 200 or monitor_response.status >= 300:
        if monitor_response.status == 401:
            raise RedfishError(
                "The update might have succeeded, but the user session was lost.\n"
                "Please use 'manager get' to confirm the version of the firmware."
            )
        raise RedfishError(
            ("Failed to update firmware: "
            f"{redfish_messages.get_error_message(monitor_response.dict)}")
        )


def update_manager(rsc: Rsc, body: dict) -> RedfishRestResponse:
    """Update the RSC manager information"""
    manager_uri = get_first_uri(rsc, "/redfish/v1/Managers")
    return rsc.perform_redfish_patch(manager_uri, body)
