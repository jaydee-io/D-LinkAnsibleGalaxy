#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: snmp_server_enable_traps_storm_control
short_description: Enable or disable SNMP storm control traps on a D-Link DGS-1250 switch
description:
  - Configures the C(snmp-server enable traps storm-control) CLI command on a D-Link DGS-1250 switch.
  - Enables or disables sending of SNMP notifications for storm control events.
  - Corresponds to CLI command described in chapter 62-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.18.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  trap_types:
    description:
      - List of storm control trap types to configure. If omitted, all types are configured.
    type: list
    elements: str
    choices: [storm-occur, storm-clear]
  state:
    description:
      - C(present) to enable, C(absent) to disable.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable all storm control traps
  jaydee_io.dlink_dgs1250.snmp_server_enable_traps_storm_control:

- name: Enable storm-occur trap only
  jaydee_io.dlink_dgs1250.snmp_server_enable_traps_storm_control:
    trap_types:
      - storm-occur

- name: Disable all storm control traps
  jaydee_io.dlink_dgs1250.snmp_server_enable_traps_storm_control:
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
        run_commands, is_config_present, build_config_diff, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, is_config_present, build_config_diff, MODE_GLOBAL_CONFIG


def _build_commands(trap_types, state):
    cmd = "snmp-server enable traps storm-control"
    if trap_types:
        cmd += " " + " ".join(trap_types)
    if state == "absent":
        return ["no " + cmd]
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            trap_types=dict(type="list", elements="str", choices=[
                            "storm-occur", "storm-clear"]),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["trap_types"], module.params["state"])
    if is_config_present(module, commands):
        module.exit_json(changed=False, commands=[], raw_output="")
        return
    diff = build_config_diff(module, commands) if module._diff else None
    if module.check_mode:
        result = dict(changed=True, commands=commands, raw_output="")
        if diff:
            result['diff'] = diff
        module.exit_json(**result)
        return
    try:
        raw_output = run_commands(module, commands, mode=MODE_GLOBAL_CONFIG)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    result = dict(changed=True, raw_output=raw_output, commands=commands)
    if diff:
        result['diff'] = diff
    module.exit_json(**result)


if __name__ == "__main__":
    main()
