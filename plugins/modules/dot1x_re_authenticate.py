#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: dot1x_re_authenticate
short_description: Re-authenticate 802.1X on a port or MAC address on a D-Link DGS-1250 switch
description:
  - Executes the C(dot1x re-authenticate) CLI command on a D-Link DGS-1250 switch.
  - Re-authenticates a specific port or a specific MAC address.
  - Corresponds to CLI command described in chapter 3-9 of the DGS-1250 CLI Reference Guide.
version_added: "0.2.0"
author:
  - Jérôme Dumesnil
options:
  interfaces:
    description:
      - List of physical port interfaces to re-authenticate.
      - Each entry can be a single port (e.g. C(eth1/0/1)) or a range (e.g. C(eth1/0/1-eth1/0/8)).
      - Mutually exclusive with C(mac_address).
    type: list
    elements: str
  mac_address:
    description:
      - MAC address to re-authenticate (for multi-auth mode).
      - Mutually exclusive with C(interfaces).
    type: str
notes:
  - This module requires C(ansible_network_os=dlink.dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Privileged EXEC Mode.
  - In multi-host mode, specify interfaces. In multi-auth mode, specify a MAC address.
"""

EXAMPLES = r"""
- name: Re-authenticate port 1
  dlink.dgs1250.dot1x_re_authenticate:
    interfaces:
      - eth1/0/1

- name: Re-authenticate a MAC address
  dlink.dgs1250.dot1x_re_authenticate:
    mac_address: "00-11-22-33-44-55"
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
    from ansible_collections.dlink.dgs1250.plugins.module_utils.dgs1250 import (
        run_commands, MODE_PRIVILEGED,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_PRIVILEGED


# ---------------------------------------------------------------------------
# Command builder
# ---------------------------------------------------------------------------

def _build_commands(interfaces, mac_address):
    """Build the CLI command list."""
    if mac_address:
        return ["dot1x re-authenticate mac-address %s" % mac_address]

    commands = []
    for iface in interfaces:
        commands.append("dot1x re-authenticate interface %s" % iface)
    return commands


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            interfaces=dict(type="list", elements="str"),
            mac_address=dict(type="str"),
        ),
        mutually_exclusive=[
            ("interfaces", "mac_address"),
        ],
        required_one_of=[
            ("interfaces", "mac_address"),
        ],
        supports_check_mode=True,
    )

    interfaces = module.params["interfaces"]
    mac_address = module.params["mac_address"]

    commands = _build_commands(interfaces, mac_address)

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
