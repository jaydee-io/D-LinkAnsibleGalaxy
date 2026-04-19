#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: show_mac_address_table
short_description: Display MAC address table on a D-Link DGS-1250 switch
description:
  - Executes the C(show mac-address-table) CLI command on a D-Link DGS-1250 switch.
  - Displays specific MAC address entries or entries for a specific interface or VLAN.
  - Corresponds to CLI command described in chapter 28-7 of the DGS-1250 CLI Reference Guide.
version_added: "0.11.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  entry_type:
    description:
      - Filter by entry type C(dynamic) or C(static). If not specified, all entries are shown.
    type: str
    choices: [dynamic, static]
  mac_addr:
    description:
      - Filter by specific MAC address.
    type: str
  interface_id:
    description:
      - Filter by specific interface.
    type: str
  vlan_id:
    description:
      - Filter by VLAN ID (1 to 4094).
    type: int
notes:
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Display all MAC address table entries
  jaydee_io.dlink_dgs1250.show_mac_address_table:
  register: result

- name: Display static MAC address table entries
  jaydee_io.dlink_dgs1250.show_mac_address_table:
    entry_type: static
  register: result

- name: Display MAC address table for VLAN 1
  jaydee_io.dlink_dgs1250.show_mac_address_table:
    vlan_id: 1
  register: result
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
        run_command,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


def _build_command(entry_type, mac_addr, interface_id, vlan_id):
    cmd = "show mac-address-table"
    if entry_type:
        cmd += " %s" % entry_type
    if mac_addr:
        cmd += " address %s" % mac_addr
    if interface_id:
        cmd += " interface %s" % interface_id
    if vlan_id is not None:
        cmd += " vlan %d" % vlan_id
    return cmd


def main():
    module = AnsibleModule(
        argument_spec=dict(
            entry_type=dict(type="str", choices=["dynamic", "static"]),
            mac_addr=dict(type="str"),
            interface_id=dict(type="str"),
            vlan_id=dict(type="int"),
        ),
        supports_check_mode=True,
    )
    command = _build_command(
        module.params["entry_type"],
        module.params["mac_addr"],
        module.params["interface_id"],
        module.params["vlan_id"],
    )
    if module.check_mode:
        module.exit_json(changed=False, commands=[command], raw_output="")
        return
    try:
        raw_output = run_command(module, command)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    module.exit_json(changed=False, raw_output=raw_output, commands=[command])


if __name__ == "__main__":
    main()
