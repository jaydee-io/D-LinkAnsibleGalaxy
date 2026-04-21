#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: ddp
short_description: Enable or disable D-Link Discovery Protocol (DDP) on a D-Link DGS-1250 switch
description:
  - Configures the C(ddp) CLI command on a D-Link DGS-1250 switch.
  - Enables or disables the DDP client function globally or on a specific interface.
  - Corresponds to CLI command described in chapter 22-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.10.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Interface on which to configure DDP (e.g. C(eth1/0/1)).
      - If not specified, DDP is configured globally.
    type: str
  state:
    description:
      - C(enabled) to enable DDP, C(disabled) to disable.
    type: str
    choices: [enabled, disabled]
    default: enabled
notes:
  - This command runs in Global Configuration Mode or Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable DDP globally
  jaydee_io.dlink_dgs1250.ddp:
    state: enabled

- name: Disable DDP globally
  jaydee_io.dlink_dgs1250.ddp:
    state: disabled

- name: Enable DDP on port 1
  jaydee_io.dlink_dgs1250.ddp:
    interface: eth1/0/1
    state: enabled

- name: Disable DDP on port 1
  jaydee_io.dlink_dgs1250.ddp:
    interface: eth1/0/1
    state: disabled
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
        run_commands, is_config_present, build_config_diff, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, is_config_present, build_config_diff, MODE_GLOBAL_CONFIG


def _build_commands(interface, state):
    """Build the CLI command list."""
    if interface:
        commands = ["interface %s" % interface]
        commands.append("ddp" if state == "enabled" else "no ddp")
        commands.append("exit")
    else:
        commands = ["ddp" if state == "enabled" else "no ddp"]
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str"),
            state=dict(type="str", choices=[
                       "enabled", "disabled"], default="enabled"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["interface"], module.params["state"])
    if is_config_present(module, commands):
        module.exit_json(changed=False, commands=[], raw_output="")
        return
    diff = build_config_diff(module, commands) if module._diff else None
    if module.check_mode:
        result = dict(changed=True, commands=commands, raw_output="")
        if diff:
            result['diff'] = diff
        module.exit_json(**result)
        return
    try:
        raw_output = run_commands(module, commands, mode=MODE_GLOBAL_CONFIG)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    result = dict(changed=True, raw_output=raw_output, commands=commands)
    if diff:
        result['diff'] = diff
    module.exit_json(**result)


if __name__ == "__main__":
    main()
