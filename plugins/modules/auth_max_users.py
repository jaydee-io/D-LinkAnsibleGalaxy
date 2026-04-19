#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: auth_max_users
short_description: Configure maximum authenticated users on a D-Link DGS-1250 switch
description:
  - Configures the C(authentication max users) CLI command on a D-Link DGS-1250 switch.
  - Sets or resets the maximum authenticated users globally or on an interface.
  - Corresponds to CLI command described in chapter 48-9 of the DGS-1250 CLI Reference Guide.
version_added: "0.15.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - The interface to configure (e.g. C(eth1/0/1)). If not specified, the global limit is set.
    type: str
  number:
    description:
      - The maximum number of authenticated users (1 to 1000). Required when C(state=present).
    type: int
  state:
    description:
      - C(present) to set the limit, C(absent) to revert to default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command can run in Global Configuration Mode or Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Set maximum authenticated users globally
  jaydee_io.dlink_dgs1250.auth_max_users:
    number: 256

- name: Set maximum authenticated users on port 1
  jaydee_io.dlink_dgs1250.auth_max_users:
    interface: eth1/0/1
    number: 10

- name: Revert maximum authenticated users to default
  jaydee_io.dlink_dgs1250.auth_max_users:
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
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(interface, number, state):
    """Build the CLI command list."""
    commands = []
    if interface:
        commands.append("interface %s" % interface)
    if state == "absent":
        commands.append("no authentication max users")
    else:
        commands.append("authentication max users %d" % number)
    if interface:
        commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str"),
            number=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["number"]),
        ],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["interface"],
        module.params["number"],
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
