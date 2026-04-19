#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: mstp_instance
short_description: Map VLANs to an MST instance on a D-Link DGS-1250 switch
description:
  - Configures the C(instance) CLI command in MST Configuration Mode on a D-Link DGS-1250 switch.
  - Maps VLANs to an MST instance or removes an MST instance.
  - Corresponds to CLI command described in chapter 46-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.15.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  instance_id:
    description:
      - The MSTP instance identifier (1 to 32).
    type: int
    required: true
  vlans:
    description:
      - The VLANs to map to the instance (e.g. C(1-100)). Required when C(state=present).
    type: str
  state:
    description:
      - C(present) to map VLANs to the instance, C(absent) to remove the instance.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in MST Configuration Mode.
"""

EXAMPLES = r"""
- name: Map VLANs 1-100 to MST instance 2
  jaydee_io.dlink_dgs1250.mstp_instance:
    instance_id: 2
    vlans: "1-100"

- name: Remove MST instance 2
  jaydee_io.dlink_dgs1250.mstp_instance:
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
        run_commands, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(instance_id, vlans, state):
    """Build the CLI command list."""
    commands = ["spanning-tree mst configuration"]
    if state == "absent":
        commands.append("no instance %d" % instance_id)
    else:
        commands.append("instance %d vlans %s" % (instance_id, vlans))
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            instance_id=dict(type="int", required=True),
            vlans=dict(type="str"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["vlans"]),
        ],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["instance_id"],
        module.params["vlans"],
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
