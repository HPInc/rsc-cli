"""Tests for models"""

import pytest

from hprsctool.models import (
    certificate,
    ethernet_interface,
    manager as manager_model,
    manager_network_protocol,
    system as system_model,
    task as task_model,
)


def test_certificate_constructor():
    cert = certificate.Certificate(
        {
            "CertificateString": "TestCert",
            "CertificateType": "TestCertType",
            "ValidNotAfter": "TestCertExpiration",
            "Id": "TestCertId",
            "Fingerprint": "TestCertFingerprint",
        }
    )
    assert cert.certificate_expiration == "TestCertExpiration"
    assert cert.certificate_id == "TestCertId"
    assert cert.certificate_fingerprint == "TestCertFingerprint"
    assert cert.certificate == "TestCert"
    assert cert.certificate_type == "TestCertType"


def test_certificate_str():
    cert = certificate.Certificate(
        {
            "CertificateString": "TestCert",
            "CertificateType": "TestCertType",
            "ValidNotAfter": "TestCertExpiration",
            "Id": "TestCertId",
            "Fingerprint": "TestCertFingerprint",
        }
    )
    expected_str = (
        "ID: TestCertId\n"
        "Certificate:\nTestCert\n"
        "Type: TestCertType\n"
        "Expiration: TestCertExpiration\n"
        "Fingerprint: TestCertFingerprint"
    )
    assert str(cert) == expected_str


def test_redfish_address_constructor():
    data = {
        "Address": "192.168.1.1",
        "SubnetMask": "255.255.255.0",
        "Gateway": "192.168.1.254",
        "AddressOrigin": "Static",
    }
    address = ethernet_interface.RedfishAddress(data)
    assert address.address == "192.168.1.1"
    assert address.subnet_mask == "255.255.255.0"
    assert address.gateway == "192.168.1.254"
    assert address.origin == "Static"


def test_redfish_address_constructor_no_data():
    with pytest.raises(ValueError, match="RedfishAddress: data is empty"):
        ethernet_interface.RedfishAddress(None)


def test_redfish_address_missing_keys():
    data = {}
    address = ethernet_interface.RedfishAddress(data)
    assert address.address == "N/A"
    assert address.subnet_mask == "N/A"
    assert address.gateway == "N/A"
    assert address.origin == "N/A"


def test_ethernet_interface_constructor():
    data = {
        "HostName": "test-host",
        "MACAddress": "00:1A:2B:3C:4D:5E",
        ethernet_interface.DHCPV4_KEY: {
            ethernet_interface.DHCP_ENABLED_KEY: True,
            ethernet_interface.USE_DNS_SERVERS_KEY: True,
        },
        "IPv4Addresses": [
            {
                "Address": "192.168.1.10",
                "SubnetMask": "255.255.255.0",
                "Gateway": "192.168.1.1",
                "AddressOrigin": "Static",
            }
        ],
        "IPv4StaticAddresses": [
            {
                "Address": "192.168.1.20",
                "SubnetMask": "255.255.255.0",
                "Gateway": "192.168.1.1",
                "AddressOrigin": "Static",
            }
        ],
        "NameServers": ["8.8.8.8", "8.8.4.4"],
        "StaticNameServers": ["1.1.1.1", "1.0.0.1"],
    }
    eth_interface = ethernet_interface.EthernetInterface(data)
    assert eth_interface.hostname == "test-host"
    assert eth_interface.mac_address == "00:1A:2B:3C:4D:5E"
    assert eth_interface.dhcp is True
    assert eth_interface.use_dns_servers is True
    assert len(eth_interface.ips) == 1
    assert isinstance(eth_interface.ips[0], ethernet_interface.RedfishAddress)
    assert eth_interface.ips[0].address == "192.168.1.10"
    assert eth_interface.ips[0].subnet_mask == "255.255.255.0"
    assert eth_interface.ips[0].gateway == "192.168.1.1"
    assert eth_interface.ips[0].origin == "Static"
    assert len(eth_interface.static_ips) == 1
    assert isinstance(eth_interface.static_ips[0], ethernet_interface.RedfishAddress)
    assert eth_interface.static_ips[0].address == "192.168.1.20"
    assert eth_interface.static_ips[0].subnet_mask == "255.255.255.0"
    assert eth_interface.static_ips[0].gateway == "192.168.1.1"
    assert eth_interface.static_ips[0].origin == "Static"
    assert eth_interface.name_servers == ["8.8.8.8", "8.8.4.4"]
    assert eth_interface.static_name_servers == ["1.1.1.1", "1.0.0.1"]


