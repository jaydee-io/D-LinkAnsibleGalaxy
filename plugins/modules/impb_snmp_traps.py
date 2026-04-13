#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: impb_snmp_traps
short_description: Enable or disable SNMP traps for IMPB on a D-Link DGS-1250 switch
description:
  - Configures the C(snmp-server enable traps ip-mac-port-binding) CLI command on a D-Link DGS-1250 switch.
  - Enables or disables SNMP notifications for IMPB violation events.
  - Corresponds to CLI command described in chapter 32-4 of the DGS-1250 CLI Reference Guide.
version_added: "0.12.0"
author:
  - Jérôme Dumesnil
options:
  state:
    description:
      - Whether to enable (C(enabled)) or disable (C(disabled)) SNMP traps for IMPB.
    type: str
    choices: [enabled, disabled]
    default: enabled
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable SNMP traps for IMPB
  jaydee_io.dlink_dgs1250.impb_snmp_traps:

- name: Disable SNMP traps for IMPB
  jaydee_io.dlink_dgs1250.impb_snmp_traps:
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


def _build_commands(state):
    if state == "enabled":
        return ["snmp-server enable traps ip-mac-port-binding"]
    return ["no snmp-server enable traps ip-mac-port-binding"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type="str", choices=["enabled", "disabled"], default="enabled"),
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
