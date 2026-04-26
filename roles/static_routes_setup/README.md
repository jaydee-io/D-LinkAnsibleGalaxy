# static_routes_setup

Configure static routes on a D-Link DGS-1250 switch: IPv4 and IPv6 routes.

## Role Variables

| Variable | Default | Description |
|---|---|---|
| `static_routes_setup_ipv4` | `[]` | List of IPv4 routes (`{network_prefix, network_mask, next_hop, route_type}`) |
| `static_routes_setup_ipv6` | `[]` | List of IPv6 routes (`{network_prefix, next_hop, route_type}`) |
| `static_routes_setup_save_config` | `false` | Save config after applying |

## Example Playbook

```yaml
- hosts: dlink_switches
  roles:
    - role: jaydee_io.dlink_dgs1250.static_routes_setup
      static_routes_setup_ipv4:
        - { network_prefix: 10.0.0.0, network_mask: 255.255.255.0, next_hop: 192.168.1.1 }
        - { network_prefix: 172.16.0.0, network_mask: 255.255.0.0, next_hop: 192.168.1.1, route_type: backup }
      static_routes_setup_ipv6:
        - { network_prefix: "2001:db8::/32", next_hop: "fe80::1" }
      static_routes_setup_save_config: true
```

## License

GPL-2.0-or-later
