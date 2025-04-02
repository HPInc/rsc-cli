"""Test cases for system operations."""
from unittest.mock import MagicMock, patch

import pytest

from hprsctool.comm.operations.system import get_system, set_system_power
from hprsctool.models.system import System

@pytest.fixture(name="mock_rsc")
def fixture_mock_rsc():
    return MagicMock()

def test_get_system(mock_rsc):
    mock_response = MagicMock()
    mock_response.dict = {"UUID": "1", "Model": "Test System"}
    mock_rsc.perform_redfish_get.return_value = mock_response

    with patch("hprsctool.comm.operations.system.System", return_value=System(mock_response.dict)):
        system = get_system(mock_rsc)
        mock_rsc.perform_redfish_get.assert_called_once_with("/redfish/v1/Systems/1")
        assert system.uuid == "1"
        assert system.model == "Test System"

def test_set_system_power_on(mock_rsc):
    state = "On"
    with patch.object(mock_rsc, 'perform_redfish_post') as mock_post:
        set_system_power(mock_rsc, state)
        mock_post.assert_called_once_with(
            "/redfish/v1/Systems/1/Actions/ComputerSystem.Reset",
            {"ResetType": state}
        )

def test_set_system_power_off(mock_rsc):
    state = "Off"
    with patch.object(mock_rsc, 'perform_redfish_post') as mock_post:
        set_system_power(mock_rsc, state)
        mock_post.assert_called_once_with(
            "/redfish/v1/Systems/1/Actions/ComputerSystem.Reset",
            {"ResetType": state}
        )
