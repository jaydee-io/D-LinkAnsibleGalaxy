#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: dhcp_snooping_clear_binding
short_description: Clear DHCP snooping binding entries on a D-Link DGS-1250 switch
description:
  - Executes the C(clear ip dhcp snooping binding) CLI command on a D-Link DGS-1250 switch.
  - Clears DHCP snooping binding table entries, optionally filtered by MAC, IP, VLAN, or interface.
  - Corresponds to CLI command described in chapter 17-5 of the DGS-1250 CLI Reference Guide.
version_added: "0.9.0"
author:
  - Jérôme Dumesnil
options:
  mac_address:
    description:
      - MAC address to filter the binding entries to clear.
    type: str
  ip_address:
    description:
      - IP address to filter the binding entries to clear.
    type: str
  vlan:
    description:
      - VLAN ID to filter the binding entries to clear.
    type: int
  interface:
    description:
      - Interface ID to filter the binding entries to clear (e.g. C(eth1/0/1)).
    type: str
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Clear all DHCP snooping binding entries
  jaydee_io.dlink_dgs1250.dhcp_snooping_clear_binding:

- name: Clear binding entries for a specific MAC address
  jaydee_io.dlink_dgs1250.dhcp_snooping_clear_binding:
    mac_address: 00:11:22:33:44:55

- name: Clear binding entries for a specific VLAN and interface
  jaydee_io.dlink_dgs1250.dhcp_snooping_clear_binding:
    vlan: 10
    interface: eth1/0/1
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


def _build_commands(mac_address, ip_address, vlan, interface):
    """Build the CLI command list."""
    cmd = "clear ip dhcp snooping binding"
    if mac_address is not None:
        cmd += " %s" % mac_address
    if ip_address is not None:
        cmd += " %s" % ip_address
    if vlan is not None:
        cmd += " vlan %d" % vlan
    if interface is not None:
        cmd += " interface %s" % interface
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            mac_address=dict(type="str"),
            ip_address=dict(type="str"),
            vlan=dict(type="int"),
            interface=dict(type="str"),
        ),
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["mac_address"],
        module.params["ip_address"],
        module.params["vlan"],
        module.params["interface"],
    )

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
