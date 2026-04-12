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
