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

## Module defaults

The collection defines an `action_group` named `dgs1250` that covers all modules. Use `module_defaults` to set common parameters once for an entire play:

```yaml
- name: Configure switches
  hosts: switches
  gather_facts: false
  module_defaults:
    group/jaydee_io.dlink_dgs1250.dgs1250: {}
  roles:
    - jaydee_io.dlink_dgs1250.base_config
    - jaydee_io.dlink_dgs1250.monitoring
```

## Modules

### Facts

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `dgs1250_facts` | Collect facts (version, unit, environment, CPU, interfaces, VLANs, MAC table, SNMP, LLDP neighbors, STP, static routes) and expose as `ansible_facts` | — |

### Resource Modules

| Module | Description | States |
|--------|-------------|--------|
| `dgs1250_vlans` | Manage VLANs declaratively (create, name, delete) | merged, replaced, overridden, deleted, gathered |
| `dgs1250_l2_interfaces` | Manage L2 interface settings (switchport mode, access VLAN, trunk VLANs) | merged, replaced, deleted, gathered |
| `dgs1250_snmp_server` | Manage SNMP community strings | merged, replaced, overridden, deleted, gathered |
| `dgs1250_logging` | Manage syslog server configuration | merged, replaced, overridden, deleted, gathered |
| `dgs1250_ntp` | Manage SNTP server configuration | merged, overridden, deleted, gathered |
| `dgs1250_static_routes` | Manage IPv4 static routes | merged, overridden, deleted, gathered |
| `dgs1250_acls` | Manage IP access-lists with rules | merged, replaced, overridden, deleted, gathered |
| `dgs1250_lag_interfaces` | Manage LAG (port-channel) member interfaces | merged, replaced, deleted, gathered |
| `dgs1250_storm_control` | Manage per-interface storm control settings | merged, replaced, deleted, gathered |
| `dgs1250_spanning_tree` | Manage per-interface STP settings (cost, priority, portfast, guard) | merged, replaced, deleted, gathered |
| `dgs1250_lldp_interfaces` | Manage per-interface LLDP transmit/receive | merged, replaced, deleted, gathered |
| `dgs1250_dns` | Manage DNS name servers | merged, overridden, deleted, gathered |

### Utility Modules

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `save_config` | Save running-config to startup-config | — |
| `config_backup` | Backup running-config to a local file | — |
| `config_restore` | Restore a configuration backup to the switch | — |
| `config_diff` | Compare running-config vs startup-config and report differences | — |
| `dgs1250_command` | Send arbitrary CLI commands to the switch | — |

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

### Basic IPv6 Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `ipv6_clear_neighbors` | Clear IPv6 neighbor cache entries (all or specific interface) | § 10-1 |
| `ipv6_address` | Configure an IPv6 address on an interface (static or link-local) | § 10-2 |
| `ipv6_address_eui64` | Configure an IPv6 address using EUI-64 interface ID | § 10-3 |
| `ipv6_address_dhcp` | Configure DHCPv6 on an interface with optional rapid-commit | § 10-4 |
| `ipv6_enable` | Enable or disable IPv6 processing on an interface | § 10-5 |
| `ipv6_hop_limit` | Configure IPv6 hop limit on an interface | § 10-6 |
| `ipv6_nd_managed_config_flag` | Enable or disable ND managed-config-flag in RA messages | § 10-7 |
| `ipv6_nd_other_config_flag` | Enable or disable ND other-config-flag in RA messages | § 10-8 |
| `ipv6_nd_prefix` | Configure IPv6 ND prefix with lifetimes and flags | § 10-9 |
| `ipv6_nd_ra_interval` | Configure IPv6 ND router advertisement interval | § 10-10 |
| `ipv6_nd_ra_lifetime` | Configure IPv6 ND router advertisement lifetime | § 10-11 |
| `ipv6_nd_suppress_ra` | Enable or disable suppression of RA messages | § 10-12 |
| `ipv6_nd_reachable_time` | Configure IPv6 ND reachable time | § 10-13 |
| `ipv6_nd_ns_interval` | Configure IPv6 ND neighbor solicitation interval | § 10-14 |
| `ipv6_neighbor` | Configure a static IPv6 neighbor cache entry | § 10-15 |
| `ipv6_show_interface` | Display IPv6 interface information | § 10-16 |
| `ipv6_show_neighbors` | Display IPv6 neighbor cache entries | § 10-17 |

### Cable Diagnostics Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `cable_diag_test` | Run cable diagnostics test on an interface | § 11-1 |
| `cable_diag_show` | Display cable diagnostics results | § 11-2 |
| `cable_diag_clear` | Clear cable diagnostics results (all or specific interface) | § 11-3 |

### Command Logging Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `command_logging` | Enable or disable command logging | § 12-1 |

### Debug Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `debug_reboot_on_error` | Enable or disable reboot on fatal error | § 13-1 |
| `debug_copy` | Copy debug information (error-log/tech-support) to a destination | § 13-2 |
| `debug_clear_error_log` | Clear the error log | § 13-3 |
| `debug_show_error_log` | Display error log information | § 13-4 |
| `debug_show_tech_support` | Display technical support information | § 13-5 |

### DHCP Auto-Configuration Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `autoconfig_enable` | Enable or disable DHCP auto-configuration | § 14-1 |
| `autoconfig_show` | Display auto-configuration status | § 14-2 |

### DHCP Client Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `dhcp_client_class_id` | Configure DHCP client vendor class identifier (Option 60) | § 15-1 |
| `dhcp_client_client_id` | Configure DHCP client ID (MAC address of a VLAN interface) | § 15-2 |
| `dhcp_client_lease` | Configure DHCP client lease time | § 15-3 |

### DHCP Relay Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `dhcp_relay_class` | Create or delete a DHCP relay class | § 16-1 |
| `dhcp_relay_ip_dhcp_class` | Create or delete a DHCP class for relay agent info matching | § 16-2 |
| `dhcp_relay_ip_dhcp_pool` | Create or delete a DHCP pool | § 16-3 |
| `dhcp_relay_destination` | Configure relay destination server in a DHCP pool | § 16-4 |
| `dhcp_relay_source` | Configure relay source address in a DHCP pool | § 16-5 |
| `dhcp_relay_target` | Configure relay target in a DHCP pool | § 16-6 |
| `dhcp_relay_info_check` | Enable or disable DHCP relay information check | § 16-7 |
| `dhcp_relay_info_policy` | Configure DHCP relay information forwarding policy | § 16-8 |
| `dhcp_relay_info_check_reply` | Enable or disable DHCP relay information check on replies | § 16-9 |
| `dhcp_relay_info_option` | Enable or disable DHCP relay information option (Option 82) | § 16-10 |
| `dhcp_relay_info_option_insert` | Enable or disable insertion of relay info on trusted ports | § 16-11 |
| `dhcp_relay_info_policy_action` | Configure per-VLAN DHCP relay information policy action | § 16-12 |
| `dhcp_relay_info_format_remote_id` | Configure DHCP relay remote-id format | § 16-13 |
| `dhcp_relay_info_format_type_remote_id` | Configure DHCP relay remote-id format type | § 16-14 |
| `dhcp_relay_info_format_circuit_id` | Configure DHCP relay circuit-id format | § 16-15 |
| `dhcp_relay_info_format_type_circuit_id` | Configure DHCP relay circuit-id format type | § 16-16 |
| `dhcp_relay_info_trust_all` | Enable or disable trust all ports for relay information | § 16-17 |
| `dhcp_relay_info_trusted` | Configure trusted interface for DHCP relay | § 16-18 |
| `dhcp_relay_local_relay_vlan` | Enable or disable DHCP local relay on VLANs | § 16-19 |
| `dhcp_relay_option_hex` | Configure DHCP relay Option 82 hex value on a VLAN | § 16-20 |
| `dhcp_relay_service_dhcp` | Enable or disable DHCP relay service | § 16-21 |
| `dhcp_relay_show_trusted_sources` | Display trusted DHCP relay sources | § 16-22 |
| `dhcp_relay_show_option_insert` | Display DHCP relay option insertion settings | § 16-23 |
| `dhcp_relay_show_policy_action` | Display DHCP relay policy action settings | § 16-24 |

