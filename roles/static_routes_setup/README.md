# static_routes_setup

Configure static routes on a D-Link DGS-1250 switch: IPv4 and IPv6 routes.

## Role Variables

| Variable | Default | Description |
|---|---|---|
| `static_routes_setup_ipv4` | `[]` | List of IPv4 routes (`{prefix, mask, next_hop, metric}`) |
| `static_routes_setup_ipv6` | `[]` | List of IPv6 routes (`{prefix, next_hop, metric}`) |
| `static_routes_setup_save_config` | `false` | Save config after applying |

## Example Playbook

```yaml
- hosts: dlink_switches
  roles:
    - role: jaydee_io.dlink_dgs1250.static_routes_setup
      static_routes_setup_ipv4:
        - { prefix: 10.0.0.0, mask: 255.255.255.0, next_hop: 192.168.1.1 }
        - { prefix: 172.16.0.0, mask: 255.255.0.0, next_hop: 192.168.1.1, metric: 10 }
      static_routes_setup_ipv6:
        - { prefix: "2001:db8::/32", next_hop: "fe80::1" }
      static_routes_setup_save_config: true
```

## License

GPL-2.0-or-later
