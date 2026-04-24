# port_security

Configure port security on a D-Link DGS-1250 switch: 802.1X, MAC limiting, and MAC-based authentication.

## Role Variables

| Variable | Default | Description |
|---|---|---|
| `port_security_dot1x_enabled` | `true` | Enable 802.1X system-wide |
| `port_security_dot1x_ports` | `[]` | List of `{interface, control, host_mode, max_users}` dicts |
| `port_security_ports` | `[]` | List of `{interface, maximum, violation}` dicts for MAC limiting |
| `port_security_mac_auth_enabled` | `false` | Enable MAC-based auth system-wide |
| `port_security_mac_auth_ports` | `[]` | List of interfaces to enable MAC auth on |
| `port_security_save_config` | `false` | Save running-config to startup-config after applying the role |

## Example Playbook

```yaml
- hosts: dlink_switches
  roles:
    - role: jaydee_io.dlink_dgs1250.port_security
      port_security_dot1x_ports:
        - { interface: eth1/0/1, control: auto }
        - { interface: eth1/0/2, control: auto, host_mode: multi-auth, max_users: 5 }
      port_security_ports:
        - { interface: eth1/0/1, maximum: 5, violation: restrict }
        - { interface: eth1/0/2, maximum: 10, violation: shutdown }
```

## License

GPL-2.0-or-later