### DHCP Snooping Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `dhcp_snooping_enable` | Enable or disable DHCP snooping | § 17-1 |
| `dhcp_snooping_info_allow_untrusted` | Enable or disable DHCP snooping info allow-untrusted | § 17-2 |
| `dhcp_snooping_database` | Configure DHCP snooping database URL or write-delay | § 17-3 |
| `dhcp_snooping_clear_database_stats` | Clear DHCP snooping database statistics | § 17-4 |
| `dhcp_snooping_clear_binding` | Clear DHCP snooping binding entries | § 17-5 |
| `dhcp_snooping_renew_database` | Renew DHCP snooping database from a URL | § 17-6 |
| `dhcp_snooping_binding` | Create a static DHCP snooping binding entry | § 17-7 |
| `dhcp_snooping_limit_entries` | Configure DHCP snooping max entries per interface | § 17-8 |
| `dhcp_snooping_limit_rate` | Configure DHCP snooping rate limit per interface | § 17-9 |
| `dhcp_snooping_station_move_deny` | Enable or disable DHCP snooping station-move deny | § 17-10 |
| `dhcp_snooping_trust` | Configure trusted interface for DHCP snooping | § 17-11 |
| `dhcp_snooping_verify_mac` | Enable or disable MAC address verification | § 17-12 |
| `dhcp_snooping_vlan` | Enable DHCP snooping on a VLAN | § 17-13 |
| `dhcp_snooping_show` | Display DHCP snooping configuration | § 17-14 |
| `dhcp_snooping_show_binding` | Display DHCP snooping binding table | § 17-15 |
| `dhcp_snooping_show_database` | Display DHCP snooping database status | § 17-16 |
| `dhcp_snooping_server_screen_profile` | Create or delete a DHCP server screen profile | § 17-17 |
| `dhcp_snooping_server_screen_hw_addr` | Add or remove a hardware address in a server screen profile | § 17-18 |
| `dhcp_snooping_server_screen` | Configure DHCP server screen on an interface | § 17-19 |
| `dhcp_snooping_server_screen_log_buffer` | Configure DHCP server screen log buffer size | § 17-20 |
| `dhcp_snooping_clear_server_screen_log` | Clear DHCP server screen log | § 17-21 |
| `dhcp_snooping_snmp_traps` | Enable or disable DHCP server screen SNMP traps | § 17-22 |
| `dhcp_snooping_show_server_screen_log` | Display DHCP server screen log | § 17-23 |

### DHCPv6 Client Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `dhcpv6_client_clear` | Clear DHCPv6 client state on an interface | § 18-1 |
| `dhcpv6_client_show` | Display DHCPv6 client information | § 18-2 |

### DHCPv6 Guard Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `dhcpv6_guard_policy` | Create or delete a DHCPv6 guard policy | § 19-1 |
| `dhcpv6_guard_device_role` | Configure device role in a DHCPv6 guard policy | § 19-2 |
| `dhcpv6_guard_match_access_list` | Configure access list match in a DHCPv6 guard policy | § 19-3 |
| `dhcpv6_guard_attach_policy` | Attach or detach a DHCPv6 guard policy on an interface | § 19-4 |
| `dhcpv6_guard_show_policy` | Display DHCPv6 guard policy information | § 19-5 |

### DHCPv6 Relay Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `dhcpv6_relay_destination` | Configure DHCPv6 relay destination address on an interface | § 20-1 |
| `dhcpv6_relay_remote_id_format` | Configure DHCPv6 relay remote-id format sub-type | § 20-2 |
| `dhcpv6_relay_remote_id_option` | Enable or disable DHCPv6 relay remote-id option (Option 37) | § 20-3 |
| `dhcpv6_relay_remote_id_policy` | Configure DHCPv6 relay remote-id forwarding policy | § 20-4 |
| `dhcpv6_relay_remote_id_profile` | Create or delete a DHCPv6 relay remote-id profile | § 20-5 |
| `dhcpv6_relay_format_string` | Configure format string in a DHCPv6 relay profile | § 20-6 |
| `dhcpv6_relay_mac_format` | Configure MAC address format for DHCPv6 relay profiles | § 20-7 |
| `dhcpv6_relay_show_mac_format` | Display DHCPv6 relay MAC address format settings | § 20-8 |
| `dhcpv6_relay_remote_id_udf` | Configure DHCPv6 relay remote-id UDF (ascii or hex) | § 20-9 |
| `dhcpv6_relay_local_relay_vlan` | Enable or disable DHCPv6 local relay on VLANs | § 20-10 |
| `dhcpv6_relay_show` | Display DHCPv6 settings or interface information | § 20-11 |

### Digital Diagnostics Monitoring (DDM) Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `ddm_show_interfaces_transceiver` | Display SFP/SFP+ transceiver monitoring parameters | § 21-1 |
| `ddm_snmp_traps_transceiver_monitoring` | Enable or disable SNMP traps for transceiver monitoring | § 21-2 |
| `ddm_transceiver_monitoring_action_shutdown` | Configure transceiver monitoring shutdown action on an interface | § 21-3 |
| `ddm_transceiver_monitoring_bias_current` | Configure transceiver monitoring bias-current thresholds | § 21-4 |
| `ddm_transceiver_monitoring_enable` | Enable or disable transceiver monitoring on an interface | § 21-5 |
| `ddm_transceiver_monitoring_rx_power` | Configure transceiver monitoring RX power thresholds | § 21-6 |
| `ddm_transceiver_monitoring_temperature` | Configure transceiver monitoring temperature thresholds | § 21-7 |
| `ddm_transceiver_monitoring_tx_power` | Configure transceiver monitoring TX power thresholds | § 21-8 |
| `ddm_transceiver_monitoring_voltage` | Configure transceiver monitoring voltage thresholds | § 21-9 |

### D-Link Discovery Protocol (DDP) Client Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `ddp` | Enable or disable DDP client globally or on an interface | § 22-1 |
| `ddp_report_timer` | Configure DDP report timer interval | § 22-2 |
| `ddp_show` | Display DDP configuration | § 22-3 |

### Domain Name System (DNS) Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `dns_clear_host` | Clear dynamically learned host entries | § 23-1 |
| `dns_ip_domain_lookup` | Enable or disable DNS domain name resolution | § 23-2 |
| `dns_ip_host` | Configure static host name to IP address mapping | § 23-3 |
| `dns_ip_name_server` | Configure DNS name server address | § 23-4 |
| `dns_ip_name_server_timeout` | Configure DNS name server timeout | § 23-5 |
| `dns_show_hosts` | Display DNS host configuration | § 23-6 |
| `dns_show_ip_name_server` | Display DNS name server configuration | § 23-7 |

