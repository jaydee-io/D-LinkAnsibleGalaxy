#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: aaa_client
short_description: Configure a RADIUS dynamic authorization client on a D-Link DGS-1250 switch
description:
  - Configures the C(client) CLI command in Dynamic Authorization Local Server Config Mode
    on a D-Link DGS-1250 switch.
  - Adds or removes a RADIUS dynamic authorization client.
  - Corresponds to CLI command described in chapter 8-11 of the DGS-1250 CLI Reference Guide.
version_added: "0.6.0"
author:
  - Jérôme Dumesnil
options:
  host:
    description:
      - IP address or hostname of the client.
    type: str
    required: true
  server_key:
    description:
      - Shared secret key for the client.
    type: str
    required: true
  encryption:
    description:
      - Encryption type for the key (C(0) for plaintext, C(7) for encrypted).
    type: int
    choices: [0, 7]
  state:
    description:
      - C(present) to add the client, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Dynamic Authorization Local Server Config Mode.
"""

EXAMPLES = r"""
- name: Add a dynamic authorization client
  jaydee_io.dlink_dgs1250.aaa_client:
    host: 192.168.1.100
    server_key: mysecret

- name: Add a client with encrypted key
  jaydee_io.dlink_dgs1250.aaa_client:
    host: 192.168.1.100
    server_key: mysecret
    encryption: 7

- name: Remove a dynamic authorization client
  jaydee_io.dlink_dgs1250.aaa_client:
    host: 192.168.1.100
    server_key: mysecret
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

def _build_commands(host, server_key, encryption, state):
    """Build the CLI command list."""
    if encryption is not None:
        key_part = "server-key %s %s" % (encryption, server_key)
    else:
        key_part = "server-key %s" % server_key

    prefix = "no " if state == "absent" else ""
    cmd = "%sclient %s %s" % (prefix, host, key_part)
    return ["aaa server radius dynamic-author", cmd, "exit"]


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(type="str", required=True),
            server_key=dict(type="str", required=True, no_log=True),
            encryption=dict(type="int", choices=[0, 7]),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["host"],
        module.params["server_key"],
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
