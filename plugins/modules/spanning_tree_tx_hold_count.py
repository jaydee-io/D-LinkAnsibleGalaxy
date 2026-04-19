#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: spanning_tree_tx_hold_count
short_description: Configure STP transmit hold count on a D-Link DGS-1250 switch
description:
  - Configures the C(spanning-tree tx-hold-count) CLI command on a D-Link DGS-1250 switch.
  - Sets the maximum number of BPDUs that can be sent before pausing for one second.
  - Corresponds to CLI command described in chapter 61-16 of the DGS-1250 CLI Reference Guide.
version_added: "0.18.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  value:
    description:
      - The transmit hold count value (1 to 10).
    type: int
  state:
    description:
      - C(present) to set the value, C(absent) to revert to default (6).
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set transmit hold count to 5
  jaydee_io.dlink_dgs1250.spanning_tree_tx_hold_count:
    value: 5

- name: Revert to default
  jaydee_io.dlink_dgs1250.spanning_tree_tx_hold_count:
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


def _build_commands(value, state):
    if state == "absent":
        return ["no spanning-tree tx-hold-count"]
    return ["spanning-tree tx-hold-count %d" % value]




def main():
    module = AnsibleModule(
        argument_spec=dict(
            value=dict(type="int"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["value"], module.params["state"])
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
