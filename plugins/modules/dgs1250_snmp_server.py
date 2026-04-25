#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dgs1250_snmp_server
short_description: Manage SNMP community strings on a D-Link DGS-1250 switch
description:
  - Manage SNMP community string configuration on D-Link DGS-1250 switches.
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
      - A list of SNMP community configurations.
    type: list
    elements: dict
    suboptions:
      community:
        description:
          - The community string name.
        type: str
        required: true
      access_type:
        description:
          - Read-only or read-write access.
        type: str
        choices: [ro, rw]
        default: ro
      view:
        description:
          - MIB view name associated with the community.
        type: str
  state:
    description:
      - The desired state of the SNMP community configuration.
    type: str
    choices: [merged, replaced, overridden, deleted, gathered]
    default: merged
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Configure SNMP communities
  jaydee_io.dlink_dgs1250.dgs1250_snmp_server:
    config:
      - community: public
        access_type: ro
      - community: private
        access_type: rw
    state: merged

- name: Gather SNMP community config
  jaydee_io.dlink_dgs1250.dgs1250_snmp_server:
    state: gathered
"""

RETURN = r"""
before:
  description: SNMP community configuration before the changes.
  returned: always (except gathered)
  type: list
  elements: dict
after:
  description: SNMP community configuration after the changes.
  returned: when changed
  type: list
  elements: dict
gathered:
  description: Current SNMP community configuration gathered from the switch.
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


def _parse_snmp_communities(config):
    communities = []
    for line in config.splitlines():
        m = re.match(
            r"^\s*snmp-server community\s+(\S+)"
            r"(?:\s+view\s+(\S+))?"
            r"(?:\s+(ro|rw))?\s*$",
            line,
        )
        if m:
            communities.append({
                "community": m.group(1),
                "view": m.group(2) or "",
                "access_type": m.group(3) or "ro",
            })
    return communities


def _gather(module):
    config = get_running_config(module)
    return _parse_snmp_communities(config)


def _index_by_name(entries):
    return {e["community"]: e for e in entries}


def _build_community_cmd(entry):
    cmd = "snmp-server community %s" % entry["community"]
    if entry.get("view"):
        cmd += " view %s" % entry["view"]
    cmd += " %s" % entry.get("access_type", "ro")
    return cmd


def _build_commands_merged(want, have_idx):
    commands = []
    for entry in want:
        name = entry["community"]
        existing = have_idx.get(name)
        if existing is None or existing != _normalize(entry):
            commands.append(_build_community_cmd(entry))
    return commands


def _build_commands_replaced(want, have_idx):
    return _build_commands_merged(want, have_idx)


def _build_commands_overridden(want, have_idx):
    commands = []
    want_idx = {e["community"]: e for e in want}
    for name in sorted(have_idx):
        if name not in want_idx:
            commands.append("no snmp-server community %s" % name)
    commands.extend(_build_commands_merged(want, have_idx))
    return commands


def _build_commands_deleted(want, have_idx):
    commands = []
    if not want:
        for name in sorted(have_idx):
            commands.append("no snmp-server community %s" % name)
    else:
        for entry in want:
            if entry["community"] in have_idx:
                commands.append(
                    "no snmp-server community %s" % entry["community"]
                )
    return commands


def _normalize(entry):
    return {
        "community": entry["community"],
        "view": entry.get("view") or "",
        "access_type": entry.get("access_type") or "ro",
    }


def main():
    element_spec = dict(
        community=dict(type="str", required=True),
        access_type=dict(type="str", choices=["ro", "rw"], default="ro"),
        view=dict(type="str"),
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
        module.exit_json(changed=False, gathered=_gather(module), commands=[])
        return

    have = _gather(module)
    have_idx = _index_by_name(have)

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
        result["after"] = _gather(module)
    elif changed:
        result["after"] = []

    module.exit_json(**result)


if __name__ == "__main__":
    main()
