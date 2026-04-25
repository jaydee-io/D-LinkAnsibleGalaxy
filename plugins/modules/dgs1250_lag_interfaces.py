#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dgs1250_lag_interfaces
short_description: Manage LAG (port-channel) interfaces on a D-Link DGS-1250 switch
description:
  - Manage Link Aggregation Group member configuration on D-Link DGS-1250 switches.
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
      - A list of LAG member configurations.
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - The member interface name (e.g. C(eth1/0/1)).
        type: str
        required: true
      channel_group:
        description:
          - The port-channel group number (1-8).
        type: int
      mode:
        description:
          - LAG mode.
        type: str
        choices: ['on', active, passive]
  state:
    description:
      - The desired state of the LAG configuration.
    type: str
    choices: [merged, replaced, deleted, gathered]
    default: merged
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Configure LAG members
  jaydee_io.dlink_dgs1250.dgs1250_lag_interfaces:
    config:
      - name: eth1/0/1
        channel_group: 1
        mode: active
      - name: eth1/0/2
        channel_group: 1
        mode: active
    state: merged

- name: Remove LAG membership
  jaydee_io.dlink_dgs1250.dgs1250_lag_interfaces:
    config:
      - name: eth1/0/1
    state: deleted

- name: Gather LAG config
  jaydee_io.dlink_dgs1250.dgs1250_lag_interfaces:
    state: gathered
"""

RETURN = r"""
before:
  description: LAG configuration before the changes.
  returned: always (except gathered)
  type: list
  elements: dict
after:
  description: LAG configuration after the changes.
  returned: when changed
  type: list
  elements: dict
gathered:
  description: Current LAG configuration gathered from the switch.
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


def _parse_lag_interfaces(config):
    members = []
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
        m = re.match(r"^\s+channel-group\s+(\d+)\s+mode\s+(on|active|passive)", line)
        if m:
            members.append({
                "name": current_iface,
                "channel_group": int(m.group(1)),
                "mode": m.group(2),
            })
    return sorted(members, key=lambda x: x["name"])


def _gather(module):
    config = get_running_config(module)
    return _parse_lag_interfaces(config)


def _index_by_name(entries):
    return {e["name"]: e for e in entries}


def _build_commands_merged(want, have_idx):
    commands = []
    for entry in want:
        name = entry["name"]
        existing = have_idx.get(name)
        if existing is None or existing.get("channel_group") != entry.get("channel_group") or existing.get("mode") != entry.get("mode"):
            if entry.get("channel_group") and entry.get("mode"):
                commands.append("interface %s" % name)
                commands.append("channel-group %d mode %s" % (entry["channel_group"], entry["mode"]))
                commands.append("exit")
    return commands


def _build_commands_replaced(want, have_idx):
    return _build_commands_merged(want, have_idx)


def _build_commands_deleted(want, have_idx):
    commands = []
    targets = [e["name"] for e in want] if want else list(have_idx.keys())
    for name in targets:
        if name in have_idx:
            commands.append("interface %s" % name)
            commands.append("no channel-group")
            commands.append("exit")
    return commands


def main():
    element_spec = dict(
        name=dict(type="str", required=True),
        channel_group=dict(type="int"),
        mode=dict(type="str", choices=["on", "active", "passive"]),
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
