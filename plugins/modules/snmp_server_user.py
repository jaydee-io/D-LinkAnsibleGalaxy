#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: snmp_server_user
short_description: Create or remove an SNMP user on a D-Link DGS-1250 switch
description:
  - Configures the C(snmp-server user) CLI command on a D-Link DGS-1250 switch.
  - Creates or removes an SNMP user with specified security model and authentication.
  - Corresponds to CLI command described in chapter 60-20 of the DGS-1250 CLI Reference Guide.
version_added: "0.17.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  user:
    description:
      - Username (max 32 characters, no spaces).
    type: str
    required: true
  group:
    description:
      - Group name the user belongs to.
    type: str
    required: true
  version:
    description:
      - SNMP version / security model.
    type: str
    required: true
    choices: [v1, v2c, v3]
  encrypted:
    description:
      - Whether the password is in encrypted format (SNMPv3 only).
    type: bool
    default: false
  auth_protocol:
    description:
      - Authentication protocol (SNMPv3 only).
    type: str
    choices: [md5, sha]
  auth_password:
    description:
      - Authentication password (SNMPv3 only).
    type: str
  priv_password:
    description:
      - Privacy password (SNMPv3 only).
    type: str
  access_list:
    description:
      - Standard IP ACL name to associate with the user.
    type: str
  state:
    description:
      - C(present) to create, C(absent) to remove.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Create SNMPv3 user with auth and priv
  jaydee_io.dlink_dgs1250.snmp_server_user:
    user: user1
    group: public
    version: v3
    auth_protocol: md5
    auth_password: authpassword
    priv_password: privpassword

- name: Remove user
  jaydee_io.dlink_dgs1250.snmp_server_user:
    user: user1
    group: public
    version: v3
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


def _build_commands(user, group, version, encrypted, auth_protocol, auth_password, priv_password, access_list, state):
    if state == "absent":
        return ["no snmp-server user %s %s %s" % (user, group, version)]
    cmd = "snmp-server user %s %s %s" % (user, group, version)
    if version == "v3":
        if encrypted:
            cmd += " encrypted"
        if auth_protocol:
            cmd += " auth %s %s" % (auth_protocol, auth_password)
            if priv_password:
                cmd += " priv %s" % priv_password
    if access_list:
        cmd += " access %s" % access_list
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            user=dict(type="str", required=True),
            group=dict(type="str", required=True),
            version=dict(type="str", required=True,
                         choices=["v1", "v2c", "v3"]),
            encrypted=dict(type="bool", default=False),
            auth_protocol=dict(type="str", choices=["md5", "sha"]),
            auth_password=dict(type="str", no_log=True),
            priv_password=dict(type="str", no_log=True),
            access_list=dict(type="str"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["user"], module.params["group"], module.params["version"],
                               module.params["encrypted"], module.params["auth_protocol"],
                               module.params["auth_password"], module.params["priv_password"],
                               module.params["access_list"], module.params["state"])
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
