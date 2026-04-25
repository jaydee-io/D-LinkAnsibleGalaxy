#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dgs1250_storm_control
short_description: Manage per-interface storm control on a D-Link DGS-1250 switch
description:
  - Manage storm control configuration per interface on D-Link DGS-1250 switches.
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
      - A list of per-interface storm control configurations.
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - The interface name (e.g. C(eth1/0/1)).
        type: str
        required: true
      broadcast:
        description:
          - Broadcast storm control level (percent).
        type: int
      multicast:
        description:
          - Multicast storm control level (percent).
        type: int
      unicast:
        description:
          - Unknown unicast storm control level (percent).
        type: int
      action:
        description:
          - Action when storm detected.
        type: str
        choices: [shutdown, drop, none]
  state:
    description:
      - The desired state of the storm control configuration.
    type: str
    choices: [merged, replaced, deleted, gathered]
    default: merged
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Configure storm control
  jaydee_io.dlink_dgs1250.dgs1250_storm_control:
    config:
      - name: eth1/0/1
        broadcast: 80
        multicast: 80
        action: shutdown
    state: merged

- name: Gather storm control config
  jaydee_io.dlink_dgs1250.dgs1250_storm_control:
    state: gathered
"""

RETURN = r"""
before:
  description: Storm control configuration before the changes.
  returned: always (except gathered)
  type: list
  elements: dict
after:
  description: Storm control configuration after the changes.
  returned: when changed
  type: list
  elements: dict
gathered:
  description: Current storm control configuration gathered from the switch.
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


def _parse_storm_control(config):
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
        m = re.match(r"^\s+storm-control\s+(broadcast|multicast|unicast)\s+level\s+(\d+)", line)
        if m:
            if current_iface not in interfaces:
                interfaces[current_iface] = {"name": current_iface}
            interfaces[current_iface][m.group(1)] = int(m.group(2))
            continue
        m = re.match(r"^\s+storm-control\s+action\s+(shutdown|drop|none)", line)
        if m:
            if current_iface not in interfaces:
                interfaces[current_iface] = {"name": current_iface}
            interfaces[current_iface]["action"] = m.group(1)
    return sorted(interfaces.values(), key=lambda x: x["name"])


def _gather(module):
    config = get_running_config(module)
    return _parse_storm_control(config)


def _index_by_name(entries):
    return {e["name"]: e for e in entries}


def _build_commands_merged(want, have_idx):
    commands = []
    for entry in want:
        name = entry["name"]
        existing = have_idx.get(name, {})
        iface_cmds = []
        for traffic in ("broadcast", "multicast", "unicast"):
            if entry.get(traffic) is not None and entry[traffic] != existing.get(traffic):
                iface_cmds.append("storm-control %s level %d" % (traffic, entry[traffic]))
        if entry.get("action") and entry["action"] != existing.get("action"):
            iface_cmds.append("storm-control action %s" % entry["action"])
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
        for traffic in ("broadcast", "multicast", "unicast"):
            if entry.get(traffic) is not None and entry[traffic] != existing.get(traffic):
                iface_cmds.append("storm-control %s level %d" % (traffic, entry[traffic]))
            elif entry.get(traffic) is None and existing.get(traffic) is not None:
                iface_cmds.append("no storm-control %s" % traffic)
        if entry.get("action") and entry["action"] != existing.get("action"):
            iface_cmds.append("storm-control action %s" % entry["action"])
        elif entry.get("action") is None and existing.get("action") is not None:
            iface_cmds.append("no storm-control action")
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
        for traffic in ("broadcast", "multicast", "unicast"):
            if existing.get(traffic) is not None:
                iface_cmds.append("no storm-control %s" % traffic)
        if existing.get("action") is not None:
            iface_cmds.append("no storm-control action")
        if iface_cmds:
            commands.append("interface %s" % name)
            commands.extend(iface_cmds)
            commands.append("exit")
    return commands


def main():
    element_spec = dict(
        name=dict(type="str", required=True),
        broadcast=dict(type="int"),
        multicast=dict(type="int"),
        unicast=dict(type="int"),
        action=dict(type="str", choices=["shutdown", "drop", "none"]),
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
