#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: dhcp_snooping_server_screen_hw_addr
short_description: Configure DHCP server screen profile hardware address entry on a D-Link DGS-1250 switch
description:
  - Configures the C(based-on hardware-address) CLI command in DHCP Server Screen Configure Mode on a D-Link DGS-1250 switch.
  - Corresponds to CLI command described in chapter 17-17 of the DGS-1250 CLI Reference Guide.
version_added: "0.9.0"
author:
  - Jérôme Dumesnil
options:
  profile:
    description:
      - The server screen profile name.
    type: str
    required: true
  mac_address:
    description:
      - The client MAC address.
    type: str
    required: true
  state:
    description:
      - C(present) to add, C(absent) to remove the entry.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in DHCP Server Screen Configure Mode.
"""

EXAMPLES = r"""
- name: Add MAC to server screen profile
  jaydee_io.dlink_dgs1250.dhcp_snooping_server_screen_hw_addr:
    profile: campus-profile
    mac_address: 00-08-01-02-03-04
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
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG

def _build_commands(profile, mac_address, state):
    """Build the CLI command list."""
    commands = ["dhcp-server-screen profile %s" % profile]
    if state == "absent":
        commands.append("no based-on hardware-address %s" % mac_address)
    else:
        commands.append("based-on hardware-address %s" % mac_address)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            profile=dict(type="str", required=True),
            mac_address=dict(type="str", required=True),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["profile"], module.params["mac_address"], module.params["state"])
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
