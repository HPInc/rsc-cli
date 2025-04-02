"""Module defining the ManagerNetworkProtocol class"""

from typing import List


class NTPSettings:
    """NTP settings model"""

    def __init__(self, data: dict) -> None:
        if data is None:
            raise ValueError("data is required")
        self.data = data

    @property
    def ntp_servers(self) -> List[str]:
        """Get the NTP servers"""
        return self.data.get("NTPServers", [])

    @property
    def ntp_protocol_enabled(self) -> bool | None:
        """Get the NTP protocol enabled"""
        return self.data.get("ProtocolEnabled", None)


class ProxySettings:
    """Proxy settings model"""

    def __init__(self, data: dict) -> None:
        if data is None:
            raise ValueError("data is required")
        self.data = data

    @property
    def proxy_enabled(self) -> bool | None:
        """Get the proxy enabled"""
        return self.data.get("Enabled", None)

    @property
    def exclude_addresses(self) -> List[str]:
        """Get the exclude addresses"""
        return self.data.get("ExcludeAddresses", [])

    @property
    def password_set(self) -> bool | None:
        """Get the password set"""
        return self.data.get("PasswordSet", None)

    @property
    def proxy_server_uri(self) -> str:
        """Get the proxy server URI"""
        return self.data.get("ProxyServerURI", "N/A")

    @property
    def username(self) -> str:
        """Get the username"""
        return self.data.get("Username", "N/A")


class ManagerNetworkProtocol:
    """Manager network protocol model"""

    def __init__(self, data: dict) -> None:
        if data is None:
            raise ValueError("data is required")
        self.data = data
        self.ntp = NTPSettings(data.get("NTP", {}))
        self.proxy = ProxySettings(data.get("Proxy", {}))

    @property
    def host_name(self) -> str:
        """Get the host name"""
        return self.data.get("HostName", "N/A")

    @property
    def ntp_settings(self) -> NTPSettings:
        """Get the NTP settings"""
        return self.ntp

    @property
    def mdns_protocol_enabled(self) -> bool | None:
        """Get the mDNS protocol enabled"""
        if (
            "Oem" in self.data
            and "HP" in self.data["Oem"]
            and "mDNSDiscoveryProtocol" in self.data["Oem"]["HP"]
        ):
            return self.data["Oem"]["HP"]["mDNSDiscoveryProtocol"].get(
                "ProtocolEnabled", None
            )
        return None

    @property
    def proxy_settings(self) -> ProxySettings:
        """Get the proxy settings"""
        return self.proxy
