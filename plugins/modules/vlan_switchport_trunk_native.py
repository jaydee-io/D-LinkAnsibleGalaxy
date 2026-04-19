#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: vlan_switchport_trunk_native
short_description: Configure trunk port native VLAN on a D-Link DGS-1250 switch
description:
  - Configures the C(switchport trunk native vlan) CLI command on a D-Link DGS-1250 switch.
  - Sets the native VLAN ID or tagging mode of a trunk port.
  - Corresponds to CLI command described in chapter 70-9 of the DGS-1250 CLI Reference Guide.
version_added: "0.19.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - The interface to configure (e.g. C(eth1/0/1)).
    type: str
    required: true
  vlan_id:
    description:
      - The native VLAN ID.
    type: int
  tag:
    description:
      - Enable tagging mode for the native VLAN.
    type: bool
    default: false
  state:
    description:
      - C(present) to set, C(absent) to revert to default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Set trunk native VLAN to 20
  jaydee_io.dlink_dgs1250.vlan_switchport_trunk_native:
    interface: eth1/0/1
    vlan_id: 20

- name: Enable native VLAN tagging
  jaydee_io.dlink_dgs1250.vlan_switchport_trunk_native:
    interface: eth1/0/1
    tag: true

- name: Revert to default
  jaydee_io.dlink_dgs1250.vlan_switchport_trunk_native:
    interface: eth1/0/1
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


def _build_commands(interface, vlan_id, tag, state):
    if state == "absent":
        cmd = "no switchport trunk native vlan"
    elif tag:
        cmd = "switchport trunk native vlan tag"
    else:
        cmd = "switchport trunk native vlan %d" % vlan_id
    return ["interface %s" % interface, cmd, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            vlan_id=dict(type="int"),
            tag=dict(type="bool", default=False),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["interface"], module.params["vlan_id"], module.params["tag"], module.params["state"])
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
