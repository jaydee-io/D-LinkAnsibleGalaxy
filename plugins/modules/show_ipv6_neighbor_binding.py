#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: show_ipv6_neighbor_binding
short_description: Display IPv6 neighbor binding table on a D-Link DGS-1250 switch
description:
  - Executes the C(show ipv6 neighbor binding) CLI command on a D-Link DGS-1250 switch.
  - Displays the IPv6 binding table entries.
  - Corresponds to CLI command described in chapter 38-7 of the DGS-1250 CLI Reference Guide.
version_added: "0.13.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  vlan_id:
    description:
      - Optional VLAN ID to filter entries.
    type: int
  interface:
    description:
      - Optional interface to filter entries (e.g. C(eth1/0/1)).
    type: str
  ipv6_address:
    description:
      - Optional IPv6 address to filter entries.
    type: str
  mac_address:
    description:
      - Optional MAC address to filter entries.
    type: str
notes:
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Display all IPv6 neighbor bindings
  jaydee_io.dlink_dgs1250.show_ipv6_neighbor_binding:
  register: result

- name: Display bindings for a specific VLAN
  jaydee_io.dlink_dgs1250.show_ipv6_neighbor_binding:
    vlan_id: 100
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


def _build_command(vlan_id, interface, ipv6_address, mac_address):
    cmd = "show ipv6 neighbor binding"
    if vlan_id is not None:
        cmd += " vlan %d" % vlan_id
    if interface:
        cmd += " interface %s" % interface
    if ipv6_address:
        cmd += " ipv6 %s" % ipv6_address
    if mac_address:
        cmd += " mac %s" % mac_address
    return cmd


def main():
    module = AnsibleModule(
        argument_spec=dict(
            vlan_id=dict(type="int"),
            interface=dict(type="str"),
            ipv6_address=dict(type="str"),
            mac_address=dict(type="str"),
        ),
        supports_check_mode=True,
    )
    command = _build_command(
        module.params["vlan_id"],
        module.params["interface"],
        module.params["ipv6_address"],
        module.params["mac_address"],
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
