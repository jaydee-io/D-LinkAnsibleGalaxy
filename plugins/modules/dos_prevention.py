#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: dos_prevention
short_description: Enable or disable DoS prevention on a D-Link DGS-1250 switch
description:
  - Configures the C(dos-prevention) CLI command on a D-Link DGS-1250 switch.
  - Enables or disables the DoS prevention mechanism for a specific attack type or all types.
  - Corresponds to CLI command described in chapter 24-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.10.0"
author:
  - Jérôme Dumesnil
options:
  attack_type:
    description:
      - The DoS attack type to configure.
      - C(all) affects all supported DoS types.
      - Supported types include C(blat), C(land), C(tcp-null-scan), C(tcp-syn-fin),
        C(tcp-syn-srcport-less-1024), C(tcp-xmas-scan), C(ping-death), C(tcp-tiny-frag),
        C(smurf), C(tcp-syn-rst), C(all).
    type: str
    required: true
  state:
    description:
      - C(enabled) to enable DoS prevention, C(disabled) to disable.
    type: str
    choices: [enabled, disabled]
    default: enabled
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable DoS prevention for land attack
  jaydee_io.dlink_dgs1250.dos_prevention:
    attack_type: land
    state: enabled

- name: Enable DoS prevention for all attack types
  jaydee_io.dlink_dgs1250.dos_prevention:
    attack_type: all
    state: enabled

- name: Disable DoS prevention for all attack types
  jaydee_io.dlink_dgs1250.dos_prevention:
    attack_type: all
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


def _build_commands(attack_type, state):
    """Build the CLI command list."""
    if state == "enabled":
        return ["dos-prevention %s" % attack_type]
    else:
        return ["no dos-prevention %s" % attack_type]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            attack_type=dict(type="str", required=True),
            state=dict(type="str", choices=["enabled", "disabled"], default="enabled"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["attack_type"], module.params["state"])
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
