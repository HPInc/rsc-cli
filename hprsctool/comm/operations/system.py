"""Commands for system management."""

from redfish.rest.v1 import RestResponse as RedfishRestResponse


from ...models.system import System
from ..remote_system_controller import Rsc
from .collection import get_first_uri

def get_system(rsc: Rsc) -> System:
    """Get the system information"""
    system_uri = get_first_uri(rsc, "/redfish/v1/Systems")
    return System(rsc.perform_redfish_get(system_uri).dict)


def set_system_power(rsc: Rsc, state: str) -> RedfishRestResponse:
    """Set the system power state"""
    body = {"ResetType": state}
    system_uri = get_first_uri(rsc, "/redfish/v1/Systems")
    return rsc.perform_redfish_post(f"{system_uri}/Actions/ComputerSystem.Reset", body)
