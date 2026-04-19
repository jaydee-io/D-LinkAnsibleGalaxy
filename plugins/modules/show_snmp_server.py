#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: show_snmp_server
short_description: Display SNMP server settings on a D-Link DGS-1250 switch
description:
  - Executes the C(show snmp-server) CLI command on a D-Link DGS-1250 switch.
  - Displays SNMP server global state settings and optionally trap related settings.
  - Corresponds to CLI command described in chapter 60-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.17.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  traps:
    description:
      - If C(true), display trap related settings instead of global settings.
    type: bool
    default: false
notes:
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Show SNMP server settings
  jaydee_io.dlink_dgs1250.show_snmp_server:

- name: Show SNMP trap settings
  jaydee_io.dlink_dgs1250.show_snmp_server:
    traps: true
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
        run_command,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


def _build_command(traps):
    cmd = "show snmp-server"
    if traps:
        cmd += " traps"
    return cmd



def main():
    module = AnsibleModule(
        argument_spec=dict(
            traps=dict(type="bool", default=False),
        ),
        supports_check_mode=True,
    )
    command = _build_command(module.params["traps"])
    if module.check_mode:
        module.exit_json(changed=False, commands=[command], raw_output="")
        return
    try:
        raw_output = run_command(module, command)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    module.exit_json(changed=False, raw_output=raw_output, commands=[command])


if __name__ == "__main__":
    main()
