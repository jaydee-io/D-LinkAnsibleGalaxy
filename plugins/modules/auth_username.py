#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: auth_username
short_description: Configure a local authentication user on a D-Link DGS-1250 switch
description:
  - Configures the C(authentication username) CLI command on a D-Link DGS-1250 switch.
  - Creates or removes a user in the local authentication database.
  - Corresponds to CLI command described in chapter 48-6 of the DGS-1250 CLI Reference Guide.
version_added: "0.15.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  name:
    description:
      - The username (max 32 characters).
    type: str
    required: true
  password:
    description:
      - The password in clear text (max 32 characters). Required when C(state=present).
    type: str
  vlan_id:
    description:
      - Optional VLAN to assign to the user.
    type: int
  state:
    description:
      - C(present) to create the user, C(absent) to remove.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Create local authentication user
  jaydee_io.dlink_dgs1250.auth_username:
    name: user1
    password: pass1

- name: Create local authentication user with VLAN
  jaydee_io.dlink_dgs1250.auth_username:
    name: user1
    password: pass1
    vlan_id: 10

- name: Remove local authentication user
  jaydee_io.dlink_dgs1250.auth_username:
    name: user1
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


def _build_commands(name, password, vlan_id, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["no authentication username %s" % name]
    cmd = "authentication username %s password %s" % (name, password)
    if vlan_id is not None:
        cmd += " vlan %d" % vlan_id
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type="str", required=True),
            password=dict(type="str", no_log=True),
            vlan_id=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["password"]),
        ],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["name"],
        module.params["password"],
        module.params["vlan_id"],
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
