#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dgs1250_ntp
short_description: Manage SNTP server configuration on a D-Link DGS-1250 switch
description:
  - Manage SNTP server configuration on D-Link DGS-1250 switches.
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
      - A list of SNTP server configurations.
    type: list
    elements: dict
    suboptions:
      address:
        description:
          - IP address or hostname of the SNTP server.
        type: str
        required: true
  state:
    description:
      - The desired state of the SNTP server configuration.
    type: str
    choices: [merged, overridden, deleted, gathered]
    default: merged
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Configure SNTP servers
  jaydee_io.dlink_dgs1250.dgs1250_ntp:
    config:
      - address: 0.pool.ntp.org
      - address: 1.pool.ntp.org
    state: merged

- name: Override — keep only these servers
  jaydee_io.dlink_dgs1250.dgs1250_ntp:
    config:
      - address: ntp.company.com
    state: overridden

- name: Gather SNTP server config
  jaydee_io.dlink_dgs1250.dgs1250_ntp:
    state: gathered
"""

RETURN = r"""
before:
  description: SNTP server configuration before the changes.
  returned: always (except gathered)
  type: list
  elements: dict
after:
  description: SNTP server configuration after the changes.
  returned: when changed
  type: list
  elements: dict
gathered:
  description: Current SNTP server configuration gathered from the switch.
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


def _parse_sntp_servers(config):
    servers = []
    for line in config.splitlines():
        m = re.match(r"^\s*sntp server\s+(\S+)\s*$", line)
        if m:
            servers.append({"address": m.group(1)})
    return servers


def _gather(module):
    config = get_running_config(module)
    return _parse_sntp_servers(config)


def _have_set(entries):
    return {e["address"] for e in entries}


def _build_commands_merged(want, have_addrs):
    commands = []
    for entry in want:
        if entry["address"] not in have_addrs:
            commands.append("sntp server %s" % entry["address"])
    return commands


def _build_commands_overridden(want, have_addrs):
    commands = []
    want_addrs = {e["address"] for e in want}
    for addr in sorted(have_addrs):
        if addr not in want_addrs:
            commands.append("no sntp server %s" % addr)
    for entry in want:
        if entry["address"] not in have_addrs:
            commands.append("sntp server %s" % entry["address"])
    return commands


def _build_commands_deleted(want, have_addrs):
    commands = []
    if not want:
        for addr in sorted(have_addrs):
            commands.append("no sntp server %s" % addr)
    else:
        for entry in want:
            if entry["address"] in have_addrs:
                commands.append("no sntp server %s" % entry["address"])
    return commands


def main():
    element_spec = dict(
        address=dict(type="str", required=True),
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
    have_addrs = _have_set(have)

    if state == "merged":
        commands = _build_commands_merged(want, have_addrs)
    elif state == "overridden":
        commands = _build_commands_overridden(want, have_addrs)
    elif state == "deleted":
        commands = _build_commands_deleted(want, have_addrs)
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
