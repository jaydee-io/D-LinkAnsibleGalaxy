#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: port_security_snmp_traps
short_description: Enable or disable SNMP traps for port security on a D-Link DGS-1250 switch
description:
  - Configures the C(snmp-server enable traps port-security) CLI command on a D-Link DGS-1250 switch.
  - Enables or disables SNMP notifications for port security address violations.
  - Corresponds to CLI command described in chapter 50-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.15.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  trap_rate:
    description:
      - The number of traps per second (0 to 1000). 0 means a trap for every violation.
    type: int
  state:
    description:
      - C(enabled) to enable SNMP traps, C(disabled) to disable them.
    type: str
    choices: [enabled, disabled]
    default: enabled
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable SNMP traps for port security
  jaydee_io.dlink_dgs1250.port_security_snmp_traps:

- name: Enable SNMP traps with rate limit
  jaydee_io.dlink_dgs1250.port_security_snmp_traps:
    trap_rate: 3

- name: Disable SNMP traps for port security
  jaydee_io.dlink_dgs1250.port_security_snmp_traps:
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


def _build_commands(trap_rate, state):
    """Build the CLI command list."""
    if state == "disabled":
        return ["no snmp-server enable traps port-security"]
    cmd = "snmp-server enable traps port-security"
    if trap_rate is not None:
        cmd += " trap-rate %d" % trap_rate
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            trap_rate=dict(type="int"),
            state=dict(type="str", choices=["enabled", "disabled"], default="enabled"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["trap_rate"],
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
