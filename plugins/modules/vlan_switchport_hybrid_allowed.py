#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: vlan_switchport_hybrid_allowed
short_description: Configure hybrid port allowed VLANs on a D-Link DGS-1250 switch
description:
  - Configures the C(switchport hybrid allowed vlan) CLI command on a D-Link DGS-1250 switch.
  - Specifies tagged or untagged VLANs for a hybrid port.
  - Corresponds to CLI command described in chapter 70-5 of the DGS-1250 CLI Reference Guide.
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
  action:
    description:
      - C(add) to add VLANs, C(remove) to remove VLANs, C(set) to overwrite.
    type: str
    choices: [add, remove, set]
    default: add
  tagging:
    description:
      - C(tagged) or C(untagged) membership. Required when action is C(add) or C(set).
    type: str
    choices: [tagged, untagged]
  vlan_id:
    description:
      - VLAN ID or range (e.g. C(1000), C(2000,3000)).
    type: str
    required: true
  state:
    description:
      - C(present) to configure, C(absent) to revert to default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Add tagged VLAN 1000 to hybrid port
  jaydee_io.dlink_dgs1250.vlan_switchport_hybrid_allowed:
    interface: eth1/0/1
    action: add
    tagging: tagged
    vlan_id: "1000"

- name: Add untagged VLANs 2000,3000
  jaydee_io.dlink_dgs1250.vlan_switchport_hybrid_allowed:
    interface: eth1/0/1
    action: add
    tagging: untagged
    vlan_id: "2000,3000"

- name: Revert to default
  jaydee_io.dlink_dgs1250.vlan_switchport_hybrid_allowed:
    interface: eth1/0/1
    vlan_id: "1000"
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


def _build_commands(interface, action, tagging, vlan_id, state):
    if state == "absent":
        cmd = "no switchport hybrid allowed vlan"
    elif action == "remove":
        cmd = "switchport hybrid allowed vlan remove %s" % vlan_id
    elif action == "add":
        cmd = "switchport hybrid allowed vlan add %s %s" % (tagging, vlan_id)
    else:
        cmd = "switchport hybrid allowed vlan %s %s" % (tagging, vlan_id)
    return ["interface %s" % interface, cmd, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            action=dict(type="str", choices=[
                        "add", "remove", "set"], default="add"),
            tagging=dict(type="str", choices=["tagged", "untagged"]),
            vlan_id=dict(type="str", required=True),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["interface"], module.params["action"],
                               module.params["tagging"], module.params["vlan_id"], module.params["state"])
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
