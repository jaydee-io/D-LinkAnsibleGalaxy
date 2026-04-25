#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dgs1250_spanning_tree
short_description: Manage per-interface STP settings on a D-Link DGS-1250 switch
description:
  - Manage per-interface Spanning Tree Protocol settings on D-Link DGS-1250 switches.
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
      - A list of per-interface STP configurations.
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - The interface name (e.g. C(eth1/0/1)).
        type: str
        required: true
      cost:
        description:
          - STP path cost (1-200000000). Use 0 to auto-detect.
        type: int
      port_priority:
        description:
          - STP port priority (0-240, in steps of 16).
        type: int
      portfast:
        description:
          - Enable or disable PortFast (edge port).
        type: bool
      guard_root:
        description:
          - Enable or disable root guard on this interface.
        type: bool
  state:
    description:
      - The desired state of the STP interface configuration.
    type: str
    choices: [merged, replaced, deleted, gathered]
    default: merged
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Configure STP on access ports
  jaydee_io.dlink_dgs1250.dgs1250_spanning_tree:
    config:
      - name: eth1/0/1
        portfast: true
        cost: 20000
      - name: eth1/0/24
        guard_root: true
    state: merged

- name: Gather STP interface config
  jaydee_io.dlink_dgs1250.dgs1250_spanning_tree:
    state: gathered
"""

RETURN = r"""
before:
  description: STP interface configuration before the changes.
  returned: always (except gathered)
  type: list
  elements: dict
after:
  description: STP interface configuration after the changes.
  returned: when changed
  type: list
  elements: dict
gathered:
  description: Current STP interface configuration gathered from the switch.
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
        run_commands, get_running_config, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, get_running_config, MODE_GLOBAL_CONFIG


def _parse_stp_interfaces(config):
    interfaces = {}
    current_iface = None
    for line in config.splitlines():
        m = re.match(r"^interface\s+(eth\S+)", line)
        if m:
            current_iface = m.group(1)
            continue
        if current_iface is None:
            continue
        if line.strip() in ("!", "exit"):
            current_iface = None
            continue
        m = re.match(r"^\s+spanning-tree cost\s+(\d+)", line)
        if m:
            interfaces.setdefault(current_iface, {"name": current_iface})
            interfaces[current_iface]["cost"] = int(m.group(1))
            continue
        m = re.match(r"^\s+spanning-tree port-priority\s+(\d+)", line)
        if m:
            interfaces.setdefault(current_iface, {"name": current_iface})
            interfaces[current_iface]["port_priority"] = int(m.group(1))
            continue
        if re.match(r"^\s+spanning-tree portfast\s*$", line):
            interfaces.setdefault(current_iface, {"name": current_iface})
            interfaces[current_iface]["portfast"] = True
            continue
        if re.match(r"^\s+spanning-tree guard root\s*$", line):
            interfaces.setdefault(current_iface, {"name": current_iface})
            interfaces[current_iface]["guard_root"] = True
            continue
    return sorted(interfaces.values(), key=lambda x: x["name"])


def _gather(module):
    config = get_running_config(module)
    return _parse_stp_interfaces(config)


def _index_by_name(entries):
    return {e["name"]: e for e in entries}


def _build_commands_merged(want, have_idx):
    commands = []
    for entry in want:
        name = entry["name"]
        existing = have_idx.get(name, {})
        iface_cmds = []
        if entry.get("cost") is not None and entry["cost"] != existing.get("cost"):
            iface_cmds.append("spanning-tree cost %d" % entry["cost"])
        if entry.get("port_priority") is not None and entry["port_priority"] != existing.get("port_priority"):
            iface_cmds.append("spanning-tree port-priority %d" % entry["port_priority"])
        if entry.get("portfast") is True and not existing.get("portfast"):
            iface_cmds.append("spanning-tree portfast")
        elif entry.get("portfast") is False and existing.get("portfast"):
            iface_cmds.append("no spanning-tree portfast")
        if entry.get("guard_root") is True and not existing.get("guard_root"):
            iface_cmds.append("spanning-tree guard root")
        elif entry.get("guard_root") is False and existing.get("guard_root"):
            iface_cmds.append("no spanning-tree guard root")
        if iface_cmds:
            commands.append("interface %s" % name)
            commands.extend(iface_cmds)
            commands.append("exit")
    return commands


def _build_commands_replaced(want, have_idx):
    commands = []
    for entry in want:
        name = entry["name"]
        existing = have_idx.get(name, {})
        iface_cmds = []
        if entry.get("cost") is not None and entry["cost"] != existing.get("cost"):
            iface_cmds.append("spanning-tree cost %d" % entry["cost"])
        elif entry.get("cost") is None and existing.get("cost") is not None:
            iface_cmds.append("no spanning-tree cost")
        if entry.get("port_priority") is not None and entry["port_priority"] != existing.get("port_priority"):
            iface_cmds.append("spanning-tree port-priority %d" % entry["port_priority"])
        elif entry.get("port_priority") is None and existing.get("port_priority") is not None:
            iface_cmds.append("no spanning-tree port-priority")
        if entry.get("portfast") is True and not existing.get("portfast"):
            iface_cmds.append("spanning-tree portfast")
        elif not entry.get("portfast") and existing.get("portfast"):
            iface_cmds.append("no spanning-tree portfast")
        if entry.get("guard_root") is True and not existing.get("guard_root"):
            iface_cmds.append("spanning-tree guard root")
        elif not entry.get("guard_root") and existing.get("guard_root"):
            iface_cmds.append("no spanning-tree guard root")
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
        if existing.get("cost") is not None:
            iface_cmds.append("no spanning-tree cost")
        if existing.get("port_priority") is not None:
            iface_cmds.append("no spanning-tree port-priority")
        if existing.get("portfast"):
            iface_cmds.append("no spanning-tree portfast")
        if existing.get("guard_root"):
            iface_cmds.append("no spanning-tree guard root")
        if iface_cmds:
            commands.append("interface %s" % name)
            commands.extend(iface_cmds)
            commands.append("exit")
    return commands


def main():
    element_spec = dict(
        name=dict(type="str", required=True),
        cost=dict(type="int"),
        port_priority=dict(type="int"),
        portfast=dict(type="bool"),
        guard_root=dict(type="bool"),
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
        module.exit_json(changed=False, gathered=_gather(module), commands=[])
        return

    have = _gather(module)
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
        result["after"] = _gather(module)
    elif changed:
        result["after"] = []

    module.exit_json(**result)


if __name__ == "__main__":
    main()
