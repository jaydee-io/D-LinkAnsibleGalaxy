#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: interface_description
short_description: Set or remove interface description on a D-Link DGS-1250 switch
description:
  - Adds or removes a description for an interface using the C(description) CLI command.
  - Corresponds to CLI command described in chapter 30-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.11.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface_id:
    description:
      - The interface to configure (e.g. C(eth1/0/10) or C(l2vlan 1)).
    type: str
    required: true
  description:
    description:
      - Description string for the interface (max 64 characters).
      - Required when C(state=present).
    type: str
  state:
    description:
      - C(present) sets the interface description.
      - C(absent) removes the interface description.
    type: str
    default: present
    choices: [present, absent]
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Set description on port 10
  jaydee_io.dlink_dgs1250.interface_description:
    interface_id: eth1/0/10
    description: "Physical Port 10"
    state: present

- name: Remove description from port 10
  jaydee_io.dlink_dgs1250.interface_description:
    interface_id: eth1/0/10
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
        run_commands, is_config_present, build_config_diff, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, is_config_present, build_config_diff, MODE_GLOBAL_CONFIG


def _build_commands(interface_id, description, state):
    if state == "absent":
        return ["interface %s" % interface_id, "no description", "exit"]
    return ["interface %s" % interface_id, "description %s" % description, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface_id=dict(type="str", required=True),
            description=dict(type="str"),
            state=dict(type="str", default="present",
                       choices=["present", "absent"]),
        ),
        required_if=[("state", "present", ["description"])],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["interface_id"],
        module.params["description"],
        module.params["state"],
    )
    if is_config_present(module, commands):
        module.exit_json(changed=False, commands=[], raw_output="")
        return
    diff = build_config_diff(module, commands) if module._diff else None
    if module.check_mode:
        result = dict(changed=True, commands=commands, raw_output="")
        if diff:
            result['diff'] = diff
        module.exit_json(**result)
        return
    try:
        raw_output = run_commands(module, commands, mode=MODE_GLOBAL_CONFIG)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    result = dict(changed=True, raw_output=raw_output, commands=commands)
    if diff:
        result['diff'] = diff
    module.exit_json(**result)


if __name__ == "__main__":
    main()
