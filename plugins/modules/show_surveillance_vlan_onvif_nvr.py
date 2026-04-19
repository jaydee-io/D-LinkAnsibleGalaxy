#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: show_surveillance_vlan_onvif_nvr
short_description: Display ONVIF NVR information on a D-Link DGS-1250 switch
description:
  - Executes the C(show surveillance vlan onvif-nvr interface) CLI command on a D-Link DGS-1250 switch.
  - Displays ONVIF-based NVR and group information.
  - Corresponds to CLI command described in chapter 63-12 of the DGS-1250 CLI Reference Guide.
version_added: "0.18.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - The interface(s) to display (e.g. C(eth1/0/1)).
    type: str
  ipc_list:
    description:
      - Display NVR group IPC list information.
    type: bool
    default: false
notes:
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Display ONVIF NVR info on port 1
  jaydee_io.dlink_dgs1250.show_surveillance_vlan_onvif_nvr:
    interface: eth1/0/1
  register: result

- name: Display ONVIF NVR IPC list on port 1
  jaydee_io.dlink_dgs1250.show_surveillance_vlan_onvif_nvr:
    interface: eth1/0/1
    ipc_list: true
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


def _build_command(interface, ipc_list):
    cmd = "show surveillance vlan onvif-nvr interface"
    if interface is not None:
        cmd += " %s" % interface
    if ipc_list:
        cmd += " ipc-list"
    return cmd



def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str"),
            ipc_list=dict(type="bool", default=False),
        ),
        supports_check_mode=True,
    )
    command = _build_command(module.params["interface"], module.params["ipc_list"])
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