### DoS Prevention Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `dos_prevention` | Enable or disable DoS prevention for a specific attack type | § 24-1 |
| `dos_prevention_show` | Display DoS prevention status and drop counters | § 24-2 |
| `dos_prevention_snmp_traps` | Enable or disable SNMP traps for DoS prevention | § 24-3 |

### Dynamic ARP Inspection Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `dai_arp_access_list` | Create or remove an ARP access list | § 25-1 |
| `dai_clear_arp_inspection_log` | Clear ARP inspection log buffer | § 25-2 |
| `dai_clear_arp_inspection_statistics` | Clear Dynamic ARP Inspection statistics | § 25-3 |
| `dai_ip_arp_inspection_filter_vlan` | Configure ARP access list for ARP inspection on a VLAN | § 25-4 |
| `dai_ip_arp_inspection_limit` | Configure ARP inspection rate limit on an interface | § 25-5 |
| `dai_ip_arp_inspection_log_buffer` | Configure ARP inspection log buffer size | § 25-6 |
| `dai_ip_arp_inspection_trust` | Configure ARP inspection trust state on an interface | § 25-7 |
| `dai_ip_arp_inspection_validate` | Configure ARP inspection additional validation checks | § 25-8 |
| `dai_ip_arp_inspection_vlan` | Enable or disable Dynamic ARP Inspection for a VLAN | § 25-9 |
| `dai_ip_arp_inspection_vlan_logging` | Configure ARP inspection logging for a VLAN | § 25-10 |
| `dai_permit_deny` | Add a permit or deny ARP entry in an ARP access list | § 25-11 |
| `dai_show_ip_arp_inspection` | Display Dynamic ARP Inspection status | § 25-12 |
| `dai_show_ip_arp_inspection_log` | Display ARP inspection log buffer | § 25-13 |

### Error Recovery Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `errdisable_recovery` | Configure error recovery for causes and interval | § 26-1 |
| `show_errdisable_recovery` | Display error-disable recovery timer settings | § 26-2 |
| `snmp_server_enable_traps_errdisable` | Enable SNMP notifications for error-disabled state | § 26-3 |

### File System Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `delete_file` | Delete a file from the switch file system | § 27-1 |
| `dir` | Display file system directory listing | § 27-2 |
| `show_storage_media_info` | Display storage media information | § 27-3 |

### Filter Database (FDB) Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `clear_mac_address_table` | Clear dynamic MAC address table entries | § 28-1 |
| `mac_address_table_aging_time` | Configure MAC address table aging time | § 28-2 |
| `mac_address_table_learning` | Enable or disable MAC address learning on an interface | § 28-3 |
| `mac_address_table_notification_change` | Configure MAC address notification function | § 28-4 |
| `mac_address_table_static` | Add or remove static MAC address table entries | § 28-5 |
| `multicast_filtering_mode` | Configure multicast packet handling mode for a VLAN | § 28-6 |
| `show_mac_address_table` | Display MAC address table entries (with structured `parsed` output) | § 28-7 |
| `show_mac_address_table_aging_time` | Display MAC address table aging time | § 28-8 |
| `show_mac_address_table_learning` | Display MAC address learning state | § 28-9 |
| `show_mac_address_table_notification_change` | Display MAC address notification configuration | § 28-10 |
| `show_multicast_filtering_mode` | Display multicast filtering mode for VLANs | § 28-11 |
| `snmp_server_enable_traps_mac_notification_change` | Enable SNMP MAC notification traps | § 28-12 |
| `snmp_trap_mac_notification_change` | Enable MAC address change notification trap on an interface | § 28-13 |

### Gratuitous ARP Trap Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `snmp_server_enable_traps_gratuitous_arp` | Enable SNMP notifications for gratuitous ARP | § 29-1 |

### Interface Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `clear_counters` | Clear counters for port interfaces | § 30-1 |
| `interface_description` | Set or remove interface description | § 30-2 |
| `show_counters` | Display interface statistic counters | § 30-5 |
| `show_interfaces` | Display interface information | § 30-6 |
| `show_interfaces_counters` | Display interface counters | § 30-7 |
| `show_interfaces_status` | Display interface connection status (with structured `parsed` output) | § 30-8 |
| `show_interfaces_utilization` | Display interface port utilization | § 30-9 |
| `show_interfaces_auto_negotiation` | Display interface auto-negotiation information | § 30-10 |
| `show_interfaces_description` | Display interface description and link status | § 30-11 |
| `show_interfaces_gbic` | Display GBIC/SFP status information | § 30-12 |

### IGMP Snooping Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `igmp_snooping_clear_statistics` | Clear IGMP snooping statistics | § 31-1 |
| `igmp_snooping_enable` | Enable or disable IGMP snooping globally or on a VLAN | § 31-2 |
| `igmp_snooping_fast_leave` | Configure IGMP snooping fast-leave on a VLAN | § 31-3 |
| `igmp_snooping_last_member_query_interval` | Configure last member query interval on a VLAN | § 31-4 |
| `igmp_snooping_mrouter` | Configure IGMP snooping multicast router ports on a VLAN | § 31-5 |
| `igmp_snooping_querier` | Enable or disable IGMP snooping querier on a VLAN | § 31-6 |
| `igmp_snooping_query_interval` | Configure IGMP snooping query interval on a VLAN | § 31-7 |
| `igmp_snooping_query_max_response_time` | Configure query max response time on a VLAN | § 31-8 |
| `igmp_snooping_query_version` | Configure IGMP snooping query version on a VLAN | § 31-9 |
| `igmp_snooping_robustness_variable` | Configure robustness variable on a VLAN | § 31-10 |
| `igmp_snooping_static_group` | Configure IGMP snooping static group on a VLAN | § 31-11 |
| `igmp_snooping_minimum_version` | Configure minimum IGMP version on a VLAN | § 31-12 |
| `show_igmp_snooping` | Display IGMP snooping information | § 31-13 |
| `show_igmp_snooping_groups` | Display IGMP snooping group information | § 31-14 |
| `show_igmp_snooping_mrouter` | Display IGMP snooping router port information | § 31-15 |
| `show_igmp_snooping_static_group` | Display IGMP snooping static group information | § 31-16 |
| `show_igmp_snooping_statistics` | Display IGMP snooping statistics | § 31-17 |

### IP-MAC-Port Binding (IMPB) Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `impb_clear_violation` | Clear IMPB violation entries | § 32-1 |
| `impb_enable` | Enable or disable IMPB access control on an interface | § 32-2 |
| `show_impb` | Display IMPB configuration or violation entries | § 32-3 |
| `impb_snmp_traps` | Enable or disable SNMP traps for IMPB | § 32-4 |

### IP Multicast (IPMC) Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `show_ip_mroute_forwarding_cache` | Display IP multicast forwarding cache | § 33-1 |

### IP Multicast Version 6 (IPMCv6) Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `show_ipv6_mroute_forwarding_cache` | Display IPv6 multicast forwarding cache | § 34-1 |

### IP Source Guard Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `ip_verify_source` | Enable or disable IP source guard on an interface | § 35-1 |
| `ip_source_binding` | Configure IP source guard static binding entry | § 35-2 |
| `show_ip_source_binding` | Display IP source guard binding entries | § 35-3 |
| `show_ip_verify_source` | Display IP source guard hardware port ACL entries | § 35-4 |

### IP Utility Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `ping` | Ping a remote host | § 36-1 |
| `ping_access_class` | Configure ping access class | § 36-2 |

