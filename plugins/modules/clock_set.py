#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: clock_set
short_description: Set the system clock on a D-Link DGS-1250 switch
description:
  - Executes the C(clock set) CLI command on a D-Link DGS-1250 switch.
  - Manually sets the system clock.
  - Corresponds to CLI command described in chapter 67-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.19.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  time:
    description:
      - The time in HH:MM:SS format (24-hour).
    type: str
    required: true
  day:
    description:
      - The day of the month.
    type: int
    required: true
  month:
    description:
      - The month name (jan, feb, mar, etc.).
    type: str
    required: true
  year:
    description:
      - The year (no abbreviation).
    type: int
    required: true
notes:
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Set the clock to 6pm on Jul 4 2023
  jaydee_io.dlink_dgs1250.clock_set:
    time: "18:00:00"
    day: 4
    month: jul
    year: 2023
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
        run_commands, MODE_PRIVILEGED,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_PRIVILEGED


def _build_commands(time, day, month, year):
    return ["clock set %s %d %s %d" % (time, day, month, year)]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            time=dict(type="str", required=True),
            day=dict(type="int", required=True),
            month=dict(type="str", required=True),
            year=dict(type="int", required=True),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["time"], module.params["day"], module.params["month"], module.params["year"])
    if module.check_mode:
        module.exit_json(changed=True, commands=commands, raw_output="")
        return
    try:
        raw_output = run_commands(module, commands, mode=MODE_PRIVILEGED)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    module.exit_json(changed=True, raw_output=raw_output, commands=commands)


if __name__ == "__main__":
    main()
