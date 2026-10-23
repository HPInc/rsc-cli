"""Tests for collection discovery and the operations that use it."""

from unittest.mock import MagicMock, call

import pytest

from hprsctool.comm.operations import cert, manager, network, system, trusted_cert
from hprsctool.comm.operations.collection import get_collection, get_first_uri
from hprsctool.comm.remote_system_controller import RedfishError, Rsc


@pytest.mark.parametrize("resource", ["Managers", "Systems", "Chassis"])
@pytest.mark.parametrize("member_id", ["1", "42", "device-uuid"])
def test_single_member_discovery(resource, member_id):
    rsc = MagicMock(spec=Rsc)
    collection_uri = f"/redfish/v1/{resource}"
    member_uri = f"{collection_uri}/{member_id}"
    rsc.perform_redfish_get.return_value.dict = {
        "Members": [{"@odata.id": member_uri}]
    }

    assert get_first_uri(rsc, collection_uri) == member_uri
    rsc.perform_redfish_get.assert_called_once_with(collection_uri)


@pytest.mark.parametrize(
    "data",
    [
        None,
        [],
        {},
        {"Members": None},
        {"Members": {}},
    ],
)
@pytest.mark.parametrize("operation", [get_collection, get_first_uri])
def test_invalid_collection(data, operation):
    rsc = MagicMock(spec=Rsc)
    rsc.perform_redfish_get.return_value.dict = data

    with pytest.raises(RedfishError, match="Discovery failed for /redfish/v1/Managers"):
        operation(rsc, "/redfish/v1/Managers")


@pytest.mark.parametrize(
    "data,expected_uri",
    [
        ({"Members": [{"@odata.id": "/a"}, {"@odata.id": "/b"}]}, "/a"),
        ({"Members": [{"@odata.id": "/a"}], "Members@odata.nextLink": "/next"}, "/a"),
    ],
)
def test_get_first_uri_returns_first_member(data, expected_uri):
    rsc = MagicMock(spec=Rsc)
    rsc.perform_redfish_get.return_value.dict = data

    assert get_first_uri(rsc, "/redfish/v1/Managers") == expected_uri
    rsc.perform_redfish_get.assert_called_once_with("/redfish/v1/Managers")


def test_get_first_uri_raises_when_collection_is_empty():
    rsc = MagicMock(spec=Rsc)
    rsc.perform_redfish_get.return_value.dict = {"Members": []}

    with pytest.raises(RedfishError, match="no members found"):
        get_first_uri(rsc, "/redfish/v1/Managers")


@pytest.mark.parametrize(
    "data",
    [
        {"Members": []},
        {"Members": [{"@odata.id": "/a"}, {"@odata.id": "/b"}]},
    ],
)
def test_get_collection_returns_collection_unchanged(data):
    rsc = MagicMock(spec=Rsc)
    rsc.perform_redfish_get.return_value.dict = data

    assert get_collection(rsc, "/redfish/v1/Managers") is data
    rsc.perform_redfish_get.assert_called_once_with("/redfish/v1/Managers")


def test_discovery_propagates_get_failure():
    rsc = MagicMock(spec=Rsc)
    rsc.perform_redfish_get.side_effect = RedfishError("GET failed")

    with pytest.raises(RedfishError, match="GET failed"):
        get_first_uri(rsc, "/redfish/v1/Managers")


@pytest.fixture(name="mock_rsc")
def fixture_mock_rsc():
    rsc = MagicMock(spec=Rsc)
    rsc.perform_redfish_get.return_value.dict = {
        "Members": [{"@odata.id": "/redfish/v1/Managers/controller-uuid"}]
    }
    return rsc


@pytest.mark.parametrize(
    "operation,suffix",
    [
        (manager.get_manager, ""),
        (network.get_manager_network_protocol, "/NetworkProtocol"),
        (cert.get_certificate, "/NetworkProtocol/HTTPS/Certificates/1"),
    ],
)
def test_manager_reads_use_discovered_uri(mock_rsc, operation, suffix):
    resource_response = MagicMock()
    resource_response.dict = {"Name": "Discovered resource"}
    mock_rsc.perform_redfish_get.side_effect = [
        mock_rsc.perform_redfish_get.return_value,
        resource_response,
    ]

    result = operation(mock_rsc)

    assert result.data == resource_response.dict
    assert mock_rsc.mock_calls == [
        call.perform_redfish_get("/redfish/v1/Managers"),
        call.perform_redfish_get(f"/redfish/v1/Managers/controller-uuid{suffix}"),
    ]


