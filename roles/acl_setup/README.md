# acl_setup

Create IP access lists with rules and apply them to interfaces on a D-Link DGS-1250 switch.

## Role Variables

| Variable | Default | Description |
|---|---|---|
| `acl_setup_ip_access_lists` | `[]` | List of ACL dicts: `{name, extended, rules}` |
| `acl_setup_interface_bindings` | `[]` | List of `{interface, acl_name}` dicts to bind ACLs to ports |
| `acl_setup_save_config` | `false` | Save running-config to startup-config after applying the role |

## Example Playbook

```yaml
- hosts: dlink_switches
  roles:
    - role: jaydee_io.dlink_dgs1250.acl_setup
      acl_setup_ip_access_lists:
        - name: WEB-FILTER
          extended: true
          rules:
            - "permit tcp any any eq 80"
            - "permit tcp any any eq 443"
            - "deny ip any any"
      acl_setup_interface_bindings:
        - { interface: eth1/0/1, acl_name: WEB-FILTER }
        - { interface: eth1/0/2, acl_name: WEB-FILTER }
```

## License

GPL-2.0-or-later
