#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dgs1250_lldp_interfaces
short_description: Manage per-interface LLDP settings on a D-Link DGS-1250 switch
description:
  - Manage per-interface LLDP transmit/receive configuration on D-Link DGS-1250 switches.
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
      - A list of per-interface LLDP configurations.
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - The interface name (e.g. C(eth1/0/1)).
        type: str
        required: true
      transmit:
        description:
          - Enable or disable LLDP transmit on this interface.
        type: bool
      receive:
        description:
          - Enable or disable LLDP receive on this interface.
        type: bool
  state:
    description:
      - The desired state of the LLDP interface configuration.
    type: str
    choices: [merged, replaced, deleted, gathered]
    default: merged
notes:
  - This command runs in Interface Configuration Mode.
  - By default LLDP transmit and receive are enabled on all interfaces.
"""

EXAMPLES = r"""
- name: Disable LLDP on access ports
  jaydee_io.dlink_dgs1250.dgs1250_lldp_interfaces:
    config:
      - name: eth1/0/1
        transmit: false
        receive: false
    state: merged

- name: Reset LLDP to defaults
  jaydee_io.dlink_dgs1250.dgs1250_lldp_interfaces:
    config:
      - name: eth1/0/1
    state: deleted

- name: Gather LLDP interface config
  jaydee_io.dlink_dgs1250.dgs1250_lldp_interfaces:
    state: gathered
"""

RETURN = r"""
before:
  description: LLDP interface configuration before the changes.
  returned: always (except gathered)
  type: list
  elements: dict
after:
  description: LLDP interface configuration after the changes.
  returned: when changed
  type: list
  elements: dict
gathered:
  description: Current LLDP interface configuration gathered from the switch.
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


def _parse_lldp_interfaces(config):
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
        if re.match(r"^\s+no lldp transmit\s*$", line):
            interfaces.setdefault(current_iface, {"name": current_iface, "transmit": True, "receive": True})
            interfaces[current_iface]["transmit"] = False
            continue
        if re.match(r"^\s+no lldp receive\s*$", line):
            interfaces.setdefault(current_iface, {"name": current_iface, "transmit": True, "receive": True})
            interfaces[current_iface]["receive"] = False
            continue
    return sorted(interfaces.values(), key=lambda x: x["name"])


def _gather(module):
    config = get_running_config(module)
    return _parse_lldp_interfaces(config)


def _index_by_name(entries):
    return {e["name"]: e for e in entries}


def _build_commands_merged(want, have_idx):
    commands = []
    for entry in want:
        name = entry["name"]
        existing = have_idx.get(name, {"transmit": True, "receive": True})
        iface_cmds = []
        if entry.get("transmit") is False and existing.get("transmit") is True:
            iface_cmds.append("no lldp transmit")
        elif entry.get("transmit") is True and existing.get("transmit") is False:
            iface_cmds.append("lldp transmit")
        if entry.get("receive") is False and existing.get("receive") is True:
            iface_cmds.append("no lldp receive")
        elif entry.get("receive") is True and existing.get("receive") is False:
            iface_cmds.append("lldp receive")
        if iface_cmds:
            commands.append("interface %s" % name)
            commands.extend(iface_cmds)
            commands.append("exit")
    return commands


def _build_commands_replaced(want, have_idx):
    return _build_commands_merged(want, have_idx)


def _build_commands_deleted(want, have_idx):
    commands = []
    targets = [e["name"] for e in want] if want else list(have_idx.keys())
    for name in targets:
        existing = have_idx.get(name)
        if existing is None:
            continue
        iface_cmds = []
        if existing.get("transmit") is False:
            iface_cmds.append("lldp transmit")
        if existing.get("receive") is False:
            iface_cmds.append("lldp receive")
        if iface_cmds:
            commands.append("interface %s" % name)
            commands.extend(iface_cmds)
            commands.append("exit")
    return commands


def main():
    element_spec = dict(
        name=dict(type="str", required=True),
        transmit=dict(type="bool"),
        receive=dict(type="bool"),
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

    if module._diff and commands:
        result['diff'] = {'prepared': '\n'.join(commands) + '\n'}

    module.exit_json(**result)


if __name__ == "__main__":
    main()
