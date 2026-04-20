#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jerome Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: mld_snooping_robustness_variable
short_description: Configure MLD snooping robustness variable on a D-Link DGS-1250 switch
description:
  - Configures the C(ipv6 mld snooping robustness-variable) CLI command on a D-Link DGS-1250 switch.
  - Corresponds to CLI command described in chapter 45-10 of the DGS-1250 CLI Reference Guide.
version_added: "0.14.0"
author:
  - "Jérôme Dumesnil (@jaydee-io)"
options:
  vlan_id:
    description:
      - The VLAN ID to configure.
    type: int
    required: true
  value:
    description:
      - The robustness variable (1 to 7).
    type: int
  state:
    description:
      - C(present) to set the value, C(absent) to revert to default (2).
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in VLAN Configuration Mode.
"""

EXAMPLES = r"""
- name: Set ipv6 mld snooping robustness-variable on VLAN 1000
  jaydee_io.dlink_dgs1250.mld_snooping_robustness_variable:
    vlan_id: 1000
    value: 3

- name: Revert ipv6 mld snooping robustness-variable to default on VLAN 1000
  jaydee_io.dlink_dgs1250.mld_snooping_robustness_variable:
    vlan_id: 1000
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


def _build_commands(vlan_id, value, state):
    if state == "absent":
        return ["vlan %d" % vlan_id, "no ipv6 mld snooping robustness-variable", "exit"]
    return ["vlan %d" % vlan_id, "ipv6 mld snooping robustness-variable %d" % value, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            vlan_id=dict(type="int", required=True),
            value=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["value"]),
        ],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["vlan_id"], module.params["value"], module.params["state"])
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
