#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dgs1250_vlans
short_description: Manage VLANs on a D-Link DGS-1250 switch using the resource module pattern
description:
  - Manage VLAN configuration on D-Link DGS-1250 switches.
  - Follows the Ansible resource module pattern with C(merged), C(replaced),
    C(overridden), C(deleted), and C(gathered) states.
version_added: "1.6.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  config:
    description:
      - A list of VLAN configurations.
    type: list
    elements: dict
    suboptions:
      vlan_id:
        description:
          - The VLAN ID (1-4094).
        type: int
        required: true
      name:
        description:
          - The VLAN name (max 32 characters).
        type: str
  state:
    description:
      - The desired state of the VLAN configuration.
      - C(merged) adds or updates VLANs without removing existing ones.
      - C(replaced) replaces the configuration of each specified VLAN.
      - C(overridden) overrides the entire VLAN configuration
        (removes VLANs not in the provided list, except VLAN 1).
      - C(deleted) removes the specified VLANs (or all non-default VLANs if no config given).
      - C(gathered) reads the current VLAN configuration from the switch.
    type: str
    choices: [merged, replaced, overridden, deleted, gathered]
    default: merged
notes:
  - VLAN 1 is the default VLAN and cannot be deleted or overridden.
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Create VLANs (merged)
  jaydee_io.dlink_dgs1250.dgs1250_vlans:
    config:
      - vlan_id: 100
        name: management
      - vlan_id: 200
        name: servers
    state: merged

- name: Replace VLAN 100 config (reset name if different)
  jaydee_io.dlink_dgs1250.dgs1250_vlans:
    config:
      - vlan_id: 100
        name: mgmt
    state: replaced

- name: Override all VLANs (remove any not listed, except VLAN 1)
  jaydee_io.dlink_dgs1250.dgs1250_vlans:
    config:
      - vlan_id: 100
        name: management
    state: overridden

- name: Delete specific VLANs
  jaydee_io.dlink_dgs1250.dgs1250_vlans:
    config:
      - vlan_id: 200
    state: deleted

- name: Delete all non-default VLANs
  jaydee_io.dlink_dgs1250.dgs1250_vlans:
    state: deleted

- name: Gather current VLAN config
  jaydee_io.dlink_dgs1250.dgs1250_vlans:
    state: gathered
  register: result
"""

RETURN = r"""
before:
  description: VLAN configuration before the changes.
  returned: always (except gathered)
  type: list
  elements: dict
after:
  description: VLAN configuration after the changes.
  returned: when changed
  type: list
  elements: dict
gathered:
  description: Current VLAN configuration gathered from the switch.
  returned: when state is C(gathered)
  type: list
  elements: dict
commands:
  description: List of CLI commands sent to the switch.
  returned: always
  type: list
  elements: str
"""

from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import (
        run_command, run_commands, MODE_GLOBAL_CONFIG,
    )
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250_parsers import (
        parse_vlans,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command, run_commands, MODE_GLOBAL_CONFIG
    from dgs1250_parsers import parse_vlans


DEFAULT_VLAN_ID = 1


def _gather_vlans(module):
    raw = run_command(module, "show vlan")
    parsed = parse_vlans(raw)
    return [{"vlan_id": v["vlan_id"], "name": v["name"]} for v in parsed]


def _index_by_id(vlan_list):
    return {v["vlan_id"]: v for v in vlan_list}


def _build_commands_merged(want, have_idx):
    commands = []
    for entry in want:
        vid = entry["vlan_id"]
        existing = have_idx.get(vid)
        if existing is None:
            commands.append("vlan %d" % vid)
            if entry.get("name"):
                commands.append("name %s" % entry["name"])
            commands.append("exit")
        else:
            if entry.get("name") and entry["name"] != existing.get("name", ""):
                commands.append("vlan %d" % vid)
                commands.append("name %s" % entry["name"])
                commands.append("exit")
    return commands


def _build_commands_replaced(want, have_idx):
    commands = []
    for entry in want:
        vid = entry["vlan_id"]
        existing = have_idx.get(vid)
        if existing is None:
            commands.append("vlan %d" % vid)
            if entry.get("name"):
                commands.append("name %s" % entry["name"])
            commands.append("exit")
        else:
            want_name = entry.get("name") or ""
            have_name = existing.get("name", "")
            if want_name != have_name:
                commands.append("vlan %d" % vid)
                if want_name:
                    commands.append("name %s" % want_name)
                else:
                    commands.append("no name")
                commands.append("exit")
    return commands


def _build_commands_overridden(want, have_idx):
    commands = []
    want_idx = _index_by_id(want)
    for vid in sorted(have_idx):
        if vid == DEFAULT_VLAN_ID:
            continue
        if vid not in want_idx:
            commands.append("no vlan %d" % vid)
    commands.extend(_build_commands_replaced(want, have_idx))
    return commands


def _build_commands_deleted(want, have_idx):
    commands = []
    if not want:
        for vid in sorted(have_idx):
            if vid == DEFAULT_VLAN_ID:
                continue
            commands.append("no vlan %d" % vid)
    else:
        for entry in want:
            vid = entry["vlan_id"]
            if vid == DEFAULT_VLAN_ID:
                continue
            if vid in have_idx:
                commands.append("no vlan %d" % vid)
    return commands


def main():
    element_spec = dict(
        vlan_id=dict(type="int", required=True),
        name=dict(type="str"),
    )

    module = AnsibleModule(
        argument_spec=dict(
            config=dict(type="list", elements="dict", options=element_spec),
            state=dict(
                type="str",
                choices=["merged", "replaced", "overridden", "deleted", "gathered"],
                default="merged",
            ),
        ),
        supports_check_mode=True,
    )

    state = module.params["state"]
    want = module.params.get("config") or []

    if state == "gathered":
        gathered = _gather_vlans(module)
        module.exit_json(changed=False, gathered=gathered, commands=[])
        return

    have = _gather_vlans(module)
    have_idx = _index_by_id(have)

    if state == "merged":
        commands = _build_commands_merged(want, have_idx)
    elif state == "replaced":
        commands = _build_commands_replaced(want, have_idx)
    elif state == "overridden":
        commands = _build_commands_overridden(want, have_idx)
    elif state == "deleted":
        commands = _build_commands_deleted(want, have_idx)
    else:
        commands = []

    changed = len(commands) > 0
    result = dict(changed=changed, before=have, commands=commands)

    if changed and not module.check_mode:
        try:
            run_commands(module, commands, mode=MODE_GLOBAL_CONFIG)
        except Exception as e:
            module.fail_json(msg="Command failed: %s" % str(e))
        result["after"] = _gather_vlans(module)

    if module._diff and commands:
        result['diff'] = {'prepared': '\n'.join(commands) + '\n'}

    module.exit_json(**result)


if __name__ == "__main__":
    main()
