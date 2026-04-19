#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: ssh_user_authentication_method
short_description: Configure SSH authentication method for a user on a D-Link DGS-1250 switch
description:
  - Configures the C(ssh user authentication-method) CLI command on a D-Link DGS-1250 switch.
  - Configures the SSH authentication method for a user account.
  - Corresponds to CLI command described in chapter 58-9 of the DGS-1250 CLI Reference Guide.
version_added: "0.17.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  user:
    description:
      - The username to configure (max 32 characters).
    type: str
    required: true
  method:
    description:
      - Authentication method. Required when C(state=present).
    type: str
    choices: [password, publickey, hostbased]
  url:
    description:
      - URL of the public key or host key file. Required for C(publickey) and C(hostbased) methods.
    type: str
  hostname:
    description:
      - Allowed host name for host-based authentication. Required for C(hostbased) method.
    type: str
  ip_address:
    description:
      - Optional IP or IPv6 address to additionally check for host-based authentication.
    type: str
  state:
    description:
      - C(present) to set the authentication method, C(absent) to revert to default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set password authentication for user
  jaydee_io.dlink_dgs1250.ssh_user_authentication_method:
    user: tom
    method: password

- name: Set publickey authentication
  jaydee_io.dlink_dgs1250.ssh_user_authentication_method:
    user: tom
    method: publickey
    url: c:/user1.pub

- name: Set hostbased authentication
  jaydee_io.dlink_dgs1250.ssh_user_authentication_method:
    user: tom
    method: hostbased
    url: c:/host.pub
    hostname: myhost

- name: Revert to default
  jaydee_io.dlink_dgs1250.ssh_user_authentication_method:
    user: tom
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


def _build_commands(user, method, url, hostname, ip_address, state):
    if state == "absent":
        return ["no ssh user %s authentication-method" % user]
    cmd = "ssh user %s authentication-method %s" % (user, method)
    if method == "publickey":
        cmd += " %s" % url
    elif method == "hostbased":
        cmd += " %s host-name %s" % (url, hostname)
        if ip_address:
            cmd += " %s" % ip_address
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            user=dict(type="str", required=True),
            method=dict(type="str", choices=[
                        "password", "publickey", "hostbased"]),
            url=dict(type="str"),
            hostname=dict(type="str"),
            ip_address=dict(type="str"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["method"])],
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["user"], module.params["method"], module.params["url"],
                               module.params["hostname"], module.params["ip_address"], module.params["state"])
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
