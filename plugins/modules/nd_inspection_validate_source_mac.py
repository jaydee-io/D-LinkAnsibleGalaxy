#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: nd_inspection_validate_source_mac
short_description: Enable or disable source MAC validation in an ND inspection policy on a D-Link DGS-1250 switch
description:
  - Configures the C(validate source-mac) CLI command in ND Inspection Policy Configuration Mode on a D-Link DGS-1250 switch.
  - Enables or disables source MAC address validation for ND messages.
  - Corresponds to CLI command described in chapter 47-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.15.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  policy:
    description:
      - Name of the ND inspection policy to configure.
    type: str
    required: true
  state:
    description:
      - C(enabled) to enable source MAC validation, C(disabled) to disable it.
    type: str
    choices: [enabled, disabled]
    default: enabled
notes:
  - This command runs in ND Inspection Policy Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable source MAC validation in ND inspection policy
  jaydee_io.dlink_dgs1250.nd_inspection_validate_source_mac:
    policy: policy1

- name: Disable source MAC validation in ND inspection policy
  jaydee_io.dlink_dgs1250.nd_inspection_validate_source_mac:
    policy: policy1
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


def _build_commands(policy, state):
    """Build the CLI command list."""
    commands = ["ipv6 nd inspection policy %s" % policy]
    if state == "enabled":
        commands.append("validate source-mac")
    else:
        commands.append("no validate source-mac")
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            policy=dict(type="str", required=True),
            state=dict(type="str", choices=["enabled", "disabled"], default="enabled"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["policy"],
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
