#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: clock_timezone
short_description: Configure the time zone on a D-Link DGS-1250 switch
description:
  - Configures the C(clock timezone) CLI command on a D-Link DGS-1250 switch.
  - Sets the time zone offset from UTC.
  - Corresponds to CLI command described in chapter 67-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.19.0"
author:
  - Jérôme Dumesnil
options:
  sign:
    description:
      - C(+) to add to UTC, C(-) to subtract from UTC.
    type: str
    choices: ["+", "-"]
  hours_offset:
    description:
      - Hours difference from UTC.
    type: int
  minutes_offset:
    description:
      - Minutes difference from UTC.
    type: int
  state:
    description:
      - C(present) to set, C(absent) to revert to default (UTC).
    type: str
    choices: [present, absent]
    default: present
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set timezone to UTC-8 (PST)
  jaydee_io.dlink_dgs1250.clock_timezone:
    sign: "-"
    hours_offset: 8

- name: Revert to UTC
  jaydee_io.dlink_dgs1250.clock_timezone:
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


def _build_commands(sign, hours_offset, minutes_offset, state):
    if state == "absent":
        return ["no clock timezone"]
    cmd = "clock timezone %s %d" % (sign, hours_offset)
    if minutes_offset is not None:
        cmd += " %d" % minutes_offset
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            sign=dict(type="str", choices=["+", "-"]),
            hours_offset=dict(type="int"),
            minutes_offset=dict(type="int"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["sign"], module.params["hours_offset"], module.params["minutes_offset"], module.params["state"])
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
