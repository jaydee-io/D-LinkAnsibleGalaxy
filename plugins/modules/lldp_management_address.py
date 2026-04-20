#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jerome Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: lldp_management_address
short_description: Configure LLDP management address on a D-Link DGS-1250 switch interface
description:
  - Configures the C(lldp management-address) CLI command on a D-Link DGS-1250 switch.
  - Configures the management address advertised on a physical interface.
  - Corresponds to CLI command described in chapter 41-7 of the DGS-1250 CLI Reference Guide.
version_added: "0.14.0"
author:
  - "Jérôme Dumesnil (@jaydee-io)"
options:
  interface:
    description:
      - The interface to configure (e.g. C(eth1/0/1)).
    type: str
    required: true
  address:
    description:
      - The IPv4 or IPv6 management address. Required when C(state=present).
    type: str
  state:
    description:
      - C(present) to set the management address, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Set LLDP management IPv4 address
  jaydee_io.dlink_dgs1250.lldp_management_address:
    interface: eth1/0/1
    address: 10.1.1.1

- name: Remove LLDP management address
  jaydee_io.dlink_dgs1250.lldp_management_address:
    interface: eth1/0/1
    address: 10.1.1.1
    state: absent

- name: Remove all LLDP management addresses
  jaydee_io.dlink_dgs1250.lldp_management_address:
    interface: eth1/0/1
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


def _build_commands(interface, address, state):
    if state == "absent":
        if address:
            cmd = "no lldp management-address %s" % address
        else:
            cmd = "no lldp management-address"
    else:
        cmd = "lldp management-address %s" % address
    return ["interface %s" % interface, cmd, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            address=dict(type="str"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["address"]),
        ],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["interface"], module.params["address"], module.params["state"])
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
