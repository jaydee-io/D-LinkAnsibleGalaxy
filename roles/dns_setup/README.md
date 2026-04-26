# dns_setup

Configure DNS on a D-Link DGS-1250 switch: name servers, domain lookup, and static host entries.

## Role Variables

| Variable | Default | Description |
|---|---|---|
| `dns_setup_domain_lookup` | — | DNS domain lookup state |
| `dns_setup_servers` | `[]` | List of DNS name server addresses |
| `dns_setup_timeout` | — | Name server timeout (seconds) |
| `dns_setup_hosts` | `[]` | Static host entries (`{hostname, address}`) |
| `dns_setup_save_config` | `false` | Save config after applying |

## Example Playbook

```yaml
- hosts: dlink_switches
  roles:
    - role: jaydee_io.dlink_dgs1250.dns_setup
      dns_setup_domain_lookup: enabled
      dns_setup_servers:
        - 8.8.8.8
        - 8.8.4.4
      dns_setup_hosts:
        - { hostname: switch1, address: 10.0.0.1 }
      dns_setup_save_config: true
```

## License

GPL-2.0-or-later
