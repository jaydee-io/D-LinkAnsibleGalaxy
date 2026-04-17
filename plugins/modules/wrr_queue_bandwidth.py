#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: wrr_queue_bandwidth
short_description: Set the WRR queue weights on a D-Link DGS-1250 switch interface
description:
  - Configures the C(wrr-queue bandwidth) CLI command on a D-Link DGS-1250 switch.
  - Sets the queue weights used by the WRR scheduling mode.
  - Corresponds to CLI command described in chapter 54-22 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
author:
  - Jérôme Dumesnil
options:
  interface:
    description:
      - The interface to configure (e.g. C(eth1/0/1)).
    type: str
    required: true
  weights:
    description:
      - List of 8 weight values (0-127), one per queue.
    type: list
    elements: int
  state:
    description:
      - C(present) to set the weights, C(absent) to revert to the default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Set WRR weights 1..8 on eth1/0/1
  jaydee_io.dlink_dgs1250.wrr_queue_bandwidth:
    interface: eth1/0/1
    weights: [1, 2, 3, 4, 5, 6, 7, 8]

- name: Revert WRR weights to default
  jaydee_io.dlink_dgs1250.wrr_queue_bandwidth:
    interface: eth1/0/1
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
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(interface, weights, state):
    commands = ["interface %s" % interface]
    if state == "absent":
        commands.append("no wrr-queue bandwidth")
    else:
        commands.append("wrr-queue bandwidth " + " ".join(str(w) for w in weights))
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            weights=dict(type="list", elements="int"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["weights"])],
        supports_check_mode=True,
    )
    w = module.params["weights"]
    if module.params["state"] == "present" and w is not None and len(w) != 8:
        module.fail_json(msg="weights must be a list of 8 integers")
    commands = _build_commands(
        module.params["interface"],
        module.params["weights"],
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
