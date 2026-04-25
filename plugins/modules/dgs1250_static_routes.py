#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dgs1250_static_routes
short_description: Manage static routes on a D-Link DGS-1250 switch
description:
  - Manage IPv4 static route configuration on D-Link DGS-1250 switches.
  - Follows the Ansible resource module pattern with C(merged),
    C(overridden), C(deleted), and C(gathered) states.
version_added: "1.6.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  config:
    description:
      - A list of static route configurations.
    type: list
    elements: dict
    suboptions:
      prefix:
        description:
          - Destination network prefix (e.g. C(10.0.0.0)).
        type: str
        required: true
      mask:
        description:
          - Subnet mask (e.g. C(255.255.255.0)).
        type: str
        required: true
      next_hop:
        description:
          - Next hop IP address.
        type: str
        required: true
      metric:
        description:
          - Route metric (distance).
        type: int
  state:
    description:
      - The desired state of the static route configuration.
    type: str
    choices: [merged, overridden, deleted, gathered]
    default: merged
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Configure static routes
  jaydee_io.dlink_dgs1250.dgs1250_static_routes:
    config:
      - prefix: 10.0.0.0
        mask: 255.255.255.0
        next_hop: 192.168.1.1
      - prefix: 172.16.0.0
        mask: 255.255.0.0
        next_hop: 192.168.1.1
        metric: 10
    state: merged

- name: Delete all static routes
  jaydee_io.dlink_dgs1250.dgs1250_static_routes:
    state: deleted

- name: Gather static route config
  jaydee_io.dlink_dgs1250.dgs1250_static_routes:
    state: gathered
"""

RETURN = r"""
before:
  description: Static route configuration before the changes.
  returned: always (except gathered)
  type: list
  elements: dict
after:
  description: Static route configuration after the changes.
  returned: when changed
  type: list
  elements: dict
gathered:
  description: Current static route configuration gathered from the switch.
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


def _parse_static_routes(config):
    routes = []
    for line in config.splitlines():
        m = re.match(
            r"^\s*ip route\s+(\S+)\s+(\S+)\s+(\S+)(?:\s+(\d+))?\s*$",
            line,
        )
        if m:
            entry = {
                "prefix": m.group(1),
                "mask": m.group(2),
                "next_hop": m.group(3),
            }
            if m.group(4):
                entry["metric"] = int(m.group(4))
            routes.append(entry)
    return routes


def _gather(module):
    config = get_running_config(module)
    return _parse_static_routes(config)


def _route_key(entry):
    return (entry["prefix"], entry["mask"], entry["next_hop"])


def _index_by_key(entries):
    return {_route_key(e): e for e in entries}


def _build_route_cmd(entry):
    cmd = "ip route %s %s %s" % (entry["prefix"], entry["mask"], entry["next_hop"])
    if entry.get("metric") is not None:
        cmd += " %d" % entry["metric"]
    return cmd


def _build_commands_merged(want, have_idx):
    commands = []
    for entry in want:
        key = _route_key(entry)
        existing = have_idx.get(key)
        if existing is None:
            commands.append(_build_route_cmd(entry))
        elif entry.get("metric") is not None and existing.get("metric") != entry["metric"]:
            commands.append("no ip route %s %s %s" % key)
            commands.append(_build_route_cmd(entry))
    return commands


def _build_commands_overridden(want, have_idx):
    commands = []
    want_idx = _index_by_key(want)
    for key in sorted(have_idx):
        if key not in want_idx:
            commands.append("no ip route %s %s %s" % key)
    commands.extend(_build_commands_merged(want, have_idx))
    return commands


def _build_commands_deleted(want, have_idx):
    commands = []
    if not want:
        for key in sorted(have_idx):
            commands.append("no ip route %s %s %s" % key)
    else:
        for entry in want:
            key = _route_key(entry)
            if key in have_idx:
                commands.append("no ip route %s %s %s" % key)
    return commands


def main():
    element_spec = dict(
        prefix=dict(type="str", required=True),
        mask=dict(type="str", required=True),
        next_hop=dict(type="str", required=True),
        metric=dict(type="int"),
    )

    module = AnsibleModule(
        argument_spec=dict(
            config=dict(type="list", elements="dict", options=element_spec),
            state=dict(
                type="str",
                choices=["merged", "overridden", "deleted", "gathered"],
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
    have_idx = _index_by_key(have)

    if state == "merged":
        commands = _build_commands_merged(want, have_idx)
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
        result["after"] = _gather(module)
    elif changed:
        result["after"] = []

    module.exit_json(**result)


if __name__ == "__main__":
    main()