def test_ethernet_interface_constructor_no_data():
    with pytest.raises(ValueError, match="EthernetInterface: data is empty"):
        ethernet_interface.EthernetInterface(None)


def test_ethernet_interface_missing_keys():
    data = {}
    eth_interface = ethernet_interface.EthernetInterface(data)
    assert eth_interface.hostname == "N/A"
    assert eth_interface.mac_address == "N/A"
    assert eth_interface.dhcp is False
    assert eth_interface.use_dns_servers is False
    assert eth_interface.ips == []
    assert eth_interface.static_ips == []
    assert eth_interface.name_servers == []
    assert eth_interface.static_name_servers == []


def test_manager_network_protocol_constructor():
    data = {
        "HostName": "test-host",
        "NTP": {
            "NTPServers": ["ntp1.example.com", "ntp2.example.com"],
            "ProtocolEnabled": True,
        },
        "Proxy": {
            "Enabled": True,
            "ExcludeAddresses": ["192.168.1.1", "192.168.1.2"],
            "PasswordSet": True,
            "ProxyServerURI": "http://proxy.example.com",
            "Username": "user",
        },
        "Oem": {"HP": {"mDNSDiscoveryProtocol": {"ProtocolEnabled": True}}},
    }
    protocol = manager_network_protocol.ManagerNetworkProtocol(data)
    assert protocol.host_name == "test-host"
    assert protocol.ntp.ntp_servers == ["ntp1.example.com", "ntp2.example.com"]
    assert protocol.ntp.ntp_protocol_enabled is True
    assert protocol.proxy.proxy_enabled is True
    assert protocol.proxy.exclude_addresses == ["192.168.1.1", "192.168.1.2"]
    assert protocol.proxy.password_set is True
    assert protocol.proxy.proxy_server_uri == "http://proxy.example.com"
    assert protocol.proxy.username == "user"
    assert protocol.mdns_protocol_enabled is True


def test_manager_network_protocol_constructor_no_data():
    protocol = manager_network_protocol.ManagerNetworkProtocol({})
    assert protocol.host_name == "N/A"
    assert protocol.ntp.ntp_servers == []
    assert protocol.ntp.ntp_protocol_enabled is None
    assert protocol.proxy.proxy_enabled is None
    assert protocol.proxy.exclude_addresses == []
    assert protocol.proxy.password_set is None
    assert protocol.proxy.proxy_server_uri == "N/A"
    assert protocol.proxy.username == "N/A"
    assert protocol.mdns_protocol_enabled is None


def test_manager_network_protocol_missing_keys():
    data = {"HostName": "test-host"}
    protocol = manager_network_protocol.ManagerNetworkProtocol(data)
    assert protocol.host_name == "test-host"
    assert protocol.ntp.ntp_servers == []
    assert protocol.ntp.ntp_protocol_enabled is None
    assert protocol.proxy.proxy_enabled is None
    assert protocol.proxy.exclude_addresses == []
    assert protocol.proxy.password_set is None
    assert protocol.proxy.proxy_server_uri == "N/A"
    assert protocol.proxy.username == "N/A"
    assert protocol.mdns_protocol_enabled is None


def test_ntp_settings_constructor():
    data = {
        "NTPServers": ["ntp1.example.com", "ntp2.example.com"],
        "ProtocolEnabled": True,
    }
    ntp_settings = manager_network_protocol.NTPSettings(data)
    assert ntp_settings.ntp_servers == ["ntp1.example.com", "ntp2.example.com"]
    assert ntp_settings.ntp_protocol_enabled is True


def test_ntp_settings_constructor_no_data():
    ntp_settings = manager_network_protocol.NTPSettings({})
    assert ntp_settings.ntp_servers == []
    assert ntp_settings.ntp_protocol_enabled is None


def test_ntp_settings_missing_keys():
    data = {"NTPServers": ["ntp1.example.com"]}
    ntp_settings = manager_network_protocol.NTPSettings(data)
    assert ntp_settings.ntp_servers == ["ntp1.example.com"]
    assert ntp_settings.ntp_protocol_enabled is None


