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

### Chapter 21 - Digital Diagnostics Monitoring (DDM) Commands

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

### Chapter 22 - D-Link Discovery Protocol (DDP) Client Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `ddp` | Enable or disable DDP client globally or on an interface | § 22-1 |
| `ddp_report_timer` | Configure DDP report timer interval | § 22-2 |
| `ddp_show` | Display DDP configuration | § 22-3 |

### Chapter 23 - Domain Name System (DNS) Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `dns_clear_host` | Clear dynamically learned host entries | § 23-1 |
| `dns_ip_domain_lookup` | Enable or disable DNS domain name resolution | § 23-2 |
| `dns_ip_host` | Configure static host name to IP address mapping | § 23-3 |
| `dns_ip_name_server` | Configure DNS name server address | § 23-4 |
| `dns_ip_name_server_timeout` | Configure DNS name server timeout | § 23-5 |
| `dns_show_hosts` | Display DNS host configuration | § 23-6 |
| `dns_show_ip_name_server` | Display DNS name server configuration | § 23-7 |

### Chapter 24 - DoS Prevention Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `dos_prevention` | Enable or disable DoS prevention for a specific attack type | § 24-1 |
| `dos_prevention_show` | Display DoS prevention status and drop counters | § 24-2 |
| `dos_prevention_snmp_traps` | Enable or disable SNMP traps for DoS prevention | § 24-3 |

### Chapter 25 - Dynamic ARP Inspection Commands

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

### Chapter 26 - Error Recovery Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `errdisable_recovery` | Configure error recovery for causes and interval | § 26-1 |
| `show_errdisable_recovery` | Display error-disable recovery timer settings | § 26-2 |
| `snmp_server_enable_traps_errdisable` | Enable SNMP notifications for error-disabled state | § 26-3 |

### Chapter 27 - File System Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `delete_file` | Delete a file from the switch file system | § 27-1 |
| `dir` | Display file system directory listing | § 27-2 |
| `show_storage_media_info` | Display storage media information | § 27-3 |

### Chapter 28 - Filter Database (FDB) Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `clear_mac_address_table` | Clear dynamic MAC address table entries | § 28-1 |
| `mac_address_table_aging_time` | Configure MAC address table aging time | § 28-2 |
| `mac_address_table_learning` | Enable or disable MAC address learning on an interface | § 28-3 |
| `mac_address_table_notification_change` | Configure MAC address notification function | § 28-4 |
| `mac_address_table_static` | Add or remove static MAC address table entries | § 28-5 |
| `multicast_filtering_mode` | Configure multicast packet handling mode for a VLAN | § 28-6 |
| `show_mac_address_table` | Display MAC address table entries | § 28-7 |
| `show_mac_address_table_aging_time` | Display MAC address table aging time | § 28-8 |
| `show_mac_address_table_learning` | Display MAC address learning state | § 28-9 |
| `show_mac_address_table_notification_change` | Display MAC address notification configuration | § 28-10 |
| `show_multicast_filtering_mode` | Display multicast filtering mode for VLANs | § 28-11 |
| `snmp_server_enable_traps_mac_notification_change` | Enable SNMP MAC notification traps | § 28-12 |
| `snmp_trap_mac_notification_change` | Enable MAC address change notification trap on an interface | § 28-13 |

### Chapter 29 - Gratuitous ARP Trap Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `snmp_server_enable_traps_gratuitous_arp` | Enable SNMP notifications for gratuitous ARP | § 29-1 |

### Chapter 30 - Interface Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `clear_counters` | Clear counters for port interfaces | § 30-1 |
| `interface_description` | Set or remove interface description | § 30-2 |
| `show_counters` | Display interface statistic counters | § 30-5 |
| `show_interfaces` | Display interface information | § 30-6 |
| `show_interfaces_counters` | Display interface counters | § 30-7 |
| `show_interfaces_status` | Display interface connection status | § 30-8 |
| `show_interfaces_utilization` | Display interface port utilization | § 30-9 |
| `show_interfaces_auto_negotiation` | Display interface auto-negotiation information | § 30-10 |
| `show_interfaces_description` | Display interface description and link status | § 30-11 |

### Chapter 31 - IGMP Snooping Commands

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

