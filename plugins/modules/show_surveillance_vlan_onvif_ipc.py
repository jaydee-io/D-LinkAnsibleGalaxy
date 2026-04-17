#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: show_surveillance_vlan_onvif_ipc
short_description: Display ONVIF IPC information on a D-Link DGS-1250 switch
description:
  - Executes the C(show surveillance vlan onvif-ipc interface) CLI command on a D-Link DGS-1250 switch.
  - Displays brief or detailed ONVIF-based IP camera information.
  - Corresponds to CLI command described in chapter 63-11 of the DGS-1250 CLI Reference Guide.
version_added: "0.18.0"
author:
  - Jérôme Dumesnil
options:
  interface:
    description:
      - The interface(s) to display (e.g. C(eth1/0/1)).
    type: str
  detail_level:
    description:
      - The level of detail to display.
    type: str
    required: true
    choices: [brief, detail]
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Display brief ONVIF IPC info on port 1
  jaydee_io.dlink_dgs1250.show_surveillance_vlan_onvif_ipc:
    interface: eth1/0/1
    detail_level: brief
  register: result

- name: Display detailed ONVIF IPC info
  jaydee_io.dlink_dgs1250.show_surveillance_vlan_onvif_ipc:
    detail_level: detail
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


def _build_command(interface, detail_level):
    cmd = "show surveillance vlan onvif-ipc interface"
    if interface is not None:
        cmd += " %s" % interface
    cmd += " %s" % detail_level
    return cmd



def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str"),
            detail_level=dict(type="str", required=True, choices=["brief", "detail"]),
        ),
        supports_check_mode=True,
    )
    command = _build_command(module.params["interface"], module.params["detail_level"])
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
