#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dhcpv6_relay_format_string
short_description: Configure DHCPv6 relay profile format string on a D-Link DGS-1250 switch
description:
  - Configures the C(format string) CLI command in DHCPv6 Profile Configuration Mode on a D-Link DGS-1250 switch.
  - Sets or removes the format string entry for a DHCPv6 relay profile.
  - Corresponds to CLI command described in chapter 20-6 of the DGS-1250 CLI Reference Guide.
version_added: "0.9.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  profile:
    description:
      - The DHCPv6 relay remote-id profile name.
    type: str
    required: true
  value:
    description:
      - The format string value. Required when C(state=present).
    type: str
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
- name: Set format string for a DHCPv6 relay profile
  jaydee_io.dlink_dgs1250.dhcpv6_relay_format_string:
    profile: profile1
    value: "%port\\:%sysname:%05svlan"

- name: Remove format string from a DHCPv6 relay profile
  jaydee_io.dlink_dgs1250.dhcpv6_relay_format_string:
    profile: profile1
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


def _build_commands(profile, value, state):
    """Build the CLI command list."""
    commands = ["ipv6 dhcp relay remote-id profile %s" % profile]
    if state == "absent":
        commands.append("no format string")
    else:
        commands.append("format string %s" % value)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            profile=dict(type="str", required=True),
            value=dict(type="str"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["value"])],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["profile"],
        module.params["value"],
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
