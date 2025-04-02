"""Module defining system structures"""

from typing import Any, Dict


SAMPLE_SYSTEM_JSON = """{
  "@odata.type": "#ComputerSystem.v1_20_0.ComputerSystem",
  "@odata.id": "/redfish/v1/Systems/1",
  "Name": "Computer System",
  "Id": "1",
  "IndicatorLED": "Off",
  "PowerState": "On",
  "Status": {
    "Health": "OK",
    "Condition": {}
  },
  "LogServices": {
    "@odata.id": "/redfish/v1/Systems/1/LogServices"
  },
  "VirtualMedia": {
    "@odata.id": "/redfish/v1/Systems/1/VirtualMedia"
  },
  "Actions": {
    "#ComputerSystem.Reset": {
      "target": "/redfish/v1/Systems/1/Actions/ComputerSystem.Reset",
      "ResetType@Redfish.AllowableValues": [
        "On",
        "GracefulShutdown",
        "ForceOff",
        "GracefulRestart",
        "ForceRestart"
      ]
    }
  },
  "Links": {
    "ManagedBy": [
      {
        "@odata.id": "/redfish/v1/Managers/1"
      }
    ]
  },
  "Bios": {
    "@odata.id": "/redfish/v1/Systems/1/Bios"
  },
  "Boot": {
    "BootSourceOverrideTarget": "None",
    "BootSourceOverrideTarget@Redfish.AllowableValues": [
      "None",
      "BiosSetup"
    ]
  },
  "Oem": {
    "HP": {
      "@odata.type": "#HP_ComputerSystem.v23_5_0.ComputerSystem",
      "MainBoardAdapterState": "Connected",
      "PowerState": "On",
      "BootState": "Booted",
      "BlinkCodeState": {
        "Type": "Power",
        "Major": 0,
        "Minor": 0,
        "MessageId": "HPBlinkCode.1.1.0.NoError"
      }
    }
  },
  "Manufacturer": "HP",
  "Model": "HP Z2 Mini G9 Workstation Desktop PC",
  "BiosVersion": "U50 Ver. 03.01.03",
  "UUID": "0e96098987c04177b34d75648eae4820",
  "SerialNumber": "MXL3034KDW",
  "AssetTag": "Z2 7th floor, cube 17",
  "Processors": {
    "@odata.id": "/redfish/v1/Systems/1/Processors"
  },
  "Memory": {
    "@odata.id": "/redfish/v1/Systems/1/Memory"
  },
  "MemorySummary": {
    "TotalSystemMemoryGiB": 16
  },
  "ProcessorSummary": {
    "CoreCount": 12,
    "Count": 1,
    "Model": "12th Gen Intel(R) Core(TM) i7-12700"
  }
}"""


class ProcessorSummary:
    """Class defining a processor summary"""

    def __init__(self, data: dict):
        if data is None:
            raise ValueError("data is required")
        self.data = data

    @property
    def core_count(self):
        return self.data.get("CoreCount", "N/A")

    @property
    def count(self):
        return self.data.get("Count", "N/A")

    @property
    def model(self):
        return self.data.get("Model", "N/A")


# pylint: disable=too-few-public-methods
class MemorySummary:
    """Class defining a memory summary"""

    def __init__(self, data: dict):
        if data is None:
            raise ValueError("data is required")
        self.data = data

    @property
    def total_system_memory_gib(self):
        return self.data.get("TotalSystemMemoryGiB", "N/A")


class BlinkCodeState:
    """Class defining a blink code state"""

    def __init__(self, data: dict):
        if data is None:
            raise ValueError("data is required")
        self.data = data

    @property
    def type(self):
        return self.data.get("Type", "N/A")

    @property
    def major(self):
        return self.data.get("Major", "N/A")

    @property
    def minor(self):
        return self.data.get("Minor", "N/A")

    @property
    def message_id(self):
        return self.data.get("MessageId", "N/A")


class System:
    """Class defining a system"""

    def __init__(self, data: Dict[str, Any]):
        if data is None:
            raise ValueError("data is required")
        self.data = data

    @property
    def manufacturer(self):
        return self.data.get("Manufacturer", "N/A")

    @property
    def model(self):
        return self.data.get("Model", "N/A")

    @property
    def bios_version(self):
        return self.data.get("BiosVersion", "N/A")

    @property
    def uuid(self):
        return self.data.get("UUID", "N/A")

    @property
    def serial_number(self):
        return self.data.get("SerialNumber", "N/A")

    @property
    def asset_tag(self):
        return self.data.get("AssetTag", "N/A")

    @property
    def processor_summary(self):
        return ProcessorSummary(self.data.get("ProcessorSummary", {}))

    @property
    def memory_summary(self):
        return MemorySummary(self.data.get("MemorySummary", {}))

    @property
    def power_state(self):
        return self.data.get("PowerState", "N/A")

    @property
    def indicator_led(self):
        return self.data.get("IndicatorLED", "N/A")

    @property
    def health(self):
        if "Status" in self.data:
            return self.data["Status"].get("Health", "N/A")
        return "N/A"

    @property
    def main_board_adapter_state(self):
        if "Oem" in self.data and "HP" in self.data["Oem"]:
            return self.data["Oem"]["HP"].get("MainBoardAdapterState", "N/A")
        return "N/A"

    @property
    def boot_state(self):
        if "Oem" in self.data and "HP" in self.data["Oem"]:
            return self.data["Oem"]["HP"].get("BootState", "N/A")
        return "N/A"

    @property
    def blink_code_state(self):
        if (
            "Oem" in self.data
            and "HP" in self.data["Oem"]
            and "BlinkCodeState" in self.data["Oem"]["HP"]
        ):
            return BlinkCodeState(self.data["Oem"]["HP"]["BlinkCodeState"])
        return BlinkCodeState({})

    @property
    def boot_source_override_target(self):
        if "Boot" in self.data:
            return self.data["Boot"].get("BootSourceOverrideTarget", "N/A")
        return "N/A"
