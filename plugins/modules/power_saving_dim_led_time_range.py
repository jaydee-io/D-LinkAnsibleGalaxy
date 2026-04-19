#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: power_saving_dim_led_time_range
short_description: Configure dim LED time range profile on a D-Link DGS-1250 switch
description:
  - Configures the C(power-saving dim-led time-range) CLI command on a D-Link DGS-1250 switch.
  - Adds or removes a time range profile for the dim LED schedule.
  - Corresponds to CLI command described in chapter 52-4 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  profile_name:
    description:
      - Name of the time range profile (max 32 characters).
    type: str
    required: true
  state:
    description:
      - C(present) to add the profile, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Add a dim LED time range profile
  jaydee_io.dlink_dgs1250.power_saving_dim_led_time_range:
    profile_name: off-duty

- name: Remove a dim LED time range profile
  jaydee_io.dlink_dgs1250.power_saving_dim_led_time_range:
    profile_name: off-duty
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


def _build_commands(profile_name, state):
    if state == "absent":
        return ["no power-saving dim-led time-range %s" % profile_name]
    return ["power-saving dim-led time-range %s" % profile_name]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            profile_name=dict(type="str", required=True),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["profile_name"],
        module.params["state"],
    )
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
