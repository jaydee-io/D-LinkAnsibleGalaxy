#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: nd_inspection_device_role
short_description: Set device role in an ND inspection policy on a D-Link DGS-1250 switch
description:
  - Configures the C(device-role) CLI command in ND Inspection Policy Configuration Mode on a D-Link DGS-1250 switch.
  - Sets or removes the device role for an ND inspection policy.
  - Corresponds to CLI command described in chapter 47-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.15.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  policy:
    description:
      - Name of the ND inspection policy to configure.
    type: str
    required: true
  role:
    description:
      - Device role to set. Required when C(state=present).
    type: str
    choices: [host, router]
  state:
    description:
      - C(present) to set the device role, C(absent) to revert to default (host).
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in ND Inspection Policy Configuration Mode.
"""

EXAMPLES = r"""
- name: Set device role to host in ND inspection policy
  jaydee_io.dlink_dgs1250.nd_inspection_device_role:
    policy: policy1
    role: host

- name: Set device role to router in ND inspection policy
  jaydee_io.dlink_dgs1250.nd_inspection_device_role:
    policy: policy1
    role: router

- name: Revert device role to default in ND inspection policy
  jaydee_io.dlink_dgs1250.nd_inspection_device_role:
    policy: policy1
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
    """Build the CLI command list."""
    commands = ["ipv6 nd inspection policy %s" % policy]
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
        required_if=[
            ("state", "present", ["role"]),
        ],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["policy"],
        module.params["role"],
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
