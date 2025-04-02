"""Test cases for redfish_config.py module."""
from unittest.mock import MagicMock, patch
import pytest
from hprsctool.comm.remote_system_controller import Rsc, RedfishConfig, check_response_for_error

@pytest.fixture(name="redfish_config")
def redfish_config_fixture():
    return RedfishConfig(
        base_url="example.com",
        username="admin",
        password="password",
        capath="",
        cafile="",
        timeout=30,
        max_retry=3,
        proxies=None
    )

@pytest.fixture(name="rsc")
def rsc_fixture(redfish_config):
    with patch("redfish.redfish_client") as mock_client:
        mock_instance = mock_client.return_value
        mock_instance.get.return_value = MagicMock(status=200, dict={}, text="")
        mock_instance.patch.return_value = MagicMock(status=200, dict={}, text="")
        mock_instance.post.return_value = MagicMock(status=200, dict={}, text="")
        mock_instance.delete.return_value = MagicMock(status=200, dict={}, text="")
        mock_instance.login.return_value = None
        mock_instance.logout.return_value = None
        yield Rsc(redfish_config)

def test_redfish_config_dict(redfish_config):
    assert redfish_config.__dict__() == {
        "base_url": "example.com",
        "username": "admin",
        "password": "password",
        "capath": "",
        "cafile": "",
        "timeout": 30,
        "max_retry": 3,
        "proxies": None
    }

def test_rsc_initialization(redfish_config):
    with patch("redfish.redfish_client") as mock_client:
        Rsc(redfish_config)
        mock_client.assert_called_once_with(
            base_url=redfish_config.base_url,
            username=redfish_config.username,
            password=redfish_config.password,
            capath=redfish_config.capath,
            cafile=redfish_config.cafile,
            timeout=redfish_config.timeout,
            max_retry=redfish_config.max_retry,
            proxies=redfish_config.proxies
        )

def test_rsc_login(rsc):
    rsc.login()
    rsc.client.login.assert_called_once_with(auth="session")

def test_rsc_logout(rsc):
    rsc.logout()
    rsc.client.logout.assert_called_once()

def test_perform_redfish_get(rsc):
    url = "/redfish/v1/Systems"
    response = rsc.perform_redfish_get(url)
    rsc.client.get.assert_called_once_with(url)
    assert response.status == 200

def test_perform_redfish_patch(rsc):
    url = "/redfish/v1/Systems"
    data = {"Name": "NewName"}
    response = rsc.perform_redfish_patch(url, data)
    rsc.client.patch.assert_called_once_with(url, body=data)
    assert response.status == 200

def test_perform_redfish_post(rsc):
    url = "/redfish/v1/Systems"
    data = {"Name": "NewName"}
    response = rsc.perform_redfish_post(url, data)
    rsc.client.post.assert_called_once_with(url, body=data, headers={}, timeout=30)
    assert response.status == 200

def test_perform_redfish_delete(rsc):
    url = "/redfish/v1/Systems"
    response = rsc.perform_redfish_delete(url)
    rsc.client.delete.assert_called_once_with(url)
    assert response.status == 200

def test_monitor_task(rsc):
    task_response = MagicMock()
    task_response.is_processing = False
    task_response.dict = {}
    task_response.retry_after = None
    response = rsc.monitor_task(task_response)
    assert response == task_response

def test_check_response_for_error_no_error():
    response = MagicMock()
    response.status = 200
    response.text = ""
    response.dict = {}
    error_message = check_response_for_error(response)
    assert error_message is None
