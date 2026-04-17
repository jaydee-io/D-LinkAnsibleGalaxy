#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: poe_clear_statistics
short_description: Clear PoE statistic counters on a D-Link DGS-1250 switch
description:
  - Executes the C(clear poe statistic) CLI command on a D-Link DGS-1250 switch.
  - Clears the PoE statistic counters for all or specific interfaces.
  - Corresponds to CLI command described in chapter 51-8 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
author:
  - Jérôme Dumesnil
options:
  target:
    description:
      - C(all) clears PoE statistics for all interfaces.
      - C(interface) clears statistics for the interface(s) in C(interface_id).
    type: str
    required: true
    choices: [all, interface]
  interface_id:
    description:
      - The interface(s) to clear (e.g. C(eth1/0/1), C(eth1/0/1-3)). Required when C(target=interface).
    type: str
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Privileged EXEC Mode.
  - Only applies to DGS-1250-28XMP and DGS-1250-52XMP models.
"""

EXAMPLES = r"""
- name: Clear PoE statistics on all interfaces
  jaydee_io.dlink_dgs1250.poe_clear_statistics:
    target: all

- name: Clear PoE statistics on port 1
  jaydee_io.dlink_dgs1250.poe_clear_statistics:
    target: interface
    interface_id: eth1/0/1
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
        return ["clear poe statistic all"]
    return ["clear poe statistic interface %s" % interface_id]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            target=dict(type="str", required=True, choices=["all", "interface"]),
            interface_id=dict(type="str"),
        ),
        required_if=[("target", "interface", ["interface_id"])],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["target"],
        module.params["interface_id"],
    )
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