def test_proxy_settings_constructor():
    data = {
        "Enabled": True,
        "ExcludeAddresses": ["192.168.1.1", "192.168.1.2"],
        "PasswordSet": True,
        "ProxyServerURI": "http://proxy.example.com",
        "Username": "user",
    }
    proxy_settings = manager_network_protocol.ProxySettings(data)
    assert proxy_settings.proxy_enabled is True
    assert proxy_settings.exclude_addresses == ["192.168.1.1", "192.168.1.2"]
    assert proxy_settings.password_set is True
    assert proxy_settings.proxy_server_uri == "http://proxy.example.com"
    assert proxy_settings.username == "user"


def test_proxy_settings_constructor_no_data():
    proxy_settings = manager_network_protocol.ProxySettings({})
    assert proxy_settings.proxy_enabled is None
    assert proxy_settings.exclude_addresses == []
    assert proxy_settings.password_set is None
    assert proxy_settings.proxy_server_uri == "N/A"
    assert proxy_settings.username == "N/A"


def test_proxy_settings_missing_keys():
    data = {"Enabled": True}
    proxy_settings = manager_network_protocol.ProxySettings(data)
    assert proxy_settings.proxy_enabled is True
    assert proxy_settings.exclude_addresses == []
    assert proxy_settings.password_set is None
    assert proxy_settings.proxy_server_uri == "N/A"
    assert proxy_settings.username == "N/A"


def test_manager_constructor():
    data = {
        "FirmwareVersion": "1.0.0",
        "SerialNumber": "123456789",
        "Model": "TestModel",
        "DateTime": "2023-01-01T00:00:00Z",
        "DateTimeLocalOffset": "+00:00",
        "Oem": {
            "HP": {
                "KVMSettings": {
                    "DisableVideoOnKVMIdle": True,
                    "DisableCollaboration": False,
                    "DisableCollaborationAuthorization": True,
                    "PortRangeBegin": 5900,
                    "PortRangeEnd": 5999,
                },
                "HPRemoteSystemManagerBindingStatus": {
                    "BindingStatus": "Bound",
                    "Organization": "TestOrg",
                },
            }
        },
    }
    manager = manager_model.Manager(data)
    assert manager.firmware_version == "1.0.0"
    assert manager.serial_number == "123456789"
    assert manager.model == "TestModel"
    assert manager.date_time == "2023-01-01T00:00:00Z"
    assert manager.date_time_offset == "+00:00"
    assert isinstance(manager.kvm_settings, manager_model.KVMSettings)
    assert manager.kvm_settings.disable_video_on_kvm_idle is True
    assert manager.kvm_settings.disable_collaboration is False
    assert manager.kvm_settings.disable_collaboration_authorization is True
    assert manager.kvm_settings.port_range_begin == 5900
    assert manager.kvm_settings.port_range_end == 5999
    assert isinstance(manager.rsm_status, manager_model.RSMStatus)
    assert manager.rsm_status.binding_status == "Bound"
    assert manager.rsm_status.organization == "TestOrg"


def test_manager_constructor_no_data():
    manager = manager_model.Manager({})
    assert manager.firmware_version == "N/A"
    assert manager.serial_number == "N/A"
    assert manager.model == "N/A"
    assert manager.date_time == "N/A"
    assert manager.date_time_offset == "N/A"
    assert manager.kvm_settings is None
    assert manager.rsm_status is None


def test_manager_constructor_missing_keys():
    data = {
        "FirmwareVersion": "1.0.0",
        "SerialNumber": "123456789",
    }
    manager = manager_model.Manager(data)
    assert manager.firmware_version == "1.0.0"
    assert manager.serial_number == "123456789"
    assert manager.model == "N/A"
    assert manager.date_time == "N/A"
    assert manager.date_time_offset == "N/A"
    assert manager.kvm_settings is None
    assert manager.rsm_status is None


def test_manager_kvm_settings_no_data():
    data = {"Oem": {"HP": {"KVMSettings": {}}}}
    manager = manager_model.Manager(data)
    assert isinstance(manager.kvm_settings, manager_model.KVMSettings)
    assert manager.kvm_settings.disable_video_on_kvm_idle is None
    assert manager.kvm_settings.disable_collaboration is None
    assert manager.kvm_settings.disable_collaboration_authorization is None
    assert manager.kvm_settings.port_range_begin is None
    assert manager.kvm_settings.port_range_end is None


