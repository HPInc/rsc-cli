"""network related commands"""

from redfish.rest.v1 import RestResponse as RedfishRestResponse

from ...models import ethernet_interface
from ...models.manager_network_protocol import ManagerNetworkProtocol
from ...comm.remote_system_controller import RedfishError, Rsc
from .collection import get_collection, get_default_uri


def get_manager_ethernet_interface_uri(rsc: Rsc) -> str:
    """Select br0 from the collection members, otherwise use the first member."""
    manager_uri = get_default_uri(rsc, "/redfish/v1/Managers")
    collection_uri = f"{manager_uri}/EthernetInterfaces"
    members = get_collection(rsc, collection_uri)["Members"]
    if not members:
        raise RedfishError(f"No Ethernet interfaces found in {collection_uri}")
    for member in members:
        uri = member["@odata.id"]
        if uri.rstrip("/").rsplit("/", 1)[-1] == "br0":
            return uri
    return members[0]["@odata.id"]

def get_manager_ethernet_interface(rsc: Rsc) -> ethernet_interface.EthernetInterface:
    """Get the RSC ethernet interface information"""
    interface_uri = get_manager_ethernet_interface_uri(rsc)
    return ethernet_interface.EthernetInterface(
        rsc.perform_redfish_get(interface_uri).dict
    )


def set_manager_ethernet_interface(rsc: Rsc, data: dict) -> RedfishRestResponse:
    """Set the RSC ethernet interface information"""
    interface_uri = get_manager_ethernet_interface_uri(rsc)
    return rsc.perform_redfish_patch(interface_uri, data)


def get_manager_network_protocol(rsc: Rsc) -> ManagerNetworkProtocol:
    """Get the RSC network protocol information"""
    manager_uri = get_default_uri(rsc, "/redfish/v1/Managers")
    return ManagerNetworkProtocol(
        rsc.perform_redfish_get(f"{manager_uri}/NetworkProtocol").dict
    )


def set_manager_network_protocol(rsc: Rsc, data: dict) -> RedfishRestResponse:
    """Set the RSC network protocol information"""
    manager_uri = get_default_uri(rsc, "/redfish/v1/Managers")
    return rsc.perform_redfish_patch(f"{manager_uri}/NetworkProtocol", data)
