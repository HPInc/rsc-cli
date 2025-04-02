"""network related commands"""

from redfish.rest.v1 import RestResponse as RedfishRestResponse

from ...models import ethernet_interface
from ...models.manager_network_protocol import ManagerNetworkProtocol
from ...comm.remote_system_controller import Rsc

def get_manager_ethernet_interface(rsc: Rsc) -> ethernet_interface.EthernetInterface:
    """Get the RSC ethernet interface information"""
    return ethernet_interface.EthernetInterface(
        rsc.perform_redfish_get("/redfish/v1/Managers/1/EthernetInterfaces/eth0").dict
    )


def set_manager_ethernet_interface(rsc: Rsc, data: dict) -> RedfishRestResponse:
    """Set the RSC ethernet interface information"""
    return rsc.perform_redfish_patch(
        "/redfish/v1/Managers/1/EthernetInterfaces/eth0", data
    )


def get_manager_network_protocol(rsc: Rsc) -> ManagerNetworkProtocol:
    """Get the RSC network protocol information"""
    return ManagerNetworkProtocol(
        rsc.perform_redfish_get("/redfish/v1/Managers/1/NetworkProtocol").dict
    )


def set_manager_network_protocol(rsc: Rsc, data: dict) -> RedfishRestResponse:
    """Set the RSC network protocol information"""
    return rsc.perform_redfish_patch("/redfish/v1/Managers/1/NetworkProtocol", data)
