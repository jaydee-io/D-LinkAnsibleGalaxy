#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: clock_summer_time
short_description: Configure daylight saving time on a D-Link DGS-1250 switch
description:
  - Configures the C(clock summer-time) CLI command on a D-Link DGS-1250 switch.
  - Configures automatic switching to summer time (daylight saving time).
  - Corresponds to CLI command described in chapter 67-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.19.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  mode:
    description:
      - C(recurring) for week/day based schedule, C(date) for specific date schedule.
    type: str
    choices: [recurring, date]
  start:
    description:
      - Start specification. For recurring use C(WEEK DAY MONTH HH:MM). For date use C(DATE MONTH YEAR HH:MM).
    type: str
  end:
    description:
      - End specification. Same format as start.
    type: str
  offset:
    description:
      - Minutes to add during summer time (30-120). Default is 60.
    type: int
  state:
    description:
      - C(present) to configure, C(absent) to disable.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set recurring summer time
  jaydee_io.dlink_dgs1250.clock_summer_time:
    mode: recurring
    start: "1 sun jun 2:00"
    end: "last sun oct 2:00"

- name: Disable summer time
  jaydee_io.dlink_dgs1250.clock_summer_time:
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
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(mode, start, end, offset, state):
    if state == "absent":
        return ["no clock summer-time"]
    cmd = "clock summer-time %s %s %s" % (mode, start, end)
    if offset is not None:
        cmd += " %d" % offset
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            mode=dict(type="str", choices=["recurring", "date"]),
            start=dict(type="str"),
            end=dict(type="str"),
            offset=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["mode"], module.params["start"],
                               module.params["end"], module.params["offset"], module.params["state"])
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