@pytest.mark.parametrize(
    "operation,args,method,suffix,body",
    [
        (manager.restart, (), "post", "/Actions/Manager.Reset",
         {"ResetType": "ForceRestart"}),
        (manager.factory_reset, (), "post", "/Actions/Manager.ResetToDefaults",
         {"ResetToDefaultsType": "ResetAll"}),
        (manager.update_manager, ({"DateTime": "2026-10-12T12:00:00Z"},), "patch", "",
         {"DateTime": "2026-10-12T12:00:00Z"}),
        (network.set_manager_network_protocol, ({"NTP": {"ProtocolEnabled": True}},),
         "patch", "/NetworkProtocol", {"NTP": {"ProtocolEnabled": True}}),
        (trusted_cert.delete_trusted_certificate, ("cert-uuid",),
         "delete", "/TrustedCertificates/cert-uuid", None),
    ],
)
def test_manager_writes_use_discovered_uri(mock_rsc, operation, args, method, suffix, body):
    operation(mock_rsc, *args)

    request = getattr(call, f"perform_redfish_{method}")
    uri = f"/redfish/v1/Managers/controller-uuid{suffix}"
    assert mock_rsc.mock_calls == [
        call.perform_redfish_get("/redfish/v1/Managers"),
        request(uri) if body is None else request(uri, body),
    ]


def test_replace_certificate_uses_discovered_uri(mock_rsc, tmp_path):
    cert_file = tmp_path / "cert.pem"
    key_file = tmp_path / "key.pem"
    cert_file.write_text("certificate", encoding="utf-8")
    key_file.write_text("key", encoding="utf-8")

    cert.replace_certificate(mock_rsc, str(cert_file), str(key_file))

    assert mock_rsc.mock_calls == [
        call.perform_redfish_get("/redfish/v1/Managers"),
        call.perform_redfish_post(
            "/redfish/v1/CertificateService/Actions/CertificateService.ReplaceCertificate",
            {
                "CertificateUri": {
                    "@odata.id": (
                        "/redfish/v1/Managers/controller-uuid"
                        "/NetworkProtocol/HTTPS/Certificates/1"
                    )
                },
                "CertificateString": "certificatekey",
                "CertificateType": "PEM",
            },
        ),
    ]


def test_add_trusted_certificate_uses_discovered_uri(mock_rsc, tmp_path):
    cert_file = tmp_path / "cert.pem"
    cert_file.write_text("certificate", encoding="utf-8")

    trusted_cert.add_trusted_certificate(mock_rsc, str(cert_file))

    assert mock_rsc.mock_calls == [
        call.perform_redfish_get("/redfish/v1/Managers"),
        call.perform_redfish_post(
            "/redfish/v1/Managers/controller-uuid/TrustedCertificates",
            {"CertificateString": "certificate", "CertificateType": "PEM"},
        ),
    ]


@pytest.mark.parametrize(
    "operation,args",
    [
        (system.get_system, ()),
        (system.set_system_power, ("On",)),
        (manager.get_manager, ()),
        (manager.restart, ()),
        (manager.factory_reset, ()),
        (manager.update_manager, ({},)),
        (network.get_manager_ethernet_interface, ()),
        (network.set_manager_ethernet_interface, ({},)),
        (network.get_manager_network_protocol, ()),
        (network.set_manager_network_protocol, ({},)),
        (cert.get_certificate, ()),
        (trusted_cert.delete_trusted_certificate, ("cert-uuid",)),
    ],
)
def test_invalid_discovery_stops_operations(mock_rsc, operation, args):
    mock_rsc.perform_redfish_get.return_value.dict = {}

    with pytest.raises(RedfishError, match="missing or invalid Members array"):
        operation(mock_rsc, *args)

    assert mock_rsc.perform_redfish_get.call_count == 1
    mock_rsc.perform_redfish_post.assert_not_called()
    mock_rsc.perform_redfish_patch.assert_not_called()
    mock_rsc.perform_redfish_delete.assert_not_called()
