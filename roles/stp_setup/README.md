# stp_setup

Configure Spanning Tree Protocol on a D-Link DGS-1250 switch: global settings, timers, and per-interface parameters.

## Role Variables

| Variable | Default | Description |
|---|---|---|
| `stp_setup_global_state` | `enabled` | STP global state |
| `stp_setup_mode` | — | STP mode (stp, rstp, mstp) |
| `stp_setup_priority` | — | Bridge priority (0-61440, multiples of 4096) |
| `stp_setup_tx_hold_count` | — | TX hold count |
| `stp_setup_timers` | — | Dict with `hello_time`, `max_age`, `forward_delay` |
| `stp_setup_interfaces` | `[]` | Per-interface settings (see below) |
| `stp_setup_save_config` | `false` | Save config after applying |

### Per-interface settings

Each item in `stp_setup_interfaces` is a dict with:

| Key | Description |
|---|---|
| `interface` | Interface name (required) |
| `state` | STP state on interface |
| `portfast` | Enable portfast (bool) |
| `cost` | Path cost |
| `port_priority` | Port priority |
| `guard_root` | Enable root guard (bool) |
| `link_type` | Link type (point-to-point, shared, auto) |
| `forward_bpdu` | Forward BPDU (bool) |
| `tcnfilter` | TCN filter (bool) |

## Example Playbook

```yaml
- hosts: dlink_switches
  roles:
    - role: jaydee_io.dlink_dgs1250.stp_setup
      stp_setup_mode: rstp
      stp_setup_priority: 4096
      stp_setup_timers:
        hello_time: 2
        max_age: 20
        forward_delay: 15
      stp_setup_interfaces:
        - { interface: eth1/0/1, portfast: true, cost: 20000 }
        - { interface: eth1/0/24, guard_root: true, port_priority: 32 }
      stp_setup_save_config: true
```

## License

GPL-2.0-or-later
