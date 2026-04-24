# dhcp_snooping_setup

Configure DHCP snooping, Dynamic ARP Inspection (DAI), and IP Source Guard on a D-Link DGS-1250 switch.

## Role Variables

| Variable | Default | Description |
|---|---|---|
| `dhcp_snooping_setup_enabled` | `true` | Enable DHCP snooping globally |
| `dhcp_snooping_setup_vlans` | `[]` | List of VLAN IDs to protect |
| `dhcp_snooping_setup_trusted_ports` | `[]` | Trusted uplink interfaces |
| `dhcp_snooping_setup_rate_limits` | `[]` | List of `{interface, rate}` dicts (pps) |
| `dhcp_snooping_setup_verify_mac` | `true` | Verify source MAC matches DHCP client |
| `dhcp_snooping_setup_dai_vlans` | `[]` | VLANs to enable DAI on |
| `dhcp_snooping_setup_dai_trusted_ports` | `[]` | DAI trusted interfaces |
| `dhcp_snooping_setup_dai_validate_src_mac` | `true` | DAI: validate source MAC |
| `dhcp_snooping_setup_dai_validate_dst_mac` | `false` | DAI: validate destination MAC |
| `dhcp_snooping_setup_dai_validate_ip` | `true` | DAI: validate IP |
| `dhcp_snooping_setup_ip_verify_source_ports` | `[]` | Ports to enable IP Source Guard on |

## Example Playbook

```yaml
- hosts: dlink_switches
  roles:
    - role: jaydee_io.dlink_dgs1250.dhcp_snooping_setup
      dhcp_snooping_setup_vlans: [100, 200]
      dhcp_snooping_setup_trusted_ports:
        - eth1/0/24
        - eth1/0/28
      dhcp_snooping_setup_rate_limits:
        - { interface: eth1/0/1, rate: 15 }
        - { interface: eth1/0/2, rate: 15 }
      dhcp_snooping_setup_dai_vlans: [100, 200]
      dhcp_snooping_setup_dai_trusted_ports:
        - eth1/0/24
        - eth1/0/28
      dhcp_snooping_setup_ip_verify_source_ports:
        - eth1/0/1
        - eth1/0/2
```

## License

GPL-2.0-or-later
