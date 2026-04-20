#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dhcp_relay_info_option_insert
short_description: Configure DHCP relay information option-insert on an interface on a D-Link DGS-1250 switch
description:
  - Configures the C(ip dhcp relay information option-insert) CLI command on a D-Link DGS-1250 switch.
  - Configures or removes the DHCP relay information option-insert setting on an interface.
  - Corresponds to CLI command described in chapter 16-7 of the DGS-1250 CLI Reference Guide.
version_added: "0.9.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Interface on which to configure option-insert (e.g. C(vlan 100)).
    type: str
    required: true
  none:
    description:
      - If C(true), use the C(none) keyword to disable option-insert.
    type: bool
    default: false
  state:
    description:
      - C(present) to configure option-insert, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable DHCP relay information option-insert on vlan 100
  jaydee_io.dlink_dgs1250.dhcp_relay_info_option_insert:
    interface: vlan 100

- name: Set option-insert to none on vlan 100
  jaydee_io.dlink_dgs1250.dhcp_relay_info_option_insert:
    interface: vlan 100
    none: true

- name: Remove DHCP relay information option-insert on vlan 100
  jaydee_io.dlink_dgs1250.dhcp_relay_info_option_insert:
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
        run_commands, is_config_present, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, is_config_present, MODE_GLOBAL_CONFIG


def _build_commands(interface, none_mode, state):
    """Build the CLI command list."""
    commands = ["interface %s" % interface]
    if state == "absent":
        if none_mode:
            commands.append("no ip dhcp relay information option-insert none")
        else:
            commands.append("no ip dhcp relay information option-insert")
    else:
        if none_mode:
            commands.append("ip dhcp relay information option-insert none")
        else:
            commands.append("ip dhcp relay information option-insert")
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            none=dict(type="bool", default=False),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["interface"],
        module.params["none"],
        module.params["state"],
    )

    if is_config_present(module, commands):
        module.exit_json(changed=False, commands=[], raw_output="")
        return
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
