# monitoring

Configure monitoring on a D-Link DGS-1250 switch: SNMP, syslog, SNTP, LLDP, and RMON.

## Role Variables

| Variable | Default | Description |
|---|---|---|
| `monitoring_snmp_server` | `enabled` | SNMP server state |
| `monitoring_snmp_community` | — | SNMP community string |
| `monitoring_snmp_community_access` | `ro` | SNMP community access (`ro` or `rw`) |
| `monitoring_snmp_location` | — | SNMP location string |
| `monitoring_snmp_contact` | — | SNMP contact string |
| `monitoring_snmp_host` | — | SNMP trap receiver address |
| `monitoring_snmp_host_version` | `2c` | SNMP trap version |
| `monitoring_snmp_host_community` | — | SNMP trap community |
| `monitoring_syslog_buffered` | `enabled` | Buffered syslog state |
| `monitoring_syslog_buffered_severity` | `warnings` | Buffered syslog severity |
| `monitoring_syslog_server` | — | Remote syslog server address |
| `monitoring_syslog_server_severity` | `warnings` | Remote syslog severity |
| `monitoring_sntp_enabled` | `enabled` | SNTP state |
| `monitoring_sntp_server` | — | SNTP server address |
| `monitoring_sntp_interval` | `720` | SNTP polling interval (seconds) |
| `monitoring_lldp_enabled` | `enabled` | LLDP state |
| `monitoring_rmon_interfaces` | `[]` | List of interfaces for RMON statistics |
| `monitoring_rmon_stats_index_start` | `1` | Starting index for RMON stats entries |
| `monitoring_save_config` | `false` | Save running-config to startup-config after applying the role |

## Example Playbook

```yaml
- hosts: dlink_switches
  roles:
    - role: jaydee_io.dlink_dgs1250.monitoring
      monitoring_snmp_community: public
      monitoring_syslog_server: 10.0.0.1
      monitoring_sntp_server: pool.ntp.org
```

## License

GPL-2.0-or-later
