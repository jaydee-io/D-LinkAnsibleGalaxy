# vlan_setup

Create VLANs and configure access/trunk ports on a D-Link DGS-1250 switch.

## Role Variables

| Variable | Default | Description |
|---|---|---|
| `vlan_setup_vlans` | `[]` | List of `{id, name}` dicts for VLANs to create |
| `vlan_setup_access_ports` | `[]` | List of `{interface, vlan_id}` dicts for access ports |
| `vlan_setup_trunk_ports` | `[]` | List of `{interface, allowed_vlans, native_vlan}` dicts for trunk ports |
| `vlan_setup_save_config` | `false` | Save running-config to startup-config after applying the role |

## Example Playbook

```yaml
- hosts: dlink_switches
  roles:
    - role: jaydee_io.dlink_dgs1250.vlan_setup
      vlan_setup_vlans:
        - { id: 100, name: management }
        - { id: 200, name: users }
        - { id: 300, name: servers }
      vlan_setup_access_ports:
        - { interface: eth1/0/1, vlan_id: 200 }
        - { interface: eth1/0/2, vlan_id: 200 }
        - { interface: eth1/0/3, vlan_id: 300 }
      vlan_setup_trunk_ports:
        - { interface: eth1/0/24, allowed_vlans: "100,200,300", native_vlan: 100 }
```

## License

GPL-2.0-or-later
