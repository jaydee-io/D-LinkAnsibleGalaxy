#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: priority_queue_cos_map
short_description: Define a CoS-to-queue map on a D-Link DGS-1250 switch
description:
  - Configures the C(priority-queue cos-map) CLI command on a D-Link DGS-1250 switch.
  - Maps one or more CoS values to a transmit queue.
  - Corresponds to CLI command described in chapter 54-11 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  queue_id:
    description:
      - Queue ID to which the CoS values are mapped.
    type: int
    required: true
  cos_values:
    description:
      - List of CoS values (0-7) to map to this queue. Required when C(state=present).
    type: list
    elements: int
  state:
    description:
      - C(present) to set the mapping, C(absent) to revert to the default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Assign CoS 3,5,6 to queue 2
  jaydee_io.dlink_dgs1250.priority_queue_cos_map:
    queue_id: 2
    cos_values: [3, 5, 6]

- name: Revert CoS-to-queue map
  jaydee_io.dlink_dgs1250.priority_queue_cos_map:
    queue_id: 2
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


def _build_commands(queue_id, cos_values, state):
    if state == "absent":
        return ["no priority-queue cos-map"]
    cos_str = " ".join(str(c) for c in cos_values)
    return ["priority-queue cos-map %d %s" % (queue_id, cos_str)]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            queue_id=dict(type="int", required=True),
            cos_values=dict(type="list", elements="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["cos_values"])],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["queue_id"],
        module.params["cos_values"],
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