### IPv6 Snooping Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `ipv6_snooping_policy` | Create or delete an IPv6 snooping policy | § 37-1 |
| `ipv6_snooping_protocol` | Configure protocol snooping in an IPv6 snooping policy | § 37-2 |
| `ipv6_snooping_limit_address_count` | Configure IPv6 snooping binding entry limit | § 37-3 |
| `ipv6_snooping_attach_policy` | Attach an IPv6 snooping policy to a VLAN | § 37-4 |
| `ipv6_snooping_station_move_deny` | Enable or disable IPv6 snooping station move deny | § 37-5 |
| `show_ipv6_snooping_policy` | Display IPv6 snooping policy information | § 37-6 |

### IPv6 Source Guard Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `ipv6_source_binding` | Configure a static IPv6 source binding entry | § 38-1 |
| `ipv6_source_guard_policy` | Create or delete an IPv6 source guard policy | § 38-2 |
| `ipv6_source_guard_deny_global_autoconfig` | Enable or disable deny global-autoconfig in an IPv6 source guard policy | § 38-3 |
| `ipv6_source_guard_permit_link_local` | Enable or disable permit link-local in an IPv6 source guard policy | § 38-4 |
| `ipv6_source_guard_attach_policy` | Attach an IPv6 source guard policy to an interface | § 38-5 |
| `show_ipv6_source_guard_policy` | Display IPv6 source guard policy configuration | § 38-6 |
| `show_ipv6_neighbor_binding` | Display IPv6 neighbor binding table | § 38-7 |

### Jumbo Frame Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `max_rcv_frame_size` | Configure maximum receive frame size on an interface | § 39-1 |

### Link Aggregation Control Protocol (LACP) Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `channel_group` | Assign an interface to a channel group | § 40-1 |
| `lacp_port_priority` | Configure LACP port priority on an interface | § 40-2 |
| `lacp_timeout` | Configure LACP timeout on an interface | § 40-3 |
| `lacp_system_priority` | Configure LACP system priority | § 40-4 |
| `port_channel_load_balance` | Configure port-channel load balance algorithm | § 40-5 |
| `show_channel_group` | Display channel group information | § 40-6 |

### Link Layer Discovery Protocol (LLDP) Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `lldp_clear_counters` | Clear LLDP statistics counters | § 41-1 |
| `lldp_clear_table` | Clear LLDP remote table | § 41-2 |
| `lldp_dot1_tlv_select` | Configure LLDP IEEE 802.1 TLV selection on an interface | § 41-3 |
| `lldp_dot3_tlv_select` | Configure LLDP IEEE 802.3 TLV selection on an interface | § 41-4 |
| `lldp_fast_count` | Configure LLDP fast transmit count | § 41-5 |
| `lldp_hold_multiplier` | Configure LLDP hold multiplier | § 41-6 |
| `lldp_management_address` | Configure LLDP management address | § 41-7 |
| `lldp_med_tlv_select` | Configure LLDP-MED TLV selection on an interface | § 41-8 |
| `lldp_receive` | Enable or disable LLDP receive on an interface | § 41-9 |
| `lldp_reinit` | Configure LLDP re-initialization delay | § 41-10 |
| `lldp_run` | Enable or disable LLDP globally | § 41-11 |
| `lldp_forward` | Enable or disable LLDP forwarding on an interface | § 41-12 |
| `lldp_tlv_select` | Configure LLDP basic TLV selection on an interface | § 41-13 |
| `lldp_transmit` | Enable or disable LLDP transmit on an interface | § 41-14 |
| `lldp_tx_delay` | Configure LLDP transmit delay | § 41-15 |
| `lldp_tx_interval` | Configure LLDP transmit interval | § 41-16 |
| `lldp_snmp_traps` | Enable or disable LLDP SNMP traps globally | § 41-17 |
| `lldp_notification_enable` | Enable or disable LLDP notification on an interface | § 41-18 |
| `lldp_subtype` | Configure LLDP subtype for management address | § 41-19 |
| `show_lldp` | Display LLDP configuration | § 41-20 |
| `show_lldp_interface` | Display LLDP configuration for an interface | § 41-21 |
| `show_lldp_local_interface` | Display LLDP local information for an interface | § 41-22 |
| `show_lldp_management_address` | Display LLDP management address information | § 41-23 |
| `show_lldp_neighbor_interface` | Display LLDP neighbor information for an interface | § 41-24 |
| `show_lldp_traffic` | Display LLDP traffic statistics | § 41-25 |
| `show_lldp_traffic_interface` | Display LLDP traffic statistics for an interface | § 41-26 |

### Loopback Detection (LBD) Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `loopback_detection_global` | Enable or disable loopback detection globally | § 42-1 |
| `loopback_detection_interface` | Enable or disable loopback detection on an interface | § 42-2 |
| `loopback_detection_interval` | Configure loopback detection interval | § 42-3 |
| `loopback_detection_vlan` | Configure loopback detection on a VLAN | § 42-4 |
| `show_loopback_detection` | Display loopback detection status | § 42-5 |
| `loopback_detection_snmp_traps` | Enable or disable loopback detection SNMP traps | § 42-6 |

### MAC-based Authentication Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `mac_auth_system_auth_control` | Enable or disable MAC authentication globally | § 43-1 |
| `mac_auth_enable` | Enable or disable MAC authentication on an interface | § 43-2 |
| `mac_auth_password` | Configure MAC authentication password | § 43-3 |
| `mac_auth_username` | Configure MAC authentication username format | § 43-4 |
| `mac_auth_snmp_traps` | Enable or disable MAC authentication SNMP traps | § 43-5 |

### Mirror Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `monitor_session_destination` | Configure port monitor session destination | § 44-1 |
| `monitor_session_source` | Configure port monitor session source | § 44-2 |
| `show_monitor_session` | Display port monitor session configuration | § 44-3 |

### MLD Snooping Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `mld_snooping_clear_statistics` | Clear MLD snooping statistics | § 45-1 |
| `mld_snooping_enable` | Enable or disable MLD snooping globally or on a VLAN | § 45-2 |
| `mld_snooping_fast_leave` | Enable or disable MLD snooping fast leave on a VLAN | § 45-3 |
| `mld_snooping_last_listener_query_interval` | Configure MLD snooping last listener query interval | § 45-4 |
| `mld_snooping_mrouter` | Configure MLD snooping multicast router port | § 45-5 |
| `mld_snooping_querier` | Enable or disable MLD snooping querier on a VLAN | § 45-6 |
| `mld_snooping_query_interval` | Configure MLD snooping query interval | § 45-7 |
| `mld_snooping_query_max_response_time` | Configure MLD snooping query max response time | § 45-8 |
| `mld_snooping_query_version` | Configure MLD snooping query version | § 45-9 |
| `mld_snooping_robustness_variable` | Configure MLD snooping robustness variable | § 45-10 |
| `mld_snooping_static_group` | Configure MLD snooping static group | § 45-11 |
| `mld_snooping_minimum_version` | Enable or disable MLD snooping minimum version on a VLAN | § 45-12 |
| `show_mld_snooping` | Display MLD snooping configuration | § 45-13 |
| `show_mld_snooping_groups` | Display MLD snooping group information | § 45-14 |
| `show_mld_snooping_mrouter` | Display MLD snooping multicast router port information | § 45-15 |
| `show_mld_snooping_static_group` | Display MLD snooping static group information | § 45-16 |
| `show_mld_snooping_statistics` | Display MLD snooping statistics | § 45-17 |

