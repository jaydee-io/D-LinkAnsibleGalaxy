#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: mls_qos_map_dscp_mutation_global
short_description: Define a named DSCP mutation map on a D-Link DGS-1250 switch
description:
  - Configures the C(mls qos map dscp-mutation) CLI command on a D-Link DGS-1250 switch.
  - Defines a named DSCP mutation map globally.
  - Corresponds to CLI command described in chapter 54-7 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  map_name:
    description:
      - Name of the DSCP mutation map (max 32 characters, no spaces).
    type: str
    required: true
  input_dscp_list:
    description:
      - Input DSCP values (0-63) to mutate. Required when C(state=present).
    type: str
  output_dscp:
    description:
      - Output (mutated) DSCP value (0-63). Required when C(state=present).
    type: int
  state:
    description:
      - C(present) to add the mutation mapping, C(absent) to remove the mutation map.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Map DSCP 30 to 8 in mutemap1
  jaydee_io.dlink_dgs1250.mls_qos_map_dscp_mutation_global:
    map_name: mutemap1
    input_dscp_list: "30"
    output_dscp: 8

- name: Delete mutation map mutemap1
  jaydee_io.dlink_dgs1250.mls_qos_map_dscp_mutation_global:
    map_name: mutemap1
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


def _build_commands(map_name, input_dscp_list, output_dscp, state):
    if state == "absent":
        return ["no mls qos map dscp-mutation %s" % map_name]
    return ["mls qos map dscp-mutation %s %s to %d" %
            (map_name, input_dscp_list, output_dscp)]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            map_name=dict(type="str", required=True),
            input_dscp_list=dict(type="str"),
            output_dscp=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["input_dscp_list", "output_dscp"])],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["map_name"],
        module.params["input_dscp_list"],
        module.params["output_dscp"],
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
