#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jerome Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: mac_auth_password
short_description: Configure MAC authentication password on a D-Link DGS-1250 switch
description:
  - Configures the C(mac-auth password) CLI command on a D-Link DGS-1250 switch.
  - Corresponds to CLI command described in chapter 43-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.14.0"
author:
  - "Jérôme Dumesnil (@jaydee-io)"
options:
  password:
    description:
      - The password string (max 16 characters). Required when C(state=present).
    type: str
  encryption:
    description:
      - C(0) for clear text, C(7) for encrypted. Default is clear text.
    type: int
    choices: [0, 7]
  state:
    description:
      - C(present) to set the password, C(absent) to revert to default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set MAC authentication password
  jaydee_io.dlink_dgs1250.mac_auth_password:
    password: newpass

- name: Set encrypted MAC authentication password
  jaydee_io.dlink_dgs1250.mac_auth_password:
    password: newpass
    encryption: 7

- name: Revert to default password
  jaydee_io.dlink_dgs1250.mac_auth_password:
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


def _build_commands(password, encryption, state):
    if state == "absent":
        return ["no mac-auth password"]
    if encryption is not None:
        return ["mac-auth password %d %s" % (encryption, password)]
    return ["mac-auth password %s" % password]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            password=dict(type="str", no_log=True),
            encryption=dict(type="int", choices=[0, 7]),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["password"]),
        ],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["password"], module.params["encryption"], module.params["state"])
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
