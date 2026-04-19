#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jerome Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: mld_snooping_static_group
short_description: Configure MLD snooping static group on a D-Link DGS-1250 switch
description:
  - Configures the C(ipv6 mld snooping static-group) CLI command on a D-Link DGS-1250 switch.
  - Adds or removes static MLD snooping group membership entries on a VLAN.
  - Corresponds to CLI command described in chapter 45-11 of the DGS-1250 CLI Reference Guide.
version_added: "0.14.0"
author:
  - Jerome Dumesnil
options:
  vlan_id:
    description:
      - The VLAN ID to configure.
    type: int
    required: true
  group_address:
    description:
      - The IPv6 multicast group address.
    type: str
    required: true
  interface_id:
    description:
      - The interface ID (e.g. C(eth1/0/5)). Required when C(state=present).
    type: str
  state:
    description:
      - C(present) to add, C(absent) to remove the static group.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in VLAN Configuration Mode.
"""

EXAMPLES = r"""
- name: Add static MLD snooping group
  jaydee_io.dlink_dgs1250.mld_snooping_static_group:
    vlan_id: 1
    group_address: "FF02::12:03"
    interface_id: eth1/0/5

- name: Remove static MLD snooping group
  jaydee_io.dlink_dgs1250.mld_snooping_static_group:
    vlan_id: 1
    group_address: "FF02::12:03"
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


def _build_commands(vlan_id, group_address, interface_id, state):
    if state == "absent":
        cmd = "no ipv6 mld snooping static-group %s" % group_address
    else:
        cmd = "ipv6 mld snooping static-group %s interface %s" % (
            group_address, interface_id)
    return ["vlan %d" % vlan_id, cmd, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            vlan_id=dict(type="int", required=True),
            group_address=dict(type="str", required=True),
            interface_id=dict(type="str"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["interface_id"]),
        ],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["vlan_id"], module.params["group_address"], module.params["interface_id"], module.params["state"])
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
