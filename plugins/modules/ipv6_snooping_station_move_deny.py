#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: ipv6_snooping_station_move_deny
short_description: Enable or disable IPv6 snooping station move deny on a D-Link DGS-1250 switch
description:
  - Configures the C(ipv6 snooping station-move deny) CLI command on a D-Link DGS-1250 switch.
  - Denies or permits the station move function for IPv6 snooping entries.
  - Corresponds to CLI command described in chapter 37-5 of the DGS-1250 CLI Reference Guide.
version_added: "0.13.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  state:
    description:
      - C(enabled) to deny station moves, C(disabled) to permit them (default behavior).
    type: str
    choices: [enabled, disabled]
    default: enabled
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Deny IPv6 snooping station moves
  jaydee_io.dlink_dgs1250.ipv6_snooping_station_move_deny:

- name: Permit IPv6 snooping station moves
  jaydee_io.dlink_dgs1250.ipv6_snooping_station_move_deny:
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
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(state):
    """Build the CLI command list."""
    if state == "enabled":
        return ["ipv6 snooping station-move deny"]
    return ["no ipv6 snooping station-move deny"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type="str", choices=[
                       "enabled", "disabled"], default="enabled"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["state"])
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
