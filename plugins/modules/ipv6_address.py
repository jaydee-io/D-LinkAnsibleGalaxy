#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: ipv6_address
short_description: Configure an IPv6 address on an interface of a D-Link DGS-1250 switch
description:
  - Configures the C(ipv6 address) CLI command on a D-Link DGS-1250 switch.
  - Assigns a static IPv6 address or a link-local address on a specific interface.
  - Corresponds to CLI command described in chapter 10-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.7.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Interface on which to configure the IPv6 address (e.g. C(vlan1)).
    type: str
    required: true
  ipv6_address:
    description:
      - IPv6 address to assign to the interface.
    type: str
    required: true
  prefix_length:
    description:
      - Prefix length for the IPv6 address. Required when C(link_local=false).
    type: int
  link_local:
    description:
      - When C(true), configure the address as a link-local address.
    type: bool
    default: false
  state:
    description:
      - C(present) to configure the address, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
"""

EXAMPLES = r"""
- name: Set an IPv6 address on vlan1
  jaydee_io.dlink_dgs1250.ipv6_address:
    interface: vlan1
    ipv6_address: 2001:db8::1
    prefix_length: 64

- name: Set a link-local address on vlan1
  jaydee_io.dlink_dgs1250.ipv6_address:
    interface: vlan1
    ipv6_address: fe80::1
    link_local: true

- name: Remove an IPv6 address
  jaydee_io.dlink_dgs1250.ipv6_address:
    interface: vlan1
    ipv6_address: 2001:db8::1
    prefix_length: 64
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


def _build_commands(interface, ipv6_address, prefix_length, link_local, state):
    """Build the CLI command list."""
    prefix = "no " if state == "absent" else ""
    if link_local:
        cmd = "%sipv6 address %s link-local" % (prefix, ipv6_address)
    else:
        cmd = "%sipv6 address %s/%d" % (prefix, ipv6_address, prefix_length)
    return ["interface %s" % interface, cmd, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            ipv6_address=dict(type="str", required=True),
            prefix_length=dict(type="int"),
            link_local=dict(type="bool", default=False),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[
            ("link_local", False, ["prefix_length"]),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["interface"],
        module.params["ipv6_address"],
        module.params["prefix_length"],
        module.params["link_local"],
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
