#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jerome Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: mld_snooping_clear_statistics
short_description: Clear MLD snooping statistics on a D-Link DGS-1250 switch
description:
  - Executes the C(clear ipv6 mld snooping statistics) CLI command on a D-Link DGS-1250 switch.
  - Clears MLD snooping statistics for all VLANs, a specific VLAN, or a specific interface.
  - Corresponds to CLI command described in chapter 45-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.14.0"
author:
  - Jerome Dumesnil
options:
  target:
    description:
      - C(all) clears statistics for all VLANs and all ports.
      - C(vlan) clears statistics for a specific VLAN (requires C(vlan_id)).
      - C(interface) clears statistics for a specific port (requires C(interface_id)).
    type: str
    required: true
    choices: [all, vlan, interface]
  vlan_id:
    description:
      - The VLAN ID. Required when C(target=vlan).
    type: int
  interface_id:
    description:
      - The interface ID (e.g. C(eth1/0/1)). Required when C(target=interface).
    type: str
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Clear all MLD snooping statistics
  jaydee_io.dlink_dgs1250.mld_snooping_clear_statistics:
    target: all

- name: Clear MLD snooping statistics for VLAN 10
  jaydee_io.dlink_dgs1250.mld_snooping_clear_statistics:
    target: vlan
    vlan_id: 10

- name: Clear MLD snooping statistics for interface
  jaydee_io.dlink_dgs1250.mld_snooping_clear_statistics:
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
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_PRIVILEGED


def _build_commands(target, vlan_id, interface_id):
    if target == "all":
        return ["clear ipv6 mld snooping statistics all"]
    elif target == "vlan":
        return ["clear ipv6 mld snooping statistics vlan %d" % vlan_id]
    else:
        return ["clear ipv6 mld snooping statistics interface %s" % interface_id]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            target=dict(type="str", required=True, choices=["all", "vlan", "interface"]),
            vlan_id=dict(type="int"),
            interface_id=dict(type="str"),
        ),
        required_if=[
            ("target", "vlan", ["vlan_id"]),
            ("target", "interface", ["interface_id"]),
        ],
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["target"], module.params["vlan_id"], module.params["interface_id"])
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
