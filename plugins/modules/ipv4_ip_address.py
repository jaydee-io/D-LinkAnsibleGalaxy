#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: ipv4_ip_address
short_description: Configure an IP address on an interface of a D-Link DGS-1250 switch
description:
  - Configures the C(ip address) CLI command on a D-Link DGS-1250 switch.
  - Assigns a static IP address or enables DHCP on a specific interface.
  - Corresponds to CLI command described in chapter 9-4 of the DGS-1250 CLI Reference Guide.
version_added: "0.6.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Interface on which to configure the IP address (e.g. C(vlan1)).
    type: str
    required: true
  ip_address:
    description:
      - IP address to assign to the interface. Mutually exclusive with C(dhcp).
    type: str
  subnet_mask:
    description:
      - Subnet mask for the IP address. Required together with C(ip_address).
    type: str
  dhcp:
    description:
      - When C(true), use DHCP to obtain an IP address. Mutually exclusive with C(ip_address).
    type: bool
    default: false
  state:
    description:
      - C(present) to configure the address, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
"""

EXAMPLES = r"""
- name: Set a static IP address on vlan1
  jaydee_io.dlink_dgs1250.ipv4_ip_address:
    interface: vlan1
    ip_address: 10.90.90.90
    subnet_mask: 255.0.0.0

- name: Enable DHCP on vlan1
  jaydee_io.dlink_dgs1250.ipv4_ip_address:
    interface: vlan1
    dhcp: true

- name: Remove a static IP address
  jaydee_io.dlink_dgs1250.ipv4_ip_address:
    interface: vlan1
    ip_address: 10.90.90.90
    subnet_mask: 255.0.0.0
    state: absent

- name: Remove DHCP configuration
  jaydee_io.dlink_dgs1250.ipv4_ip_address:
    interface: vlan1
    dhcp: true
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


def _build_commands(interface, ip_address, subnet_mask, dhcp, state):
    """Build the CLI command list."""
    prefix = "no " if state == "absent" else ""
    if dhcp:
        return ["interface %s" % interface, "%sip address dhcp" % prefix, "exit"]
    return ["interface %s" % interface, "%sip address %s %s" % (prefix, ip_address, subnet_mask), "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            ip_address=dict(type="str"),
            subnet_mask=dict(type="str"),
            dhcp=dict(type="bool", default=False),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        mutually_exclusive=[
            ("ip_address", "dhcp"),
        ],
        required_if=[
            ("dhcp", False, ["ip_address", "subnet_mask"], True),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["interface"],
        module.params["ip_address"],
        module.params["subnet_mask"],
        module.params["dhcp"],
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
