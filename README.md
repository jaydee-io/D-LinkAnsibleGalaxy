# D-Link DGS-1250 Ansible Collection

Ansible Galaxy collection for administering D-Link DGS-1250 Series Gigabit Ethernet Smart Managed Switches.

## Documentation

[DGS-1250 Series CLI Reference Guide v2.04](https://support.dlink.com/resource/products/DGS-1250-SERIES/REVA/DGS-1250%20Series_A1%20A2_CLI%20Manual_v2.04(US).pdf)

## Requirements

- Ansible >= 2.14
- Python >= 3.9
- `ansible.netcommon` collection >= 2.0.0

## Installation

```bash
ansible-galaxy collection install dlink.dgs1250
```

## Inventory

The collection uses the `ansible.netcommon.network_cli` connection plugin.
Connection parameters are defined in the inventory, not in individual tasks.

### INI format

```ini
[switches]
sw1 ansible_host=192.168.1.1
sw2 ansible_host=192.168.1.2

[switches:vars]
ansible_connection=ansible.netcommon.network_cli
ansible_network_os=dlink.dgs1250.dgs1250
ansible_user=admin
ansible_password=admin
ansible_port=22
```

### YAML format

```yaml
all:
  children:
    switches:
      hosts:
        sw1:
          ansible_host: 192.168.1.1
        sw2:
          ansible_host: 192.168.1.2
      vars:
        ansible_connection: ansible.netcommon.network_cli
        ansible_network_os: dlink.dgs1250.dgs1250
        ansible_user: admin
        ansible_password: admin
        ansible_port: 22
```

### Connection variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ansible_connection` | yes | Must be `ansible.netcommon.network_cli` |
| `ansible_network_os` | yes | Must be `dlink.dgs1250.dgs1250` |
| `ansible_host` | yes | IP address or hostname of the switch |
| `ansible_user` | yes | SSH username |
| `ansible_password` | yes | SSH password |
| `ansible_port` | no | SSH port (default: 22) |

## Modules

| Module | Description | CLI Reference |
|--------|-------------|---------------|
| `environment` | Display fan, temperature, and power status | § 2-10 |
| `unit` | Display model, serial number, uptime, and memory usage | § 2-11 |
| `cpu_utilization` | Display CPU utilization (5s, 1min, 5min) | § 2-12 |
| `version` | Display system MAC address, hardware and firmware version | § 2-13 |
| `snmp_environment_traps` | Enable or disable SNMP traps for fan, power, temperature | § 2-14 |
| `environment_temperature_threshold` | Configure temperature thresholds (high/low) | § 2-15 |
| `memory_utilization` | Display DRAM and FLASH memory usage | § 2-16 |
| `privilege` | Display current privilege level | § 2-17 |
| `dot1x_clear_counters` | Clear 802.1X counters on all or specific interfaces | § 3-1 |
| `dot1x_control_direction` | Configure 802.1X traffic control direction (both/in) on a port | § 3-2 |
| `dot1x_default` | Reset 802.1X parameters to defaults on a port | § 3-3 |
| `dot1x_port_control` | Configure port authorization state (auto/force-authorized/force-unauthorized) | § 3-4 |
| `dot1x_forward_pdu` | Enable or disable 802.1X PDU forwarding on a port | § 3-5 |
| `dot1x_initialize` | Initialize 802.1X authenticator state machine on a port or MAC address | § 3-6 |
| `dot1x_max_req` | Configure maximum EAP request retransmissions (1-10) on a port | § 3-7 |
| `dot1x_pae_authenticator` | Enable or disable 802.1X PAE authenticator on a port | § 3-8 |
| `dot1x_re_authenticate` | Re-authenticate 802.1X on a port or MAC address | § 3-9 |
| `dot1x_system_auth_control` | Enable or disable 802.1X authentication globally | § 3-10 |
| `dot1x_timeout` | Configure 802.1X timers (server-timeout, supp-timeout, tx-period) on a port | § 3-11 |
| `dot1x_show` | Display 802.1X global or interface configuration | § 3-12 |
| `dot1x_show_diagnostics` | Display 802.1X diagnostics counters per interface | § 3-13 |
| `dot1x_show_statistics` | Display 802.1X EAPOL frame statistics per interface | § 3-14 |
| `dot1x_show_session_statistics` | Display 802.1X session statistics per interface | § 3-15 |
| `dot1x_snmp_traps` | Enable or disable 802.1X SNMP traps | § 3-16 |

## Usage example

```yaml
- name: Check switch status
  hosts: switches
  gather_facts: false
  tasks:
    - name: Get environment status
      dlink.dgs1250.environment:
      register: env

    - name: Show temperatures
      ansible.builtin.debug:
        var: env.temperatures

    - name: Get CPU utilization
      dlink.dgs1250.cpu_utilization:
      register: cpu

    - name: Warn if CPU is high
      ansible.builtin.debug:
        msg: "High CPU: {{ cpu.five_seconds_percent }}%"
      when: cpu.five_seconds_percent > 80

    - name: Get unit information
      dlink.dgs1250.unit:
      register: unit_info

    - name: Show uptime
      ansible.builtin.debug:
        msg: "Uptime: {{ unit_info.unit.uptime.days }}d {{ unit_info.unit.uptime.hours }}h"

    - name: Set temperature thresholds
      dlink.dgs1250.environment_temperature_threshold:
        high: 100
        low: 20
```

## Running unit tests

```bash
pip install pytest
pytest tests/unit/
```
