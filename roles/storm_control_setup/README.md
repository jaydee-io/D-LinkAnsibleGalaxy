# storm_control_setup

Configure storm control and loopback detection on a D-Link DGS-1250 switch.

## Role Variables

| Variable | Default | Description |
|---|---|---|
| `storm_control_ports` | `[]` | List of `{interface, traffic_type, level_mode, rise, low, action}` dicts |
| `storm_control_polling_interval` | (none) | Polling interval in seconds |
| `storm_control_polling_retries` | (none) | Number of retries |
| `storm_control_loopback_enabled` | `true` | Enable loopback detection globally |
| `storm_control_loopback_mode` | (none) | Mode: `port-based` or `vlan-based` |
| `storm_control_loopback_interval` | (none) | Detection interval in seconds |
| `storm_control_loopback_ports` | `[]` | Interfaces to enable loopback detection on |

## Example Playbook

```yaml
- hosts: dlink_switches
  roles:
    - role: jaydee_io.dlink_dgs1250.storm_control_setup
      storm_control_ports:
        - { interface: eth1/0/1, traffic_type: broadcast, level_mode: percent, rise: 20, low: 10, action: drop }
        - { interface: eth1/0/1, traffic_type: multicast, level_mode: percent, rise: 30, low: 15, action: drop }
      storm_control_loopback_mode: port-based
      storm_control_loopback_interval: 10
      storm_control_loopback_ports:
        - eth1/0/1
        - eth1/0/2
        - eth1/0/3
```

## License

GPL-2.0-or-later
