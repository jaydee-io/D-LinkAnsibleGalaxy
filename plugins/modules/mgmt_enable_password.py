#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: mgmt_enable_password
short_description: Set or remove the enable password on a D-Link DGS-1250 switch
description:
  - Configures the C(enable password) CLI command on a D-Link DGS-1250 switch.
  - Use C(state=absent) to reset the password to empty.
  - Corresponds to CLI command described in chapter 5-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.4.0"
author:
  - Jérôme Dumesnil
options:
  password:
    description:
      - The enable password string. Required when C(state=present).
    type: str
  encryption:
    description:
      - Password encryption type.
    type: int
    choices: [0, 7, 15]
  state:
    description:
      - C(present) to set the password, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - Use C(no_log=true) on the task to avoid logging the password.
"""

EXAMPLES = r"""
- name: Set enable password
  jaydee_io.dlink_dgs1250.mgmt_enable_password:
    password: MyEnablePassword
  no_log: true

- name: Remove enable password
  jaydee_io.dlink_dgs1250.mgmt_enable_password:
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


def _build_commands(password, encryption, state):
    if state == "absent":
        return ["no enable password"]
    enc = "%d " % encryption if encryption is not None else ""
    return ["enable password %s%s" % (enc, password)]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            password=dict(type="str", no_log=True),
            encryption=dict(type="int", choices=[0, 7, 15]),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["password"]),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(module.params["password"], module.params["encryption"], module.params["state"])

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
