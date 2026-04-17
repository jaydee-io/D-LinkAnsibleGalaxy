#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: show_snmp_server_trap_sending
short_description: Display per-port SNMP trap sending state on a D-Link DGS-1250 switch
description:
  - Executes the C(show snmp-server trap-sending) CLI command on a D-Link DGS-1250 switch.
  - Displays the per port SNMP trap sending state.
  - Corresponds to CLI command described in chapter 60-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.17.0"
author:
  - Jérôme Dumesnil
options:
  interface:
    description:
      - Interface(s) to display (e.g. C(eth1/0/1-9)). If omitted, all interfaces are displayed.
    type: str
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Show all trap sending states
  jaydee_io.dlink_dgs1250.show_snmp_server_trap_sending:

- name: Show trap sending for specific ports
  jaydee_io.dlink_dgs1250.show_snmp_server_trap_sending:
    interface: eth1/0/1-9
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


def _build_command(interface):
    cmd = "show snmp-server trap-sending"
    if interface:
        cmd += " interface %s" % interface
    return cmd



def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str"),
        ),
        supports_check_mode=True,
    )
    command = _build_command(module.params["interface"])
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
