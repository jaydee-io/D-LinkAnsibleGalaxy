#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: dhcp_client_class_id
short_description: Configure DHCP client vendor class identifier on a D-Link DGS-1250 switch
description:
  - Configures the C(ip dhcp client class-id) CLI command on a D-Link DGS-1250 switch.
  - Sets the vendor class identifier (Option 60) for the DHCP discover message.
  - Corresponds to CLI command described in chapter 15-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.8.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Interface on which to configure the DHCP client class-id (e.g. C(vlan 100)).
    type: str
    required: true
  value:
    description:
      - The vendor class identifier string. Required when C(state=present).
    type: str
  hex:
    description:
      - If C(true), the value is specified as a hexadecimal string.
    type: bool
    default: false
  state:
    description:
      - C(present) to set the class-id, C(absent) to revert to default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Set DHCP client class-id to VOIP-Device on vlan 100
  jaydee_io.dlink_dgs1250.dhcp_client_class_id:
    interface: vlan 100
    value: VOIP-Device

- name: Set DHCP client class-id as hex on vlan 100
  jaydee_io.dlink_dgs1250.dhcp_client_class_id:
    interface: vlan 100
    value: "112233"
    hex: true

- name: Reset DHCP client class-id to default on vlan 100
  jaydee_io.dlink_dgs1250.dhcp_client_class_id:
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
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(interface, value, hex_mode, state):
    """Build the CLI command list."""
    commands = ["interface %s" % interface]
    if state == "absent":
        commands.append("no ip dhcp client class-id")
    elif hex_mode:
        commands.append("ip dhcp client class-id hex %s" % value)
    else:
        commands.append("ip dhcp client class-id %s" % value)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            value=dict(type="str"),
            hex=dict(type="bool", default=False),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["value"]),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["interface"],
        module.params["value"],
        module.params["hex"],
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
