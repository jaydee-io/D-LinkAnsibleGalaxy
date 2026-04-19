#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: dhcp_relay_info_format_remote_id
short_description: Configure DHCP relay information option format remote-id on a D-Link DGS-1250 switch
description:
  - Configures the C(ip dhcp relay information option format remote-id) CLI command on a D-Link DGS-1250 switch.
  - Sets or removes the remote-id format for DHCP relay Option 82.
  - Corresponds to CLI command described in chapter 16-10 of the DGS-1250 CLI Reference Guide.
version_added: "0.9.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  format:
    description:
      - The remote-id format to use. Required when C(state=present).
    type: str
    choices: [default, string, vendor2, vendor3]
  string_value:
    description:
      - The string value when C(format=string).
    type: str
  state:
    description:
      - C(present) to set the format, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set remote-id format to default
  jaydee_io.dlink_dgs1250.dhcp_relay_info_format_remote_id:
    format: default

- name: Set remote-id format to a custom string
  jaydee_io.dlink_dgs1250.dhcp_relay_info_format_remote_id:
    format: string
    string_value: MY-SWITCH

- name: Set remote-id format to vendor3
  jaydee_io.dlink_dgs1250.dhcp_relay_info_format_remote_id:
    format: vendor3

- name: Remove remote-id format configuration
  jaydee_io.dlink_dgs1250.dhcp_relay_info_format_remote_id:
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


def _build_commands(fmt, string_value, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["no ip dhcp relay information option format remote-id"]
    if fmt == "string":
        return ["ip dhcp relay information option format remote-id string %s" % string_value]
    return ["ip dhcp relay information option format remote-id %s" % fmt]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            format=dict(type="str", choices=["default", "string", "vendor2", "vendor3"]),
            string_value=dict(type="str"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["format"]),
            ("format", "string", ["string_value"]),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["format"],
        module.params["string_value"],
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
