#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: port_security_clear
short_description: Clear auto-learned secured MAC addresses on a D-Link DGS-1250 switch
description:
  - Executes the C(clear port-security) CLI command on a D-Link DGS-1250 switch.
  - Deletes auto-learned secured MAC addresses.
  - Corresponds to CLI command described in chapter 50-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.15.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  target:
    description:
      - C(all) clears all auto-learned secured entries.
      - C(address) clears a specific MAC address (requires C(mac_address)).
      - C(interface) clears entries on a specific interface (requires C(interface_id)).
    type: str
    required: true
    choices: [all, address, interface]
  mac_address:
    description:
      - The MAC address to clear (e.g. C(0080.0070.0007)). Required when C(target=address).
    type: str
  interface_id:
    description:
      - The interface ID (e.g. C(eth1/0/1)). Required when C(target=interface).
    type: str
  vlan_id:
    description:
      - Optional VLAN ID to filter the clear operation.
    type: int
notes:
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Clear all auto-learned secured entries
  jaydee_io.dlink_dgs1250.port_security_clear:
    target: all

- name: Clear a specific MAC address
  jaydee_io.dlink_dgs1250.port_security_clear:
    target: address
    mac_address: "0080.0070.0007"

- name: Clear secured entries on an interface
  jaydee_io.dlink_dgs1250.port_security_clear:
    target: interface
    interface_id: eth1/0/1
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


def _build_commands(target, mac_address, interface_id, vlan_id):
    if target == "all":
        cmd = "clear port-security all"
    elif target == "address":
        cmd = "clear port-security address %s" % mac_address
    else:
        cmd = "clear port-security interface %s" % interface_id
    if vlan_id is not None:
        cmd += " vlan %d" % vlan_id
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            target=dict(type="str", required=True, choices=[
                        "all", "address", "interface"]),
            mac_address=dict(type="str"),
            interface_id=dict(type="str"),
            vlan_id=dict(type="int"),
        ),
        required_if=[
            ("target", "address", ["mac_address"]),
            ("target", "interface", ["interface_id"]),
        ],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["target"],
        module.params["mac_address"],
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
