#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: dhcp_snooping_show_binding
short_description: Display DHCP snooping binding entries on a D-Link DGS-1250 switch
description:
  - Executes the C(show ip dhcp snooping binding) CLI command on a D-Link DGS-1250 switch.
  - Corresponds to CLI command described in chapter 17-15 of the DGS-1250 CLI Reference Guide.
version_added: "0.9.0"
author:
  - Jérôme Dumesnil
options:
  ip_address:
    description:
      - Filter by IP address.
    type: str
  mac_address:
    description:
      - Filter by MAC address.
    type: str
  vlan:
    description:
      - Filter by VLAN ID.
    type: int
  interface:
    description:
      - Filter by interface.
    type: str
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Display all snooping binding entries
  jaydee_io.dlink_dgs1250.dhcp_snooping_show_binding:

- name: Display binding entries for VLAN 100
  jaydee_io.dlink_dgs1250.dhcp_snooping_show_binding:
    vlan: 100
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

def _build_command(ip_address=None, mac_address=None, vlan=None, interface=None):
    """Build the CLI command."""
    cmd = "show ip dhcp snooping binding"
    if ip_address:
        cmd += " %s" % ip_address
    if mac_address:
        cmd += " %s" % mac_address
    if vlan:
        cmd += " vlan %s" % vlan
    if interface:
        cmd += " interface %s" % interface
    return cmd


def main():
    module = AnsibleModule(
        argument_spec=dict(
            ip_address=dict(type="str"),
            mac_address=dict(type="str"),
            vlan=dict(type="int"),
            interface=dict(type="str"),
        ),
        supports_check_mode=True,
    )
    command = _build_command(
        module.params["ip_address"], module.params["mac_address"],
        module.params["vlan"], module.params["interface"],
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