### MSTP Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `mstp_instance` | Map VLANs to an MST instance | § 46-1 |
| `mstp_name` | Configure MST region name | § 46-2 |
| `mstp_revision` | Configure MST configuration revision number | § 46-3 |
| `show_spanning_tree_mst` | Display MSTP information | § 46-4 |
| `mstp_interface` | Configure MSTP cost or port-priority on an interface | § 46-5 |
| `mstp_max_hops` | Configure MSTP maximum hop count | § 46-7 |
| `mstp_hello_time` | Configure MSTP hello-time on an interface | § 46-8 |
| `mstp_priority` | Configure MSTP bridge priority | § 46-9 |

### Neighbor Discovery (ND) Inspection Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `nd_inspection_policy` | Create or remove an ND inspection policy | § 47-1 |
| `nd_inspection_validate_source_mac` | Enable or disable source MAC validation in an ND inspection policy | § 47-2 |
| `nd_inspection_device_role` | Set device role in an ND inspection policy | § 47-3 |
| `nd_inspection_attach_policy` | Apply an ND inspection policy to an interface | § 47-4 |
| `show_nd_inspection_policy` | Display ND inspection policy information | § 47-5 |

### Network Access Authentication Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `auth_guest_vlan` | Configure authentication guest VLAN on an interface | § 48-1 |
| `auth_host_mode` | Configure authentication host-mode on an interface | § 48-2 |
| `auth_periodic` | Enable or disable periodic re-authentication on an interface | § 48-3 |
| `auth_timer_reauthentication` | Configure authentication re-authentication timer on an interface | § 48-4 |
| `auth_timer_restart` | Configure authentication restart timer on an interface | § 48-5 |
| `auth_username` | Configure a local authentication user | § 48-6 |
| `auth_clear_sessions` | Clear authentication sessions | § 48-7 |
| `auth_username_mac_format` | Configure MAC address format for authentication usernames | § 48-8 |
| `auth_max_users` | Configure maximum authenticated users | § 48-9 |
| `auth_mac_move_deny` | Enable or disable MAC move denial | § 48-10 |
| `auth_authorization_disable` | Enable or disable authorization | § 48-11 |
| `show_auth_sessions` | Display authentication sessions | § 48-12 |

### Network Protocol Port Protection Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `network_protocol_port_protect` | Enable or disable network protocol port protection | § 49-1 |
| `show_network_protocol_port_protect` | Display network protocol port protection status | § 49-2 |

### Port Security Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `port_security_clear` | Clear auto-learned secured MAC addresses | § 50-1 |
| `show_port_security` | Display port security settings | § 50-2 |
| `port_security_snmp_traps` | Enable or disable SNMP traps for port security | § 50-3 |
| `switchport_port_security` | Configure port security on an interface | § 50-4 |

### Power over Ethernet (PoE) Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `poe_pd_description` | Configure PoE PD description on an interface | § 51-1 |
| `poe_pd_legacy_support` | Enable or disable PoE legacy PD support | § 51-2 |
| `poe_pd_priority` | Configure PoE PD priority on an interface | § 51-3 |
| `poe_policy_preempt` | Enable or disable PoE policy preempt | § 51-4 |
| `poe_power_inline` | Configure PoE power inline on an interface | § 51-5 |
| `poe_usage_threshold` | Configure PoE usage threshold | § 51-6 |
| `poe_snmp_traps` | Enable or disable PoE SNMP traps | § 51-7 |
| `poe_clear_statistics` | Clear PoE statistics | § 51-8 |
| `show_poe_power_inline` | Display PoE power inline status | § 51-9 |
| `show_poe_power_module` | Display PoE power module status | § 51-10 |
| `poe_pd_alive` | Configure PoE PD alive check on an interface | § 51-11 |
| `show_poe_pd_alive` | Display PoE PD alive check status | § 51-12 |

### Power Saving Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `dim_led` | Enable or disable LED dimming | § 52-1 |
| `power_saving` | Enable or disable global power saving | § 52-2 |
| `power_saving_eee` | Enable or disable Energy Efficient Ethernet on an interface | § 52-3 |
| `power_saving_dim_led_time_range` | Configure the dim LED time range | § 52-4 |
| `power_saving_hibernation_time_range` | Configure the hibernation time range | § 52-5 |
| `power_saving_shutdown_time_range` | Configure the port shutdown time range | § 52-6 |
| `show_power_saving` | Display power saving configuration | § 52-7 |

### Protocol Independent Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `ip_route` | Configure a static IPv4 route | § 53-1 |
| `ipv6_route` | Configure a static IPv6 route | § 53-2 |
| `show_ip_route` | Display the IPv4 routing table | § 53-3 |
| `show_ip_route_summary` | Display a summary of the IPv4 routing table | § 53-4 |
| `show_ipv6_route` | Display the IPv6 routing table | § 53-5 |
| `show_ipv6_route_summary` | Display a summary of the IPv6 routing table | § 53-6 |

### Quality of Service (QoS) Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `policy_map_class` | Attach a class map to a policy map | § 54-1 |
| `class_map` | Create or modify a class-map | § 54-2 |
| `class_map_match` | Configure match criteria inside a class-map | § 54-3 |
| `mls_qos_cos` | Configure the default CoS value of an interface | § 54-4 |
| `mls_qos_dscp_mutation` | Attach an ingress DSCP mutation map to an interface | § 54-5 |
| `mls_qos_map_dscp_cos` | Configure the DSCP-to-CoS map on an interface | § 54-6 |
| `mls_qos_map_dscp_mutation_global` | Define a named DSCP mutation map | § 54-7 |
| `mls_qos_scheduler` | Configure the QoS scheduling mechanism on an interface | § 54-8 |
| `mls_qos_trust` | Configure the trust state of an interface | § 54-9 |
| `policy_map` | Create or remove a policy-map | § 54-10 |
| `priority_queue_cos_map` | Define a CoS-to-queue map | § 54-11 |
| `queue_rate_limit` | Configure the bandwidth for a CoS queue | § 54-12 |
| `rate_limit` | Configure ingress or egress bandwidth limit on an interface | § 54-13 |
| `service_policy` | Attach a service policy to an interface | § 54-14 |
| `policy_map_set` | Configure the set action inside a policy-map class | § 54-15 |
| `show_class_map` | Display class-map configuration | § 54-16 |
| `show_mls_qos_interface` | Display port-level QoS configuration | § 54-17 |
| `show_mls_qos_map_dscp_mutation` | Display the DSCP mutation map configuration | § 54-18 |
| `show_mls_qos_queueing` | Display QoS queueing information | § 54-19 |
| `show_policy_map` | Display the policy-map configuration | § 54-20 |
| `wdrr_queue_bandwidth` | Set the WDRR queue quantum on an interface | § 54-21 |
| `wrr_queue_bandwidth` | Set the WRR queue weights on an interface | § 54-22 |

### Remote Network MONitoring (RMON) Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `rmon_collection_stats` | Enable RMON statistics collection on an interface | § 55-1 |
| `rmon_collection_history` | Enable RMON history statistics on an interface | § 55-2 |
| `rmon_alarm` | Configure an RMON alarm entry | § 55-3 |
| `rmon_event` | Configure an RMON event entry | § 55-4 |
| `show_rmon_alarm` | Display the RMON alarm configuration | § 55-5 |
| `show_rmon_events` | Display the RMON event table | § 55-6 |
| `show_rmon_history` | Display RMON history statistics | § 55-7 |
| `show_rmon_statistics` | Display RMON Ethernet statistics | § 55-8 |
| `snmp_server_enable_traps_rmon` | Enable or disable SNMP traps for RMON | § 55-9 |

