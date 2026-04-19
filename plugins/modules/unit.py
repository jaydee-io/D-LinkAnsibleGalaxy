#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: unit
short_description: Display system unit information of a D-Link DGS-1250 switch
description:
  - Executes the C(show unit) CLI command on a D-Link DGS-1250 switch.
  - Returns structured data for model, serial number, status, uptime, and memory usage.
  - Corresponds to CLI command described in chapter 2-11 of the DGS-1250 CLI Reference Guide.
version_added: "0.1.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options: {}
notes:
"""

EXAMPLES = r"""
- name: Get unit information
  jaydee_io.dlink_dgs1250.unit:
  register: unit_info

- name: Display model name
  ansible.builtin.debug:
    msg: "Switch model: {{ unit_info.model.model_name }}"

- name: Fail if unit status is not ok
  jaydee_io.dlink_dgs1250.unit:
  register: unit_info
  failed_when: unit_info.unit.status != 'ok'
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
model:
  description: Model information.
  returned: always
  type: dict
  contains:
    model_description:
      description: Hardware description of the switch.
      type: str
      sample: "24P 10/100/1000M PoE + 4P 10G SFP+"
    model_name:
      description: Model name of the switch.
      type: str
      sample: "DGS-1250-28XMP"
unit:
  description: Unit status information.
  returned: always
  type: dict
  contains:
    serial_number:
      description: Serial number of the switch.
      type: str
      sample: "DGS1250102030"
    status:
      description: Unit status.
      type: str
      sample: "ok"
    uptime:
      description: System uptime broken down into days, hours, minutes and seconds.
      type: dict
      contains:
        days:
          description: Number of days.
          type: int
          sample: 0
        hours:
          description: Number of hours.
          type: int
          sample: 0
        minutes:
          description: Number of minutes.
          type: int
          sample: 38
        seconds:
          description: Number of seconds.
          type: int
          sample: 59
    uptime_raw:
      description: Total uptime in seconds.
      type: int
      sample: 2339
memory:
  description: Memory usage for DRAM and FLASH.
  returned: always
  type: list
  elements: dict
  contains:
    type:
      description: Memory type (DRAM or FLASH).
      type: str
      sample: "DRAM"
    total_kb:
      description: Total memory in kilobytes.
      type: int
      sample: 243268
    used_kb:
      description: Used memory in kilobytes.
      type: int
      sample: 125248
    free_kb:
      description: Free memory in kilobytes.
      type: int
      sample: 118020
"""

import re
from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import run_command
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


# ---------------------------------------------------------------------------
# Output parsers
# ---------------------------------------------------------------------------

def _parse_model(output):
    """
    Parse the model section.

    Expected format:
           Model Descr                            Model Name
    -------------------------------------------  -----------------------------
     24P 10/100/1000M PoE + 4P 10G SFP+           DGS-1250-28XMP
    """
    result = {"model_description": "", "model_name": ""}
    in_section = False

    for line in output.splitlines():
        if "Model Descr" in line and "Model Name" in line:
            in_section = True
            continue
        if not in_section:
            continue
        if re.match(r"^[-\s]+$", line):
            continue

        # Data line: description followed by model name separated by 2+ spaces
        m = re.match(r"^\s*(.+?)\s{2,}(\S+)\s*$", line)
        if m:
            result["model_description"] = m.group(1).strip()
            result["model_name"] = m.group(2).strip()
            break

    return result


def _parse_uptime(raw_uptime):
    """
    Parse a DdTHhMmSs uptime string into a dict and total seconds.

    Example: "3DT2H38M59S" -> {"days": 3, "hours": 2, "minutes": 38, "seconds": 59}, 268739
    """
    uptime = {"days": 0, "hours": 0, "minutes": 0, "seconds": 0}
    m = re.match(r"(\d+)DT(\d+)H(\d+)M(\d+)S", raw_uptime)
    if m:
        uptime["days"] = int(m.group(1))
        uptime["hours"] = int(m.group(2))
        uptime["minutes"] = int(m.group(3))
        uptime["seconds"] = int(m.group(4))
    total = (
        uptime["days"] * 86400
        + uptime["hours"] * 3600
        + uptime["minutes"] * 60
        + uptime["seconds"]
    )
    return uptime, total


def _parse_unit_info(output):
    """
    Parse the unit info section.

    Expected format:
           Serial-Number                Status        Up Time
    ---------------------------------  ---------  -----------------
     DGS1250102030                      ok         0DT0H38M59S
    """
    result = {"serial_number": "", "status": "", "uptime": {"days": 0, "hours": 0, "minutes": 0, "seconds": 0}, "uptime_raw": 0}
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
            result["serial_number"] = m.group(1).strip()
            result["status"] = m.group(2).strip()
            result["uptime"], result["uptime_raw"] = _parse_uptime(m.group(3).strip())
            break

    return result


def _parse_memory(output):
    """
    Parse the memory section.

    Expected format:
     Memory     Total       Used        Free
    --------  ----------  ----------  ----------
     DRAM      243268 K    125248 K    118020 K
     FLASH      45220 K     24920 K     20300 K
    """
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
            r"^\s*(DRAM|FLASH)\s+(\d+)\s*K\s+(\d+)\s*K\s+(\d+)\s*K\s*$",
            line
        )
        if m:
            memory.append({
                "type": m.group(1),
                "total_kb": int(m.group(2)),
                "used_kb": int(m.group(3)),
                "free_kb": int(m.group(4)),
            })

    return memory


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(),
        supports_check_mode=True,
    )

    try:
        raw_output = run_command(module, "show unit")
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    module.exit_json(
        changed=False,
        raw_output=raw_output,
        model=_parse_model(raw_output),
        unit=_parse_unit_info(raw_output),
        memory=_parse_memory(raw_output),
    )


if __name__ == "__main__":
    main()
