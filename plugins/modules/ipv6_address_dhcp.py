#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: ipv6_address_dhcp
short_description: Configure IPv6 DHCP address on an interface of a D-Link DGS-1250 switch
description:
  - Configures the C(ipv6 address dhcp) CLI command on a D-Link DGS-1250 switch.
  - Enables or disables DHCPv6 address acquisition on a specific interface.
  - Corresponds to CLI command described in chapter 10-4 of the DGS-1250 CLI Reference Guide.
version_added: "0.7.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Interface on which to configure DHCPv6 (e.g. C(vlan1)).
    type: str
    required: true
  rapid_commit:
    description:
      - When C(true), enable the rapid-commit option for DHCPv6.
    type: bool
    default: false
  state:
    description:
      - C(present) to enable DHCPv6, C(absent) to disable it.
    type: str
    choices: [present, absent]
    default: present
"""

EXAMPLES = r"""
- name: Enable DHCPv6 on vlan1
  jaydee_io.dlink_dgs1250.ipv6_address_dhcp:
    interface: vlan1

- name: Enable DHCPv6 with rapid-commit on vlan1
  jaydee_io.dlink_dgs1250.ipv6_address_dhcp:
    interface: vlan1
    rapid_commit: true

- name: Disable DHCPv6 on vlan1
  jaydee_io.dlink_dgs1250.ipv6_address_dhcp:
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
        run_commands, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(interface, rapid_commit, state):
    """Build the CLI command list."""
    if state == "absent":
        cmd = "no ipv6 address dhcp"
    else:
        cmd = "ipv6 address dhcp"
        if rapid_commit:
            cmd += " rapid-commit"
    return ["interface %s" % interface, cmd, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            rapid_commit=dict(type="bool", default=False),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["interface"],
        module.params["rapid_commit"],
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
