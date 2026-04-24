#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dgs1250_facts
short_description: Collect facts from a D-Link DGS-1250 switch and expose them as ansible_facts
description:
  - Gathers system information from a D-Link DGS-1250 switch by executing
    multiple CLI commands and returning all parsed data as C(ansible_facts).
  - Collects version, model, serial number, uptime, memory usage, CPU utilization,
    fan/temperature/power status, interface status, VLANs, and MAC address table.
  - Similar in spirit to C(ios_facts) from the Cisco IOS collection.
  - The C(gather) parameter allows selecting which subsets of facts to collect.
  - All facts are exposed under C(ansible_facts.dgs1250) for use in subsequent tasks.
version_added: "1.2.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  gather:
    description:
      - List of fact subsets to collect.
      - If omitted or set to C([all]), all subsets are gathered.
    type: list
    elements: str
    choices: [all, version, unit, environment, cpu, interfaces, vlans, mac_table]
    default: [all]
notes:
  - This command runs in User/Privileged EXEC Mode.
  - Facts are returned both as top-level return values and under C(ansible_facts.dgs1250).
"""

EXAMPLES = r"""
- name: Gather all facts
  jaydee_io.dlink_dgs1250.dgs1250_facts:
  register: facts

- name: Display switch model and firmware
  ansible.builtin.debug:
    msg: "{{ ansible_facts.dgs1250.version.module_name }} running {{ ansible_facts.dgs1250.version.runtime }}"

- name: Gather only version and CPU utilization
  jaydee_io.dlink_dgs1250.dgs1250_facts:
    gather:
      - version
      - cpu
  register: facts

- name: Fail if CPU is too high
  jaydee_io.dlink_dgs1250.dgs1250_facts:
    gather: [cpu]
  register: facts
  failed_when: facts.cpu.five_minutes_percent > 90

- name: List all VLANs
  jaydee_io.dlink_dgs1250.dgs1250_facts:
    gather: [vlans]

- name: Check interface status
  jaydee_io.dlink_dgs1250.dgs1250_facts:
    gather: [interfaces]

- name: Use facts in conditional tasks
  jaydee_io.dlink_dgs1250.dgs1250_facts:
    gather: [version, unit]

- name: Conditional on firmware version
  ansible.builtin.debug:
    msg: "Firmware is up to date"
  when: ansible_facts.dgs1250.version.runtime == "2.04.P003"
"""

RETURN = r"""
commands:
  description: List of CLI commands sent to the switch.
  returned: always
  type: list
  elements: str
ansible_facts:
  description: Facts returned under ansible_facts.dgs1250.
  returned: always
  type: dict
  contains:
    dgs1250:
      description: All gathered facts keyed by subset name.
      type: dict
version:
  description: Version information (MAC address, model, hardware revision, firmware).
  returned: when 'version' or 'all' is in gather
  type: dict
  contains:
    system_mac_address:
      description: System MAC address.
      type: str
    module_name:
      description: Model name of the switch.
      type: str
    hardware_version:
      description: Hardware revision.
      type: str
    runtime:
      description: Runtime firmware version.
      type: str
unit:
  description: Unit information (model, serial number, uptime, memory).
  returned: when 'unit' or 'all' is in gather
  type: dict
  contains:
    model:
      description: Model information.
      type: dict
    unit:
      description: Unit status (serial number, status, uptime).
      type: dict
    memory:
      description: Memory usage for DRAM and FLASH.
      type: list
      elements: dict
environment:
  description: Environment status (fans, temperatures, power modules).
  returned: when 'environment' or 'all' is in gather
  type: dict
  contains:
    temperatures:
      description: Temperature sensor readings.
      type: list
      elements: dict
    fans:
      description: Fan status.
      type: list
      elements: dict
    power:
      description: Power module status.
      type: list
      elements: dict
