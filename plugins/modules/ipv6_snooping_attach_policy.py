#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: ipv6_snooping_attach_policy
short_description: Attach an IPv6 snooping policy to a VLAN on a D-Link DGS-1250 switch
description:
  - Configures the C(ipv6 snooping policy attach-policy) CLI command in VLAN Configuration Mode on a D-Link DGS-1250 switch.
  - Applies an IPv6 snooping policy to a specified VLAN.
  - Corresponds to CLI command described in chapter 37-4 of the DGS-1250 CLI Reference Guide.
version_added: "0.13.0"
author:
  - Jérôme Dumesnil
options:
  vlan_id:
    description:
      - The VLAN ID to attach the policy to.
    type: int
    required: true
  policy:
    description:
      - Name of the IPv6 snooping policy. Required when C(state=present).
    type: str
  state:
    description:
      - C(present) to attach the policy, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in VLAN Configuration Mode.
"""

EXAMPLES = r"""
- name: Attach IPv6 snooping policy to VLAN 200
  jaydee_io.dlink_dgs1250.ipv6_snooping_attach_policy:
    vlan_id: 200
    policy: policy1

- name: Remove IPv6 snooping policy from VLAN 200
  jaydee_io.dlink_dgs1250.ipv6_snooping_attach_policy:
    vlan_id: 200
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


def _build_commands(vlan_id, policy, state):
    """Build the CLI command list."""
    commands = ["vlan %d" % vlan_id]
    if state == "absent":
        commands.append("no ipv6 snooping policy attach-policy")
    else:
        commands.append("ipv6 snooping policy attach-policy %s" % policy)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            vlan_id=dict(type="int", required=True),
            policy=dict(type="str"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["policy"]),
        ],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["vlan_id"],
        module.params["policy"],
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
