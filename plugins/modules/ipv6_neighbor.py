#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: ipv6_neighbor
short_description: Configure a static IPv6 neighbor entry on a D-Link DGS-1250 switch
description:
  - Configures the C(ipv6 neighbor) CLI command on a D-Link DGS-1250 switch.
  - Adds or removes a static IPv6 neighbor entry.
  - Corresponds to CLI command described in chapter 10-15 of the DGS-1250 CLI Reference Guide.
version_added: "0.7.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  ipv6_address:
    description:
      - IPv6 address of the neighbor entry.
    type: str
    required: true
  interface:
    description:
      - Interface associated with the neighbor entry (e.g. C(vlan1)).
    type: str
    required: true
  mac_address:
    description:
      - MAC address of the neighbor. Required when C(state=present).
    type: str
  state:
    description:
      - C(present) to add the neighbor entry, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Add a static IPv6 neighbor entry
  jaydee_io.dlink_dgs1250.ipv6_neighbor:
    ipv6_address: 2001:db8::1
    interface: vlan1
    mac_address: 00-01-02-03-04-05

- name: Remove a static IPv6 neighbor entry
  jaydee_io.dlink_dgs1250.ipv6_neighbor:
    ipv6_address: 2001:db8::1
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
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(ipv6_address, interface, mac_address, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["no ipv6 neighbor %s %s" % (ipv6_address, interface)]
    return ["ipv6 neighbor %s %s %s" % (ipv6_address, interface, mac_address)]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            ipv6_address=dict(type="str", required=True),
            interface=dict(type="str", required=True),
            mac_address=dict(type="str"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["mac_address"]),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["ipv6_address"],
        module.params["interface"],
        module.params["mac_address"],
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
