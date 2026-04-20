#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: ipv6_hop_limit
short_description: Configure IPv6 hop limit on an interface of a D-Link DGS-1250 switch
description:
  - Configures the C(ipv6 hop-limit) CLI command on a D-Link DGS-1250 switch.
  - Sets or resets the IPv6 hop limit value on a specific interface.
  - Corresponds to CLI command described in chapter 10-6 of the DGS-1250 CLI Reference Guide.
version_added: "0.7.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Interface on which to configure the IPv6 hop limit (e.g. C(vlan1)).
    type: str
    required: true
  value:
    description:
      - Hop limit value (0-255). Required when C(state=present).
    type: int
  state:
    description:
      - C(present) to set the hop limit, C(absent) to reset to default.
    type: str
    choices: [present, absent]
    default: present
"""

EXAMPLES = r"""
- name: Set IPv6 hop limit to 64 on vlan1
  jaydee_io.dlink_dgs1250.ipv6_hop_limit:
    interface: vlan1
    value: 64

- name: Reset IPv6 hop limit to default on vlan1
  jaydee_io.dlink_dgs1250.ipv6_hop_limit:
    interface: vlan1
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


def _build_commands(interface, value, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["interface %s" % interface, "no ipv6 hop-limit", "exit"]
    return ["interface %s" % interface, "ipv6 hop-limit %d" % value, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
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
        module.params["interface"],
        module.params["value"],
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