def test_manager_rsm_status_no_data():
    data = {"Oem": {"HP": {"HPRemoteSystemManagerBindingStatus": {}}}}
    manager = manager_model.Manager(data)
    assert isinstance(manager.rsm_status, manager_model.RSMStatus)
    assert manager.rsm_status.binding_status == "N/A"
    assert manager.rsm_status.organization == "N/A"


def test_rsm_status_constructor():
    data = {"BindingStatus": "Bound", "Organization": "TestOrg"}
    rsm_status = manager_model.RSMStatus(data)
    assert rsm_status.binding_status == "Bound"
    assert rsm_status.organization == "TestOrg"


def test_rsm_status_constructor_no_data():
    rsm_status = manager_model.RSMStatus({})
    assert rsm_status.binding_status == "N/A"
    assert rsm_status.organization == "N/A"


def test_rsm_status_missing_keys():
    data = {"BindingStatus": "Bound"}
    rsm_status = manager_model.RSMStatus(data)
    assert rsm_status.binding_status == "Bound"
    assert rsm_status.organization == "N/A"


def test_kvm_settings_constructor():
    data = {
        "DisableVideoOnKVMIdle": True,
        "DisableCollaboration": False,
        "DisableCollaborationAuthorization": True,
        "PortRangeBegin": 5900,
        "PortRangeEnd": 5999,
    }
    kvm_settings = manager_model.KVMSettings(data)
    assert kvm_settings.disable_video_on_kvm_idle is True
    assert kvm_settings.disable_collaboration is False
    assert kvm_settings.disable_collaboration_authorization is True
    assert kvm_settings.port_range_begin == 5900
    assert kvm_settings.port_range_end == 5999


def test_kvm_settings_constructor_no_data():
    with pytest.raises(ValueError, match="data is required"):
        manager_model.KVMSettings(None)


def test_kvm_settings_missing_keys():
    data = {}
    kvm_settings = manager_model.KVMSettings(data)
    assert kvm_settings.disable_video_on_kvm_idle is None
    assert kvm_settings.disable_collaboration is None
    assert kvm_settings.disable_collaboration_authorization is None
    assert kvm_settings.port_range_begin is None
    assert kvm_settings.port_range_end is None


def test_system_constructor():
    manufacturer = "HP"
    model = "HP Z2 Mini G9 Workstation Desktop PC"
    bios_version = "U50 Ver. 03.01.03"
    uuid = "0e96098987c04177b34d75648eae4820"
    serial_number = "MXL3034KDW"
    asset_tag = "Z2 7th floor, cube 17"
    processor_core_count = 12
    processor_count = 1
    processor_model = "12th Gen Intel(R) Core(TM) i7-12700"
    memory_total_system_memory_gib = 16
    power_state = "On"
    indicator_led = "Off"
    health = "OK"
    main_board_adapter_state = "Connected"
    boot_state = "Booted"
    blink_code_type = "Power"
    blink_code_major = 0
    blink_code_minor = 0
    blink_code_message_id = "HPBlinkCode.1.1.0.NoError"
    boot_source_override_target = "None"

    system_under_test = system_model.System(
        {
            "Manufacturer": manufacturer,
            "Model": model,
            "BiosVersion": bios_version,
            "UUID": uuid,
            "SerialNumber": serial_number,
            "AssetTag": asset_tag,
            "ProcessorSummary": {
                "CoreCount": processor_core_count,
                "Count": processor_count,
                "Model": processor_model,
            },
            "MemorySummary": {"TotalSystemMemoryGiB": memory_total_system_memory_gib},
            "PowerState": power_state,
            "IndicatorLED": indicator_led,
            "Status": {"Health": health},
            "Oem": {
                "HP": {
                    "MainBoardAdapterState": main_board_adapter_state,
                    "BootState": boot_state,
                    "BlinkCodeState": {
                        "Type": blink_code_type,
                        "Major": blink_code_major,
                        "Minor": blink_code_minor,
                        "MessageId": blink_code_message_id,
                    },
                }
            },
            "Boot": {"BootSourceOverrideTarget": boot_source_override_target},
        }
    )

    assert system_under_test.manufacturer == manufacturer
    assert system_under_test.model == model
    assert system_under_test.bios_version == bios_version
    assert system_under_test.uuid == uuid
    assert system_under_test.serial_number == serial_number
    assert system_under_test.asset_tag == asset_tag
    assert system_under_test.processor_summary.core_count == processor_core_count
    assert system_under_test.processor_summary.count == processor_count
    assert system_under_test.processor_summary.model == processor_model
    assert (
        system_under_test.memory_summary.total_system_memory_gib
        == memory_total_system_memory_gib
    )
    assert system_under_test.power_state == power_state
    assert system_under_test.indicator_led == indicator_led
    assert system_under_test.health == health
    assert system_under_test.main_board_adapter_state == main_board_adapter_state
    assert system_under_test.boot_state == boot_state
    assert system_under_test.blink_code_state.type == blink_code_type
    assert system_under_test.blink_code_state.major == blink_code_major
    assert system_under_test.blink_code_state.minor == blink_code_minor
    assert system_under_test.blink_code_state.message_id == blink_code_message_id
    assert system_under_test.boot_source_override_target == boot_source_override_target


