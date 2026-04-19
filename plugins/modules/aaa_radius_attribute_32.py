#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: aaa_radius_attribute_32
short_description: Configure RADIUS attribute 32 on a D-Link DGS-1250 switch
description:
  - Configures the C(radius-server attribute 32 include-in-access-req) CLI command
    on a D-Link DGS-1250 switch.
  - Sets or removes the NAS-Identifier (attribute 32) included in RADIUS Access-Request packets.
  - Corresponds to CLI command described in chapter 8-19 of the DGS-1250 CLI Reference Guide.
version_added: "0.6.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  value:
    description:
      - The NAS-Identifier string to include in Access-Request packets.
      - Required when C(state=present).
    type: str
  state:
    description:
      - C(present) to set the attribute, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set RADIUS attribute 32
  jaydee_io.dlink_dgs1250.aaa_radius_attribute_32:
    value: my-switch

- name: Remove RADIUS attribute 32
  jaydee_io.dlink_dgs1250.aaa_radius_attribute_32:
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


# ---------------------------------------------------------------------------
# Command builder
# ---------------------------------------------------------------------------

def _build_commands(value, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["no radius-server attribute 32 include-in-access-req"]
    return ["radius-server attribute 32 include-in-access-req %s" % value]


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            value=dict(type="str"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["value"]),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(module.params["value"], module.params["state"])

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
