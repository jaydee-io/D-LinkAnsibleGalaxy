#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: mstp_name
short_description: Configure MST region name on a D-Link DGS-1250 switch
description:
  - Configures the C(name) CLI command in MST Configuration Mode on a D-Link DGS-1250 switch.
  - Sets or removes the name of an MST region.
  - Corresponds to CLI command described in chapter 46-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.15.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  name:
    description:
      - The MST region name (max 32 characters). Required when C(state=present).
    type: str
  state:
    description:
      - C(present) to set the name, C(absent) to revert to default (MAC address).
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in MST Configuration Mode.
"""

EXAMPLES = r"""
- name: Set MST region name
  jaydee_io.dlink_dgs1250.mstp_name:
    name: MName

- name: Revert MST region name to default
  jaydee_io.dlink_dgs1250.mstp_name:
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


def _build_commands(name, state):
    """Build the CLI command list."""
    commands = ["spanning-tree mst configuration"]
    if state == "absent":
        commands.append("no name")
    else:
        commands.append("name %s" % name)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type="str"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["name"]),
        ],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["name"],
        module.params["state"],
    )
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
