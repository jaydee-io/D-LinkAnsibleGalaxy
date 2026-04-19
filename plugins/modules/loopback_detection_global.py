#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jerome Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: loopback_detection_global
short_description: Enable or disable loopback detection globally on a D-Link DGS-1250 switch
description:
  - Configures the C(loopback-detection) CLI command on a D-Link DGS-1250 switch.
  - Enables or disables loopback detection globally and optionally sets the detection mode.
  - Corresponds to CLI command described in chapter 42-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.14.0"
author:
  - Jerome Dumesnil
options:
  mode:
    description:
      - The detection mode. C(port-based) or C(vlan-based).
    type: str
    choices: [port-based, vlan-based]
  state:
    description:
      - Whether to enable (C(enabled)) or disable (C(disabled)) loopback detection.
    type: str
    choices: [enabled, disabled]
    default: enabled
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable loopback detection globally
  jaydee_io.dlink_dgs1250.loopback_detection_global:

- name: Enable loopback detection with port-based mode
  jaydee_io.dlink_dgs1250.loopback_detection_global:
    mode: port-based

- name: Disable loopback detection globally
  jaydee_io.dlink_dgs1250.loopback_detection_global:
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
        run_commands, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(mode, state):
    commands = []
    if state == "enabled":
        commands.append("loopback-detection")
        if mode:
            commands.append("loopback-detection mode %s" % mode)
    else:
        commands.append("no loopback-detection")
        if mode:
            commands.append("no loopback-detection mode")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            mode=dict(type="str", choices=["port-based", "vlan-based"]),
            state=dict(type="str", choices=["enabled", "disabled"], default="enabled"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["mode"], module.params["state"])
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
