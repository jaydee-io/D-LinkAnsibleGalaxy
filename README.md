# D-Link DGS-1250 Ansible Collection

Ansible Galaxy collection for administering D-Link DGS-1250 Series Gigabit Ethernet Smart Managed Switches.

## Documentation

[DGS-1250 Series CLI Reference Guide v2.04](https://support.dlink.com/resource/products/DGS-1250-SERIES/REVA/DGS-1250%20Series_A1%20A2_CLI%20Manual_v2.04(US).pdf)

## Requirements

- Ansible >= 2.14
- Python >= 3.9
- `ansible.netcommon` collection >= 2.0.0

## Installation

```bash
ansible-galaxy collection install jaydee_io.dlink_dgs1250
```

## Inventory

The collection uses the `ansible.netcommon.network_cli` connection plugin.
Connection parameters are defined in the inventory, not in individual tasks.

### INI format

```ini
[switches]
sw1 ansible_host=192.168.1.1
sw2 ansible_host=192.168.1.2

[switches:vars]
ansible_connection=ansible.netcommon.network_cli
ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250
ansible_user=admin
ansible_password=admin
ansible_port=22
```

### YAML format

```yaml
all:
  children:
    switches:
      hosts:
        sw1:
          ansible_host: 192.168.1.1
        sw2:
          ansible_host: 192.168.1.2
      vars:
        ansible_connection: ansible.netcommon.network_cli
        ansible_network_os: jaydee_io.dlink_dgs1250.dgs1250
        ansible_user: admin
        ansible_password: admin
        ansible_port: 22
```

### Connection variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ansible_connection` | yes | Must be `ansible.netcommon.network_cli` |
| `ansible_network_os` | yes | Must be `jaydee_io.dlink_dgs1250.dgs1250` |
| `ansible_host` | yes | IP address or hostname of the switch |
| `ansible_user` | yes | SSH username |
| `ansible_password` | yes | SSH password |
| `ansible_port` | no | SSH port (default: 22) |

## Modules

### Basic Switch Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `environment` | Display fan, temperature, and power status | § 2-10 |
| `unit` | Display model, serial number, uptime, and memory usage | § 2-11 |
| `cpu_utilization` | Display CPU utilization (5s, 1min, 5min) | § 2-12 |
| `version` | Display system MAC address, hardware and firmware version | § 2-13 |
| `snmp_environment_traps` | Enable or disable SNMP traps for fan, power, temperature | § 2-14 |
| `environment_temperature_threshold` | Configure temperature thresholds (high/low) | § 2-15 |
| `memory_utilization` | Display DRAM and FLASH memory usage | § 2-16 |
| `privilege` | Display current privilege level | § 2-17 |

### 802.1X Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `dot1x_clear_counters` | Clear 802.1X counters on all or specific interfaces | § 3-1 |
| `dot1x_control_direction` | Configure 802.1X traffic control direction (both/in) on a port | § 3-2 |
| `dot1x_default` | Reset 802.1X parameters to defaults on a port | § 3-3 |
| `dot1x_port_control` | Configure port authorization state (auto/force-authorized/force-unauthorized) | § 3-4 |
| `dot1x_forward_pdu` | Enable or disable 802.1X PDU forwarding on a port | § 3-5 |
| `dot1x_initialize` | Initialize 802.1X authenticator state machine on a port or MAC address | § 3-6 |
| `dot1x_max_req` | Configure maximum EAP request retransmissions (1-10) on a port | § 3-7 |
| `dot1x_pae_authenticator` | Enable or disable 802.1X PAE authenticator on a port | § 3-8 |
| `dot1x_re_authenticate` | Re-authenticate 802.1X on a port or MAC address | § 3-9 |
| `dot1x_system_auth_control` | Enable or disable 802.1X authentication globally | § 3-10 |
| `dot1x_timeout` | Configure 802.1X timers (server-timeout, supp-timeout, tx-period) on a port | § 3-11 |
| `dot1x_show` | Display 802.1X global or interface configuration | § 3-12 |
| `dot1x_show_diagnostics` | Display 802.1X diagnostics counters per interface | § 3-13 |
| `dot1x_show_statistics` | Display 802.1X EAPOL frame statistics per interface | § 3-14 |
| `dot1x_show_session_statistics` | Display 802.1X session statistics per interface | § 3-15 |
| `dot1x_snmp_traps` | Enable or disable 802.1X SNMP traps | § 3-16 |

### Access Control List (ACL) Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `acl_resequence` | Re-sequence ACL entries starting sequence and increment | § 4-1 |
| `acl_hardware_counter` | Enable or disable ACL hardware packet counter | § 4-2 |
| `acl_clear_hardware_counter` | Clear ACL hardware packet counters | § 4-3 |
| `acl_ip_access_group` | Apply or remove an IP access list on an interface | § 4-4 |
| `acl_ip_access_list` | Create or delete a standard/extended IP access list | § 4-5 |
| `acl_ipv6_access_group` | Apply or remove an IPv6 access list on an interface | § 4-6 |
| `acl_ipv6_access_list` | Create or delete a standard/extended IPv6 access list | § 4-7 |
| `acl_list_remark` | Add or remove a remark on an ACL | § 4-8 |
| `acl_mac_access_group` | Apply or remove a MAC access list on an interface | § 4-9 |
| `acl_mac_access_list` | Create or delete a MAC access list | § 4-10 |
| `acl_rule_ip` | Add or remove a permit/deny rule in an IP access list | § 4-11 |
| `acl_rule_ipv6` | Add or remove a permit/deny rule in an IPv6 access list | § 4-12 |
| `acl_rule_mac` | Add or remove a permit/deny rule in a MAC access list | § 4-13 |
| `acl_show_access_group` | Display access group bindings per interface | § 4-14 |
| `acl_show_access_list` | Display access list configuration and rules | § 4-15 |

### Administration Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `mgmt_access_class` | Restrict access via a line (console/telnet/ssh) with an IP ACL | § 5-1 |
| `mgmt_enable_password` | Set or remove the enable password | § 5-3 |
| `mgmt_ip_http_server` | Enable or disable the HTTP server | § 5-4 |
| `mgmt_ip_http_secure_server` | Enable or disable the HTTPS server with optional SSL policy | § 5-5 |
| `mgmt_ip_http_access_class` | Apply or remove an ACL on HTTP/HTTPS server | § 5-6 |
| `mgmt_ip_http_service_port` | Set or reset the HTTP/HTTPS service port | § 5-7 |
| `mgmt_ip_http_timeout` | Set or reset the HTTP session timeout | § 5-8 |
| `mgmt_ip_telnet_server` | Enable or disable the Telnet server | § 5-9 |
| `mgmt_ip_telnet_service_port` | Set or reset the Telnet service port | § 5-10 |
| `mgmt_service_password_encryption` | Enable or disable password encryption service | § 5-12 |
| `mgmt_show_terminal` | Display terminal settings (length, width, baud rate) | § 5-13 |
| `mgmt_show_ip_telnet_server` | Display Telnet server status | § 5-14 |
| `mgmt_show_ip_http_server` | Display HTTP server status | § 5-15 |
| `mgmt_show_ip_http_secure_server` | Display HTTPS server status | § 5-16 |
| `mgmt_show_users` | Display active user sessions | § 5-17 |
| `mgmt_terminal_length` | Set terminal length (current session or default) | § 5-18 |
| `mgmt_terminal_speed` | Set console terminal baud rate | § 5-19 |
| `mgmt_session_timeout` | Set session idle timeout on a line | § 5-20 |
| `mgmt_terminal_width` | Set terminal width (current session or default) | § 5-21 |
| `mgmt_username` | Create or remove a user account | § 5-22 |
| `mgmt_password` | Set or remove line password (console/telnet/ssh) | § 5-23 |
| `mgmt_clear_line` | Disconnect a user session by line ID | § 5-24 |

### ARP Spoofing Prevention Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `arp_spoofing_prevention` | Configure ARP spoofing prevention entry (gateway IP/MAC/interface) | § 6-1 |
| `arp_show_spoofing_prevention` | Display ARP spoofing prevention entries | § 6-2 |

### Asymmetric VLAN Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `asymmetric_vlan` | Enable or disable asymmetric VLAN | § 7-1 |

### AAA Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `aaa_accounting_network` | Configure AAA accounting network default method list | § 8-1 |
| `aaa_authentication_enable` | Configure AAA authentication enable default method list | § 8-2 |
| `aaa_authentication_dot1x` | Configure AAA authentication dot1x default method list | § 8-3 |
| `aaa_authentication_login` | Configure AAA authentication login method list (default or named) | § 8-4 |
| `aaa_authentication_mac_auth` | Configure AAA authentication mac-auth default method list | § 8-5 |
| `aaa_group_server_radius` | Create or delete a RADIUS server group | § 8-6 |
| `aaa_group_server_tacacs` | Create or delete a TACACS+ server group | § 8-7 |
| `aaa_new_model` | Enable or disable AAA new-model | § 8-8 |
| `aaa_server_radius_dynamic_author` | Enable or disable RADIUS dynamic authorization | § 8-9 |
| `aaa_clear_counters_servers` | Clear AAA server counters (all, RADIUS, TACACS+, or server group) | § 8-10 |
| `aaa_client` | Configure a RADIUS dynamic authorization client | § 8-11 |
| `aaa_ip_http_auth_login` | Configure IP HTTP AAA login authentication method list | § 8-12 |
| `aaa_ip_radius_source_interface` | Set or remove IP RADIUS source interface | § 8-13 |
| `aaa_ip_tacacs_source_interface` | Set or remove IP TACACS source interface | § 8-14 |
| `aaa_ipv6_radius_source_interface` | Set or remove IPv6 RADIUS source interface | § 8-15 |
| `aaa_ipv6_tacacs_source_interface` | Set or remove IPv6 TACACS source interface | § 8-16 |
| `aaa_login_authentication` | Configure login authentication on a line (console/telnet/ssh) | § 8-17 |
| `aaa_port` | Configure RADIUS dynamic authorization listening port | § 8-18 |
| `aaa_radius_attribute_32` | Configure RADIUS attribute 32 (NAS-Identifier) in Access-Request | § 8-19 |
| `aaa_radius_attribute_4` | Configure RADIUS attribute 4 (NAS-IP-Address) | § 8-20 |
| `aaa_radius_attribute_55` | Enable or disable RADIUS attribute 55 in Accounting-Request | § 8-21 |
| `aaa_radius_deadtime` | Configure RADIUS server deadtime | § 8-22 |
| `aaa_radius_server_host` | Configure a RADIUS server host with key and options | § 8-23 |
| `aaa_server_radius` | Add or remove a server from a RADIUS group | § 8-24 |
| `aaa_server_tacacs` | Add or remove a server from a TACACS+ group | § 8-25 |
| `aaa_show` | Display AAA status (enabled/disabled) | § 8-26 |
| `aaa_tacacs_server_host` | Configure a TACACS+ server host with key and options | § 8-27 |
| `aaa_show_radius_statistics` | Display RADIUS server statistics | § 8-28 |
| `aaa_show_tacacs_statistics` | Display TACACS+ server statistics | § 8-29 |

### Basic IPv4 Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `ipv4_arp` | Configure a static ARP entry (IP to MAC mapping) | § 9-1 |
| `ipv4_arp_timeout` | Configure ARP timeout on an interface | § 9-2 |
| `ipv4_clear_arp_cache` | Clear ARP cache entries | § 9-3 |
| `ipv4_ip_address` | Configure an IP address or DHCP on an interface | § 9-4 |
| `ipv4_show_arp` | Display ARP table entries | § 9-5 |
| `ipv4_show_arp_timeout` | Display ARP timeout settings | § 9-6 |
| `ipv4_show_ip_interface` | Display IP interface information | § 9-7 |

## Usage example

```yaml
- name: Check switch status
  hosts: switches
  gather_facts: false
  tasks:
    - name: Get environment status
      jaydee_io.dlink_dgs1250.environment:
      register: env

    - name: Show temperatures
      ansible.builtin.debug:
        var: env.temperatures

    - name: Get CPU utilization
      jaydee_io.dlink_dgs1250.cpu_utilization:
      register: cpu

    - name: Warn if CPU is high
      ansible.builtin.debug:
        msg: "High CPU: {{ cpu.five_seconds_percent }}%"
      when: cpu.five_seconds_percent > 80

    - name: Get unit information
      jaydee_io.dlink_dgs1250.unit:
      register: unit_info

    - name: Show uptime
      ansible.builtin.debug:
        msg: "Uptime: {{ unit_info.unit.uptime.days }}d {{ unit_info.unit.uptime.hours }}h"

    - name: Set temperature thresholds
      jaydee_io.dlink_dgs1250.environment_temperature_threshold:
        high: 100
        low: 20
```

## Running unit tests

```bash
pip install pytest
pytest tests/unit/
```
