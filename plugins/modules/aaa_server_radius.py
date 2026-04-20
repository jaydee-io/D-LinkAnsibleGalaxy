#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: aaa_server_radius
short_description: Add or remove a server from a RADIUS group on a D-Link DGS-1250 switch
description:
  - Configures the C(server) CLI command in RADIUS Group Server Config Mode
    on a D-Link DGS-1250 switch.
  - Adds or removes a RADIUS server address from a server group.
  - Corresponds to CLI command described in chapter 8-24 of the DGS-1250 CLI Reference Guide.
version_added: "0.6.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  group_name:
    description:
      - Name of the RADIUS server group.
    type: str
    required: true
  address:
    description:
      - IP or IPv6 address of the RADIUS server.
    type: str
    required: true
  state:
    description:
      - C(present) to add the server, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in RADIUS Group Server Config Mode.
"""

EXAMPLES = r"""
- name: Add server to RADIUS group
  jaydee_io.dlink_dgs1250.aaa_server_radius:
    group_name: my_group
    address: 192.168.1.100

- name: Remove server from RADIUS group
  jaydee_io.dlink_dgs1250.aaa_server_radius:
    group_name: my_group
    address: 192.168.1.100
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


# ---------------------------------------------------------------------------
# Command builder
# ---------------------------------------------------------------------------

def _build_commands(group_name, address, state):
    """Build the CLI command list."""
    prefix = "no " if state == "absent" else ""
    return [
        "aaa group server radius %s" % group_name,
        "%sserver %s" % (prefix, address),
        "exit",
    ]


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            group_name=dict(type="str", required=True),
            address=dict(type="str", required=True),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["group_name"],
        module.params["address"],
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
