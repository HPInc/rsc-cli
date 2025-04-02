"""Module defining the EthernetInterface class"""


DHCPV4_KEY = "DHCPv4"
DHCP_ENABLED_KEY = "DHCPEnabled"
USE_DNS_SERVERS_KEY = "UseDNSServers"
IPV4_ADDRESSES_KEY = "IPv4Addresses"
IPV4_ADDRESS_KEY = "IPv4Address"
STATIC_IPV4_ADDRESSES_KEY = "IPv4StaticAddresses"
NAME_SERVERS_KEY = "NameServers"
STATIC_NAME_SERVERS_KEY = "StaticNameServers"
HOST_NAME_KEY = "HostName"
MAC_ADDRESS_KEY = "MACAddress"
ADDRESS_KEY = "Address"
SUBNET_MASK_KEY = "SubnetMask"
GATEWAY_KEY = "Gateway"
ADDRESS_ORIGIN_KEY = "AddressOrigin"


class RedfishAddress:
    """Class defining a Redfish address"""

    def __init__(self, data: dict):
        if data is None:
            raise ValueError("RedfishAddress: data is empty")
        self.data = data

    @property
    def address(self):
        return self.data.get(ADDRESS_KEY, "N/A")

    @property
    def subnet_mask(self):
        return self.data.get(SUBNET_MASK_KEY, "N/A")

    @property
    def gateway(self):
        return self.data.get(GATEWAY_KEY, "N/A")

    @property
    def origin(self):
        return self.data.get(ADDRESS_ORIGIN_KEY, "N/A")


class EthernetInterface:
    """Class defining the EthernetInterface Redfish type"""

    def __init__(self, data: dict):
        if data is None:
            raise ValueError("EthernetInterface: data is empty")
        self.data = data

    @property
    def hostname(self) -> str:
        return self.data.get(HOST_NAME_KEY, "N/A")

    @property
    def mac_address(self) -> str:
        return self.data.get(MAC_ADDRESS_KEY, "N/A")

    @property
    def dhcp(self) -> bool:
        return self.data.get(DHCPV4_KEY, {}).get(
            DHCP_ENABLED_KEY, False
        )

    @property
    def use_dns_servers(self) -> bool:
        return self.data.get(DHCPV4_KEY, {}).get(
            USE_DNS_SERVERS_KEY, False
        )

    @property
    def ips(self) -> list:
        return [
            RedfishAddress(i)
            for i in self.data.get(IPV4_ADDRESSES_KEY, [])
        ]

    @property
    def static_ips(self) -> list:
        return [
            RedfishAddress(i)
            for i in self.data.get(STATIC_IPV4_ADDRESSES_KEY, [])
        ]

    @property
    def name_servers(self) -> list:
        return self.data.get(NAME_SERVERS_KEY, [])

    @property
    def static_name_servers(self) -> list:
        return self.data.get(STATIC_NAME_SERVERS_KEY, [])
