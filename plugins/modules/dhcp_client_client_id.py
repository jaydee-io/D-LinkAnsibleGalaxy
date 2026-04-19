#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dhcp_client_client_id
short_description: Configure DHCP client ID on a D-Link DGS-1250 switch
description:
  - Configures the C(ip dhcp client client-id) CLI command on a D-Link DGS-1250 switch.
  - Specifies the VLAN interface whose MAC address will be used as the client ID.
  - Corresponds to CLI command described in chapter 15-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.8.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Interface on which to configure the DHCP client-id (e.g. C(vlan 100)).
    type: str
    required: true
  client_interface:
    description:
      - The VLAN interface whose MAC address will be used as the client ID (e.g. C(vlan 100)).
        Required when C(state=present).
    type: str
  state:
    description:
      - C(present) to set the client-id, C(absent) to revert to default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Set DHCP client-id to use MAC of vlan 100
  jaydee_io.dlink_dgs1250.dhcp_client_client_id:
    interface: vlan 100
    client_interface: vlan 100

- name: Reset DHCP client-id to default on vlan 100
  jaydee_io.dlink_dgs1250.dhcp_client_client_id:
    interface: vlan 100
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


def _build_commands(interface, client_interface, state):
    """Build the CLI command list."""
    commands = ["interface %s" % interface]
    if state == "absent":
        commands.append("no ip dhcp client client-id")
    else:
        commands.append("ip dhcp client client-id %s" % client_interface)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            client_interface=dict(type="str"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["client_interface"]),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["interface"],
        module.params["client_interface"],
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
