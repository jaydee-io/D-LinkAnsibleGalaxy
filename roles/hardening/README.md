# hardening

Harden a D-Link DGS-1250 switch: disable HTTP/Telnet, enable HTTPS/SSH, enforce password encryption, session timeouts, and management ACL.

## Role Variables

| Variable | Default | Description |
|---|---|---|
| `hardening_http_server` | `disabled` | HTTP server state |
| `hardening_https_server` | `enabled` | HTTPS server state |
| `hardening_https_ssl_policy` | — | SSL policy name for HTTPS |
| `hardening_ssh_server` | `enabled` | SSH server state |
| `hardening_telnet_server` | `disabled` | Telnet server state |
| `hardening_password_encryption` | `enabled` | Password encryption state |
| `hardening_session_timeout_console` | `5` | Console session timeout (minutes) |
| `hardening_session_timeout_telnet` | `5` | Telnet session timeout (minutes) |
| `hardening_session_timeout_ssh` | `10` | SSH session timeout (minutes) |
| `hardening_mgmt_acl` | — | Management ACL name |
| `hardening_mgmt_acl_lines` | `[ssh, telnet]` | Line types to apply the ACL to |
| `hardening_save_config` | `false` | Save running-config to startup-config after applying the role |

## Example Playbook

```yaml
- hosts: dlink_switches
  roles:
    - role: jaydee_io.dlink_dgs1250.hardening
      hardening_session_timeout_ssh: 15
      hardening_mgmt_acl: MGMT-ACL
```

## License

GPL-2.0-or-later
