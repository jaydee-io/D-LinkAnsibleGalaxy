# link_aggregation

Configure link aggregation (LACP/static) and port-channel load balancing on a D-Link DGS-1250 switch.

## Role Variables

| Variable | Default | Description |
|---|---|---|
| `link_aggregation_load_balance` | `src-dst-mac` | Load balancing algorithm |
| `link_aggregation_system_priority` | (none) | LACP system priority (lower = higher) |
| `link_aggregation_port_channels` | `[]` | List of port-channel dicts (see below) |

### Port channel dict format

```yaml
- channel_no: 1             # Port-channel number (1-8)
  mode: active              # on (static), active (LACP), passive (LACP)
  members:
    - { interface: eth1/0/23, lacp_timeout: short }
    - { interface: eth1/0/24, lacp_priority: 100 }
```

## Example Playbook

```yaml
- hosts: dlink_switches
  roles:
    - role: jaydee_io.dlink_dgs1250.link_aggregation
      link_aggregation_load_balance: src-dst-ip
      link_aggregation_port_channels:
        - channel_no: 1
          mode: active
          members:
            - { interface: eth1/0/23, lacp_timeout: short }
            - { interface: eth1/0/24, lacp_timeout: short }
        - channel_no: 2
          mode: on
          members:
            - { interface: eth1/0/21 }
            - { interface: eth1/0/22 }
```

## License

GPL-2.0-or-later
