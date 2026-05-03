# ntp_setup

Configure SNTP time synchronization on a D-Link DGS-1250 switch.

## Role Variables

| Variable | Default | Description |
|---|---|---|
| `ntp_setup_enabled` | `enabled` | SNTP state |
| `ntp_setup_servers` | `[]` | List of SNTP server addresses |
| `ntp_setup_interval` | `720` | Polling interval (seconds) |
| `ntp_setup_save_config` | `false` | Save config after applying |

## Example Playbook

```yaml
- hosts: dlink_switches
  roles:
    - role: jaydee_io.dlink_dgs1250.ntp_setup
      ntp_setup_servers:
        - pool.ntp.org
        - 10.0.0.1
      ntp_setup_interval: 300
      ntp_setup_save_config: true
```

## Variable validation

The role imports a `validate.yml` task file that uses `ansible.builtin.assert` to validate user-provided variables (types, ranges, required fields) before any configuration is applied. The validation step is tagged `[validate]`, so you can run validation only — without touching the switch — with `--tags validate`:

```bash
ansible-playbook play.yml --tags validate
```

## License

GPL-2.0-or-later
