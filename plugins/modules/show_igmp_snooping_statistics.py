#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: show_igmp_snooping_statistics
short_description: Display IGMP snooping statistics on a D-Link DGS-1250 switch
description:
  - Executes the C(show ip igmp snooping statistics) CLI command on a D-Link DGS-1250 switch.
  - Displays IGMP snooping statistics information by interface or by VLAN.
  - Corresponds to CLI command described in chapter 31-17 of the DGS-1250 CLI Reference Guide.
version_added: "0.12.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  target:
    description:
      - C(interface) displays statistics by interface.
      - C(vlan) displays statistics by VLAN.
    type: str
    required: true
    choices: [interface, vlan]
  interface_id:
    description:
      - Optional interface ID to filter by (e.g. C(eth1/0/1)). Only used when C(target=interface).
    type: str
  vlan_id:
    description:
      - Optional VLAN ID to filter by. Only used when C(target=vlan).
    type: int
notes:
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Display IGMP snooping statistics by interface
  jaydee_io.dlink_dgs1250.show_igmp_snooping_statistics:
    target: interface
  register: result

- name: Display IGMP snooping statistics for VLAN 1
  jaydee_io.dlink_dgs1250.show_igmp_snooping_statistics:
    target: vlan
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


def _build_command(target, interface_id, vlan_id):
    if target == "interface":
        if interface_id:
            return "show ip igmp snooping statistics interface %s" % interface_id
        return "show ip igmp snooping statistics interface"
    else:
        if vlan_id:
            return "show ip igmp snooping statistics vlan %d" % vlan_id
        return "show ip igmp snooping statistics vlan"


def main():
    module = AnsibleModule(
        argument_spec=dict(
            target=dict(type="str", required=True,
                        choices=["interface", "vlan"]),
            interface_id=dict(type="str"),
            vlan_id=dict(type="int"),
        ),
        supports_check_mode=True,
    )
    command = _build_command(
        module.params["target"],
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
