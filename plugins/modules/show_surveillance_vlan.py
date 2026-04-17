#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: show_surveillance_vlan
short_description: Display surveillance VLAN settings on a D-Link DGS-1250 switch
description:
  - Executes the C(show surveillance vlan) CLI command on a D-Link DGS-1250 switch.
  - Displays surveillance VLAN configurations and device information.
  - Corresponds to CLI command described in chapter 63-10 of the DGS-1250 CLI Reference Guide.
version_added: "0.18.0"
author:
  - Jérôme Dumesnil
options:
  device:
    description:
      - Display learned surveillance device information.
    type: bool
    default: false
  interface:
    description:
      - The interface(s) to display (e.g. C(eth1/0/1), C(eth1/0/1-4)).
    type: str
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Display surveillance VLAN global settings
  jaydee_io.dlink_dgs1250.show_surveillance_vlan:
  register: result

- name: Display surveillance VLAN devices
  jaydee_io.dlink_dgs1250.show_surveillance_vlan:
    device: true
  register: result

- name: Display surveillance VLAN on port 1
  jaydee_io.dlink_dgs1250.show_surveillance_vlan:
    interface: eth1/0/1
  register: result
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
        run_command,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


def _build_command(device, interface):
    cmd = "show surveillance vlan"
    if device:
        cmd += " device"
    if interface is not None:
        cmd += " interface %s" % interface
    return cmd



def main():
    module = AnsibleModule(
        argument_spec=dict(
            device=dict(type="bool", default=False),
            interface=dict(type="str"),
        ),
        supports_check_mode=True,
    )
    command = _build_command(module.params["device"], module.params["interface"])
    if module.check_mode:
        module.exit_json(changed=False, commands=[command], raw_output="")
        return
    try:
        raw_output = run_command(module, command)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    module.exit_json(changed=False, raw_output=raw_output, commands=[command])


if __name__ == "__main__":
    main()
