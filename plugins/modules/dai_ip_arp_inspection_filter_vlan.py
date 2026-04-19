#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dai_ip_arp_inspection_filter_vlan
short_description: Configure ARP access list for ARP inspection on a D-Link DGS-1250 switch
description:
  - Configures the C(ip arp inspection filter) CLI command on a D-Link DGS-1250 switch.
  - Specifies an ARP access list to be used for ARP inspection checks for a VLAN.
  - Corresponds to CLI command described in chapter 25-4 of the DGS-1250 CLI Reference Guide.
version_added: "0.10.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  acl_name:
    description:
      - The ARP access control list name (maximum 32 characters).
    type: str
    required: true
  vlan_id:
    description:
      - The VLAN ID or range associated with the ARP access list.
    type: str
    required: true
  static:
    description:
      - If C(true), drop packets if IP-to-Ethernet MAC binding pair is not permitted by the ARP ACL.
    type: bool
    default: false
  state:
    description:
      - C(present) to configure, C(absent) to remove.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Apply ARP ACL to VLAN 10 for DAI
  jaydee_io.dlink_dgs1250.dai_ip_arp_inspection_filter_vlan:
    acl_name: static-arp-list
    vlan_id: "10"

- name: Apply ARP ACL static to VLAN 10
  jaydee_io.dlink_dgs1250.dai_ip_arp_inspection_filter_vlan:
    acl_name: static-arp-list
    vlan_id: "10"
    static: true

- name: Remove ARP ACL from VLAN 10
  jaydee_io.dlink_dgs1250.dai_ip_arp_inspection_filter_vlan:
    acl_name: static-arp-list
    vlan_id: "10"
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


def _build_commands(acl_name, vlan_id, static, state):
    """Build the CLI command list."""
    if state == "absent":
        cmd = "no ip arp inspection filter %s vlan %s" % (acl_name, vlan_id)
        if static:
            cmd += " static"
    else:
        cmd = "ip arp inspection filter %s vlan %s" % (acl_name, vlan_id)
        if static:
            cmd += " static"
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            acl_name=dict(type="str", required=True),
            vlan_id=dict(type="str", required=True),
            static=dict(type="bool", default=False),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["acl_name"],
        module.params["vlan_id"],
        module.params["static"],
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
