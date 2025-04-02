"""manager models"""


class KVMSettings:
    """Class defining KVM settings"""

    def __init__(self, data: dict):
        if data is None:
            raise ValueError("data is required")
        self.data = data

    @property
    def disable_video_on_kvm_idle(self):
        return self.data.get("DisableVideoOnKVMIdle", None)

    @property
    def disable_collaboration(self):
        return self.data.get("DisableCollaboration", None)

    @property
    def disable_collaboration_authorization(self):
        return self.data.get("DisableCollaborationAuthorization", None)

    @property
    def port_range_begin(self):
        return self.data.get("PortRangeBegin", None)

    @property
    def port_range_end(self):
        return self.data.get("PortRangeEnd", None)


class RSMStatus:
    """Class defining RSM status"""

    def __init__(self, data: dict):
        if data is None:
            raise ValueError("data is required")
        self.data = data

    @property
    def binding_status(self):
        return self.data.get("BindingStatus", "N/A")

    @property
    def organization(self):
        return self.data.get("Organization", "N/A")


class Manager:
    """Class defining a Manager"""

    def __init__(self, data: dict):
        if data is None:
            raise ValueError("data is required")
        self.data = data

    @property
    def firmware_version(self) -> str:
        return self.data.get("FirmwareVersion", "N/A")

    @property
    def serial_number(self) -> str:
        return self.data.get("SerialNumber", "N/A")

    @property
    def model(self) -> str:
        return self.data.get("Model", "N/A")

    @property
    def kvm_settings(self) -> KVMSettings | None:
        if (
            "Oem" in self.data
            and "HP" in self.data["Oem"]
            and "KVMSettings" in self.data["Oem"]["HP"]
        ):
            return KVMSettings(self.data["Oem"]["HP"]["KVMSettings"])
        return None

    @property
    def rsm_status(self) -> RSMStatus | None:
        if (
            "Oem" in self.data
            and "HP" in self.data["Oem"]
            and "HPRemoteSystemManagerBindingStatus" in self.data["Oem"]["HP"]
        ):
            return RSMStatus(
                self.data["Oem"]["HP"]["HPRemoteSystemManagerBindingStatus"]
            )
        return None

    @property
    def date_time(self) -> str:
        return self.data.get("DateTime", "N/A")

    @property
    def date_time_offset(self) -> str:
        return self.data.get("DateTimeLocalOffset", "N/A")