### Router Advertisement (RA) Guard Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `ipv6_nd_raguard_policy` | Create or remove an RA guard policy | § 56-1 |
| `ipv6_nd_raguard_device_role` | Configure the device role in an RA guard policy | § 56-2 |
| `ipv6_nd_raguard_match_access_list` | Filter RA messages by IPv6 access list in an RA guard policy | § 56-3 |
| `ipv6_nd_raguard_attach_policy` | Apply an RA guard policy on an interface | § 56-4 |
| `show_ipv6_nd_raguard_policy` | Display RA guard policy information | § 56-5 |

### Safeguard Engine Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `clear_cpu_protect_counters` | Clear CPU protect counters | § 57-1 |
| `cpu_protect_safeguard` | Enable or configure the Safeguard Engine | § 57-2 |
| `cpu_protect_sub_interface` | Configure CPU protect rate limit by sub-interface | § 57-3 |
| `cpu_protect_type` | Configure CPU protect rate limit by protocol type | § 57-4 |
| `show_cpu_protect_safeguard` | Display Safeguard Engine settings | § 57-5 |
| `show_cpu_protect_sub_interface` | Display CPU protect sub-interface settings | § 57-6 |
| `show_cpu_protect_type` | Display CPU protect type settings | § 57-7 |
| `snmp_server_enable_traps_safeguard_engine` | Enable or disable SNMP traps for Safeguard Engine | § 57-8 |

### Secure Shell (SSH) Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `crypto_key_generate` | Generate RSA or DSA key pair | § 58-1 |
| `crypto_key_zeroize` | Delete RSA or DSA key pair | § 58-2 |
| `ip_ssh_settings` | Configure SSH timeout and authentication retries | § 58-3 |
| `ip_ssh_server` | Enable or disable the SSH server | § 58-4 |
| `ip_ssh_service_port` | Configure the SSH service port | § 58-5 |
| `show_crypto_key_mypubkey` | Display RSA or DSA public key | § 58-6 |
| `show_ip_ssh` | Display SSH configuration settings | § 58-7 |
| `show_ssh` | Display SSH server connections | § 58-8 |
| `ssh_user_authentication_method` | Configure SSH authentication method for a user | § 58-9 |

### Secure Sockets Layer (SSL) Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `ssl_no_certificate` | Delete an imported certificate from a trust point | § 59-1 |
| `crypto_pki_import_pem` | Import PEM certificates and keys to a trust point | § 59-2 |
| `crypto_pki_trustpoint` | Create or remove a trust point | § 59-3 |
| `crypto_pki_certificate_chain` | Enter Certificate Chain Configuration Mode | § 59-4 |
| `crypto_pki_trustpoint_primary` | Set a trust point as primary | § 59-5 |
| `show_crypto_pki_trustpoints` | Display trust point information | § 59-6 |
| `show_ssl_service_policy` | Display SSL service policy | § 59-7 |
| `ssl_service_policy` | Configure an SSL service policy | § 59-8 |
| `crypto_pki_certificate_generate` | Generate a self-signed certificate | § 59-9 |

### Simple Network Management Protocol (SNMP) Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `show_snmp_trap_link_status` | Display per-interface link status trap state | § 60-1 |
| `show_snmp_server` | Display SNMP server settings | § 60-2 |
| `show_snmp_server_trap_sending` | Display per-port SNMP trap sending state | § 60-3 |
| `snmp_server` | Enable or disable the SNMP agent | § 60-4 |
| `snmp_server_contact` | Configure SNMP system contact information | § 60-5 |
| `snmp_server_enable_traps` | Enable or disable SNMP trap sending globally | § 60-6 |
| `snmp_server_enable_traps_snmp` | Enable or disable specific SNMP notification traps | § 60-7 |
| `snmp_server_location` | Configure SNMP system location | § 60-8 |
| `snmp_server_name` | Configure SNMP system name | § 60-9 |
| `snmp_server_trap_sending` | Enable or disable SNMP trap sending on an interface | § 60-10 |
| `snmp_server_service_port` | Configure the SNMP UDP port | § 60-11 |
| `snmp_server_response_broadcast_request` | Enable or disable SNMP broadcast request response | § 60-12 |
| `snmp_trap_link_status` | Enable or disable link-status traps on an interface | § 60-13 |
| `show_snmp` | Display SNMP settings | § 60-14 |
| `show_snmp_user` | Display SNMP user information | § 60-15 |
| `snmp_server_community` | Configure SNMP community string | § 60-16 |
| `snmp_server_engine_id` | Configure the SNMP engine ID | § 60-17 |
| `snmp_server_group` | Configure an SNMP group | § 60-18 |
| `snmp_server_host` | Configure an SNMP notification recipient | § 60-19 |
| `snmp_server_user` | Create or remove an SNMP user | § 60-20 |
| `snmp_server_view` | Create or remove an SNMP view entry | § 60-21 |

### Spanning Tree Protocol (STP) Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `clear_spanning_tree_detected_protocols` | Restart STP protocol migration | § 61-1 |
| `show_spanning_tree` | Display STP/RSTP information | § 61-2 |
| `show_spanning_tree_configuration_interface` | Display STP interface configuration | § 61-3 |
| `snmp_server_enable_traps_stp` | Enable or disable SNMP STP traps | § 61-4 |
| `spanning_tree_global_state` | Enable or disable STP globally | § 61-5 |
| `spanning_tree_timers` | Configure STP timer values | § 61-6 |
| `spanning_tree_state` | Enable or disable STP on an interface | § 61-7 |
| `spanning_tree_cost` | Configure STP port path cost | § 61-8 |
| `spanning_tree_guard_root` | Enable or disable STP root guard | § 61-9 |
| `spanning_tree_link_type` | Configure STP link type | § 61-10 |
| `spanning_tree_mode` | Configure STP mode (MSTP/RSTP/STP) | § 61-11 |
| `spanning_tree_portfast` | Configure STP port fast mode | § 61-12 |
| `spanning_tree_port_priority` | Configure STP port priority | § 61-13 |
| `spanning_tree_priority` | Configure STP bridge priority | § 61-14 |
| `spanning_tree_tcnfilter` | Enable or disable STP TCN filtering | § 61-15 |
| `spanning_tree_tx_hold_count` | Configure STP transmit hold count | § 61-16 |
| `spanning_tree_forward_bpdu` | Enable or disable STP BPDU forwarding | § 61-17 |

### Storm Control Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `snmp_server_enable_traps_storm_control` | Enable or disable SNMP storm control traps | § 62-1 |
| `storm_control` | Configure storm control thresholds and action | § 62-2 |
| `storm_control_polling` | Configure storm control polling interval and retries | § 62-3 |
| `show_storm_control` | Display storm control settings | § 62-4 |

### Surveillance VLAN Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `surveillance_vlan` | Configure surveillance VLAN | § 63-1 |
| `surveillance_vlan_aging` | Configure surveillance VLAN aging time | § 63-2 |
| `surveillance_vlan_enable` | Enable or disable surveillance VLAN on an interface | § 63-3 |
| `surveillance_vlan_mac_address` | Configure surveillance VLAN OUI | § 63-4 |
| `surveillance_vlan_onvif_discover_port` | Configure ONVIF discover port | § 63-5 |
| `surveillance_vlan_onvif_ipc_state` | Configure ONVIF IPC state | § 63-6 |
| `surveillance_vlan_onvif_ipc_description` | Configure ONVIF IPC description | § 63-7 |
| `surveillance_vlan_onvif_nvr_description` | Configure ONVIF NVR description | § 63-8 |
| `surveillance_vlan_qos` | Configure surveillance VLAN CoS priority | § 63-9 |
| `show_surveillance_vlan` | Display surveillance VLAN settings | § 63-10 |
| `show_surveillance_vlan_onvif_ipc` | Display ONVIF IPC information | § 63-11 |
| `show_surveillance_vlan_onvif_nvr` | Display ONVIF NVR information | § 63-12 |

