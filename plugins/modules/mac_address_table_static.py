#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: mac_address_table_static
short_description: Configure static MAC address table entries on a D-Link DGS-1250 switch
description:
  - Adds or removes a static MAC address entry from the MAC address table using the
    C(mac-address-table static) CLI command.
  - Corresponds to CLI command described in chapter 28-5 of the DGS-1250 CLI Reference Guide.
version_added: "0.11.0"
author:
  - Jérôme Dumesnil
options:
  mac_addr:
    description:
      - The MAC address of the entry (unicast).
      - Required when C(state=present).
    type: str
  vlan_id:
    description:
      - The VLAN ID of the entry (1 to 4094).
      - Required when C(state=present).
    type: int
  interface_id:
    description:
      - The forwarding interface. Mutually exclusive with C(drop).
    type: str
  drop:
    description:
      - Drop frames sent to or from the specified MAC address on the VLAN.
    type: bool
    default: false
  remove_all:
    description:
      - Remove all static MAC address entries (C(no mac-address-table static all)).
    type: bool
    default: false
  state:
    description:
      - C(present) adds the static MAC address entry.
      - C(absent) removes the static MAC address entry.
    type: str
    default: present
    choices: [present, absent]
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Add static MAC address entry forwarding to port 1
  jaydee_io.dlink_dgs1250.mac_address_table_static:
    mac_addr: "C2:F3:22:0A:12:F4"
    vlan_id: 4
    interface_id: eth1/0/1
    state: present

- name: Add static MAC drop entry
  jaydee_io.dlink_dgs1250.mac_address_table_static:
    mac_addr: "00:01:00:02:00:07"
    vlan_id: 6
    drop: true
    state: present

- name: Remove all static MAC entries
  jaydee_io.dlink_dgs1250.mac_address_table_static:
    remove_all: true
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


def _build_commands(mac_addr, vlan_id, interface_id, drop, remove_all, state):
    if state == "absent":
        if remove_all:
            return ["no mac-address-table static all"]
        cmd = "no mac-address-table static %s vlan %d" % (mac_addr, vlan_id)
        if interface_id:
            cmd += " interface %s" % interface_id
        return [cmd]
    cmd = "mac-address-table static %s vlan %d" % (mac_addr, vlan_id)
    if drop:
        cmd += " drop"
    else:
        cmd += " interface %s" % interface_id
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            mac_addr=dict(type="str"),
            vlan_id=dict(type="int"),
            interface_id=dict(type="str"),
            drop=dict(type="bool", default=False),
            remove_all=dict(type="bool", default=False),
            state=dict(type="str", default="present", choices=["present", "absent"]),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["mac_addr"],
        module.params["vlan_id"],
        module.params["interface_id"],
        module.params["drop"],
        module.params["remove_all"],
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
