#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: poe_pd_priority
short_description: Configure PoE PD priority on an interface on a D-Link DGS-1250 switch
description:
  - Configures the C(poe pd priority) CLI command on a D-Link DGS-1250 switch.
  - Sets the priority for provisioning power to a PoE port.
  - Corresponds to CLI command described in chapter 51-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - The PoE interface to configure (e.g. C(eth1/0/1)).
    type: str
    required: true
  priority:
    description:
      - The priority level. Required when C(state=present).
    type: str
    choices: [critical, high, low]
  state:
    description:
      - C(present) to set the priority, C(absent) to revert to default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Interface Configuration Mode.
  - Only applies to DGS-1250-28XMP and DGS-1250-52XMP models.
"""

EXAMPLES = r"""
- name: Set PoE priority to critical
  jaydee_io.dlink_dgs1250.poe_pd_priority:
    interface: eth1/0/1
    priority: critical

- name: Revert PoE priority to default
  jaydee_io.dlink_dgs1250.poe_pd_priority:
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


def _build_commands(interface, priority, state):
    commands = ["interface %s" % interface]
    if state == "absent":
        commands.append("no poe pd priority")
    else:
        commands.append("poe pd priority %s" % priority)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            priority=dict(type="str", choices=["critical", "high", "low"]),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["priority"])],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["interface"],
        module.params["priority"],
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
