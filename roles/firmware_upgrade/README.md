# firmware_upgrade

Upload firmware via TFTP, set boot image, and optionally reboot a D-Link DGS-1250 switch.

## Role Variables

| Variable | Default | Description |
|---|---|---|
| `firmware_upgrade_tftp_source` | (required) | TFTP URL to the firmware file |
| `firmware_upgrade_boot_image` | `Image2` | Boot image slot: `Image1` or `Image2` |
| `firmware_upgrade_save_before` | `true` | Save running-config before upgrading |
| `firmware_upgrade_reboot` | `false` | Reboot the switch after uploading firmware |
| `firmware_upgrade_save_config` | `false` | Save running-config to startup-config after applying the role |

## Example Playbook

```yaml
- hosts: dlink_switches
  roles:
    - role: jaydee_io.dlink_dgs1250.firmware_upgrade
      firmware_upgrade_tftp_source: "tftp://10.1.1.254/DGS-1250-28X_fw_2.10.B012.had"
      firmware_upgrade_boot_image: Image2
      firmware_upgrade_reboot: true
```

## Variable validation

The role imports a `validate.yml` task file that uses `ansible.builtin.assert` to validate user-provided variables (types, ranges, required fields) before any configuration is applied. The validation step is tagged `[validate]`, so you can run validation only — without touching the switch — with `--tags validate`:

```bash
ansible-playbook play.yml --tags validate
```

## License

GPL-2.0-or-later
