# qos_setup

Configure QoS on a D-Link DGS-1250 switch: trust mode, CoS/DSCP, class maps, policy maps, and service policies.

## Role Variables

| Variable | Default | Description |
|---|---|---|
| `qos_setup_trust_ports` | `[]` | List of `{interface, trust}` dicts (`cos` or `dscp`) |
| `qos_setup_cos_ports` | `[]` | List of `{interface, cos_value}` dicts (0-7) |
| `qos_setup_scheduler_ports` | `[]` | List of `{interface, algorithm}` dicts (`sp`, `rr`, `wrr`, `wdrr`) |
| `qos_setup_class_maps` | `[]` | List of `{name, match_type, matches}` dicts |
| `qos_setup_policy_maps` | `[]` | List of `{name, classes}` dicts |
| `qos_setup_service_policies` | `[]` | List of `{interface, policy_name}` dicts |

## Example Playbook

```yaml
- hosts: dlink_switches
  roles:
    - role: jaydee_io.dlink_dgs1250.qos_setup
      qos_setup_trust_ports:
        - { interface: eth1/0/1, trust: dscp }
      qos_setup_class_maps:
        - name: VOICE
          match_type: match-any
          matches:
            - { criteria: dscp, value: "46" }
            - { criteria: cos, value: "5" }
      qos_setup_policy_maps:
        - name: VOICE-POLICY
          classes:
            - { class_name: VOICE, set_action: cos-queue, set_value: 5 }
      qos_setup_service_policies:
        - { interface: eth1/0/1, policy_name: VOICE-POLICY }
```

## License

GPL-2.0-or-later
