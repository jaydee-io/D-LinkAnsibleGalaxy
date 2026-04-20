#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dhcpv6_guard_attach_policy
short_description: Attach a DHCPv6 guard policy to an interface on a D-Link DGS-1250 switch
description:
  - Configures the C(ipv6 dhcp guard attach-policy) CLI command in Interface Configuration Mode on a D-Link DGS-1250 switch.
  - Attaches or detaches a DHCPv6 guard policy on an interface.
  - Corresponds to CLI command described in chapter 19-4 of the DGS-1250 CLI Reference Guide.
version_added: "0.9.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Interface on which to attach the policy (e.g. C(eth1/0/1)).
    type: str
    required: true
  policy_name:
    description:
      - Name of the DHCPv6 guard policy to attach. If omitted when C(state=present), attaches without a specific policy name.
    type: str
  state:
    description:
      - C(present) to attach the policy, C(absent) to detach it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Attach DHCPv6 guard policy to interface
  jaydee_io.dlink_dgs1250.dhcpv6_guard_attach_policy:
    interface: eth1/0/1
    policy_name: POLICY1

- name: Attach DHCPv6 guard policy without specific name
  jaydee_io.dlink_dgs1250.dhcpv6_guard_attach_policy:
    interface: eth1/0/1

- name: Detach DHCPv6 guard policy from interface
  jaydee_io.dlink_dgs1250.dhcpv6_guard_attach_policy:
    interface: eth1/0/1
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


def _build_commands(interface, policy_name, state):
    """Build the CLI command list."""
    commands = ["interface %s" % interface]
    if state == "absent":
        commands.append("no ipv6 dhcp guard attach-policy")
    else:
        cmd = "ipv6 dhcp guard attach-policy"
        if policy_name:
            cmd += " %s" % policy_name
        commands.append(cmd)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            policy_name=dict(type="str"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["interface"],
        module.params["policy_name"],
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
