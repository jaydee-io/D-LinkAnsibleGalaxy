# monitoring

Configure monitoring on a D-Link DGS-1250 switch: SNMP, syslog, SNTP, LLDP, and RMON.

## Role Variables

### SNMP

| Variable | Default | Description |
|---|---|---|
| `monitoring_snmp_server` | `enabled` | SNMP server state |
| `monitoring_snmp_communities` | `[]` | List of SNMP communities (`{community, access_type}`) |
| `monitoring_snmp_community` | — | Single SNMP community (backward compat) |
| `monitoring_snmp_community_access` | `ro` | Single community access (`ro` or `rw`) |
| `monitoring_snmp_location` | — | SNMP location string |
| `monitoring_snmp_contact` | — | SNMP contact string |
| `monitoring_snmp_engine_id` | — | SNMP engine ID |
| `monitoring_snmp_hosts` | `[]` | List of SNMP trap receivers (`{host, version, community}`) |
| `monitoring_snmp_host` | — | Single trap receiver (backward compat) |
| `monitoring_snmp_host_version` | `2c` | Single trap version |
| `monitoring_snmp_host_community` | — | Single trap community |
| `monitoring_snmp_traps` | `[]` | Trap categories to enable (snmp, stp, storm_control, rmon, safeguard_engine, errdisable, mac_notification_change, gratuitous_arp) |
| `monitoring_snmp_service_port` | — | SNMP service port |

### Syslog

| Variable | Default | Description |
|---|---|---|
| `monitoring_syslog_buffered` | `enabled` | Buffered syslog state |
| `monitoring_syslog_buffered_severity` | `warnings` | Buffered syslog severity |
| `monitoring_syslog_servers` | `[]` | List of syslog servers (`{address, severity}`) |
| `monitoring_syslog_server` | — | Single syslog server (backward compat) |
| `monitoring_syslog_server_severity` | `warnings` | Single server severity |
| `monitoring_syslog_discriminator` | — | Syslog discriminator name |

### SNTP

| Variable | Default | Description |
|---|---|---|
| `monitoring_sntp_enabled` | `enabled` | SNTP state |
| `monitoring_sntp_servers` | `[]` | List of SNTP server addresses |
| `monitoring_sntp_server` | — | Single SNTP server (backward compat) |
| `monitoring_sntp_interval` | `720` | SNTP polling interval (seconds) |

### LLDP

| Variable | Default | Description |
|---|---|---|
| `monitoring_lldp_enabled` | `enabled` | LLDP state |
| `monitoring_lldp_tx_interval` | — | LLDP TX interval (seconds) |
| `monitoring_lldp_hold_multiplier` | — | LLDP hold multiplier |
| `monitoring_lldp_reinit` | — | LLDP reinit delay (seconds) |
| `monitoring_lldp_tx_delay` | — | LLDP TX delay (seconds) |
| `monitoring_lldp_notification` | — | LLDP SNMP traps state |

### RMON

| Variable | Default | Description |
|---|---|---|
| `monitoring_rmon_interfaces` | `[]` | List of interfaces for RMON statistics |
| `monitoring_rmon_stats_index_start` | `1` | Starting index for RMON stats entries |

### General

| Variable | Default | Description |
|---|---|---|
| `monitoring_save_config` | `false` | Save running-config to startup-config after applying the role |

## Example Playbook

```yaml
- hosts: dlink_switches
  roles:
    - role: jaydee_io.dlink_dgs1250.monitoring
      monitoring_snmp_communities:
        - { community: public, access_type: ro }
        - { community: private, access_type: rw }
      monitoring_snmp_location: "Server room A"
      monitoring_snmp_contact: "admin@example.com"
      monitoring_snmp_hosts:
        - { host: 10.0.0.1, version: "2c", community: public }
      monitoring_snmp_traps: [snmp, stp, storm_control]
      monitoring_syslog_servers:
        - { address: 10.0.0.1, severity: warnings }
        - { address: 10.0.0.2, severity: informational }
      monitoring_sntp_servers: [pool.ntp.org, 10.0.0.1]
      monitoring_lldp_tx_interval: 30
      monitoring_save_config: true
```

## License

GPL-2.0-or-later
