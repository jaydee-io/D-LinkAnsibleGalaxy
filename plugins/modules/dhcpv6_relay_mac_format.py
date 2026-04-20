#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dhcpv6_relay_mac_format
short_description: Configure DHCPv6 relay MAC address format on a D-Link DGS-1250 switch
description:
  - Configures the C(ipv6 dhcp relay information option mac-format case) CLI command on a D-Link DGS-1250 switch.
  - Sets or resets the MAC address format for DHCPv6 Option 18/37 profiles.
  - Corresponds to CLI command described in chapter 20-7 of the DGS-1250 CLI Reference Guide.
version_added: "0.9.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  case:
    description:
      - The MAC address case format. Required when C(state=present).
    type: str
    choices: [lowercase, uppercase]
  delimiter:
    description:
      - The MAC address delimiter. Required when C(state=present).
    type: str
    choices: [hyphen, colon, dot, none]
  number:
    description:
      - The delimiter number value.
    type: int
    choices: [1, 2, 5]
  state:
    description:
      - C(present) to set, C(absent) to revert to default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set DHCPv6 relay MAC format
  jaydee_io.dlink_dgs1250.dhcpv6_relay_mac_format:
    case: uppercase
    delimiter: hyphen
    number: 5

- name: Reset DHCPv6 relay MAC format
  jaydee_io.dlink_dgs1250.dhcpv6_relay_mac_format:
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


def _build_commands(case, delimiter, number, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["no ipv6 dhcp relay information option mac-format case"]
    cmd = "ipv6 dhcp relay information option mac-format case %s delimiter %s" % (
        case, delimiter)
    if number is not None:
        cmd += " number %d" % number
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            case=dict(type="str", choices=["lowercase", "uppercase"]),
            delimiter=dict(type="str", choices=[
                           "hyphen", "colon", "dot", "none"]),
            number=dict(type="int", choices=[1, 2, 5]),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["case", "delimiter"])],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["case"],
        module.params["delimiter"],
        module.params["number"],
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
