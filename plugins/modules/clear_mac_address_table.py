#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: clear_mac_address_table
short_description: Clear dynamic MAC address table entries on a D-Link DGS-1250 switch
description:
  - Executes the C(clear mac-address-table dynamic) CLI command on a D-Link DGS-1250 switch.
  - Clears dynamic MAC addresses for all entries, a specific address, interface, or VLAN.
  - Corresponds to CLI command described in chapter 28-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.11.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  target:
    description:
      - C(all) clears all dynamic MAC addresses.
      - C(address) clears a specific MAC address (requires C(mac_addr)).
      - C(interface) clears entries for a specific interface (requires C(interface_id)).
      - C(vlan) clears entries for a specific VLAN (requires C(vlan_id)).
    type: str
    required: true
    choices: [all, address, interface, vlan]
  mac_addr:
    description:
      - The MAC address to delete. Required when C(target=address).
    type: str
  interface_id:
    description:
      - The interface ID (e.g. C(eth1/0/1)). Required when C(target=interface).
    type: str
  vlan_id:
    description:
      - The VLAN ID (1 to 4094). Required when C(target=vlan).
    type: int
notes:
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Clear all dynamic MAC addresses
  jaydee_io.dlink_dgs1250.clear_mac_address_table:
    target: all

- name: Clear a specific MAC address
  jaydee_io.dlink_dgs1250.clear_mac_address_table:
    target: address
    mac_addr: "00:08:00:70:00:07"

- name: Clear dynamic MAC addresses for VLAN 10
  jaydee_io.dlink_dgs1250.clear_mac_address_table:
    target: vlan
    vlan_id: 10
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
        run_commands, MODE_PRIVILEGED,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_PRIVILEGED


def _build_commands(target, mac_addr, interface_id, vlan_id):
    if target == "all":
        return ["clear mac-address-table dynamic all"]
    elif target == "address":
        return ["clear mac-address-table dynamic address %s" % mac_addr]
    elif target == "interface":
        return ["clear mac-address-table dynamic interface %s" % interface_id]
    else:
        return ["clear mac-address-table dynamic vlan %d" % vlan_id]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            target=dict(type="str", required=True, choices=[
                        "all", "address", "interface", "vlan"]),
            mac_addr=dict(type="str"),
            interface_id=dict(type="str"),
            vlan_id=dict(type="int"),
        ),
        required_if=[
            ("target", "address", ["mac_addr"]),
            ("target", "interface", ["interface_id"]),
            ("target", "vlan", ["vlan_id"]),
        ],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["target"],
        module.params["mac_addr"],
        module.params["interface_id"],
        module.params["vlan_id"],
    )
    if module.check_mode:
        module.exit_json(changed=True, commands=commands, raw_output="")
        return
    try:
        raw_output = run_commands(module, commands, mode=MODE_PRIVILEGED)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    module.exit_json(changed=True, raw_output=raw_output, commands=commands)


if __name__ == "__main__":
    main()