### Chapter 32 - IP-MAC-Port Binding (IMPB) Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `impb_clear_violation` | Clear IMPB violation entries | § 32-1 |
| `impb_enable` | Enable or disable IMPB access control on an interface | § 32-2 |
| `show_impb` | Display IMPB configuration or violation entries | § 32-3 |
| `impb_snmp_traps` | Enable or disable SNMP traps for IMPB | § 32-4 |

### Chapter 33 - IP Multicast (IPMC) Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `show_ip_mroute_forwarding_cache` | Display IP multicast forwarding cache | § 33-1 |

### Chapter 34 - IP Multicast Version 6 (IPMCv6) Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `show_ipv6_mroute_forwarding_cache` | Display IPv6 multicast forwarding cache | § 34-1 |

### Chapter 35 - IP Source Guard Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `ip_verify_source` | Enable or disable IP source guard on an interface | § 35-1 |
| `ip_source_binding` | Configure IP source guard static binding entry | § 35-2 |
| `show_ip_source_binding` | Display IP source guard binding entries | § 35-3 |
| `show_ip_verify_source` | Display IP source guard hardware port ACL entries | § 35-4 |

### Chapter 36 - IP Utility Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `ping` | Ping a remote host | § 36-1 |
| `ping_access_class` | Configure ping access class | § 36-2 |

### Chapter 37 - IPv6 Snooping Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `ipv6_snooping_policy` | Create or delete an IPv6 snooping policy | § 37-1 |
| `ipv6_snooping_protocol` | Configure protocol snooping in an IPv6 snooping policy | § 37-2 |
| `ipv6_snooping_limit_address_count` | Configure IPv6 snooping binding entry limit | § 37-3 |
| `ipv6_snooping_attach_policy` | Attach an IPv6 snooping policy to a VLAN | § 37-4 |
| `ipv6_snooping_station_move_deny` | Enable or disable IPv6 snooping station move deny | § 37-5 |
| `show_ipv6_snooping_policy` | Display IPv6 snooping policy information | § 37-6 |

### Chapter 38 - IPv6 Source Guard Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `ipv6_source_binding` | Configure a static IPv6 source binding entry | § 38-1 |
| `ipv6_source_guard_policy` | Create or delete an IPv6 source guard policy | § 38-2 |
| `ipv6_source_guard_deny_global_autoconfig` | Enable or disable deny global-autoconfig in an IPv6 source guard policy | § 38-3 |
| `ipv6_source_guard_permit_link_local` | Enable or disable permit link-local in an IPv6 source guard policy | § 38-4 |
| `ipv6_source_guard_attach_policy` | Attach an IPv6 source guard policy to an interface | § 38-5 |
| `show_ipv6_source_guard_policy` | Display IPv6 source guard policy configuration | § 38-6 |
| `show_ipv6_neighbor_binding` | Display IPv6 neighbor binding table | § 38-7 |

### Chapter 39 - Jumbo Frame Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `max_rcv_frame_size` | Configure maximum receive frame size on an interface | § 39-1 |

### Chapter 40 - Link Aggregation Control Protocol (LACP) Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `channel_group` | Assign an interface to a channel group | § 40-1 |
| `lacp_port_priority` | Configure LACP port priority on an interface | § 40-2 |
| `lacp_timeout` | Configure LACP timeout on an interface | § 40-3 |
| `lacp_system_priority` | Configure LACP system priority | § 40-4 |
| `port_channel_load_balance` | Configure port-channel load balance algorithm | § 40-5 |
| `show_channel_group` | Display channel group information | § 40-6 |

### Chapter 41 - Link Layer Discovery Protocol (LLDP) Commands

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

### Chapter 42 - Loopback Detection (LBD) Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `loopback_detection_global` | Enable or disable loopback detection globally | § 42-1 |
| `loopback_detection_interface` | Enable or disable loopback detection on an interface | § 42-2 |
| `loopback_detection_interval` | Configure loopback detection interval | § 42-3 |
| `loopback_detection_vlan` | Configure loopback detection on a VLAN | § 42-4 |
| `show_loopback_detection` | Display loopback detection status | § 42-5 |
| `loopback_detection_snmp_traps` | Enable or disable loopback detection SNMP traps | § 42-6 |

