#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: duplex
short_description: Configure duplex mode on a D-Link DGS-1250 switch interface
description:
  - Configures the C(duplex) CLI command on a D-Link DGS-1250 switch interface.
  - Sets the duplex mode to full, half, or auto.
  - Corresponds to CLI command described in chapter 64-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.18.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - The interface to configure (e.g. C(eth1/0/1)).
    type: str
    required: true
  mode:
    description:
      - The duplex mode to set.
    type: str
    choices: [full, half, auto]
  state:
    description:
      - C(present) to set the mode, C(absent) to revert to default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Set duplex to auto on port 1
  jaydee_io.dlink_dgs1250.duplex:
    interface: eth1/0/1
    mode: auto

- name: Revert duplex to default
  jaydee_io.dlink_dgs1250.duplex:
    interface: eth1/0/1
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


def _build_commands(interface, mode, state):
    commands = ["interface %s" % interface]
    if state == "absent":
        commands.append("no duplex")
    else:
        commands.append("duplex %s" % mode)
    commands.append("exit")
    return commands




def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            mode=dict(type="str", choices=["full", "half", "auto"]),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["interface"], module.params["mode"], module.params["state"])
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
