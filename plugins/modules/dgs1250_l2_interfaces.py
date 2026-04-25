#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dgs1250_l2_interfaces
short_description: Manage Layer 2 interface VLAN settings on a D-Link DGS-1250 switch
description:
  - Manage Layer 2 interface configuration (switchport mode, access VLAN,
    trunk allowed VLANs, trunk native VLAN) on D-Link DGS-1250 switches.
  - Follows the Ansible resource module pattern with C(merged), C(replaced),
    C(deleted), and C(gathered) states.
version_added: "1.6.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  config:
    description:
      - A list of Layer 2 interface configurations.
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - The interface name (e.g. C(eth1/0/1)).
        type: str
        required: true
      mode:
        description:
          - The switchport mode.
        type: str
        choices: [access, trunk, hybrid]
      access:
        description:
          - Access mode settings.
        type: dict
        suboptions:
          vlan_id:
            description:
              - The access VLAN ID.
            type: int
      trunk:
        description:
          - Trunk mode settings.
        type: dict
        suboptions:
          native_vlan:
            description:
              - The native VLAN ID for the trunk.
            type: int
          allowed_vlans:
            description:
              - List of allowed VLAN IDs on the trunk.
            type: list
            elements: int
  state:
    description:
      - The desired state of the interface configuration.
      - C(merged) adds or updates interface settings without removing existing ones.
      - C(replaced) replaces the L2 configuration for each specified interface.
      - C(deleted) resets the specified interfaces to default L2 settings.
      - C(gathered) reads the current L2 interface configuration from the switch.
    type: str
    choices: [merged, replaced, deleted, gathered]
    default: merged
notes:
  - This command runs in Interface/Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Configure access ports
  jaydee_io.dlink_dgs1250.dgs1250_l2_interfaces:
    config:
      - name: eth1/0/1
        mode: access
        access:
          vlan_id: 100
      - name: eth1/0/2
        mode: access
        access:
          vlan_id: 200
    state: merged

- name: Configure trunk port
  jaydee_io.dlink_dgs1250.dgs1250_l2_interfaces:
    config:
      - name: eth1/0/24
        mode: trunk
        trunk:
          native_vlan: 1
          allowed_vlans: [100, 200, 300]
    state: merged

- name: Reset ports to default
  jaydee_io.dlink_dgs1250.dgs1250_l2_interfaces:
    config:
      - name: eth1/0/1
      - name: eth1/0/2
    state: deleted

- name: Gather L2 interface config
  jaydee_io.dlink_dgs1250.dgs1250_l2_interfaces:
    state: gathered
  register: result
"""

RETURN = r"""
before:
  description: L2 interface configuration before the changes.
  returned: always (except gathered)
  type: list
  elements: dict
after:
  description: L2 interface configuration after the changes.
  returned: when changed
  type: list
  elements: dict
gathered:
  description: Current L2 interface configuration gathered from the switch.
  returned: when state is C(gathered)
  type: list
  elements: dict
commands:
  description: List of CLI commands sent to the switch.
  returned: always
  type: list
  elements: str
