#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: ipv6_nd_raguard_device_role
short_description: Configure the device role in an RA guard policy on a D-Link DGS-1250 switch
description:
  - Configures the C(device-role) CLI command inside an RA guard policy on a D-Link DGS-1250 switch.
  - Sets the role of the attached device to host or router.
  - Corresponds to CLI command described in chapter 56-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.17.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  policy:
    description:
      - The RA guard policy name.
    type: str
    required: true
  role:
    description:
      - The device role. Required when C(state=present).
    type: str
    choices: [host, router]
  state:
    description:
      - C(present) to set the device role, C(absent) to revert to default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in RA Guard Policy Configuration Mode.
"""

EXAMPLES = r"""
- name: Set device role to router in policy
  jaydee_io.dlink_dgs1250.ipv6_nd_raguard_device_role:
    policy: raguard1
    role: router

- name: Revert device role to default
  jaydee_io.dlink_dgs1250.ipv6_nd_raguard_device_role:
    policy: raguard1
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


def _build_commands(policy, role, state):
    commands = ["ipv6 nd raguard policy %s" % policy]
    if state == "absent":
        commands.append("no device-role")
    else:
        commands.append("device-role %s" % role)
    commands.append("exit")
    return commands



def main():
    module = AnsibleModule(
        argument_spec=dict(
            policy=dict(type="str", required=True),
            role=dict(type="str", choices=["host", "router"]),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["role"])],
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["policy"], module.params["role"], module.params["state"])
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
