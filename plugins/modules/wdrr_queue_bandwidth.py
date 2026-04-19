#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: wdrr_queue_bandwidth
short_description: Set the WDRR queue quantum on a D-Link DGS-1250 switch interface
description:
  - Configures the C(wdrr-queue bandwidth) CLI command on a D-Link DGS-1250 switch.
  - Sets the queue quantum values used by the WDRR scheduling mode.
  - Corresponds to CLI command described in chapter 54-21 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
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
  quantums:
    description:
      - List of 8 quantum values (0-127), one per queue.
    type: list
    elements: int
  state:
    description:
      - C(present) to set the quantums, C(absent) to revert to the default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Set WDRR quantums 1..8 on eth1/0/1
  jaydee_io.dlink_dgs1250.wdrr_queue_bandwidth:
    interface: eth1/0/1
    quantums: [1, 2, 3, 4, 5, 6, 7, 8]

- name: Revert WDRR quantums to default
  jaydee_io.dlink_dgs1250.wdrr_queue_bandwidth:
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
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(interface, quantums, state):
    commands = ["interface %s" % interface]
    if state == "absent":
        commands.append("no wdrr-queue bandwidth")
    else:
        commands.append("wdrr-queue bandwidth " + " ".join(str(q)
                        for q in quantums))
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            quantums=dict(type="list", elements="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["quantums"])],
        supports_check_mode=True,
    )
    q = module.params["quantums"]
    if module.params["state"] == "present" and q is not None and len(q) != 8:
        module.fail_json(msg="quantums must be a list of 8 integers")
    commands = _build_commands(
        module.params["interface"],
        module.params["quantums"],
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