"""

import re
from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import (
        run_command, run_commands, get_running_config, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import (
        run_command, run_commands, get_running_config, MODE_GLOBAL_CONFIG,
    )


def _parse_l2_interfaces(running_config):
    """Parse running-config to extract per-interface L2 settings."""
    interfaces = {}
    current_iface = None

    for line in running_config.splitlines():
        m = re.match(r"^interface\s+(eth\S+)", line)
        if m:
            current_iface = m.group(1)
            if current_iface not in interfaces:
                interfaces[current_iface] = {
                    "name": current_iface,
                    "mode": "hybrid",
                    "access": {"vlan_id": 1},
                    "trunk": {"native_vlan": 1, "allowed_vlans": []},
                }
            continue

        if current_iface is None:
            continue

        if line.strip() == "!" or line.strip() == "exit":
            current_iface = None
            continue

        entry = interfaces[current_iface]

        m = re.match(r"^\s+switchport mode\s+(access|trunk|hybrid)", line)
        if m:
            entry["mode"] = m.group(1)
            continue

        m = re.match(r"^\s+switchport access vlan\s+(\d+)", line)
        if m:
            entry["access"]["vlan_id"] = int(m.group(1))
            continue

        m = re.match(r"^\s+switchport trunk native vlan\s+(\d+)", line)
        if m:
            entry["trunk"]["native_vlan"] = int(m.group(1))
            continue

        m = re.match(r"^\s+switchport trunk allowed vlan add\s+(.+)", line)
        if m:
            for part in m.group(1).split(","):
                part = part.strip()
                if "-" in part:
                    bounds = part.split("-", 1)
                    entry["trunk"]["allowed_vlans"].extend(
                        range(int(bounds[0]), int(bounds[1]) + 1)
                    )
                else:
                    entry["trunk"]["allowed_vlans"].append(int(part))
            continue

    return sorted(interfaces.values(), key=lambda x: x["name"])


def _gather_l2_interfaces(module):
    config = get_running_config(module)
    return _parse_l2_interfaces(config)


def _index_by_name(iface_list):
    return {i["name"]: i for i in iface_list}


def _build_commands_merged(want, have_idx):
    commands = []
    for entry in want:
        name = entry["name"]
        existing = have_idx.get(name, {
            "mode": "hybrid",
            "access": {"vlan_id": 1},
            "trunk": {"native_vlan": 1, "allowed_vlans": []},
        })
        iface_cmds = []

        want_mode = entry.get("mode")
        if want_mode and want_mode != existing.get("mode"):
            iface_cmds.append("switchport mode %s" % want_mode)

        if entry.get("access"):
            want_vid = entry["access"].get("vlan_id")
            if want_vid and want_vid != existing.get("access", {}).get("vlan_id"):
                iface_cmds.append("switchport access vlan %d" % want_vid)

        if entry.get("trunk"):
            trunk = entry["trunk"]
            if trunk.get("native_vlan") is not None:
                if trunk["native_vlan"] != existing.get("trunk", {}).get("native_vlan"):
                    iface_cmds.append(
                        "switchport trunk native vlan %d" % trunk["native_vlan"]
                    )
            if trunk.get("allowed_vlans"):
                have_allowed = set(existing.get("trunk", {}).get("allowed_vlans", []))
                want_allowed = set(trunk["allowed_vlans"])
                to_add = sorted(want_allowed - have_allowed)
                if to_add:
                    vlan_str = ",".join(str(v) for v in to_add)
                    iface_cmds.append(
                        "switchport trunk allowed vlan add %s" % vlan_str
                    )

        if iface_cmds:
            commands.append("interface %s" % name)
            commands.extend(iface_cmds)
            commands.append("exit")

    return commands


def _build_commands_replaced(want, have_idx):
    commands = []
    for entry in want:
        name = entry["name"]
        existing = have_idx.get(name, {
            "mode": "hybrid",
            "access": {"vlan_id": 1},
            "trunk": {"native_vlan": 1, "allowed_vlans": []},
        })
        iface_cmds = []

        want_mode = entry.get("mode") or "hybrid"
        if want_mode != existing.get("mode", "hybrid"):
            iface_cmds.append("switchport mode %s" % want_mode)

        if want_mode == "access":
            want_vid = (entry.get("access") or {}).get("vlan_id", 1)
            if want_vid != existing.get("access", {}).get("vlan_id", 1):
                iface_cmds.append("switchport access vlan %d" % want_vid)
            have_native = existing.get("trunk", {}).get("native_vlan", 1)
            if have_native != 1:
                iface_cmds.append("no switchport trunk native vlan")
            if existing.get("trunk", {}).get("allowed_vlans"):
                iface_cmds.append("no switchport trunk allowed vlan")

        elif want_mode == "trunk":
            trunk = entry.get("trunk") or {}
            want_native = trunk.get("native_vlan", 1)
            if want_native != existing.get("trunk", {}).get("native_vlan", 1):
                iface_cmds.append(
                    "switchport trunk native vlan %d" % want_native
                )
            want_allowed = set(trunk.get("allowed_vlans") or [])
            have_allowed = set(existing.get("trunk", {}).get("allowed_vlans", []))
            to_remove = sorted(have_allowed - want_allowed)
            to_add = sorted(want_allowed - have_allowed)
            if to_remove:
                vlan_str = ",".join(str(v) for v in to_remove)
                iface_cmds.append(
                    "switchport trunk allowed vlan remove %s" % vlan_str
                )
            if to_add:
                vlan_str = ",".join(str(v) for v in to_add)
                iface_cmds.append(
                    "switchport trunk allowed vlan add %s" % vlan_str
                )
            have_vid = existing.get("access", {}).get("vlan_id", 1)
            if have_vid != 1:
                iface_cmds.append("no switchport access vlan")

        else:
            have_vid = existing.get("access", {}).get("vlan_id", 1)
            if have_vid != 1:
                iface_cmds.append("no switchport access vlan")
            have_native = existing.get("trunk", {}).get("native_vlan", 1)
            if have_native != 1:
                iface_cmds.append("no switchport trunk native vlan")
            if existing.get("trunk", {}).get("allowed_vlans"):
                iface_cmds.append("no switchport trunk allowed vlan")

        if iface_cmds:
            commands.append("interface %s" % name)
            commands.extend(iface_cmds)
            commands.append("exit")

    return commands


def _build_commands_deleted(want, have_idx):
    commands = []
    targets = [e["name"] for e in want] if want else list(have_idx.keys())
    for name in targets:
        existing = have_idx.get(name)
        if existing is None:
            continue
        iface_cmds = []
        if existing.get("mode", "hybrid") != "hybrid":
            iface_cmds.append("no switchport mode")
        if existing.get("access", {}).get("vlan_id", 1) != 1:
            iface_cmds.append("no switchport access vlan")
        if existing.get("trunk", {}).get("native_vlan", 1) != 1:
            iface_cmds.append("no switchport trunk native vlan")
        if existing.get("trunk", {}).get("allowed_vlans"):
            iface_cmds.append("no switchport trunk allowed vlan")
        if iface_cmds:
            commands.append("interface %s" % name)
            commands.extend(iface_cmds)
            commands.append("exit")
    return commands


def main():
    access_spec = dict(
        vlan_id=dict(type="int"),
    )
    trunk_spec = dict(
        native_vlan=dict(type="int"),
        allowed_vlans=dict(type="list", elements="int"),
    )
    element_spec = dict(
        name=dict(type="str", required=True),
        mode=dict(type="str", choices=["access", "trunk", "hybrid"]),
        access=dict(type="dict", options=access_spec),
        trunk=dict(type="dict", options=trunk_spec),
    )

    module = AnsibleModule(
        argument_spec=dict(
            config=dict(type="list", elements="dict", options=element_spec),
            state=dict(
                type="str",
                choices=["merged", "replaced", "deleted", "gathered"],
                default="merged",
            ),
        ),
        supports_check_mode=True,
    )

    state = module.params["state"]
    want = module.params.get("config") or []

    if state == "gathered":
        gathered = _gather_l2_interfaces(module)
        module.exit_json(changed=False, gathered=gathered, commands=[])
        return

    have = _gather_l2_interfaces(module)
    have_idx = _index_by_name(have)

    if state == "merged":
        commands = _build_commands_merged(want, have_idx)
    elif state == "replaced":
        commands = _build_commands_replaced(want, have_idx)
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
        result["after"] = _gather_l2_interfaces(module)
    elif changed:
        result["after"] = []

    module.exit_json(**result)


if __name__ == "__main__":
    main()
