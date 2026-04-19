#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dhcpv6_relay_remote_id_policy
short_description: Configure DHCPv6 relay remote-id policy on a D-Link DGS-1250 switch
description:
  - Configures the C(ipv6 dhcp relay remote-id policy) CLI command on a D-Link DGS-1250 switch.
  - Sets or removes the Option 37 forwarding policy for the DHCPv6 relay agent.
  - Corresponds to CLI command described in chapter 20-4 of the DGS-1250 CLI Reference Guide.
version_added: "0.9.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  policy:
    description:
      - The forwarding policy to set. Required when C(state=present).
    type: str
    choices: [drop, keep]
  state:
    description:
      - C(present) to set, C(absent) to revert to default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set DHCPv6 relay remote-id policy to drop
  jaydee_io.dlink_dgs1250.dhcpv6_relay_remote_id_policy:
    policy: drop

- name: Reset DHCPv6 relay remote-id policy
  jaydee_io.dlink_dgs1250.dhcpv6_relay_remote_id_policy:
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


def _build_commands(policy, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["no ipv6 dhcp relay remote-id policy"]
    return ["ipv6 dhcp relay remote-id policy %s" % policy]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            policy=dict(type="str", choices=["drop", "keep"]),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["policy"])],
        supports_check_mode=True,
    )

    commands = _build_commands(module.params["policy"], module.params["state"])

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
