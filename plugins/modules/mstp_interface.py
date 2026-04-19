#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: mstp_interface
short_description: Configure MSTP cost or port-priority on an interface on a D-Link DGS-1250 switch
description:
  - Configures the C(spanning-tree mst) CLI command in Interface Configuration Mode on a D-Link DGS-1250 switch.
  - Sets the path cost or port priority for an MST instance on an interface.
  - Corresponds to CLI command described in chapter 46-5 of the DGS-1250 CLI Reference Guide.
version_added: "0.15.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - The interface to configure (e.g. C(eth1/0/1)).
    type: str
    required: true
  instance_id:
    description:
      - The MSTP instance identifier.
    type: int
    required: true
  cost:
    description:
      - The path cost for the instance (1 to 200000000). Mutually exclusive with C(port_priority).
    type: int
  port_priority:
    description:
      - The port priority for the instance (0 to 240, increments of 16). Mutually exclusive with C(cost).
    type: int
  state:
    description:
      - C(present) to set the value, C(absent) to revert to default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Set MSTP cost for instance 0 on port 1
  jaydee_io.dlink_dgs1250.mstp_interface:
    interface: eth1/0/1
    instance_id: 0
    cost: 17031970

- name: Set MSTP port-priority for instance 0 on port 1
  jaydee_io.dlink_dgs1250.mstp_interface:
    interface: eth1/0/1
    instance_id: 0
    port_priority: 64

- name: Revert MSTP cost to default for instance 0
  jaydee_io.dlink_dgs1250.mstp_interface:
    interface: eth1/0/1
    instance_id: 0
    state: absent
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


def _build_commands(interface, instance_id, cost, port_priority, state):
    """Build the CLI command list."""
    commands = ["interface %s" % interface]
    if state == "absent":
        if cost is not None:
            commands.append("no spanning-tree mst %d cost" % instance_id)
        elif port_priority is not None:
            commands.append(
                "no spanning-tree mst %d port-priority" % instance_id)
        else:
            commands.append("no spanning-tree mst %d cost" % instance_id)
    else:
        if cost is not None:
            commands.append("spanning-tree mst %d cost %d" %
                            (instance_id, cost))
        else:
            commands.append("spanning-tree mst %d port-priority %d" %
                            (instance_id, port_priority))
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            instance_id=dict(type="int", required=True),
            cost=dict(type="int"),
            port_priority=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_one_of=[
            ("cost", "port_priority"),
        ],
        mutually_exclusive=[
            ("cost", "port_priority"),
        ],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["interface"],
        module.params["instance_id"],
        module.params["cost"],
        module.params["port_priority"],
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
