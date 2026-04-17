#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: policy_map_set
short_description: Configure the C(set) action inside a policy-map class on a D-Link DGS-1250 switch
description:
  - Configures the C(set) CLI command inside a policy-map class on a D-Link DGS-1250 switch.
  - Sets the precedence, DSCP, CoS, or CoS queue of the matched packets.
  - Corresponds to CLI command described in chapter 54-15 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
author:
  - Jérôme Dumesnil
options:
  policy_map:
    description:
      - Name of the policy map.
    type: str
    required: true
  class_name:
    description:
      - Name of the class map inside the policy map.
    type: str
    required: true
  action:
    description:
      - Action to set on matched packets.
    type: str
    required: true
    choices: [precedence, ip-precedence, dscp, ip-dscp, cos, cos-queue]
  value:
    description:
      - Value associated with the action.
    type: int
    required: true
  state:
    description:
      - C(present) to set the action, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Policy-map Class Configuration Mode.
"""

EXAMPLES = r"""
- name: Set IP DSCP 10 on class1 in policy1
  jaydee_io.dlink_dgs1250.policy_map_set:
    policy_map: policy1
    class_name: class1
    action: ip-dscp
    value: 10

- name: Remove set DSCP
  jaydee_io.dlink_dgs1250.policy_map_set:
    policy_map: policy1
    class_name: class1
    action: ip-dscp
    value: 10
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


ACTION_MAP = {
    "precedence": "precedence",
    "ip-precedence": "ip precedence",
    "dscp": "dscp",
    "ip-dscp": "ip dscp",
    "cos": "cos",
    "cos-queue": "cos-queue",
}


def _build_commands(policy_map, class_name, action, value, state):
    kw = ACTION_MAP[action]
    set_cmd = "set %s %d" % (kw, value)
    commands = [
        "policy-map %s" % policy_map,
        "class %s" % class_name,
    ]
    if state == "absent":
        commands.append("no " + set_cmd)
    else:
        commands.append(set_cmd)
    commands.append("exit")
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            policy_map=dict(type="str", required=True),
            class_name=dict(type="str", required=True),
            action=dict(type="str", required=True, choices=list(ACTION_MAP.keys())),
            value=dict(type="int", required=True),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["policy_map"],
        module.params["class_name"],
        module.params["action"],
        module.params["value"],
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
