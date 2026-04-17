#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: storm_control_polling
short_description: Configure storm control polling on a D-Link DGS-1250 switch
description:
  - Configures the C(storm-control polling) CLI command on a D-Link DGS-1250 switch.
  - Sets the polling interval and retry count for storm control.
  - Corresponds to CLI command described in chapter 62-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.18.0"
author:
  - Jérôme Dumesnil
options:
  interval:
    description:
      - The polling interval in seconds (5 to 600).
    type: int
  retries:
    description:
      - The retry count (0 to 360) or C(infinite).
    type: str
  state:
    description:
      - C(present) to set the value, C(absent) to revert to default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set storm control polling interval to 15 seconds
  jaydee_io.dlink_dgs1250.storm_control_polling:
    interval: 15

- name: Set storm control retries to infinite
  jaydee_io.dlink_dgs1250.storm_control_polling:
    retries: infinite

- name: Revert polling interval to default
  jaydee_io.dlink_dgs1250.storm_control_polling:
    interval: 5
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


def _build_commands(interval, retries, state):
    commands = []
    if state == "absent":
        if interval is not None:
            commands.append("no storm-control polling interval")
        if retries is not None:
            commands.append("no storm-control polling retries")
    else:
        if interval is not None:
            commands.append("storm-control polling interval %d" % interval)
        if retries is not None:
            commands.append("storm-control polling retries %s" % retries)
    return commands




def main():
    module = AnsibleModule(
        argument_spec=dict(
            interval=dict(type="int"),
            retries=dict(type="str"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["interval"], module.params["retries"], module.params["state"])
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
