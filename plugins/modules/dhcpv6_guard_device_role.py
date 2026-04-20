#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dhcpv6_guard_device_role
short_description: Set device role in a DHCPv6 guard policy on a D-Link DGS-1250 switch
description:
  - Configures the C(device-role) CLI command in DHCPv6 Guard Policy Configuration Mode on a D-Link DGS-1250 switch.
  - Sets or removes the device role for a DHCPv6 guard policy.
  - Corresponds to CLI command described in chapter 19-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.9.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  policy:
    description:
      - Name of the DHCPv6 guard policy to configure.
    type: str
    required: true
  role:
    description:
      - Device role to set. Required when C(state=present).
    type: str
    choices: [client, server]
  state:
    description:
      - C(present) to set the device role, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in DHCPv6 Guard Policy Configuration Mode.
"""

EXAMPLES = r"""
- name: Set device role to server in DHCPv6 guard policy
  jaydee_io.dlink_dgs1250.dhcpv6_guard_device_role:
    policy: POLICY1
    role: server

- name: Remove device role from DHCPv6 guard policy
  jaydee_io.dlink_dgs1250.dhcpv6_guard_device_role:
    policy: POLICY1
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
        run_commands, is_config_present, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, is_config_present, MODE_GLOBAL_CONFIG


def _build_commands(policy, role, state):
    """Build the CLI command list."""
    commands = ["ipv6 dhcp guard policy %s" % policy]
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
            role=dict(type="str", choices=["client", "server"]),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
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

    if is_config_present(module, commands):
        module.exit_json(changed=False, commands=[], raw_output="")
        return
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