### Switch Port Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `duplex` | Configure duplex mode on an interface | § 64-1 |
| `flowcontrol` | Configure flow control on an interface | § 64-2 |
| `mdix` | Configure MDIX state on an interface | § 64-3 |
| `speed` | Configure port speed on an interface | § 64-4 |

### System File Management Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `boot_config` | Configure boot configuration file | § 65-1 |
| `boot_image` | Configure boot image file | § 65-2 |
| `clear_running_config` | Clear the running configuration | § 65-3 |
| `reset_system` | Reset the system to factory defaults | § 65-4 |
| `configure_replace` | Replace running configuration | § 65-5 |
| `file_copy` | Copy files (TFTP upload/download, save config) | § 65-6 |
| `show_boot` | Display boot settings | § 65-7 |
| `show_running_config` | Display running configuration | § 65-8 |
| `show_startup_config` | Display startup configuration | § 65-9 |

### System Log Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `clear_logging` | Clear system log messages | § 66-1 |
| `logging_buffered` | Configure logging to local buffer | § 66-2 |
| `logging_discriminator` | Configure a logging discriminator | § 66-3 |
| `logging_server` | Configure a SYSLOG server | § 66-4 |
| `show_logging` | Display system log messages | § 66-5 |
| `show_attack_logging` | Display attack log messages | § 66-6 |
| `clear_attack_logging` | Clear attack log messages | § 66-7 |

### Time and SNTP Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `clock_set` | Set the system clock | § 67-1 |
| `clock_summer_time` | Configure daylight saving time | § 67-2 |
| `clock_timezone` | Configure the time zone | § 67-3 |
| `show_clock` | Display time and date | § 67-4 |
| `show_sntp` | Display SNTP server information | § 67-5 |
| `sntp_server` | Configure an SNTP server | § 67-6 |
| `sntp_enable` | Enable or disable SNTP | § 67-7 |
| `sntp_interval` | Configure SNTP polling interval | § 67-8 |

### Time Range Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `time_range_periodic` | Configure a periodic time range | § 68-1 |
| `show_time_range` | Display time range profiles | § 68-2 |
| `time_range` | Create or delete a time range profile | § 68-3 |

### Traffic Segmentation Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `show_traffic_segmentation_forward` | Display traffic segmentation | § 69-1 |
| `traffic_segmentation_forward` | Configure traffic segmentation | § 69-2 |

### Virtual LAN (VLAN) Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `vlan_acceptable_frame` | Configure acceptable frame types | § 70-1 |
| `vlan_ingress_checking` | Enable or disable ingress checking | § 70-2 |
| `show_vlan` | Display VLAN information (with structured `parsed` output) | § 70-3 |
| `vlan_switchport_access` | Configure access VLAN | § 70-4 |
| `vlan_switchport_hybrid_allowed` | Configure hybrid port allowed VLANs | § 70-5 |
| `vlan_switchport_hybrid_native` | Configure hybrid port native VLAN | § 70-6 |
| `vlan_switchport_mode` | Configure VLAN port mode | § 70-7 |
| `vlan_switchport_trunk_allowed` | Configure trunk port allowed VLANs | § 70-8 |
| `vlan_switchport_trunk_native` | Configure trunk port native VLAN | § 70-9 |
| `vlan` | Create or delete VLANs | § 70-10 |
| `vlan_name` | Configure VLAN name | § 70-11 |

### Voice VLAN Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `voice_vlan` | Configure voice VLAN | § 71-1 |
| `voice_vlan_aging` | Configure voice VLAN aging time | § 71-2 |
| `voice_vlan_enable` | Enable or disable voice VLAN on an interface | § 71-3 |
| `voice_vlan_mac_address` | Configure voice VLAN OUI | § 71-4 |
| `voice_vlan_mode` | Configure voice VLAN learning mode | § 71-5 |
| `voice_vlan_qos` | Configure voice VLAN CoS priority | § 71-6 |
| `show_voice_vlan` | Display voice VLAN settings | § 71-7 |

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

## Roles

The collection includes ready-to-use roles for common switch administration tasks.

All roles support a `<role_name>_save_config` variable (default: `false`). Set it to `true` to automatically save the running-config to startup-config after the role applies changes.

### `hardening`

Secures a switch by disabling insecure protocols and enforcing best practices:
disable HTTP/Telnet, enable HTTPS/SSH, enforce password encryption, set session timeouts, and apply management ACLs.

```yaml
- hosts: switches
  roles:
    - role: jaydee_io.dlink_dgs1250.hardening
      vars:
        hardening_session_timeout_ssh: 10
        hardening_mgmt_acl: mgmt-acl
```

### `monitoring`

Configures monitoring services: SNMP (multiple communities, traps, hosts), syslog (multiple servers), SNTP (multiple servers), LLDP (global settings), and RMON statistics.

```yaml
- hosts: switches
  roles:
    - role: jaydee_io.dlink_dgs1250.monitoring
      vars:
        monitoring_snmp_communities:
          - { community: public, access_type: ro }
          - { community: private, access_type: rw }
        monitoring_snmp_location: "Server room A"
        monitoring_snmp_hosts:
          - { host: 10.0.0.1, version: "2c", community: public }
        monitoring_snmp_traps: [snmp, stp, storm_control]
        monitoring_syslog_servers:
          - { address: 10.0.0.1, severity: warnings }
        monitoring_sntp_servers: [pool.ntp.org]
        monitoring_lldp_tx_interval: 30
```

### `base_config`

Applies baseline configuration: hostname, location, timezone, NTP, logging, STP mode, and VLAN creation.

```yaml
- hosts: switches
  roles:
    - role: jaydee_io.dlink_dgs1250.base_config
      vars:
        base_config_hostname: "sw-floor3"
        base_config_timezone_sign: "+"
        base_config_timezone_hours: 1
        base_config_sntp_server: "192.168.1.10"
        base_config_stp_mode: rstp
        base_config_vlans:
          - { id: 100, name: management }
          - { id: 200, name: users }
```

### `vlan_setup`

Creates VLANs and configures access/trunk ports in a single role.

```yaml
- hosts: switches
  roles:
    - role: jaydee_io.dlink_dgs1250.vlan_setup
      vars:
        vlan_setup_vlans:
          - { id: 100, name: management }
          - { id: 200, name: users }
        vlan_setup_access_ports:
          - { interface: eth1/0/1, vlan_id: 200 }
        vlan_setup_trunk_ports:
          - { interface: eth1/0/24, allowed_vlans: "100,200", native_vlan: 100 }
```

### `acl_setup`

Creates IP access lists with rules and applies them to interfaces.

```yaml
- hosts: switches
  roles:
    - role: jaydee_io.dlink_dgs1250.acl_setup
      vars:
        acl_setup_ip_access_lists:
          - name: WEB-FILTER
            extended: true
            rules:
              - "permit tcp any any eq 80"
              - "permit tcp any any eq 443"
              - "deny ip any any"
        acl_setup_interface_bindings:
          - { interface: eth1/0/1, acl_name: WEB-FILTER }
```

### `firmware_upgrade`

