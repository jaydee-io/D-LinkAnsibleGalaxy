#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: aaa_radius_server_host
short_description: Configure a RADIUS server host on a D-Link DGS-1250 switch
description:
  - Configures the C(radius-server host) CLI command on a D-Link DGS-1250 switch.
  - Adds or removes a RADIUS server host with optional parameters.
  - Corresponds to CLI command described in chapter 8-23 of the DGS-1250 CLI Reference Guide.
version_added: "0.6.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  host:
    description:
      - IP address or IPv6 address of the RADIUS server.
    type: str
    required: true
  auth_port:
    description:
      - UDP port for RADIUS authentication.
    type: int
  acct_port:
    description:
      - UDP port for RADIUS accounting.
    type: int
  timeout:
    description:
      - Timeout in seconds for waiting for a reply.
    type: int
  retransmit:
    description:
      - Number of retransmission attempts.
    type: int
  key:
    description:
      - Shared secret key. Required when C(state=present).
    type: str
  encryption:
    description:
      - Encryption type for the key (C(0) for plaintext, C(7) for encrypted).
    type: int
    choices: [0, 7]
  state:
    description:
      - C(present) to add the server, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Add RADIUS server with key
  jaydee_io.dlink_dgs1250.aaa_radius_server_host:
    host: 192.168.1.100
    key: mysecret

- name: Add RADIUS server with all options
  jaydee_io.dlink_dgs1250.aaa_radius_server_host:
    host: 192.168.1.100
    auth_port: 1812
    acct_port: 1813
    timeout: 5
    retransmit: 3
    key: mysecret
    encryption: 7

- name: Remove RADIUS server
  jaydee_io.dlink_dgs1250.aaa_radius_server_host:
    host: 192.168.1.100
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


# ---------------------------------------------------------------------------
# Command builder
# ---------------------------------------------------------------------------

def _build_commands(host, auth_port, acct_port, timeout, retransmit, key, encryption, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["no radius-server host %s" % host]

    cmd = "radius-server host %s" % host
    if auth_port is not None:
        cmd += " auth-port %s" % auth_port
    if acct_port is not None:
        cmd += " acct-port %s" % acct_port
    if timeout is not None:
        cmd += " timeout %s" % timeout
    if retransmit is not None:
        cmd += " retransmit %s" % retransmit
    if encryption is not None:
        cmd += " key %s %s" % (encryption, key)
    else:
        cmd += " key %s" % key
    return [cmd]


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(type="str", required=True),
            auth_port=dict(type="int"),
            acct_port=dict(type="int"),
            timeout=dict(type="int"),
            retransmit=dict(type="int"),
            key=dict(type="str", no_log=True),
            encryption=dict(type="int", choices=[0, 7]),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["key"]),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["host"],
        module.params["auth_port"],
        module.params["acct_port"],
        module.params["timeout"],
        module.params["retransmit"],
        module.params["key"],
        module.params["encryption"],
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