cpu:
  description: CPU utilization percentages.
  returned: when 'cpu' or 'all' is in gather
  type: dict
  contains:
    five_seconds_percent:
      description: CPU utilization over the last 5 seconds.
      type: int
    one_minute_percent:
      description: CPU utilization over the last 1 minute.
      type: int
    five_minutes_percent:
      description: CPU utilization over the last 5 minutes.
      type: int
interfaces:
  description: List of interface status entries.
  returned: when 'interfaces' or 'all' is in gather
  type: list
  elements: dict
  contains:
    port:
      description: Interface name.
      type: str
    status:
      description: Link status (connected, not-connected, disabled).
      type: str
    vlan:
      description: Access VLAN ID.
      type: str
    duplex:
      description: Duplex mode (auto, full, half).
      type: str
    speed:
      description: Port speed (auto, 10M, 100M, 1000M, 10G).
      type: str
    type:
      description: Port media type (1000BASE-T, 10GBASE-SR, etc.).
      type: str
vlans:
  description: List of configured VLANs.
  returned: when 'vlans' or 'all' is in gather
  type: list
  elements: dict
  contains:
    vlan_id:
      description: VLAN ID.
      type: int
    name:
      description: VLAN name.
      type: str
    tagged_ports:
      description: Tagged member ports.
      type: str
    untagged_ports:
      description: Untagged member ports.
      type: str
mac_table:
  description: List of MAC address table entries.
  returned: when 'mac_table' or 'all' is in gather
  type: list
  elements: dict
  contains:
    vlan:
      description: VLAN ID.
      type: int
    mac_address:
      description: MAC address.
      type: str
    type:
      description: Entry type (Static, Dynamic).
      type: str
    port:
      description: Forwarding port.
      type: str