def test_system_constructor_no_data():
    system_under_test = system_model.System({})

    assert system_under_test.manufacturer == "N/A"
    assert system_under_test.model == "N/A"
    assert system_under_test.bios_version == "N/A"
    assert system_under_test.uuid == "N/A"
    assert system_under_test.serial_number == "N/A"
    assert system_under_test.asset_tag == "N/A"
    assert system_under_test.processor_summary.core_count == "N/A"
    assert system_under_test.processor_summary.count == "N/A"
    assert system_under_test.processor_summary.model == "N/A"
    assert system_under_test.memory_summary.total_system_memory_gib == "N/A"
    assert system_under_test.power_state == "N/A"
    assert system_under_test.indicator_led == "N/A"
    assert system_under_test.health == "N/A"
    assert system_under_test.main_board_adapter_state == "N/A"
    assert system_under_test.boot_state == "N/A"
    assert system_under_test.blink_code_state.type == "N/A"
    assert system_under_test.blink_code_state.major == "N/A"
    assert system_under_test.blink_code_state.minor == "N/A"
    assert system_under_test.blink_code_state.message_id == "N/A"
    assert system_under_test.boot_source_override_target == "N/A"


def test_blink_code_state_constructor():
    data = {
        "Type": "Power",
        "Major": 1,
        "Minor": 2,
        "MessageId": "HPBlinkCode.1.1.0.Error",
    }
    blink_code_state = system_model.BlinkCodeState(data)
    assert blink_code_state.type == "Power"
    assert blink_code_state.major == 1
    assert blink_code_state.minor == 2
    assert blink_code_state.message_id == "HPBlinkCode.1.1.0.Error"


def test_blink_code_state_constructor_no_data():
    blink_code_state = system_model.BlinkCodeState({})
    assert blink_code_state.type == "N/A"
    assert blink_code_state.major == "N/A"
    assert blink_code_state.minor == "N/A"
    assert blink_code_state.message_id == "N/A"


def test_blink_code_state_missing_keys():
    data = {"Type": "Power"}
    blink_code_state = system_model.BlinkCodeState(data)
    assert blink_code_state.type == "Power"
    assert blink_code_state.major == "N/A"
    assert blink_code_state.minor == "N/A"
    assert blink_code_state.message_id == "N/A"


def test_memory_summary_constructor():
    data = {"TotalSystemMemoryGiB": 16}
    memory_summary = system_model.MemorySummary(data)
    assert memory_summary.total_system_memory_gib == 16


def test_memory_summary_constructor_no_data():
    memory_summary = system_model.MemorySummary({})
    assert memory_summary.total_system_memory_gib == "N/A"


def test_memory_summary_constructor_none_data():
    with pytest.raises(ValueError, match="data is required"):
        system_model.MemorySummary(None)


def test_processor_summary_constructor():
    data = {"CoreCount": 12, "Count": 1, "Model": "12th Gen Intel(R) Core(TM) i7-12700"}
    processor_summary = system_model.ProcessorSummary(data)
    assert processor_summary.core_count == 12
    assert processor_summary.count == 1
    assert processor_summary.model == "12th Gen Intel(R) Core(TM) i7-12700"


