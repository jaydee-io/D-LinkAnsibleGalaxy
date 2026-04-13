#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: show_ip_source_binding
short_description: Display IP source guard binding entries on a D-Link DGS-1250 switch
description:
  - Executes the C(show ip source binding) CLI command on a D-Link DGS-1250 switch.
  - Displays IP source guard binding entries on the switch.
  - Corresponds to CLI command described in chapter 35-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.12.0"
author:
  - Jérôme Dumesnil
options:
  ip_addr:
    description:
      - Optional IP address to filter by.
    type: str
  mac_addr:
    description:
      - Optional MAC address to filter by.
    type: str
  binding_type:
    description:
      - Optional filter by binding type.
    type: str
    choices: [dhcp-snooping, static]
  vlan_id:
    description:
      - Optional VLAN ID to filter by.
    type: int
  interface_id:
    description:
      - Optional interface ID to filter by (e.g. C(eth1/0/3)).
    type: str
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Display all IP source guard binding entries
  jaydee_io.dlink_dgs1250.show_ip_source_binding:
  register: result

- name: Display binding entries for a specific IP
  jaydee_io.dlink_dgs1250.show_ip_source_binding:
    ip_addr: "10.1.1.10"
  register: result

- name: Display static binding entries
  jaydee_io.dlink_dgs1250.show_ip_source_binding:
    binding_type: static
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


def _build_command(ip_addr, mac_addr, binding_type, vlan_id, interface_id):
    cmd = "show ip source binding"
    if ip_addr:
        cmd += " %s" % ip_addr
    if mac_addr:
        cmd += " %s" % mac_addr
    if binding_type:
        cmd += " %s" % binding_type
    if vlan_id:
        cmd += " vlan %d" % vlan_id
    if interface_id:
        cmd += " interface %s" % interface_id
    return cmd


def main():
    module = AnsibleModule(
        argument_spec=dict(
            ip_addr=dict(type="str"),
            mac_addr=dict(type="str"),
            binding_type=dict(type="str", choices=["dhcp-snooping", "static"]),
            vlan_id=dict(type="int"),
            interface_id=dict(type="str"),
        ),
        supports_check_mode=True,
    )
    command = _build_command(
        module.params["ip_addr"],
        module.params["mac_addr"],
        module.params["binding_type"],
        module.params["vlan_id"],
        module.params["interface_id"],
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
