#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jerome Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: lldp_tx_interval
short_description: Configure LLDP transmission interval on a D-Link DGS-1250 switch
description:
  - Configures the C(lldp tx-interval) CLI command on a D-Link DGS-1250 switch.
  - Corresponds to CLI command described in chapter 41-16 of the DGS-1250 CLI Reference Guide.
version_added: "0.14.0"
author:
  - "Jérôme Dumesnil (@jaydee-io)"
options:
  seconds:
    description:
      - The interval in seconds (5 to 32768).
    type: int
  state:
    description:
      - C(present) to set the value, C(absent) to revert to default (30).
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set lldp tx-interval
  jaydee_io.dlink_dgs1250.lldp_tx_interval:
    seconds: 50

- name: Revert lldp tx-interval to default
  jaydee_io.dlink_dgs1250.lldp_tx_interval:
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


def _build_commands(seconds, state):
    if state == "absent":
        return ["no lldp tx-interval"]
    return ["lldp tx-interval %d" % seconds]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            seconds=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["seconds"]),
        ],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["seconds"], module.params["state"])
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
