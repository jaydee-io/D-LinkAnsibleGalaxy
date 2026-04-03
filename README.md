# D-Link DGS-1250 Ansible Collection

Ansible Galaxy collection for administering D-Link DGS-1250 Series Gigabit Ethernet Smart Managed Switches.

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
| `environment` | Display fan, temperature, and power status | ch. 2-10 |

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
