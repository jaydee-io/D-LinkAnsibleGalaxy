#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: ddm_snmp_traps_transceiver_monitoring
short_description: Enable or disable SNMP traps for transceiver monitoring on a D-Link DGS-1250 switch
description:
  - Configures the C(snmp-server enable traps transceiver-monitoring) CLI command on a D-Link DGS-1250 switch.
  - Enables or disables the sending of optical transceiver monitoring SNMP notifications.
  - Corresponds to CLI command described in chapter 21-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.10.0"
author:
  - Jérôme Dumesnil
options:
  trap_type:
    description:
      - Specifies whether to enable alarm, warning, or all trap types.
      - If not specified, all transceiver-monitoring SNMP notifications are affected.
    type: str
    choices: [alarm, warning]
  state:
    description:
      - C(enabled) to enable, C(disabled) to disable.
    type: str
    choices: [enabled, disabled]
    default: enabled
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable all transceiver monitoring traps
  jaydee_io.dlink_dgs1250.ddm_snmp_traps_transceiver_monitoring:
    state: enabled

- name: Enable warning traps only
  jaydee_io.dlink_dgs1250.ddm_snmp_traps_transceiver_monitoring:
    trap_type: warning
    state: enabled

- name: Disable alarm traps
  jaydee_io.dlink_dgs1250.ddm_snmp_traps_transceiver_monitoring:
    trap_type: alarm
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


def _build_commands(trap_type, state):
    """Build the CLI command list."""
    if state == "enabled":
        cmd = "snmp-server enable traps transceiver-monitoring"
    else:
        cmd = "no snmp-server enable traps transceiver-monitoring"
    if trap_type:
        cmd += " %s" % trap_type
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            trap_type=dict(type="str", choices=["alarm", "warning"]),
            state=dict(type="str", choices=["enabled", "disabled"], default="enabled"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["trap_type"], module.params["state"])
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
