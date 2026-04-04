#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: environment
short_description: Display environment status (fan, temperature, power) of a D-Link DGS-1250 switch
description:
  - Executes the C(show environment) CLI command on a D-Link DGS-1250 switch via SSH.
  - Returns structured data for fan status, temperature sensors, and power modules.
  - Corresponds to CLI command described in chapter 2-10 of the DGS-1250 CLI Reference Guide.
version_added: "0.1.0"
author:
  - Jérôme Dumesnil
options:
  host:
    description: IP address or hostname of the switch.
    required: true
    type: str
  username:
    description: SSH username.
    required: true
    type: str
  password:
    description: SSH password.
    required: true
    type: str
    no_log: true
  port:
    description: SSH port.
    type: int
    default: 22
  timeout:
    description: SSH connection timeout in seconds.
    type: int
    default: 30
  component:
    description:
      - Which environment component to query.
      - If omitted, all components are returned (equivalent to C(show environment) with no argument).
    type: str
    choices: [fan, power, temperature]
notes:
  - Requires C(paramiko) on the Ansible controller (C(pip install paramiko)).
  - The switch must be reachable via SSH from the Ansible controller.
"""

EXAMPLES = r"""
- name: Get full environment status
  dlink.dgs1250.environment:
    host: 192.168.1.1
    username: admin
    password: admin
  register: env_status

- name: Check fan status only
  dlink.dgs1250.environment:
    host: 192.168.1.1
    username: admin
    password: admin
    component: fan
  register: fan_status

- name: Fail if any power module is not In-operation
  dlink.dgs1250.environment:
    host: 192.168.1.1
    username: admin
    password: admin
    component: power
  register: power_status
  failed_when: >
    power_status.power | selectattr('status', '!=', 'In-operation') | list | length > 0
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
  sample: "Detail Temperature Status:\n..."
temperatures:
  description: List of temperature sensors with their current value and threshold range.
  returned: when component is 'temperature' or not specified
  type: list
  elements: dict
  contains:
    name:
      description: Sensor description and ID.
      type: str
      sample: "Central Temperature/1"
    current_celsius:
      description: Current temperature in Celsius.
      type: int
      sample: 33
    threshold_min_celsius:
      description: Lower threshold in Celsius.
      type: int
      sample: 11
    threshold_max_celsius:
      description: Upper threshold in Celsius.
      type: int
      sample: 79
    out_of_range:
      description: True if the temperature is outside the threshold range.
      type: bool
      sample: false
fans:
  description: List of fans with their status.
  returned: when component is 'fan' or not specified
  type: list
  elements: dict
  contains:
    name:
      description: Fan identifier.
      type: str
      sample: "Right Fan 1"
    status:
      description: Fan status (OK or FAIL).
      type: str
      sample: "OK"
power:
  description: List of power modules with their status.
  returned: when component is 'power' or not specified
  type: list
  elements: dict
  contains:
    module:
      description: Power module name.
      type: str
      sample: "Power 1"
    status:
      description: Power status (In-operation, Failed, or Empty).
      type: str
      sample: "In-operation"
"""

import re
from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.dlink.dgs1250.plugins.module_utils.dgs1250 import (
        CONNECTION_ARGSPEC,
        HAS_PARAMIKO,
        connection_from_params,
    )
except ImportError:
    # Fallback for running outside collection context (unit tests, etc.)
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import CONNECTION_ARGSPEC, HAS_PARAMIKO, connection_from_params


# ---------------------------------------------------------------------------
# Output parsers
# ---------------------------------------------------------------------------

def _parse_temperatures(output):
    """
    Parse the 'Detail Temperature Status' section.

    Expected format:
        Central Temperature/1         33C/11~79C
    """
    temperatures = []
    in_section = False
    out_of_range_marker = False

    for line in output.splitlines():
        if "Detail Temperature Status" in line:
            in_section = True
            continue
        if in_section and line.startswith("Detail ") and "Temperature" not in line:
            break
        if not in_section:
            continue

        # Detect the warning line about out-of-range sensors
        if "temperature is out of threshold range" in line.lower():
            out_of_range_marker = True
            continue

        # Match "Name/ID    <value>C/<min>~<max>C"
        m = re.match(
            r"^(.+?)\s{2,}(\d+)C/(\d+)~(\d+)C\s*(\*?)\s*$",
            line
        )
        if m:
            name = m.group(1).strip()
            current = int(m.group(2))
            thr_min = int(m.group(3))
            thr_max = int(m.group(4))
            out_of_range = bool(m.group(5)) or not (thr_min <= current <= thr_max)
            temperatures.append(
                {
                    "name": name,
                    "current_celsius": current,
                    "threshold_min_celsius": thr_min,
                    "threshold_max_celsius": thr_max,
                    "out_of_range": out_of_range,
                }
            )

    return temperatures


def _parse_fans(output):
    """
    Parse the 'Detail Fan Status' section.

    Expected format (all fans on one or more lines):
        Right Fan 1 (OK)     Right Fan 2 (OK)
    """
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
        if re.match(r"^-+$", line.strip()):
            continue

        # Each fan entry looks like: "Right Fan 1 (OK)"
        for m in re.finditer(r"([\w\s]+?)\s*\((OK|FAIL)\)", line):
            fans.append({"name": m.group(1).strip(), "status": m.group(2)})

    return fans


def _parse_power(output):
    """
    Parse the 'Detail Power Status' section.

    Expected format:
        Power 1           In-operation
    """
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

    return power


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    argument_spec = dict(**CONNECTION_ARGSPEC)
    argument_spec["component"] = dict(
        type="str",
        choices=["fan", "power", "temperature"],
        default=None,
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    if not HAS_PARAMIKO:
        module.fail_json(msg="paramiko is required: pip install paramiko")

    component = module.params["component"]

    command = "show environment"
    if component:
        command += " " + component

    try:
        with connection_from_params(module.params) as conn:
            raw_output = conn.send_command(command)
    except Exception as e:
        module.fail_json(msg="SSH connection or command failed: %s" % str(e))

    result = dict(changed=False, raw_output=raw_output)

    if component in (None, "temperature"):
        result["temperatures"] = _parse_temperatures(raw_output)

    if component in (None, "fan"):
        result["fans"] = _parse_fans(raw_output)

    if component in (None, "power"):
        result["power"] = _parse_power(raw_output)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
