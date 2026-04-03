# D-Link DGS-1250 Ansible Collection

Ansible Galaxy collection for administering D-Link DGS-1250 Series Gigabit Ethernet Smart Managed Switches.

## Documentation

[DGS-1250 Series CLI Reference Guide v2.04](https://support.dlink.com/resource/products/DGS-1250-SERIES/REVA/DGS-1250%20Series_A1%20A2_CLI%20Manual_v2.04(US).pdf)

## Requirements

- Ansible >= 2.14
- Python >= 3.9
- `paramiko` on the Ansible controller: `pip install paramiko`

## Installation

```bash
ansible-galaxy collection install dlink.dgs1250
```

## Modules

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `environment` | Display fan, temperature, and power status | § 2-10 |
| `unit` | Display model, serial number, uptime, and memory usage | § 2-11 |

## Usage example

```yaml
- name: Check switch environment
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Get environment status
      dlink.dgs1250.environment:
        host: 192.168.1.1
        username: admin
        password: admin
      register: env

    - name: Show temperatures
      ansible.builtin.debug:
        var: env.temperatures
```

## Running unit tests

```bash
pip install pytest
pytest tests/unit/
```
