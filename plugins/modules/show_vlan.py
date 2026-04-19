#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: show_vlan
short_description: Display VLAN information on a D-Link DGS-1250 switch
description:
  - Executes the C(show vlan) CLI command on a D-Link DGS-1250 switch.
  - Displays VLAN parameters and member ports.
  - Corresponds to CLI command described in chapter 70-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.19.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  vlan_id:
    description:
      - VLAN ID or range to display (e.g. C(100), C(100-200)).
    type: str
  interface:
    description:
      - Interface(s) to display VLAN settings for (e.g. C(eth1/0/1), C(eth1/0/1-2)).
    type: str
notes:
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Display all VLANs
  jaydee_io.dlink_dgs1250.show_vlan:
  register: result

- name: Display VLAN 100
  jaydee_io.dlink_dgs1250.show_vlan:
    vlan_id: "100"
  register: result

- name: Display VLAN settings for port 1
  jaydee_io.dlink_dgs1250.show_vlan:
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
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


def _build_command(vlan_id, interface):
    cmd = "show vlan"
    if vlan_id is not None:
        cmd += " %s" % vlan_id
    elif interface is not None:
        cmd += " interface %s" % interface
    return cmd


def main():
    module = AnsibleModule(
        argument_spec=dict(
            vlan_id=dict(type="str"),
            interface=dict(type="str"),
        ),
        mutually_exclusive=[["vlan_id", "interface"]],
        supports_check_mode=True,
    )
    command = _build_command(
        module.params["vlan_id"], module.params["interface"])
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
