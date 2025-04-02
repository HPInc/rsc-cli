"""Module for working with redfish messages"""
import re
from typing import List

import requests


cached_registries = {}

message_id_regex = re.compile(r"(?P<registry>\w+\.\d+\.\d+\.\d+)\.(?P<message_id>\w+)")


def get_redfish_message(address: str, message_id: str, message_args: list[str] | None = None):
    """Get the redfish message from the registry"""

    match = message_id_regex.match(message_id)
    if not match:
        raise ValueError(f"Invalid message ID: {message_id}")
    registry = match.group("registry")
    message_id = match.group("message_id")

    if registry not in cached_registries:
        response = requests.get(
            f"https://{address.split('//')[1]}/registries/en/{registry}.json",
            verify=False,
            timeout=5,
        )
        response.raise_for_status()
        cached_registries[registry] = response.json()

    registry_data = cached_registries[registry]

    if message_id in registry_data["Messages"]:
        base_messsage = registry_data["Messages"][message_id]["Message"]
        if message_args:
            for arg_index, arg in enumerate(message_args):
                base_messsage = base_messsage.replace(f"%{arg_index+1}", arg)
        return base_messsage

    raise ValueError(f"Message ID {message_id} not found in registry {registry}")

def get_error_message(resp_json: dict) -> str | None:
    """Get the error message from a response"""

    message = None
    message_args = []

    if resp_json is None:
        return None

    if "error" in resp_json:
        resp_json = resp_json["error"]

    message_info = resp_json.get("@Message.ExtendedInfo", [])

    if len(message_info) > 0:
        message = resp_json["@Message.ExtendedInfo"][0]["Message"]
        message_args = resp_json["@Message.ExtendedInfo"][0].get("MessageArgs", [])

    if message is not None:
        return get_message_and_args(message, message_args)

    return None

def get_message_and_args(message: str, message_args: List[str]) -> str:
    """Get the message with arguments"""

    for index, arg in enumerate(message_args):
        message = message.replace(f"%{index+1}", arg)

    return message
