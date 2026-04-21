#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jerome Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: loopback_detection_snmp_traps
short_description: Enable or disable SNMP traps for loopback detection on a D-Link DGS-1250 switch
description:
  - Configures the C(snmp-server enable traps loopback-detection) CLI command on a D-Link DGS-1250 switch.
  - Corresponds to CLI command described in chapter 42-6 of the DGS-1250 CLI Reference Guide.
version_added: "0.14.0"
author:
  - "Jérôme Dumesnil (@jaydee-io)"
options:
  state:
    description:
      - Whether to enable (C(enabled)) or disable (C(disabled)) the SNMP traps.
    type: str
    choices: [enabled, disabled]
    default: enabled
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable loopback detection SNMP traps
  jaydee_io.dlink_dgs1250.loopback_detection_snmp_traps:

- name: Disable loopback detection SNMP traps
  jaydee_io.dlink_dgs1250.loopback_detection_snmp_traps:
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


def _build_commands(state):
    if state == "enabled":
        return ["snmp-server enable traps loopback-detection"]
    return ["no snmp-server enable traps loopback-detection"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type="str", choices=[
                       "enabled", "disabled"], default="enabled"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["state"])
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
