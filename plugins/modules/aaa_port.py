#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: aaa_port
short_description: Configure the RADIUS dynamic authorization port on a D-Link DGS-1250 switch
description:
  - Configures the C(port) CLI command in Dynamic Authorization Local Server Config Mode
    on a D-Link DGS-1250 switch.
  - Sets or removes the listening port for RADIUS dynamic authorization.
  - Corresponds to CLI command described in chapter 8-18 of the DGS-1250 CLI Reference Guide.
version_added: "0.6.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  port:
    description:
      - UDP port number for dynamic authorization (1-65535).
      - Required when C(state=present).
    type: int
  state:
    description:
      - C(present) to set the port, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Dynamic Authorization Local Server Config Mode.
"""

EXAMPLES = r"""
- name: Set dynamic authorization port
  jaydee_io.dlink_dgs1250.aaa_port:
    port: 1650

- name: Remove dynamic authorization port
  jaydee_io.dlink_dgs1250.aaa_port:
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

def _build_commands(port, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["aaa server radius dynamic-author", "no port", "exit"]
    return ["aaa server radius dynamic-author", "port %s" % port, "exit"]


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            port=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["port"]),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(module.params["port"], module.params["state"])

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
