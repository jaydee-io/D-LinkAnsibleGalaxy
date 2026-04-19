#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: dgs1250_facts
short_description: Collect basic facts from a D-Link DGS-1250 switch in a single call
description:
  - Gathers essential system information from a D-Link DGS-1250 switch by executing
    multiple CLI commands (C(show version), C(show unit), C(show environment),
    C(show cpu utilization)) and returning all parsed data in one result.
  - Provides a convenient way to collect version, model, serial number, uptime,
    memory usage, CPU utilization, fan/temperature/power status in a single task.
  - The C(gather) parameter allows selecting which subsets of facts to collect.
version_added: "0.21.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  gather:
    description:
      - List of fact subsets to collect.
      - If omitted or set to C([all]), all subsets are gathered.
    type: list
    elements: str
    choices: [all, version, unit, environment, cpu]
    default: [all]
notes:
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Gather all facts
  jaydee_io.dlink_dgs1250.dgs1250_facts:
  register: facts

- name: Display switch model and firmware
  ansible.builtin.debug:
    msg: "{{ facts.version.module_name }} running {{ facts.version.runtime }}"

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
"""

RETURN = r"""
commands:
  description: List of CLI commands sent to the switch.
  returned: always
  type: list
  elements: str
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
"""

import re
from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import (
        run_command,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


# ---------------------------------------------------------------------------
# CLI commands for each subset
# ---------------------------------------------------------------------------

SUBSET_COMMANDS = {
    "version": "show version",
    "unit": "show unit",
    "environment": "show environment",
    "cpu": "show cpu utilization",
}


def _build_commands(gather):
    """Return the list of CLI commands to run based on the requested subsets."""
    if "all" in gather:
        subsets = ["version", "unit", "environment", "cpu"]
    else:
        subsets = [s for s in ["version", "unit", "environment", "cpu"] if s in gather]
    return subsets, [SUBSET_COMMANDS[s] for s in subsets]


# ---------------------------------------------------------------------------
# Output parsers (same logic as the individual modules)
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
            uptime_m = re.match(r"(\d+)DT(\d+)H(\d+)M(\d+)S", m.group(3).strip())
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
            power.append({"module": m.group(1).strip(), "status": m.group(2).strip()})

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


_PARSERS = {
    "version": _parse_version,
    "unit": _parse_unit,
    "environment": _parse_environment,
    "cpu": _parse_cpu,
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
                choices=["all", "version", "unit", "environment", "cpu"],
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
    for subset, command in zip(subsets, commands):
        try:
            raw_output = run_command(module, command)
        except Exception as e:
            module.fail_json(msg="Command '%s' failed: %s" % (command, str(e)))
        result[subset] = _PARSERS[subset](raw_output)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
