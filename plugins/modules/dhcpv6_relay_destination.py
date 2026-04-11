#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: dhcpv6_relay_destination
short_description: Configure DHCPv6 relay destination on a D-Link DGS-1250 switch
description:
  - Configures the C(ipv6 dhcp relay destination) CLI command on a D-Link DGS-1250 switch.
  - Adds or removes a DHCPv6 relay destination address on an interface.
  - Corresponds to CLI command described in chapter 20-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.9.0"
author:
  - Jérôme Dumesnil
options:
  interface:
    description:
      - Interface on which to configure the relay destination (e.g. C(vlan1)).
    type: str
    required: true
  address:
    description:
      - The DHCPv6 relay destination IPv6 address.
    type: str
    required: true
  output_interface:
    description:
      - Optional output interface for the relay destination.
    type: str
  state:
    description:
      - C(present) to add, C(absent) to remove.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Add DHCPv6 relay destination on vlan1
  jaydee_io.dlink_dgs1250.dhcpv6_relay_destination:
    interface: vlan1
    address: "FE80::250:A2FF:FEBF:A056"
    output_interface: vlan1

- name: Remove DHCPv6 relay destination
  jaydee_io.dlink_dgs1250.dhcpv6_relay_destination:
    interface: vlan1
    address: "FE80::250:A2FF:FEBF:A056"
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


def _build_commands(interface, address, output_interface, state):
    """Build the CLI command list."""
    commands = ["interface %s" % interface]
    if state == "absent":
        cmd = "no ipv6 dhcp relay destination %s" % address
        if output_interface:
            cmd += " %s" % output_interface
    else:
        cmd = "ipv6 dhcp relay destination %s" % address
        if output_interface:
            cmd += " %s" % output_interface
    commands.append(cmd)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            address=dict(type="str", required=True),
            output_interface=dict(type="str"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["interface"],
        module.params["address"],
        module.params["output_interface"],
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
