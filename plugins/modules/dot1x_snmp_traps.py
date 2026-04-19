#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dot1x_snmp_traps
short_description: Enable or disable 802.1X SNMP traps on a D-Link DGS-1250 switch
description:
  - Configures the C(snmp-server enable traps dot1x) CLI command on a D-Link DGS-1250 switch.
  - Enables or disables SNMP notifications for 802.1X authentication events.
  - Corresponds to CLI command described in chapter 3-16 of the DGS-1250 CLI Reference Guide.
version_added: "0.2.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  state:
    description:
      - Whether 802.1X SNMP traps should be enabled or disabled.
    type: str
    choices: [enabled, disabled]
    default: enabled
notes:
  - This command requires Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable 802.1X SNMP traps
  jaydee_io.dlink_dgs1250.dot1x_snmp_traps:

- name: Disable 802.1X SNMP traps
  jaydee_io.dlink_dgs1250.dot1x_snmp_traps:
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


# ---------------------------------------------------------------------------
# Command builder
# ---------------------------------------------------------------------------

def _build_command(state):
    """Build the CLI command string."""
    prefix = "" if state == "enabled" else "no "
    return prefix + "snmp-server enable traps dot1x"


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type="str", choices=[
                       "enabled", "disabled"], default="enabled"),
        ),
        supports_check_mode=True,
    )

    state = module.params["state"]

    command = _build_command(state)
    commands = [command]

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
