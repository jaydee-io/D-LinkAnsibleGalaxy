# base_config

Apply base configuration to a D-Link DGS-1250 switch: hostname, NTP, logging, STP mode, and VLANs.

## Role Variables

| Variable | Default | Description |
|---|---|---|
| `base_config_hostname` | — | System hostname |
| `base_config_location` | — | SNMP location string |
| `base_config_contact` | — | SNMP contact string |
| `base_config_timezone_sign` | `+` | UTC offset sign |
| `base_config_timezone_hours` | `0` | UTC offset hours |
| `base_config_timezone_minutes` | `0` | UTC offset minutes |
| `base_config_sntp_server` | — | SNTP server address |
| `base_config_syslog_server` | — | Syslog server address |
| `base_config_syslog_severity` | `warnings` | Syslog severity level |
| `base_config_stp_mode` | `rstp` | Spanning tree mode (`mstp`, `rstp`, or `stp`) |
| `base_config_vlans` | `[]` | List of `{id, name}` dicts for VLANs to create |
| `base_config_save_config` | `false` | Save running-config to startup-config after applying the role |

## Example Playbook

```yaml
- hosts: dlink_switches
  roles:
    - role: jaydee_io.dlink_dgs1250.base_config
      base_config_hostname: switch-01
      base_config_stp_mode: rstp
      base_config_vlans:
        - { id: 100, name: management }
        - { id: 200, name: users }
```

## License

GPL-2.0-or-later
