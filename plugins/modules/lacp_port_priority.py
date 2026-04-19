#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: lacp_port_priority
short_description: Configure LACP port priority on a D-Link DGS-1250 switch interface
description:
  - Configures the C(lacp port-priority) CLI command on a D-Link DGS-1250 switch.
  - Sets the LACP port priority on an interface.
  - Corresponds to CLI command described in chapter 40-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.13.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - The interface to configure (e.g. C(eth1/0/4)).
    type: str
    required: true
  priority:
    description:
      - The port priority value (1 to 65535). Required when C(state=present).
    type: int
  state:
    description:
      - C(present) to set the priority, C(absent) to revert to default (32768).
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Set LACP port priority
  jaydee_io.dlink_dgs1250.lacp_port_priority:
    interface: eth1/0/4
    priority: 20000

- name: Revert LACP port priority to default
  jaydee_io.dlink_dgs1250.lacp_port_priority:
    interface: eth1/0/4
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


def _build_commands(interface, priority, state):
    """Build the CLI command list."""
    commands = ["interface %s" % interface]
    if state == "absent":
        commands.append("no lacp port-priority")
    else:
        commands.append("lacp port-priority %d" % priority)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            priority=dict(type="int"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["priority"]),
        ],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["interface"],
        module.params["priority"],
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
