#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: snmp_server_trap_sending
short_description: Enable or disable SNMP trap sending on an interface on a D-Link DGS-1250 switch
description:
  - Configures the C(snmp-server trap-sending disable) CLI command on a D-Link DGS-1250 switch.
  - Enables or disables the sending of notifications for a port.
  - Corresponds to CLI command described in chapter 60-10 of the DGS-1250 CLI Reference Guide.
version_added: "0.17.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - The interface to configure (e.g. C(eth1/0/8)).
    type: str
    required: true
  state:
    description:
      - C(enabled) to enable trap sending, C(disabled) to disable it.
    type: str
    choices: [enabled, disabled]
    default: enabled
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Disable trap sending on port 8
  jaydee_io.dlink_dgs1250.snmp_server_trap_sending:
    interface: eth1/0/8
    state: disabled

- name: Re-enable trap sending on port 8
  jaydee_io.dlink_dgs1250.snmp_server_trap_sending:
    interface: eth1/0/8
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


def _build_commands(interface, state):
    commands = ["interface %s" % interface]
    if state == "disabled":
        commands.append("snmp-server trap-sending disable")
    else:
        commands.append("no snmp-server trap-sending disable")
    commands.append("exit")
    return commands



def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            state=dict(type="str", choices=["enabled", "disabled"], default="enabled"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["interface"], module.params["state"])
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
