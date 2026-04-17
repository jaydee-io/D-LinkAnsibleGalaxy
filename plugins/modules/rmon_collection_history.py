#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: rmon_collection_history
short_description: Enable RMON history statistics on an interface of a D-Link DGS-1250 switch
description:
  - Configures the C(rmon collection history) CLI command on a D-Link DGS-1250 switch.
  - Enables or disables RMON MIB history statistics gathering on an interface.
  - Corresponds to CLI command described in chapter 55-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
author:
  - Jérôme Dumesnil
options:
  interface:
    description:
      - The interface to configure (e.g. C(eth1/0/8)).
    type: str
    required: true
  index:
    description:
      - History group table index (1-65535).
    type: int
    required: true
  owner:
    description:
      - Owner string (max 127 characters).
    type: str
  buckets:
    description:
      - Number of buckets for the history group (1-65535, default 50).
    type: int
  interval:
    description:
      - Polling interval in seconds (1-3600).
    type: int
  state:
    description:
      - C(present) to enable history, C(absent) to disable.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable RMON history on eth1/0/8
  jaydee_io.dlink_dgs1250.rmon_collection_history:
    interface: eth1/0/8
    index: 101
    owner: "it@domain.com"
    interval: 2000

- name: Disable RMON history
  jaydee_io.dlink_dgs1250.rmon_collection_history:
    interface: eth1/0/8
    index: 101
    state: absent
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
commands:
  description: List of CLI commands sent to the switch.
  returned: always
  type: list
  elements: str
"""

from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import (
        run_commands, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(interface, index, owner, buckets, interval, state):
    commands = ["interface %s" % interface]
    if state == "absent":
        commands.append("no rmon collection history %d" % index)
    else:
        cmd = "rmon collection history %d" % index
        if owner:
            cmd += " owner %s" % owner
        if buckets is not None:
            cmd += " buckets %d" % buckets
        if interval is not None:
            cmd += " interval %d" % interval
        commands.append(cmd)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            index=dict(type="int", required=True),
            owner=dict(type="str"),
            buckets=dict(type="int"),
            interval=dict(type="int"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["interface"],
        module.params["index"],
        module.params["owner"],
        module.params["buckets"],
        module.params["interval"],
        module.params["state"],
    )
    if module.check_mode:
        module.exit_json(changed=True, commands=commands, raw_output="")
        return
    try:
        raw_output = run_commands(module, commands, mode=MODE_GLOBAL_CONFIG)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    module.exit_json(changed=True, raw_output=raw_output, commands=commands)


if __name__ == "__main__":
    main()
