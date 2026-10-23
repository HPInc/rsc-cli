"""Tests for preferred manager Ethernet interface discovery."""

from unittest.mock import MagicMock, call

import pytest

from hprsctool.comm.operations import network
from hprsctool.comm.remote_system_controller import RedfishError, Rsc

MANAGER_URI = "/redfish/v1/Managers/controller-uuid"
COLLECTION_URI = f"{MANAGER_URI}/EthernetInterfaces"


@pytest.fixture(name="mock_rsc")
def fixture_mock_rsc():
    return MagicMock(spec=Rsc)


def response(data):
    """Create a Redfish response with the given body."""
    return MagicMock(dict=data)


@pytest.mark.parametrize(
    "interface_ids,selected",
    [
        (["eth0", "br0"], "br0"),
        (["br0", "eth0"], "br0"),
        (["br0"], "br0"),
        (["eth1", "eth0"], "eth1"),
    ],
)
@pytest.mark.parametrize("method", ["get", "patch"])
def test_network_operations_select_interface(mock_rsc, interface_ids, selected, method):
    mock_rsc.perform_redfish_get.side_effect = [
        response({"Members": [{"@odata.id": MANAGER_URI}]}),
        response({"Members": [
            {"@odata.id": f"{COLLECTION_URI}/{interface_id}"}
            for interface_id in interface_ids
        ]}),
        response({"Id": selected}),
    ]
    expected_calls = [
        call.perform_redfish_get("/redfish/v1/Managers"),
        call.perform_redfish_get(COLLECTION_URI),
    ]
    if method == "get":
        result = network.get_manager_ethernet_interface(mock_rsc)
        assert result.data == {"Id": selected}
        expected_calls.append(call.perform_redfish_get(f"{COLLECTION_URI}/{selected}"))
    else:
        body = {"HostName": "new-host"}
        result = network.set_manager_ethernet_interface(mock_rsc, body)
        assert result is mock_rsc.perform_redfish_patch.return_value
        expected_calls.append(call.perform_redfish_patch(f"{COLLECTION_URI}/{selected}", body))

    assert mock_rsc.mock_calls == expected_calls


def test_returns_immediately_when_br0_is_found(mock_rsc):
    mock_rsc.perform_redfish_get.side_effect = [
        response({"Members": [{"@odata.id": MANAGER_URI}]}),
        response({
            "Members": [{"@odata.id": f"{COLLECTION_URI}/br0"}, None],
            "Members@odata.nextLink": f"{COLLECTION_URI}?page=2",
        }),
    ]

    assert network.get_manager_ethernet_interface_uri(mock_rsc) == f"{COLLECTION_URI}/br0"
    assert mock_rsc.perform_redfish_get.call_args_list == [
        call("/redfish/v1/Managers"),
        call(COLLECTION_URI),
    ]


@pytest.mark.parametrize(
    "member_uris,expected_uri",
    [
        # br0 as a substring of the leaf is not a br0 match; fall back to first member
        ([f"{COLLECTION_URI}/eth0", f"{COLLECTION_URI}/br0-extra"], f"{COLLECTION_URI}/eth0"),
        ([f"{COLLECTION_URI}/eth0", f"{COLLECTION_URI}/xbr0"], f"{COLLECTION_URI}/eth0"),
        # br0 in a non-leaf path segment does not match
        ([f"{COLLECTION_URI}/eth0", f"{COLLECTION_URI}/br0/eth0"], f"{COLLECTION_URI}/eth0"),
        # a trailing slash on the leaf still matches br0
        ([f"{COLLECTION_URI}/br0/"], f"{COLLECTION_URI}/br0/"),
    ],
)
def test_br0_matches_only_the_uri_leaf(mock_rsc, member_uris, expected_uri):
    mock_rsc.perform_redfish_get.side_effect = [
        response({"Members": [{"@odata.id": MANAGER_URI}]}),
        response({"Members": [{"@odata.id": uri} for uri in member_uris]}),
    ]

    assert network.get_manager_ethernet_interface_uri(mock_rsc) == expected_uri


def test_falls_back_to_first_member_when_br0_is_absent(mock_rsc):
    mock_rsc.perform_redfish_get.side_effect = [
        response({"Members": [{"@odata.id": MANAGER_URI}]}),
        response({"Members": [
            {"@odata.id": f"{COLLECTION_URI}/eth1"},
            {"@odata.id": f"{COLLECTION_URI}/eth0"},
        ]}),
    ]

    assert network.get_manager_ethernet_interface_uri(mock_rsc) == f"{COLLECTION_URI}/eth1"


def test_raises_when_collection_has_no_members(mock_rsc):
    mock_rsc.perform_redfish_get.side_effect = [
        response({"Members": [{"@odata.id": MANAGER_URI}]}),
        response({"Members": []}),
    ]

    with pytest.raises(RedfishError, match="No Ethernet interfaces found"):
        network.get_manager_ethernet_interface_uri(mock_rsc)


@pytest.mark.parametrize("failure_stage", ["collection", "get", "patch"])
def test_request_errors_do_not_trigger_fallback(mock_rsc, failure_stage):
    error = RedfishError("Request failed")
    responses = [
        response({"Members": [{"@odata.id": MANAGER_URI}]}),
        response({"Members": [
            {"@odata.id": f"{COLLECTION_URI}/eth0"},
            {"@odata.id": f"{COLLECTION_URI}/br0"},
        ]}),
    ]
    if failure_stage == "collection":
        responses[1] = error
    elif failure_stage == "get":
        responses.append(error)
    else:
        mock_rsc.perform_redfish_patch.side_effect = error
    mock_rsc.perform_redfish_get.side_effect = responses

    with pytest.raises(RedfishError, match="Request failed"):
        if failure_stage == "get":
            network.get_manager_ethernet_interface(mock_rsc)
        else:
            network.set_manager_ethernet_interface(mock_rsc, {})

    assert call(f"{COLLECTION_URI}/eth0") not in mock_rsc.perform_redfish_get.call_args_list
    assert not any(
        request.args[0] == f"{COLLECTION_URI}/eth0"
        for request in mock_rsc.perform_redfish_patch.call_args_list
    )