Uploads firmware via TFTP, sets boot image, and optionally reboots.

```yaml
- hosts: switches
  roles:
    - role: jaydee_io.dlink_dgs1250.firmware_upgrade
      vars:
        firmware_upgrade_tftp_source: "tftp://10.1.1.254/DGS-1250-28X_fw_2.10.B012.had"
        firmware_upgrade_boot_image: Image2
        firmware_upgrade_reboot: true
```

### `port_security`

Configures 802.1X, MAC-based authentication, and port security (MAC limiting).

```yaml
- hosts: switches
  roles:
    - role: jaydee_io.dlink_dgs1250.port_security
      vars:
        port_security_dot1x_ports:
          - { interface: eth1/0/1, control: auto }
          - { interface: eth1/0/2, control: auto, host_mode: multi-auth, max_users: 5 }
        port_security_ports:
          - { interface: eth1/0/1, maximum: 5, violation: restrict }
```

### `dhcp_snooping_setup`

Configures DHCP snooping, Dynamic ARP Inspection (DAI), and IP Source Guard.

```yaml
- hosts: switches
  roles:
    - role: jaydee_io.dlink_dgs1250.dhcp_snooping_setup
      vars:
        dhcp_snooping_setup_vlans: [100, 200]
        dhcp_snooping_setup_trusted_ports: ["eth1/0/24"]
        dhcp_snooping_setup_rate_limits:
          - { interface: eth1/0/1, rate: 15 }
        dhcp_snooping_setup_dai_vlans: [100, 200]
        dhcp_snooping_setup_dai_trusted_ports: ["eth1/0/24"]
```

### `qos_setup`

Configures QoS: trust mode, CoS/DSCP, class maps, policy maps, and service policies.

```yaml
- hosts: switches
  roles:
    - role: jaydee_io.dlink_dgs1250.qos_setup
      vars:
        qos_setup_trust_ports:
          - { interface: eth1/0/1, trust: dscp }
        qos_setup_class_maps:
          - name: VOICE
            match_type: match-any
            matches:
              - { criteria: dscp, value: "46" }
        qos_setup_policy_maps:
          - name: VOICE-POLICY
            classes:
              - { class_name: VOICE, set_action: cos-queue, set_value: 5 }
        qos_setup_service_policies:
          - { interface: eth1/0/1, policy_name: VOICE-POLICY }
```

### `link_aggregation`

Configures link aggregation (LACP/static) and port-channel load balancing.

```yaml
- hosts: switches
  roles:
    - role: jaydee_io.dlink_dgs1250.link_aggregation
      vars:
        link_aggregation_load_balance: src-dst-ip
        link_aggregation_port_channels:
          - channel_no: 1
            mode: active
            members:
              - { interface: eth1/0/23, lacp_timeout: short }
              - { interface: eth1/0/24, lacp_timeout: short }
```

### `storm_control_setup`

Configures storm control thresholds and loopback detection.

```yaml
- hosts: switches
  roles:
    - role: jaydee_io.dlink_dgs1250.storm_control_setup
      vars:
        storm_control_setup_ports:
          - { interface: eth1/0/1, traffic_type: broadcast, level_mode: percent, rise: 20, low: 10, action: drop }
        storm_control_setup_loopback_mode: port-based
        storm_control_setup_loopback_ports: ["eth1/0/1", "eth1/0/2"]
```

### `aaa_setup`

Configures AAA authentication with RADIUS/TACACS+ servers.

```yaml
- hosts: switches
  roles:
    - role: jaydee_io.dlink_dgs1250.aaa_setup
      vars:
        aaa_setup_radius_servers:
          - { host: 10.1.1.10, key: "s3cret" }
        aaa_setup_radius_group: CORP-RADIUS
        aaa_setup_auth_login_methods: ["group radius", "local"]
        aaa_setup_login_lines: [ssh, telnet]
```

### `stp_setup`

Configures Spanning Tree Protocol: global settings (mode, priority, timers) and per-interface parameters (portfast, guard root, cost, priority).

```yaml
- hosts: switches
  roles:
    - role: jaydee_io.dlink_dgs1250.stp_setup
      vars:
        stp_setup_mode: rstp
        stp_setup_priority: 4096
        stp_setup_timers:
          hello_time: 2
          max_age: 20
          forward_delay: 15
        stp_setup_interfaces:
          - { interface: eth1/0/1, portfast: true, cost: 20000 }
          - { interface: eth1/0/24, guard_root: true, port_priority: 32 }
```

### `lldp_setup`

Configures LLDP: global settings (TX interval, hold multiplier, TLV selection) and per-interface transmit/receive.

```yaml
- hosts: switches
  roles:
    - role: jaydee_io.dlink_dgs1250.lldp_setup
      vars:
        lldp_setup_tx_interval: 30
        lldp_setup_hold_multiplier: 4
        lldp_setup_interfaces:
          - { interface: eth1/0/1, transmit: false, receive: false }
```

### `ntp_setup`

Configures SNTP time synchronization with multiple servers.

```yaml
- hosts: switches
  roles:
    - role: jaydee_io.dlink_dgs1250.ntp_setup
      vars:
        ntp_setup_servers:
          - pool.ntp.org
          - 10.0.0.1
        ntp_setup_interval: 300
```

### `dns_setup`

Configures DNS: name servers, domain lookup, and static host entries.

```yaml
- hosts: switches
  roles:
    - role: jaydee_io.dlink_dgs1250.dns_setup
      vars:
        dns_setup_domain_lookup: enabled
        dns_setup_servers:
          - 8.8.8.8
          - 8.8.4.4
        dns_setup_hosts:
          - { host_name: switch1, address: 10.0.0.1 }
```

### `static_routes_setup`

Configures IPv4 and IPv6 static routes.

```yaml
- hosts: switches
  roles:
    - role: jaydee_io.dlink_dgs1250.static_routes_setup
      vars:
        static_routes_setup_ipv4:
          - { network_prefix: 10.0.0.0, network_mask: 255.255.255.0, next_hop: 192.168.1.1 }
          - { network_prefix: 172.16.0.0, network_mask: 255.255.0.0, next_hop: 192.168.1.1, route_type: backup }
        static_routes_setup_ipv6:
          - { network_prefix: "2001:db8::/32", next_hop: "fe80::1" }
```

## Example playbooks

Sample playbooks are available in [`docs/examples/`](docs/examples/):

| Playbook | Description |
|----------|-------------|
| `initial_provisioning.yml` | Full initial switch setup using base roles |
| `backup_restore.yml` | Backup and restore configuration via TFTP |
| `security_audit.yml` | Audit switch for common security issues |
| `firmware_update.yml` | Download and apply firmware update via TFTP |
| `full_monitoring.yml` | Deploy full monitoring stack (SNMP, syslog, NTP, LLDP, STP) |
| `network_baseline.yml` | Establish network foundations (DNS, NTP, static routes, STP, LLDP) |

## Running tests

### Unit tests

```bash
pip install pytest
pytest tests/unit/
```

### Integration tests

Integration tests run real commands against a physical switch. Copy the sample config and fill in your test switch details:

```bash
cp tests/integration/integration_config.yml.sample tests/integration/integration_config.yml
# Edit integration_config.yml with your switch IP, credentials, etc.
ansible-test integration --local
```

## Changelog

A detailed changelog in [antsibull-changelog](https://github.com/ansible-community/antsibull-changelog) format is available in [`changelogs/changelog.yaml`](changelogs/changelog.yaml).
