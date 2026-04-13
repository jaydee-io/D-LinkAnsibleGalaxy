#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: igmp_snooping_fast_leave
short_description: Configure IGMP snooping fast-leave on a VLAN on a D-Link DGS-1250 switch
description:
  - Configures the C(ip igmp snooping fast-leave) CLI command on a D-Link DGS-1250 switch.
  - Enables or disables IGMP snooping fast-leave on a specific VLAN.
  - Corresponds to CLI command described in chapter 31-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.12.0"
author:
  - Jérôme Dumesnil
options:
  vlan_id:
    description:
      - The VLAN ID to configure.
    type: int
    required: true
  state:
    description:
      - Whether to enable (C(enabled)) or disable (C(disabled)) fast-leave.
    type: str
    choices: [enabled, disabled]
    default: enabled
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in VLAN Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable IGMP snooping fast-leave on VLAN 1
  jaydee_io.dlink_dgs1250.igmp_snooping_fast_leave:
    vlan_id: 1

- name: Disable IGMP snooping fast-leave on VLAN 1
  jaydee_io.dlink_dgs1250.igmp_snooping_fast_leave:
    vlan_id: 1
    state: disabled
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


def _build_commands(vlan_id, state):
    cmd = "ip igmp snooping fast-leave" if state == "enabled" else "no ip igmp snooping fast-leave"
    return ["vlan %d" % vlan_id, cmd, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            vlan_id=dict(type="int", required=True),
            state=dict(type="str", choices=["enabled", "disabled"], default="enabled"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["vlan_id"], module.params["state"])
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
