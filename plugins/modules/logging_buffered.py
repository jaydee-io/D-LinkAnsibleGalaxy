#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: logging_buffered
short_description: Configure logging to local buffer on a D-Link DGS-1250 switch
description:
  - Configures the C(logging buffered) CLI command on a D-Link DGS-1250 switch.
  - Enables or disables logging of system messages to the local message buffer.
  - Corresponds to CLI command described in chapter 66-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.19.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  severity:
    description:
      - The severity level name. Messages at this level or higher are logged.
    type: str
    choices: [emergencies, alerts, critical, errors, warnings, notifications, informational, debugging]
  discriminator:
    description:
      - Name of the discriminator to filter messages.
    type: str
  write_delay:
    description:
      - Interval in seconds for writing logging buffer to FLASH.
      - Use C(infinite) string or an integer value.
    type: str
  state:
    description:
      - C(enabled) to enable, C(disabled) to disable, C(default) to revert to default.
    type: str
    choices: [enabled, disabled, default]
    default: enabled
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable logging buffered with errors severity
  jaydee_io.dlink_dgs1250.logging_buffered:
    severity: errors

- name: Disable logging buffered
  jaydee_io.dlink_dgs1250.logging_buffered:
    state: disabled

- name: Revert to default
  jaydee_io.dlink_dgs1250.logging_buffered:
    state: default
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


def _build_commands(severity, discriminator, write_delay, state):
    if state == "disabled":
        return ["no logging buffered"]
    if state == "default":
        return ["default logging buffered"]
    cmd = "logging buffered"
    if severity is not None:
        cmd += " severity %s" % severity
    if discriminator is not None:
        cmd += " discriminator %s" % discriminator
    if write_delay is not None:
        cmd += " write-delay %s" % write_delay
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            severity=dict(type="str", choices=["emergencies", "alerts", "critical",
                          "errors", "warnings", "notifications", "informational", "debugging"]),
            discriminator=dict(type="str"),
            write_delay=dict(type="str"),
            state=dict(type="str", choices=[
                       "enabled", "disabled", "default"], default="enabled"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["severity"], module.params["discriminator"], module.params["write_delay"], module.params["state"])
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
