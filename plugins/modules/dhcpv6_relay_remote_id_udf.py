#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dhcpv6_relay_remote_id_udf
short_description: Configure DHCPv6 relay remote-id UDF on a D-Link DGS-1250 switch
description:
  - Configures the C(ipv6 dhcp relay remote-id udf) CLI command on a D-Link DGS-1250 switch.
  - Sets or removes the User Define Field (UDF) for the remote ID.
  - Corresponds to CLI command described in chapter 20-9 of the DGS-1250 CLI Reference Guide.
version_added: "0.9.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  value:
    description:
      - The UDF string value. Required when C(state=present).
    type: str
  hex:
    description:
      - If C(true), the value is specified as a hexadecimal string.
    type: bool
    default: false
  state:
    description:
      - C(present) to set, C(absent) to remove.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set DHCPv6 relay remote-id UDF to ASCII string
  jaydee_io.dlink_dgs1250.dhcpv6_relay_remote_id_udf:
    value: PARADISE001

- name: Set DHCPv6 relay remote-id UDF to hex string
  jaydee_io.dlink_dgs1250.dhcpv6_relay_remote_id_udf:
    value: "010c08"
    hex: true

- name: Remove DHCPv6 relay remote-id UDF
  jaydee_io.dlink_dgs1250.dhcpv6_relay_remote_id_udf:
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


def _build_commands(value, hex_mode, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["no ipv6 dhcp relay remote-id udf"]
    if hex_mode:
        return ["ipv6 dhcp relay remote-id udf hex %s" % value]
    return ["ipv6 dhcp relay remote-id udf ascii %s" % value]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            value=dict(type="str"),
            hex=dict(type="bool", default=False),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["value"])],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["value"],
        module.params["hex"],
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