def test_processor_summary_constructor_no_data():
    processor_summary = system_model.ProcessorSummary({})
    assert processor_summary.core_count == "N/A"
    assert processor_summary.count == "N/A"
    assert processor_summary.model == "N/A"


def test_processor_summary_missing_keys():
    data = {"CoreCount": 12}
    processor_summary = system_model.ProcessorSummary(data)
    assert processor_summary.core_count == 12
    assert processor_summary.count == "N/A"
    assert processor_summary.model == "N/A"


def test_processor_summary_constructor_none():
    with pytest.raises(ValueError, match="data is required"):
        system_model.ProcessorSummary(None)


def test_task_constructor():
    data = {
        "Id": "Task1",
        "TaskMonitor": "/redfish/v1/TaskService/Tasks/Task1",
        "StartTime": "2023-01-01T00:00:00Z",
        "EndTime": "2023-01-01T01:00:00Z",
        "TaskState": "Running",
        "TaskStatus": "OK",
        "Name": "Sample Task",
    }
    task = task_model.Task(data)
    assert task.task_id == "Task1"
    assert task.task_monitor == "/redfish/v1/TaskService/Tasks/Task1"
    assert task.start_time == "2023-01-01T00:00:00Z"
    assert task.end_time == "2023-01-01T01:00:00Z"
    assert task.task_state == "Running"
    assert task.task_status == "OK"
    assert task.name == "Sample Task"


def test_task_constructor_no_data():
    with pytest.raises(ValueError, match="data is required"):
        task_model.Task(None)


def test_task_missing_keys():
    data = {}
    task = task_model.Task(data)
    assert task.task_id == "N/A"
    assert task.task_monitor == "N/A"
    assert task.start_time == "N/A"
    assert task.end_time == "N/A"
    assert task.task_state == "N/A"
    assert task.task_status == "N/A"
    assert task.name == "N/A"


def test_task_str():
    data = {
        "Id": "Task1",
        "TaskMonitor": "/redfish/v1/TaskService/Tasks/Task1",
        "StartTime": "2023-01-01T00:00:00Z",
        "EndTime": "2023-01-01T01:00:00Z",
        "TaskState": "Running",
        "TaskStatus": "OK",
        "Name": "Sample Task",
    }
    task = task_model.Task(data)
    expected_str = (
        "Task Task1:\n"
        "\tName: Sample Task\n"
        "\tState: Running\n"
        "\tStatus: OK\n"
        "\tStart time: 2023-01-01T00:00:00Z\n"
        "\tEnd time: 2023-01-01T01:00:00Z\n"
        "\tMonitor: /redfish/v1/TaskService/Tasks/Task1"
    )
    assert str(task) == expected_str


def test_task_collection_constructor():
    data = {
        "Members": [
            {"@odata.id": "/redfish/v1/TaskService/Tasks/Task1"},
            {"@odata.id": "/redfish/v1/TaskService/Tasks/Task2"},
        ]
    }
    task_collection = task_model.TaskCollection(data)
    assert len(task_collection.members) == 2
    assert task_collection.members[0] == "/redfish/v1/TaskService/Tasks/Task1"
    assert task_collection.members[1] == "/redfish/v1/TaskService/Tasks/Task2"


def test_task_collection_constructor_no_data():
    with pytest.raises(ValueError, match="data is required"):
        task_model.TaskCollection(None)


def test_task_collection_constructor_empty_members():
    data = {}
    task_collection = task_model.TaskCollection(data)
    assert len(task_collection.members) == 0


def test_task_collection_str():
    data = {
        "Members": [
            {"@odata.id": "/redfish/v1/TaskService/Tasks/Task1"},
            {"@odata.id": "/redfish/v1/TaskService/Tasks/Task2"},
        ]
    }
    task_collection = task_model.TaskCollection(data)
    assert str(task_collection) == "TaskCollection with 2 tasks"


def test_task_collection_iter():
    data = {
        "Members": [
            {"@odata.id": "/redfish/v1/TaskService/Tasks/Task1"},
            {"@odata.id": "/redfish/v1/TaskService/Tasks/Task2"},
        ]
    }
    task_collection = task_model.TaskCollection(data)
    members = list(iter(task_collection))
    assert len(members) == 2
    assert members[0] == "/redfish/v1/TaskService/Tasks/Task1"
    assert members[1] == "/redfish/v1/TaskService/Tasks/Task2"
