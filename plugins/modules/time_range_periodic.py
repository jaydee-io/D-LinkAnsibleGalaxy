#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: time_range_periodic
short_description: Configure a periodic time range on a D-Link DGS-1250 switch
description:
  - Configures the C(periodic) CLI command within a time-range profile on a D-Link DGS-1250 switch.
  - Adds or removes a periodic time specification in a time range profile.
  - Corresponds to CLI command described in chapter 68-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.19.0"
author:
  - Jérôme Dumesnil
options:
  name:
    description:
      - Name of the time-range profile.
    type: str
    required: true
  mode:
    description:
      - C(daily) for daily schedule, C(weekly) for weekly schedule.
    type: str
    required: true
    choices: [daily, weekly]
  start:
    description:
      - Start time. For daily use C(HH:MM). For weekly use C(DAY HH:MM).
    type: str
    required: true
  end:
    description:
      - End time. For daily use C(HH:MM). For weekly use C([DAY] HH:MM).
    type: str
    required: true
  state:
    description:
      - C(present) to add, C(absent) to remove.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Time-range Configuration Mode.
"""

EXAMPLES = r"""
- name: Add daily time range
  jaydee_io.dlink_dgs1250.time_range_periodic:
    name: rdtime
    mode: daily
    start: "9:00"
    end: "12:00"

- name: Add weekly time range
  jaydee_io.dlink_dgs1250.time_range_periodic:
    name: rdtime
    mode: weekly
    start: "saturday 00:00"
    end: "monday 00:00"

- name: Remove daily time range
  jaydee_io.dlink_dgs1250.time_range_periodic:
    name: rdtime
    mode: daily
    start: "9:00"
    end: "12:00"
    state: absent
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
commands:
  description: List of CLI commands sent to the switch.
  returned: always
  type: list
  elements: str
"""

from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import (
        run_commands, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(name, mode, start, end, state):
    prefix = "no " if state == "absent" else ""
    cmd = "%speriodic %s %s to %s" % (prefix, mode, start, end)
    return ["time-range %s" % name, cmd, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type="str", required=True),
            mode=dict(type="str", required=True, choices=["daily", "weekly"]),
            start=dict(type="str", required=True),
            end=dict(type="str", required=True),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["name"], module.params["mode"], module.params["start"], module.params["end"], module.params["state"])
    if module.check_mode:
        module.exit_json(changed=True, commands=commands, raw_output="")
        return
    try:
        raw_output = run_commands(module, commands, mode=MODE_GLOBAL_CONFIG)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    module.exit_json(changed=True, raw_output=raw_output, commands=commands)


if __name__ == "__main__":
    main()
