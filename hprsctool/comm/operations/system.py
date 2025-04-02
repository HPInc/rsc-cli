"""Commands for system management."""

from redfish.rest.v1 import RestResponse as RedfishRestResponse


from ...models.system import System
from ..remote_system_controller import Rsc

def get_system(rsc: Rsc) -> System:
    """Get the system information"""
    return System(rsc.perform_redfish_get("/redfish/v1/Systems/1").dict)


def set_system_power(rsc: Rsc, state: str) -> RedfishRestResponse:
    """Set the system power state"""
    body = {"ResetType": state}
    return rsc.perform_redfish_post("/redfish/v1/Systems/1/Actions/ComputerSystem.Reset", body)
