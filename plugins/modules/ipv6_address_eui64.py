#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: ipv6_address_eui64
short_description: Configure an IPv6 EUI-64 address on an interface of a D-Link DGS-1250 switch
description:
  - Configures the C(ipv6 address eui-64) CLI command on a D-Link DGS-1250 switch.
  - Assigns an IPv6 address using EUI-64 interface identifier on a specific interface.
  - Corresponds to CLI command described in chapter 10-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.7.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Interface on which to configure the IPv6 EUI-64 address (e.g. C(vlan1)).
    type: str
    required: true
  ipv6_prefix:
    description:
      - IPv6 prefix to use with EUI-64.
    type: str
    required: true
  prefix_length:
    description:
      - Prefix length for the IPv6 prefix.
    type: int
    required: true
  state:
    description:
      - C(present) to configure the address, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
"""

EXAMPLES = r"""
- name: Set an IPv6 EUI-64 address on vlan1
  jaydee_io.dlink_dgs1250.ipv6_address_eui64:
    interface: vlan1
    ipv6_prefix: "2001:db8::"
    prefix_length: 64

- name: Remove an IPv6 EUI-64 address
  jaydee_io.dlink_dgs1250.ipv6_address_eui64:
    interface: vlan1
    ipv6_prefix: "2001:db8::"
    prefix_length: 64
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


def _build_commands(interface, ipv6_prefix, prefix_length, state):
    """Build the CLI command list."""
    prefix = "no " if state == "absent" else ""
    cmd = "%sipv6 address %s/%d eui-64" % (prefix, ipv6_prefix, prefix_length)
    return ["interface %s" % interface, cmd, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            ipv6_prefix=dict(type="str", required=True),
            prefix_length=dict(type="int", required=True),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["interface"],
        module.params["ipv6_prefix"],
        module.params["prefix_length"],
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
