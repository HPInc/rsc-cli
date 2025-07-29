HP Remote System Controller CLI tool
------------------------------------

This is a command-line interface tool for interacting with the [HP Remote System Controller (RSC)](https://www.hp.com/us-en/solutions/remote-system-controller.html), allowing users to manage the host workstation, and the RSC itself, remotely. It is written in Python and uses [DMTF's redfish library](https://github.com/DMTF/python-redfish-library) to interact with the [RSC's Redfish REST API](https://developers.hp.com/hp-remote-system-controller/api/hp-remote-system-controller-api-2412).

The tool was tested in Windows 11, and should work in Linux and MacOS as well.

### Features
- Get RSC information
- Get host workstation information and state
- Power operations on host workstation (on, off, reset, etc.)
- Manage RSC settings:
    - Change administrator password
    - Change network settings (DHCP, static addresses, proxy, etc.)
    - Change date and time settings (time, timezone, NTP server, etc.)
    - Firmware update
    - Restart
    - Reset to factory defaults
    - Certificate management

### Installation

#### Option 1: Download Precompiled Release (Recommended)
Download the latest release from the [GitHub Releases page](../../releases). Extract the zip file to a folder of your choice and run the `install.bat` script to install the tool and bundled dependencies.

**Note**: This installation method uses your system Python installation. If you prefer to use a virtual environment, create one using `python -m venv <env_name>` and activate it before running the install script.

#### Option 2: Build from Source
If you need to build from source or want to contribute to the project, see [BUILD.md](BUILD.md) for detailed build instructions.

### Usage

The tool provides a command-line interface with built-in help. After installation, you can run:

```shell
hprsctool --help
```

For detailed usage examples and all available commands, see [USAGE.md](USAGE.md).

#### Quick Examples:
- Get system information: `hprsctool -u admin -p adminpassword -a myrscaddress system get`
- Power operations: `hprsctool -u admin -p adminpassword -a myrscaddress system power On`
- Network settings: `hprsctool -u admin -p adminpassword -a myrscaddress manager network get`

### Requirements

- Python 3.12 or later (download from [python.org](https://www.python.org/downloads/))

### Documentation

- **[USAGE.md](USAGE.md)** - Comprehensive usage examples and command reference
- **[BUILD.md](BUILD.md)** - Build instructions for developers and contributors
