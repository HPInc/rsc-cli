# USAGE Examples

This document provides simple usage examples for all available commands in hprsctool.

## Basic Command Structure

All commands follow this basic structure:
```
hprsctool -u <username> -p <password> -a <rsc_address> <command> [subcommand] [options]
```

## System Commands

### Get system information
```
hprsctool -u admin -p adminpassword -a myrscaddress system get
```

### Power operations
```
# Power on
hprsctool -u admin -p adminpassword -a myrscaddress system power On

# Graceful shutdown
hprsctool -u admin -p adminpassword -a myrscaddress system power GracefulShutdown

# Force power off
hprsctool -u admin -p adminpassword -a myrscaddress system power ForceOff

# Graceful restart
hprsctool -u admin -p adminpassword -a myrscaddress system power GracefulRestart

# Force restart
hprsctool -u admin -p adminpassword -a myrscaddress system power ForceRestart
```

## User Management Commands

### List all accounts
```
hprsctool -u admin -p adminpassword -a myrscaddress account list
```

### Get account details
```
hprsctool -u admin -p adminpassword -a myrscaddress account get <account_id>
```

### Create new account
```
hprsctool -u admin -p adminpassword -a myrscaddress account create <new_username> <new_password> <role_id>
```

### Change account password
```
hprsctool -u admin -p adminpassword -a myrscaddress account change-password <account_id> <new_password>
```

### Change account role
```
hprsctool -u admin -p adminpassword -a myrscaddress account change-role <account_id> <role_id>
```

### Delete account
```
hprsctool -u admin -p adminpassword -a myrscaddress account delete <account_id>
```

## Role Management Commands

### List all roles
```
hprsctool -u admin -p adminpassword -a myrscaddress role list
```

### Get role details
```
hprsctool -u admin -p adminpassword -a myrscaddress role get <role_id>
```

### Create new role
```
hprsctool -u admin -p adminpassword -a myrscaddress role create <role_id> --assigned-privileges <priv1> <priv2> --oem-privileges <oem1> <oem2>
```

### Update role privileges
```
hprsctool -u admin -p adminpassword -a myrscaddress role update <role_id> --assigned-privileges <priv1> <priv2> --oem-privileges <oem1> <oem2>
```

### Delete role
```
hprsctool -u admin -p adminpassword -a myrscaddress role delete <role_id>
```

### List available privileges
```
hprsctool -u admin -p adminpassword -a myrscaddress role list-privileges
```

## Task Commands

### List all tasks
```
hprsctool -u admin -p adminpassword -a myrscaddress tasks list
```

### List only running tasks
```
hprsctool -u admin -p adminpassword -a myrscaddress tasks list --running
```

### Get specific task details
```
hprsctool -u admin -p adminpassword -a myrscaddress tasks get 12345
```

### Cancel a running task
```
hprsctool -u admin -p adminpassword -a myrscaddress tasks cancel 12345
```

## Manager Commands

### Get RSC information
```
hprsctool -u admin -p adminpassword -a myrscaddress manager get
```

### Change admin password
```
hprsctool -u admin -p adminpassword -a myrscaddress manager change_password newpassword123
```

### Restart RSC
```
hprsctool -u admin -p adminpassword -a myrscaddress manager restart
```

### Factory reset RSC
```
hprsctool -u admin -p adminpassword -a myrscaddress manager factory_reset
```

### Update firmware
```
hprsctool -u admin -p adminpassword -a myrscaddress manager update \path\to\firmware.xz
```

## Certificate Management

### Get current certificate information
```
hprsctool -u admin -p adminpassword -a myrscaddress manager cert get
```

### Replace HTTPS certificate
```
hprsctool -u admin -p adminpassword -a myrscaddress manager cert replace \path\to\cert.pem \path\to\key.pem
```

## Trusted Certificate Management

### List trusted certificates
```
hprsctool -u admin -p adminpassword -a myrscaddress manager trusted_cert list
```

### Add trusted certificate
```
hprsctool -u admin -p adminpassword -a myrscaddress manager trusted_cert add \path\to\cert.pem
```

### Delete trusted certificate
```
hprsctool -u admin -p adminpassword -a myrscaddress manager trusted_cert delete cert123
```

## Network Settings

### Get network settings
```
hprsctool -u admin -p adminpassword -a myrscaddress manager network get
```

### Configure static IP
```
hprsctool -u admin -p adminpassword -a myrscaddress manager network set --static_address 192.168.1.50 --subnet_mask 255.255.255.0 --gateway 192.168.1.1 --dhcp disable
```

### Enable DHCP
```
hprsctool -u admin -p adminpassword -a myrscaddress manager network set --dhcp enable
```

### Set DNS servers
```
hprsctool -u admin -p adminpassword -a myrscaddress manager network set --name_server 8.8.8.8 --name_server 8.8.4.4
```

### Configure proxy
```
hprsctool -u admin -p adminpassword -a myrscaddress manager network set --proxy enable --proxyserver "http://proxy.company.com:8080" --proxyexclude "192.168.1.0/24"
```

### Enable/disable mDNS
```
hprsctool -u admin -p adminpassword -a myrscaddress manager network set --mdns enable
```

## Time Settings

### Get time settings
```
hprsctool -u admin -p adminpassword -a myrscaddress manager time get
```

### Set time manually
```
hprsctool -u admin -p adminpassword -a myrscaddress manager time set --time "2024-12-25T10:30:00-05:00"
```

### Set timezone offset
```
hprsctool -u admin -p adminpassword -a myrscaddress manager time set --offset="-05:00"
```

### Enable NTP
```
hprsctool -u admin -p adminpassword -a myrscaddress manager time set --ntp enable
```

### Configure NTP servers
```
hprsctool -u admin -p adminpassword -a myrscaddress manager time set --ntp enable --ntpserver pool.ntp.org --ntpserver time.google.com
```

## Getting Help

### General help
```
hprsctool --help
```

### Command-specific help
```
hprsctool system --help
hprsctool manager network --help
hprsctool user --help
```

### Version information
```
hprsctool --version
```

## Common Parameters

- `-u, --username`: Username for the RSC (required)
- `-p, --password`: Password for the RSC (required)  
- `-a, --address`: IP address or hostname of the RSC (required)

## Notes

- Replace `admin`, `adminpassword`, and `myrscaddress` with your actual RSC credentials and address
- File paths should be enclosed in quotes if they contain spaces
- Use `--help` with any command to see available options and detailed usage information
- Some operations may take time to complete and will show progress or confirmation messages
