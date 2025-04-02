"""Module defining the RSC class and refish operations"""

from dataclasses import dataclass
import json
import time
from typing import Any, Dict

import redfish
import redfish.rest.v1 as redfish_rest_v1
from redfish.rest.v1 import RestResponse as RedfishRestResponse
from . import redfish_messages


# pylint: disable=too-many-instance-attributes
@dataclass
class RedfishConfig:
    """Class defining a Redfish configuration"""

    base_url: str
    username: str
    password: str
    capath: str = ""
    cafile: str = ""
    timeout: int = 30
    max_retry: int = 3
    proxies: Dict[str, str] | None = None

    def __dict__(self):
        return {
            "base_url": self.base_url,
            "username": self.username,
            "password": self.password,
            "capath": self.capath,
            "cafile": self.cafile,
            "timeout": self.timeout,
            "max_retry": self.max_retry,
            "proxies": self.proxies
        }


def check_response_for_error(response) -> str | None:
    """Get the error message from a response"""
    status = response.status
    if status < 200 or status >= 300:
        if response.text:
            return redfish_messages.get_error_message(response.dict)
        return "HTTP error: " + str(status)
    return None


class RedfishError(Exception):
    """Class defining a Redfish error"""

    def __init__(self, message: str):
        super().__init__(message)


class Rsc:
    """Class defining an RSC"""

    def __init__(self, config: RedfishConfig):
        self.config = config
        try:
            self.client = redfish.redfish_client(**config.__dict__())
        except redfish.rest.v1.InvalidCredentialsError as exc:
            raise RedfishError("Invalid credentials") from exc
        except redfish.rest.v1.RetriesExhaustedError as exc:
            raise RedfishError("Failed to connect to the RSC") from exc
        self.address = config.base_url

    def perform_redfish_get(self, url: str) -> RedfishRestResponse:
        """Perform a Redfish action"""
        response = self.client.get(url)
        error_msg = check_response_for_error(response)
        if error_msg:
            raise RedfishError(f"GET failed for {url}: {error_msg}")
        return response

    def perform_redfish_patch(self, url: str, data: dict) -> RedfishRestResponse:
        """Perform a Redfish action"""
        response = self.client.patch(url, body=data)
        error_msg = check_response_for_error(response)
        if error_msg:
            raise RedfishError(f"PATCH failed for {url}: {error_msg}")
        return response

    def perform_redfish_post(
        self, url: str, data: Any, is_multipart: bool = False
    ) -> RedfishRestResponse:
        """Perform a Redfish action"""
        headers = {}
        if is_multipart:
            headers = {"Content-Type": "multipart/form-data"}
        response: RedfishRestResponse = self.client.post(
            url,
            body=data,
            headers=headers,
            timeout=(3600 if is_multipart else self.config.timeout),
        )
        error_msg = check_response_for_error(response)
        if error_msg:
            raise RedfishError(f"POST failed for {url}: {error_msg}")

        return response

    def login(self):
        """Login to the RSC"""
        try:
            self.client.login(auth="session")
        except redfish_rest_v1.SessionCreationError as e:
            exp_msg = ""
            # SessionCreationError does not have a message attribute.
            # It returns the body of the response as a string after a newline.
            err_str = str(e).split("\n")
            error_msg = err_str[1] if len(err_str) > 1 else ""
            if len(error_msg) > 0:
                try:
                    body = json.loads(error_msg)
                    exp_msg = f"Login failed: {redfish_messages.get_error_message(body)}"
                except (ValueError, json.JSONDecodeError):
                    exp_msg = f"Login failed: {error_msg}"
            raise RedfishError(exp_msg) from e
        except Exception as e:
            raise RedfishError(f"Login failed: {str(e)}") from e

    def logout(self):
        """Logout from the RSC"""
        self.client.logout()

    def perform_redfish_delete(self, url: str) -> RedfishRestResponse:
        """Perform a Redfish action"""
        response = self.client.delete(url)
        error_msg = check_response_for_error(response)
        if error_msg:
            raise RedfishError(f"DELETE failed for {url}: {error_msg}")
        return response

    def monitor_task(self, task_response: RedfishRestResponse) -> RedfishRestResponse:
        """Monitors a task until it is completed. Returns the final response of the task monitor."""

        previous_message = ""
        previous_line_len = 0

        while task_response.is_processing:
            task_body = task_response.dict

            if "Messages" not in task_body:
                print(".", end="", flush=True)
            else:
                message_to_display = ""
                if "PercentComplete" in task_body:
                    message_to_display = f"{task_body['PercentComplete']}%"
                if len(task_body["Messages"]) > 0:
                    message = task_body["Messages"][0]["Message"]
                    message_to_display += f" - {message}"
                # Keep previous messages visible
                if previous_message not in (message, ""):
                    print("\n")
                # left-justify current line to overwrite previous line
                message_to_display = f"{message_to_display: <{previous_line_len}}"

                print(f"\r{message_to_display}", end="", flush=True)
                previous_message = message
                previous_line_len = len(message_to_display)

            retry_time = task_response.retry_after
            time.sleep(retry_time if retry_time else 5)
            task_response = task_response.monitor(self.client)

        print("\n")
        return task_response
