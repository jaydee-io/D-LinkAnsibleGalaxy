#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: show_igmp_snooping_groups
short_description: Display IGMP snooping group information on a D-Link DGS-1250 switch
description:
  - Executes the C(show ip igmp snooping groups) CLI command on a D-Link DGS-1250 switch.
  - Displays IGMP snooping group information learned on the switch.
  - Corresponds to CLI command described in chapter 31-14 of the DGS-1250 CLI Reference Guide.
version_added: "0.12.0"
author:
  - Jérôme Dumesnil
options:
  vlan_id:
    description:
      - Optional VLAN ID to filter by.
    type: int
  ip_address:
    description:
      - Optional group IP address to filter by.
    type: str
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Display all IGMP snooping groups
  jaydee_io.dlink_dgs1250.show_igmp_snooping_groups:
  register: result

- name: Display IGMP snooping groups for VLAN 1
  jaydee_io.dlink_dgs1250.show_igmp_snooping_groups:
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
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


def _build_command(vlan_id, ip_address):
    cmd = "show ip igmp snooping groups"
    if vlan_id:
        cmd += " vlan %d" % vlan_id
    elif ip_address:
        cmd += " %s" % ip_address
    return cmd


def main():
    module = AnsibleModule(
        argument_spec=dict(
            vlan_id=dict(type="int"),
            ip_address=dict(type="str"),
        ),
        mutually_exclusive=[("vlan_id", "ip_address")],
        supports_check_mode=True,
    )
    command = _build_command(module.params["vlan_id"], module.params["ip_address"])
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
