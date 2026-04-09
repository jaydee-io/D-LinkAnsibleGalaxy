#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: aaa_tacacs_server_host
short_description: Configure a TACACS+ server host on a D-Link DGS-1250 switch
description:
  - Configures the C(tacacs-server host) CLI command on a D-Link DGS-1250 switch.
  - Adds or removes a TACACS+ server host with optional parameters.
  - Corresponds to CLI command described in chapter 8-27 of the DGS-1250 CLI Reference Guide.
version_added: "0.6.0"
author:
  - Jérôme Dumesnil
options:
  host:
    description:
      - IP address or IPv6 address of the TACACS+ server.
    type: str
    required: true
  port:
    description:
      - TCP port for TACACS+ communication.
    type: int
  timeout:
    description:
      - Timeout in seconds for waiting for a reply.
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
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Add TACACS+ server with key
  jaydee_io.dlink_dgs1250.aaa_tacacs_server_host:
    host: 192.168.1.200
    key: mysecret

- name: Add TACACS+ server with all options
  jaydee_io.dlink_dgs1250.aaa_tacacs_server_host:
    host: 192.168.1.200
    port: 49
    timeout: 5
    key: mysecret
    encryption: 7

- name: Remove TACACS+ server
  jaydee_io.dlink_dgs1250.aaa_tacacs_server_host:
    host: 192.168.1.200
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


# ---------------------------------------------------------------------------
# Command builder
# ---------------------------------------------------------------------------

def _build_commands(host, port, timeout, key, encryption, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["no tacacs-server host %s" % host]

    cmd = "tacacs-server host %s" % host
    if port is not None:
        cmd += " port %s" % port
    if timeout is not None:
        cmd += " timeout %s" % timeout
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
            port=dict(type="int"),
            timeout=dict(type="int"),
            key=dict(type="str", no_log=True),
            encryption=dict(type="int", choices=[0, 7]),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["key"]),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["host"],
        module.params["port"],
        module.params["timeout"],
        module.params["key"],
        module.params["encryption"],
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