### Chapter 43 - MAC-based Authentication Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `mac_auth_system_auth_control` | Enable or disable MAC authentication globally | § 43-1 |
| `mac_auth_enable` | Enable or disable MAC authentication on an interface | § 43-2 |
| `mac_auth_password` | Configure MAC authentication password | § 43-3 |
| `mac_auth_username` | Configure MAC authentication username format | § 43-4 |
| `mac_auth_snmp_traps` | Enable or disable MAC authentication SNMP traps | § 43-5 |

### Chapter 44 - Mirror Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `monitor_session_destination` | Configure port monitor session destination | § 44-1 |
| `monitor_session_source` | Configure port monitor session source | § 44-2 |
| `show_monitor_session` | Display port monitor session configuration | § 44-3 |

### Chapter 45 - MLD Snooping Commands

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

### Chapter 46 - MSTP Commands

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

### Chapter 47 - Neighbor Discovery (ND) Inspection Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `nd_inspection_policy` | Create or remove an ND inspection policy | § 47-1 |
| `nd_inspection_validate_source_mac` | Enable or disable source MAC validation in an ND inspection policy | § 47-2 |
| `nd_inspection_device_role` | Set device role in an ND inspection policy | § 47-3 |
| `nd_inspection_attach_policy` | Apply an ND inspection policy to an interface | § 47-4 |
| `show_nd_inspection_policy` | Display ND inspection policy information | § 47-5 |

### Chapter 48 - Network Access Authentication Commands

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

### Chapter 49 - Network Protocol Port Protection Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `network_protocol_port_protect` | Enable or disable network protocol port protection | § 49-1 |
| `show_network_protocol_port_protect` | Display network protocol port protection status | § 49-2 |

### Chapter 50 - Port Security Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `port_security_clear` | Clear auto-learned secured MAC addresses | § 50-1 |
| `show_port_security` | Display port security settings | § 50-2 |
| `port_security_snmp_traps` | Enable or disable SNMP traps for port security | § 50-3 |
| `switchport_port_security` | Configure port security on an interface | § 50-4 |

### Chapter 51 - Power over Ethernet (PoE) Commands

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

### Chapter 52 - Power Saving Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `dim_led` | Enable or disable LED dimming | § 52-1 |
| `power_saving` | Enable or disable global power saving | § 52-2 |
| `power_saving_eee` | Enable or disable Energy Efficient Ethernet on an interface | § 52-3 |
| `power_saving_dim_led_time_range` | Configure the dim LED time range | § 52-4 |
| `power_saving_hibernation_time_range` | Configure the hibernation time range | § 52-5 |
| `power_saving_shutdown_time_range` | Configure the port shutdown time range | § 52-6 |
| `show_power_saving` | Display power saving configuration | § 52-7 |

### Chapter 53 - Protocol Independent Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `ip_route` | Configure a static IPv4 route | § 53-1 |
| `ipv6_route` | Configure a static IPv6 route | § 53-2 |
| `show_ip_route` | Display the IPv4 routing table | § 53-3 |
| `show_ip_route_summary` | Display a summary of the IPv4 routing table | § 53-4 |
| `show_ipv6_route` | Display the IPv6 routing table | § 53-5 |
| `show_ipv6_route_summary` | Display a summary of the IPv6 routing table | § 53-6 |

### Chapter 54 - Quality of Service (QoS) Commands

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

### Chapter 55 - Remote Network MONitoring (RMON) Commands

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

### Chapter 56 - Router Advertisement (RA) Guard Commands

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `ipv6_nd_raguard_policy` | Create or remove an RA guard policy | § 56-1 |
| `ipv6_nd_raguard_device_role` | Configure the device role in an RA guard policy | § 56-2 |
| `ipv6_nd_raguard_match_access_list` | Filter RA messages by IPv6 access list in an RA guard policy | § 56-3 |
| `ipv6_nd_raguard_attach_policy` | Apply an RA guard policy on an interface | § 56-4 |
| `show_ipv6_nd_raguard_policy` | Display RA guard policy information | § 56-5 |

### Chapter 57 - Safeguard Engine Commands

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

### Chapter 58 - Secure Shell (SSH) Commands

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

### Chapter 59 - Secure Sockets Layer (SSL) Commands

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

### Chapter 60 - Simple Network Management Protocol (SNMP) Commands

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
