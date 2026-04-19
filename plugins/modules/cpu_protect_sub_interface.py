#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: cpu_protect_sub_interface
short_description: Configure CPU protect rate limit by sub-interface on a D-Link DGS-1250 switch
description:
  - Configures the C(cpu-protect sub-interface) CLI command on a D-Link DGS-1250 switch.
  - Sets the rate limit for traffic destined for the CPU by sub-interface type.
  - Corresponds to CLI command described in chapter 57-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.17.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  sub_interface:
    description:
      - The sub-interface type to configure.
    type: str
    required: true
    choices: [manage, protocol, route]
  rate:
    description:
      - Threshold value in packets per second. 0 drops all packets. Required when C(state=present).
    type: int
  state:
    description:
      - C(present) to set the rate limit, C(absent) to revert to default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set manage sub-interface rate to 1000 pps
  jaydee_io.dlink_dgs1250.cpu_protect_sub_interface:
    sub_interface: manage
    rate: 1000

- name: Revert manage sub-interface to default
  jaydee_io.dlink_dgs1250.cpu_protect_sub_interface:
    sub_interface: manage
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


def _build_commands(sub_interface, rate, state):
    if state == "absent":
        return ["no cpu-protect sub-interface %s" % sub_interface]
    return ["cpu-protect sub-interface %s pps %d" % (sub_interface, rate)]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            sub_interface=dict(type="str", required=True, choices=[
                               "manage", "protocol", "route"]),
            rate=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["rate"])],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["sub_interface"], module.params["rate"], module.params["state"])
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
