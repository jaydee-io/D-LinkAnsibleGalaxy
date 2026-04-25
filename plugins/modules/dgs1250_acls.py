#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dgs1250_acls
short_description: Manage IP access-lists on a D-Link DGS-1250 switch
description:
  - Manage IP access-list configuration on D-Link DGS-1250 switches.
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
      - A list of IP access-list configurations.
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - The access-list name.
        type: str
        required: true
      rules:
        description:
          - Ordered list of ACL rules.
        type: list
        elements: dict
        suboptions:
          action:
            description:
              - Permit or deny.
            type: str
            choices: [permit, deny]
            required: true
          source:
            description:
              - Source address (e.g. C(any), C(host 10.0.0.1), C(10.0.0.0 0.0.0.255)).
            type: str
            required: true
          destination:
            description:
              - Destination address (same format as source).
            type: str
            default: any
  state:
    description:
      - The desired state of the ACL configuration.
    type: str
    choices: [merged, replaced, overridden, deleted, gathered]
    default: merged
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Configure ACLs
  jaydee_io.dlink_dgs1250.dgs1250_acls:
    config:
      - name: mgmt-acl
        rules:
          - action: permit
            source: "10.0.0.0 0.0.0.255"
          - action: deny
            source: any
    state: merged

- name: Delete an ACL
  jaydee_io.dlink_dgs1250.dgs1250_acls:
    config:
      - name: mgmt-acl
    state: deleted

- name: Gather ACL config
  jaydee_io.dlink_dgs1250.dgs1250_acls:
    state: gathered
"""

RETURN = r"""
before:
  description: ACL configuration before the changes.
  returned: always (except gathered)
  type: list
  elements: dict
after:
  description: ACL configuration after the changes.
  returned: when changed
  type: list
  elements: dict
gathered:
  description: Current ACL configuration gathered from the switch.
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


def _parse_acls(config):
    acls = []
    current = None
    for line in config.splitlines():
        m = re.match(r"^ip access-list extended\s+(\S+)\s*$", line)
        if m:
            if current is not None:
                acls.append(current)
            current = {"name": m.group(1), "rules": []}
            continue
        if current is None:
            continue
        if line.strip() in ("!", "exit"):
            acls.append(current)
            current = None
            continue
        m = re.match(r"^\s+(permit|deny)\s+(.+)$", line)
        if m:
            parts = m.group(2).strip().split()
            source = parts[0] if parts else "any"
            if len(parts) > 1 and parts[0] not in ("any", "host"):
                source = "%s %s" % (parts[0], parts[1])
                dest_parts = parts[2:]
            elif len(parts) > 1 and parts[0] == "host":
                source = "host %s" % parts[1]
                dest_parts = parts[2:]
            else:
                dest_parts = parts[1:]

            destination = "any"
            if dest_parts:
                if dest_parts[0] == "host" and len(dest_parts) > 1:
                    destination = "host %s" % dest_parts[1]
                elif dest_parts[0] != "any" and len(dest_parts) > 1:
                    destination = "%s %s" % (dest_parts[0], dest_parts[1])
                elif dest_parts[0] == "any":
                    destination = "any"
                else:
                    destination = dest_parts[0]

            current["rules"].append({
                "action": m.group(1),
                "source": source,
                "destination": destination,
            })
    if current is not None:
        acls.append(current)
    return acls


def _gather(module):
    config = get_running_config(module)
    return _parse_acls(config)


def _index_by_name(entries):
    return {e["name"]: e for e in entries}


def _build_acl_commands(entry):
    commands = ["ip access-list extended %s" % entry["name"]]
    for rule in entry.get("rules") or []:
        cmd = "%s %s" % (rule["action"], rule["source"])
        if rule.get("destination") and rule["destination"] != "any":
            cmd += " %s" % rule["destination"]
        commands.append(cmd)
    commands.append("exit")
    return commands


def _build_commands_merged(want, have_idx):
    commands = []
    for entry in want:
        name = entry["name"]
        existing = have_idx.get(name)
        if existing is None:
            commands.extend(_build_acl_commands(entry))
        elif entry.get("rules") and entry["rules"] != existing.get("rules", []):
            commands.append("no ip access-list extended %s" % name)
            commands.extend(_build_acl_commands(entry))
    return commands


def _build_commands_replaced(want, have_idx):
    return _build_commands_merged(want, have_idx)


def _build_commands_overridden(want, have_idx):
    commands = []
    want_idx = {e["name"]: e for e in want}
    for name in sorted(have_idx):
        if name not in want_idx:
            commands.append("no ip access-list extended %s" % name)
    commands.extend(_build_commands_merged(want, have_idx))
    return commands


def _build_commands_deleted(want, have_idx):
    commands = []
    if not want:
        for name in sorted(have_idx):
            commands.append("no ip access-list extended %s" % name)
    else:
        for entry in want:
            if entry["name"] in have_idx:
                commands.append("no ip access-list extended %s" % entry["name"])
    return commands


def main():
    rule_spec = dict(
        action=dict(type="str", choices=["permit", "deny"], required=True),
        source=dict(type="str", required=True),
        destination=dict(type="str", default="any"),
    )

    element_spec = dict(
        name=dict(type="str", required=True),
        rules=dict(type="list", elements="dict", options=rule_spec),
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
