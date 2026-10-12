"""Redfish collection discovery."""

from ..remote_system_controller import RedfishError, Rsc

def get_collection(rsc: Rsc, collection_uri: str) -> dict:
    """GET a Redfish Collection."""
    data = rsc.perform_redfish_get(collection_uri).dict
    members = data.get("Members") if isinstance(data, dict) else None
    if not isinstance(members, list):
        raise RedfishError(
            f"Discovery failed for {collection_uri}: missing or invalid Members array"
        )
    return data


def get_default_uri(rsc: Rsc, collection_uri: str) -> str:
    """Get the first URI in a Redfish Collection."""
    data = get_collection(rsc, collection_uri)
    members = data["Members"]
    if members:
        return members[0]["@odata.id"]
