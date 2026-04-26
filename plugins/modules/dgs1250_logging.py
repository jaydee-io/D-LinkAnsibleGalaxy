#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dgs1250_logging
short_description: Manage syslog server configuration on a D-Link DGS-1250 switch
description:
  - Manage syslog server configuration on D-Link DGS-1250 switches.
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
      - A list of syslog server configurations.
    type: list
    elements: dict
    suboptions:
      address:
        description:
          - IP address of the syslog server.
        type: str
        required: true
      severity:
        description:
          - Minimum severity level to log.
        type: str
        choices: [emergencies, alerts, critical, errors, warnings, notifications, informational, debugging]
        default: informational
      facility:
        description:
          - Syslog facility.
        type: str
        choices: [local0, local1, local2, local3, local4, local5, local6, local7]
  state:
    description:
      - The desired state of the syslog server configuration.
    type: str
    choices: [merged, replaced, overridden, deleted, gathered]
    default: merged
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Configure syslog servers
  jaydee_io.dlink_dgs1250.dgs1250_logging:
    config:
      - address: 192.168.1.100
        severity: warnings
      - address: 192.168.1.101
        severity: informational
    state: merged

- name: Gather syslog server config
  jaydee_io.dlink_dgs1250.dgs1250_logging:
    state: gathered
"""

RETURN = r"""
before:
  description: Syslog server configuration before the changes.
  returned: always (except gathered)
  type: list
  elements: dict
after:
  description: Syslog server configuration after the changes.
  returned: when changed
  type: list
  elements: dict
gathered:
  description: Current syslog server configuration gathered from the switch.
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


def _parse_logging_servers(config):
    servers = []
    for line in config.splitlines():
        m = re.match(
            r"^\s*logging server\s+(\S+)"
            r"(?:\s+severity\s+(\S+))?"
            r"(?:\s+facility\s+(\S+))?\s*$",
            line,
        )
        if m:
            servers.append({
                "address": m.group(1),
                "severity": m.group(2) or "informational",
                "facility": m.group(3) or "",
            })
    return servers


def _gather(module):
    config = get_running_config(module)
    return _parse_logging_servers(config)


def _index_by_addr(entries):
    return {e["address"]: e for e in entries}


def _build_server_cmd(entry):
    cmd = "logging server %s" % entry["address"]
    if entry.get("severity"):
        cmd += " severity %s" % entry["severity"]
    if entry.get("facility"):
        cmd += " facility %s" % entry["facility"]
    return cmd


def _normalize(entry):
    return {
        "address": entry["address"],
        "severity": entry.get("severity") or "informational",
        "facility": entry.get("facility") or "",
    }


def _build_commands_merged(want, have_idx):
    commands = []
    for entry in want:
        existing = have_idx.get(entry["address"])
        if existing is None or existing != _normalize(entry):
            commands.append(_build_server_cmd(entry))
    return commands


def _build_commands_replaced(want, have_idx):
    return _build_commands_merged(want, have_idx)


def _build_commands_overridden(want, have_idx):
    commands = []
    want_idx = {e["address"]: e for e in want}
    for addr in sorted(have_idx):
        if addr not in want_idx:
            commands.append("no logging server %s" % addr)
    commands.extend(_build_commands_merged(want, have_idx))
    return commands


def _build_commands_deleted(want, have_idx):
    commands = []
    if not want:
        for addr in sorted(have_idx):
            commands.append("no logging server %s" % addr)
    else:
        for entry in want:
            if entry["address"] in have_idx:
                commands.append("no logging server %s" % entry["address"])
    return commands


def main():
    element_spec = dict(
        address=dict(type="str", required=True),
        severity=dict(
            type="str",
            choices=["emergencies", "alerts", "critical", "errors",
                     "warnings", "notifications", "informational", "debugging"],
            default="informational",
        ),
        facility=dict(
            type="str",
            choices=["local0", "local1", "local2", "local3",
                     "local4", "local5", "local6", "local7"],
        ),
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
    have_idx = _index_by_addr(have)

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

    if module._diff and commands:
        result['diff'] = {'prepared': '\n'.join(commands) + '\n'}

    module.exit_json(**result)


if __name__ == "__main__":
    main()
