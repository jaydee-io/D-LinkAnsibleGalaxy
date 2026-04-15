#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jerome Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: lldp_clear_counters
short_description: Clear LLDP statistics on a D-Link DGS-1250 switch
description:
  - Executes the C(clear lldp counters) CLI command on a D-Link DGS-1250 switch.
  - Clears LLDP statistics globally, for all interfaces, or for a specific interface.
  - Corresponds to CLI command described in chapter 41-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.14.0"
author:
  - Jerome Dumesnil
options:
  target:
    description:
      - C(all) clears LLDP counter information for all interfaces and global LLDP statistics.
      - C(interface) clears LLDP counter information for a specific interface (requires C(interface_id)).
      - If not specified, only the LLDP global counters will be cleared.
    type: str
    choices: [all, interface]
  interface_id:
    description:
      - The interface ID (e.g. C(eth1/0/1)). Required when C(target=interface).
    type: str
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Clear all LLDP statistics
  jaydee_io.dlink_dgs1250.lldp_clear_counters:
    target: all

- name: Clear LLDP statistics for an interface
  jaydee_io.dlink_dgs1250.lldp_clear_counters:
    target: interface
    interface_id: eth1/0/1

- name: Clear LLDP global counters only
  jaydee_io.dlink_dgs1250.lldp_clear_counters:
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
        run_commands, MODE_PRIVILEGED,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_PRIVILEGED


def _build_commands(target, interface_id):
    if target == "all":
        return ["clear lldp counters all"]
    elif target == "interface":
        return ["clear lldp counters interface %s" % interface_id]
    return ["clear lldp counters"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            target=dict(type="str", choices=["all", "interface"]),
            interface_id=dict(type="str"),
        ),
        required_if=[
            ("target", "interface", ["interface_id"]),
        ],
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["target"], module.params["interface_id"])
    if module.check_mode:
        module.exit_json(changed=True, commands=commands, raw_output="")
        return
    try:
        raw_output = run_commands(module, commands, mode=MODE_PRIVILEGED)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    module.exit_json(changed=True, raw_output=raw_output, commands=commands)


if __name__ == "__main__":
    main()
