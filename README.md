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
This tool requires Python 3.11 or later. You can install it from the [official website](https://www.python.org/downloads/).
Download the latest release from this repository's release section, and extract the zip file to a folder of your choice. Run the `install.bat` script to install the tool and bundled dependencies.

**Note**: installing the tool in this way will use your python installation, and not a virtual environment. If you want to use a virtual environment, you can create one using `python -m venv <env_name>` and activate it before running the install script. Refer to the [Python documentation](https://docs.python.org/3/tutorial/venv.html) for more information on how to create and use virtual environments.

### Usage
After installation, you can run the `hprsctool` command in the command prompt or terminal. The tool has a built-in help system that you can access by running `hprsctool --help`. To get help on individual commands, run `hprsctool <command> --help`.

Examples:
- Get host workstation information:
```shell
hprsctool -u admin -p adminpassword -a myrscaddress system get
```
- Power off (forced) the host workstation:
```shell
hprsctool -u admin -p adminpassword -a myrscaddress system power ForceOff
```
- Get RSC network settings:
```shell
hprsctool -u admin -p adminpassword -a myrscaddress manager network get
```
- Update the RSC firmware:
```shell
hprsctool -u admin -p adminpassword -a myrscaddress manager update \path\to\firmware.xz 
```

### Create Windows bundle
1. Install Python 3.12 or later
2. Install poetry:
```shell
pip install poetry
```
3. Clone the repository:
```shell
git clone
```
3. Build the project using poetry:
```shell
poetry build
```
4. In Windows power shell, invoke the createbundle\createbundle.ps1 script to create a zip file with an install script and all dependencies packed as wheels.
