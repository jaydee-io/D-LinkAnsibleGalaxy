# aaa_setup

Configure AAA authentication (RADIUS/TACACS+) on a D-Link DGS-1250 switch.

## Role Variables

| Variable | Default | Description |
|---|---|---|
| `aaa_setup_enabled` | `true` | Enable AAA new-model |
| `aaa_setup_radius_servers` | `[]` | List of `{host, key, auth_port, acct_port, timeout, retransmit}` dicts |
| `aaa_setup_radius_group` | (none) | RADIUS server group name |
| `aaa_setup_tacacs_servers` | `[]` | List of `{host, key, port, timeout}` dicts |
| `aaa_setup_tacacs_group` | (none) | TACACS+ server group name |
| `aaa_setup_auth_login_methods` | (none) | Login authentication method list |
| `aaa_setup_auth_enable_methods` | (none) | Enable authentication method list |
| `aaa_setup_accounting_network_methods` | (none) | Network accounting method list |
| `aaa_setup_login_lines` | `[ssh, telnet]` | Lines to apply login authentication to |
| `aaa_setup_save_config` | `false` | Save running-config to startup-config after applying the role |

## Example Playbook

```yaml
- hosts: dlink_switches
  roles:
    - role: jaydee_io.dlink_dgs1250.aaa_setup
      aaa_setup_radius_servers:
        - { host: 10.1.1.10, key: "s3cret" }
        - { host: 10.1.1.11, key: "s3cret" }
      aaa_setup_radius_group: CORP-RADIUS
      aaa_setup_auth_login_methods:
        - "group radius"
        - local
      aaa_setup_auth_enable_methods:
        - "group radius"
        - enable
      aaa_setup_login_lines:
        - ssh
        - telnet
```

## License

GPL-2.0-or-later
