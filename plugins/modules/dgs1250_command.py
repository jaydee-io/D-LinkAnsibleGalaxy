#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dgs1250_command
short_description: Send arbitrary CLI commands to a D-Link DGS-1250 switch
description:
  - Sends one or more arbitrary CLI commands to a D-Link DGS-1250 switch
    and returns the raw output.
  - Similar in spirit to C(ios_command) from the Cisco IOS collection.
  - Use this module for CLI commands not covered by a dedicated module.
version_added: "1.1.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  commands:
    description:
      - Ordered list of CLI commands to send to the switch.
    type: list
    elements: str
    required: true
  mode:
    description:
      - CLI mode in which to execute the commands.
    type: str
    choices: [user, privileged, global_config]
    default: privileged
notes:
  - This module always reports C(changed=False) when C(mode) is C(user)
    or C(privileged) (read-only modes).
  - When C(mode=global_config), C(changed=True) is reported because the
    commands may modify the switch configuration.
"""

EXAMPLES = r"""
- name: Run a show command
  jaydee_io.dlink_dgs1250.dgs1250_command:
    commands:
      - show vlan
  register: result

- name: Display the output
  ansible.builtin.debug:
    var: result.raw_output

- name: Send configuration commands
  jaydee_io.dlink_dgs1250.dgs1250_command:
    commands:
      - interface ethernet 1/0/1
      - description Uplink
      - exit
    mode: global_config

- name: Clear MAC address table
  jaydee_io.dlink_dgs1250.dgs1250_command:
    commands:
      - clear mac-address-table dynamic
    mode: privileged
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI commands.
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
        run_commands, MODE_USER, MODE_PRIVILEGED, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_USER, MODE_PRIVILEGED, MODE_GLOBAL_CONFIG

_MODE_MAP = {
    "user": MODE_USER,
    "privileged": MODE_PRIVILEGED,
    "global_config": MODE_GLOBAL_CONFIG,
}


# ---------------------------------------------------------------------------
# Command builder
# ---------------------------------------------------------------------------

def _build_commands(commands):
    """Return the command list as-is (pass-through)."""
    return list(commands)


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            commands=dict(type="list", elements="str", required=True),
            mode=dict(type="str", choices=[
                      "user", "privileged", "global_config"], default="privileged"),
        ),
        supports_check_mode=True,
    )

    commands = _build_commands(module.params["commands"])
    mode = _MODE_MAP[module.params["mode"]]
    changed = (mode == MODE_GLOBAL_CONFIG)

    if module.check_mode:
        module.exit_json(changed=changed, commands=commands, raw_output="")
        return

    try:
        raw_output = run_commands(module, commands, mode=mode)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    module.exit_json(changed=changed, raw_output=raw_output, commands=commands)


if __name__ == "__main__":
    main()
