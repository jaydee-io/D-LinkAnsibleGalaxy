# lldp_setup

Configure LLDP on a D-Link DGS-1250 switch: global settings, TLV selection, and per-interface transmit/receive.

## Role Variables

### Global settings

| Variable | Default | Description |
|---|---|---|
| `lldp_setup_enabled` | `enabled` | LLDP global state |
| `lldp_setup_tx_interval` | — | TX interval (seconds) |
| `lldp_setup_hold_multiplier` | — | Hold multiplier |
| `lldp_setup_reinit` | — | Reinit delay (seconds) |
| `lldp_setup_tx_delay` | — | TX delay (seconds) |
| `lldp_setup_fast_count` | — | Fast count |
| `lldp_setup_notification` | — | Notification state |
| `lldp_setup_snmp_traps` | — | SNMP traps state |
| `lldp_setup_management_address` | — | Management address |
| `lldp_setup_forward` | — | LLDP forwarding state |
| `lldp_setup_tlv_select` | — | TLV selection |
| `lldp_setup_dot1_tlv_select` | — | 802.1 TLV selection |
| `lldp_setup_dot3_tlv_select` | — | 802.3 TLV selection |
| `lldp_setup_med_tlv_select` | — | MED TLV selection |
| `lldp_setup_subtype` | — | LLDP subtype |

### Per-interface settings

| Variable | Default | Description |
|---|---|---|
| `lldp_setup_interfaces` | `[]` | List of dicts with `interface`, `transmit` (bool), `receive` (bool) |

### General

| Variable | Default | Description |
|---|---|---|
| `lldp_setup_save_config` | `false` | Save config after applying |

## Example Playbook

```yaml
- hosts: dlink_switches
  roles:
    - role: jaydee_io.dlink_dgs1250.lldp_setup
      lldp_setup_tx_interval: 30
      lldp_setup_hold_multiplier: 4
      lldp_setup_notification: enabled
      lldp_setup_interfaces:
        - { interface: eth1/0/1, transmit: false, receive: false }
        - { interface: eth1/0/24, transmit: true, receive: false }
      lldp_setup_save_config: true
```

## License

GPL-2.0-or-later
