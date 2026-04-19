#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: ipv6_snooping_protocol
short_description: Configure protocol snooping in an IPv6 snooping policy on a D-Link DGS-1250 switch
description:
  - Configures the C(protocol) CLI command in IPv6 Snooping Configuration Mode on a D-Link DGS-1250 switch.
  - Specifies that addresses should be snooped with DHCPv6 or NDP.
  - Corresponds to CLI command described in chapter 37-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.13.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  policy:
    description:
      - Name of the IPv6 snooping policy to configure.
    type: str
    required: true
  protocol:
    description:
      - The protocol to enable or disable for snooping.
    type: str
    required: true
    choices: [dhcp, ndp]
  state:
    description:
      - C(present) to enable the protocol, C(absent) to disable it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in IPv6 Snooping Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable DHCPv6 snooping in a policy
  jaydee_io.dlink_dgs1250.ipv6_snooping_protocol:
    policy: policy1
    protocol: dhcp

- name: Disable NDP snooping in a policy
  jaydee_io.dlink_dgs1250.ipv6_snooping_protocol:
    policy: policy1
    protocol: ndp
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


def _build_commands(policy, protocol, state):
    """Build the CLI command list."""
    commands = ["ipv6 snooping policy %s" % policy]
    if state == "absent":
        commands.append("no protocol %s" % protocol)
    else:
        commands.append("protocol %s" % protocol)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            policy=dict(type="str", required=True),
            protocol=dict(type="str", required=True, choices=["dhcp", "ndp"]),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["policy"],
        module.params["protocol"],
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