"""

import re
from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import (
        run_command,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


# ---------------------------------------------------------------------------
# CLI commands for each subset
# ---------------------------------------------------------------------------

ALL_SUBSETS = ["version", "unit", "environment", "cpu",
               "interfaces", "vlans", "mac_table"]

SUBSET_COMMANDS = {
    "version": "show version",
    "unit": "show unit",
    "environment": "show environment",
    "cpu": "show cpu utilization",
    "interfaces": "show interfaces status",
    "vlans": "show vlan",
    "mac_table": "show mac-address-table",
}


def _build_commands(gather):
    """Return the list of CLI commands to run based on the requested subsets."""
    if "all" in gather:
        subsets = list(ALL_SUBSETS)
    else:
        subsets = [s for s in ALL_SUBSETS if s in gather]
    return subsets, [SUBSET_COMMANDS[s] for s in subsets]


# ---------------------------------------------------------------------------
# Output parsers
# ---------------------------------------------------------------------------

def _parse_version(output):
    result = {
        "system_mac_address": "",
        "module_name": "",
        "hardware_version": "",
        "runtime": "",
    }
    for line in output.splitlines():
        m = re.match(r"^\s*System MAC Address:\s*(\S+)", line)
        if m:
            result["system_mac_address"] = m.group(1).strip()
            continue
        m = re.match(r"^\s*Module Name\s+(\S+)", line)
        if m:
            result["module_name"] = m.group(1).strip()
            continue
        m = re.match(r"^\s*H/W\s+(\S+)", line)
        if m:
            result["hardware_version"] = m.group(1).strip()
            continue
        m = re.match(r"^\s*Runtime\s+(\S+)", line)
        if m:
            result["runtime"] = m.group(1).strip()
            continue
    return result


def _parse_unit(output):
    model = {"model_description": "", "model_name": ""}
    in_section = False
    for line in output.splitlines():
        if "Model Descr" in line and "Model Name" in line:
            in_section = True
            continue
        if not in_section:
            continue
        if re.match(r"^[-\s]+$", line):
            continue
        m = re.match(r"^\s*(.+?)\s{2,}(\S+)\s*$", line)
        if m:
            model["model_description"] = m.group(1).strip()
            model["model_name"] = m.group(2).strip()
            break

    unit_info = {
        "serial_number": "", "status": "",
        "uptime": {"days": 0, "hours": 0, "minutes": 0, "seconds": 0},
        "uptime_raw": 0,
    }
    in_section = False
    for line in output.splitlines():
        if "Serial-Number" in line and "Status" in line:
            in_section = True
            continue
        if not in_section:
            continue
        if re.match(r"^[-\s]+$", line):
            continue
        m = re.match(r"^\s*(\S+)\s{2,}(\S+)\s{2,}(\S+)\s*$", line)
        if m:
            unit_info["serial_number"] = m.group(1).strip()
            unit_info["status"] = m.group(2).strip()
            uptime_m = re.match(
                r"(\d+)DT(\d+)H(\d+)M(\d+)S", m.group(3).strip())
            if uptime_m:
                unit_info["uptime"] = {
                    "days": int(uptime_m.group(1)),
                    "hours": int(uptime_m.group(2)),
                    "minutes": int(uptime_m.group(3)),
                    "seconds": int(uptime_m.group(4)),
                }
                unit_info["uptime_raw"] = (
                    int(uptime_m.group(1)) * 86400
                    + int(uptime_m.group(2)) * 3600
                    + int(uptime_m.group(3)) * 60
                    + int(uptime_m.group(4))
                )
            break

    memory = []
    in_section = False
    for line in output.splitlines():
        if re.match(r"^\s*Memory\s+Total\s+Used\s+Free", line):
            in_section = True
            continue
        if not in_section:
            continue
        if re.match(r"^[-\s]+$", line):
            continue
        m = re.match(
            r"^\s*(DRAM|FLASH)\s+(\d+)\s*K\s+(\d+)\s*K\s+(\d+)\s*K\s*$", line
        )
        if m:
            memory.append({
                "type": m.group(1),
                "total_kb": int(m.group(2)),
                "used_kb": int(m.group(3)),
                "free_kb": int(m.group(4)),
            })

    return {"model": model, "unit": unit_info, "memory": memory}


def _parse_environment(output):
    temperatures = []
    in_section = False
    for line in output.splitlines():
        if "Detail Temperature Status" in line:
            in_section = True
            continue
        if in_section and line.startswith("Detail ") and "Temperature" not in line:
            break
        if not in_section:
            continue
        m = re.match(r"^(.+?)\s{2,}(\d+)C/(\d+)~(\d+)C\s*(\*?)\s*$", line)
        if m:
            current = int(m.group(2))
            thr_min = int(m.group(3))
            thr_max = int(m.group(4))
            temperatures.append({
                "name": m.group(1).strip(),
                "current_celsius": current,
                "threshold_min_celsius": thr_min,
                "threshold_max_celsius": thr_max,
                "out_of_range": bool(m.group(5)) or not (thr_min <= current <= thr_max),
            })

    fans = []
    in_section = False
    for line in output.splitlines():
        if "Detail Fan Status" in line:
            in_section = True
            continue
        if in_section and line.startswith("Detail ") and "Fan" not in line:
            break
        if not in_section:
            continue
        for m in re.finditer(r"([\w\s]+?)\s*\((OK|FAIL)\)", line):
            fans.append({"name": m.group(1).strip(), "status": m.group(2)})

    power = []
    in_section = False
    for line in output.splitlines():
        if "Detail Power Status" in line:
            in_section = True
            continue
        if in_section and line.startswith("Detail ") and "Power" not in line:
            break
        if not in_section:
            continue
        if re.match(r"^[-\s]+$", line):
            continue
        if line.strip().startswith("Power Module"):
            continue
        m = re.match(r"^(Power\s+\S+)\s{2,}(.+)$", line)
        if m:
            power.append({"module": m.group(1).strip(),
                         "status": m.group(2).strip()})

    return {"temperatures": temperatures, "fans": fans, "power": power}


def _parse_cpu(output):
    result = {
        "five_seconds_percent": 0,
        "one_minute_percent": 0,
        "five_minutes_percent": 0,
    }
    for line in output.splitlines():
        m = re.match(r"^\s*Five seconds\s*-\s*(\d+)\s*%", line, re.IGNORECASE)
        if m:
            result["five_seconds_percent"] = int(m.group(1))
            continue
        m = re.match(r"^\s*One minute\s*-\s*(\d+)\s*%", line, re.IGNORECASE)
        if m:
            result["one_minute_percent"] = int(m.group(1))
            continue
        m = re.match(r"^\s*Five minutes\s*-\s*(\d+)\s*%", line, re.IGNORECASE)
        if m:
            result["five_minutes_percent"] = int(m.group(1))
            continue
    return result


def _parse_interfaces(output):
    interfaces = []
    lines = output.splitlines()
    i = 0
    while i < len(lines):
        m = re.match(
            r"^\s*(eth\S+)\s+(connected|not-connected|disabled)\s+"
            r"(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s*$",
            lines[i],
        )
        if m:
            interfaces.append({
                "port": m.group(1),
                "status": m.group(2),
                "vlan": m.group(3),
                "duplex": m.group(4),
                "speed": m.group(5),
                "type": m.group(6),
            })
        i += 1
    return interfaces


def _parse_vlans(output):
    vlans = []
    current = None
    for line in output.splitlines():
        m = re.match(r"^\s*VLAN\s+(\d+)\s*$", line)
        if m:
            if current is not None:
                vlans.append(current)
            current = {
                "vlan_id": int(m.group(1)),
                "name": "",
                "tagged_ports": "",
                "untagged_ports": "",
            }
            continue
        if current is None:
            continue
        m = re.match(r"^\s*Name\s*:\s*(.*?)\s*$", line)
        if m:
            current["name"] = m.group(1)
            continue
        m = re.match(r"^\s*Tagged Member Ports\s*:\s*(.*?)\s*$", line)
        if m:
            current["tagged_ports"] = m.group(1)
            continue
        m = re.match(r"^\s*Untagged Member Ports\s*:\s*(.*?)\s*$", line)
        if m:
            current["untagged_ports"] = m.group(1)
            continue
    if current is not None:
        vlans.append(current)
    return vlans


def _parse_mac_table(output):
    entries = []
    for line in output.splitlines():
        m = re.match(
            r"^\s*(\d+)\s+([\dA-Fa-f]{2}(?:[-:][\dA-Fa-f]{2}){5})\s+"
            r"(Static|Dynamic)\s+(\S+)\s*$",
            line,
        )
        if m:
            entries.append({
                "vlan": int(m.group(1)),
                "mac_address": m.group(2),
                "type": m.group(3),
                "port": m.group(4),
            })
    return entries


_PARSERS = {
    "version": _parse_version,
    "unit": _parse_unit,
    "environment": _parse_environment,
    "cpu": _parse_cpu,
    "interfaces": _parse_interfaces,
    "vlans": _parse_vlans,
    "mac_table": _parse_mac_table,
}


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            gather=dict(
                type="list",
                elements="str",
                default=["all"],
                choices=["all", "version", "unit", "environment", "cpu",
                         "interfaces", "vlans", "mac_table"],
            ),
        ),
        supports_check_mode=True,
    )

    gather = module.params["gather"]
    subsets, commands = _build_commands(gather)

    if module.check_mode:
        module.exit_json(changed=False, commands=commands)
        return

    result = dict(changed=False, commands=commands)
    facts = {}
    for subset, command in zip(subsets, commands):
        try:
            raw_output = run_command(module, command)
        except Exception as e:
            module.fail_json(msg="Command '%s' failed: %s" % (command, str(e)))
        parsed = _PARSERS[subset](raw_output)
        result[subset] = parsed
        facts[subset] = parsed

    result["ansible_facts"] = {"dgs1250": facts}
    module.exit_json(**result)


if __name__ == "__main__":
    main()
