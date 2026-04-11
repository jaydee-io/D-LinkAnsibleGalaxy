#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: dhcp_snooping_binding
short_description: Manually configure a DHCP snooping binding entry on a D-Link DGS-1250 switch
description:
  - Configures the C(ip dhcp snooping binding) CLI command on a D-Link DGS-1250 switch.
  - Manually adds a static binding entry to the DHCP snooping binding table.
  - Corresponds to CLI command described in chapter 17-7 of the DGS-1250 CLI Reference Guide.
version_added: "0.9.0"
author:
  - Jérôme Dumesnil
options:
  mac_address:
    description:
      - MAC address for the binding entry.
    type: str
    required: true
  vlan:
    description:
      - VLAN ID for the binding entry.
    type: int
    required: true
  ip_address:
    description:
      - IP address for the binding entry.
    type: str
    required: true
  interface:
    description:
      - Interface for the binding entry (e.g. C(eth1/0/1)).
    type: str
    required: true
  expiry:
    description:
      - Expiry time in seconds for the binding entry.
    type: int
    required: true
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Add a static DHCP snooping binding entry
  jaydee_io.dlink_dgs1250.dhcp_snooping_binding:
    mac_address: 00:11:22:33:44:55
    vlan: 10
    ip_address: 192.168.1.100
    interface: eth1/0/1
    expiry: 86400
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


def _build_commands(mac_address, vlan, ip_address, interface, expiry):
    """Build the CLI command list."""
    return [
        "ip dhcp snooping binding %s vlan %d %s interface %s expiry %d"
        % (mac_address, vlan, ip_address, interface, expiry)
    ]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            mac_address=dict(type="str", required=True),
            vlan=dict(type="int", required=True),
            ip_address=dict(type="str", required=True),
            interface=dict(type="str", required=True),
            expiry=dict(type="int", required=True),
        ),
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["mac_address"],
        module.params["vlan"],
        module.params["ip_address"],
        module.params["interface"],
        module.params["expiry"],
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
