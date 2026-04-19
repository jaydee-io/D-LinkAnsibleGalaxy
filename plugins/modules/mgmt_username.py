#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: mgmt_username
short_description: Create or remove a user account on a D-Link DGS-1250 switch
description:
  - Configures the C(username) CLI command on a D-Link DGS-1250 switch.
  - Creates a user with optional password or removes an existing user.
  - Corresponds to CLI command described in chapter 5-22 of the DGS-1250 CLI Reference Guide.
version_added: "0.4.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  name:
    description:
      - The username to create or remove.
    type: str
    required: true
  password:
    description:
      - The password for the user. Mutually exclusive with C(nopassword).
    type: str
  encryption:
    description:
      - Password encryption type.
    type: int
    choices: [0, 7, 15]
  nopassword:
    description:
      - If C(true), create the user with no password. Mutually exclusive with C(password).
    type: bool
    default: false
  state:
    description:
      - C(present) to create the user, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
"""

EXAMPLES = r"""
- name: Create user admin with password
  jaydee_io.dlink_dgs1250.mgmt_username:
    name: admin
    password: SecurePass123
  no_log: true

- name: Create user guest with no password
  jaydee_io.dlink_dgs1250.mgmt_username:
    name: guest
    nopassword: true

- name: Remove user guest
  jaydee_io.dlink_dgs1250.mgmt_username:
    name: guest
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


def _build_commands(name, password, encryption, nopassword, state):
    if state == "absent":
        return ["no username %s" % name]
    if nopassword:
        return ["username %s nopassword" % name]
    if password:
        enc = "%d " % encryption if encryption is not None else ""
        return ["username %s password %s%s" % (name, enc, password)]
    return ["username %s" % name]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type="str", required=True),
            password=dict(type="str", no_log=True),
            encryption=dict(type="int", choices=[0, 7, 15]),
            nopassword=dict(type="bool", default=False),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        mutually_exclusive=[
            ("password", "nopassword"),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["name"],
        module.params["password"],
        module.params["encryption"],
        module.params["nopassword"],
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
