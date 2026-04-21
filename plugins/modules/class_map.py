#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: class_map
short_description: Create or modify a class-map on a D-Link DGS-1250 switch
description:
  - Configures the C(class-map) CLI command on a D-Link DGS-1250 switch.
  - Creates or modifies a class map that defines packet matching criteria.
  - Corresponds to CLI command described in chapter 54-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  name:
    description:
      - Name of the class map (max 32 characters).
    type: str
    required: true
  match_type:
    description:
      - How to evaluate multiple match criteria (logical AND or OR).
    type: str
    choices: [match-all, match-any]
  state:
    description:
      - C(present) to create or modify the class map, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Create class-map match-all
  jaydee_io.dlink_dgs1250.class_map:
    name: class_home_user
    match_type: match-all

- name: Create class-map with default match-any
  jaydee_io.dlink_dgs1250.class_map:
    name: cos

- name: Remove class-map
  jaydee_io.dlink_dgs1250.class_map:
    name: cos
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


def _build_commands(name, match_type, state):
    if state == "absent":
        return ["no class-map %s" % name]
    cmd = "class-map"
    if match_type:
        cmd += " %s" % match_type
    cmd += " %s" % name
    commands = [cmd, "exit"]
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type="str", required=True),
            match_type=dict(type="str", choices=["match-all", "match-any"]),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["name"],
        module.params["match_type"],
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
