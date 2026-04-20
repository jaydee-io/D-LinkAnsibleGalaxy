#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: mstp_priority
short_description: Configure MSTP bridge priority on a D-Link DGS-1250 switch
description:
  - Configures the C(spanning-tree mst priority) CLI command on a D-Link DGS-1250 switch.
  - Sets or resets the bridge priority for a specific MSTP instance.
  - Corresponds to CLI command described in chapter 46-9 of the DGS-1250 CLI Reference Guide.
version_added: "0.15.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  instance_id:
    description:
      - The MSTP instance identifier. Instance 0 represents the CIST.
    type: int
    required: true
  priority:
    description:
      - The bridge priority (0 to 61440, must be divisible by 4096). Required when C(state=present).
    type: int
  state:
    description:
      - C(present) to set the priority, C(absent) to revert to default (32768).
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set MSTP bridge priority for instance 2
  jaydee_io.dlink_dgs1250.mstp_priority:
    instance_id: 2
    priority: 0

- name: Revert MSTP bridge priority to default for instance 2
  jaydee_io.dlink_dgs1250.mstp_priority:
    instance_id: 2
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
        run_commands, is_config_present, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, is_config_present, MODE_GLOBAL_CONFIG


def _build_commands(instance_id, priority, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["no spanning-tree mst %d priority" % instance_id]
    return ["spanning-tree mst %d priority %d" % (instance_id, priority)]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            instance_id=dict(type="int", required=True),
            priority=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["priority"]),
        ],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["instance_id"],
        module.params["priority"],
        module.params["state"],
    )
    if is_config_present(module, commands):
        module.exit_json(changed=False, commands=[], raw_output="")
        return
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
