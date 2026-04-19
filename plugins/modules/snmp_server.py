#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: snmp_server
short_description: Enable or disable the SNMP agent on a D-Link DGS-1250 switch
description:
  - Configures the C(snmp-server) CLI command on a D-Link DGS-1250 switch.
  - Enables or disables the SNMP agent.
  - Corresponds to CLI command described in chapter 60-4 of the DGS-1250 CLI Reference Guide.
version_added: "0.17.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  state:
    description:
      - C(enabled) to enable the SNMP agent, C(disabled) to disable it.
    type: str
    choices: [enabled, disabled]
    default: enabled
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable SNMP server
  jaydee_io.dlink_dgs1250.snmp_server:

- name: Disable SNMP server
  jaydee_io.dlink_dgs1250.snmp_server:
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
    if state == "disabled":
        return ["no snmp-server"]
    return ["snmp-server"]


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
