#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: show_mac_address_table_notification_change
short_description: Display MAC address notification configuration on a D-Link DGS-1250 switch
description:
  - Executes the C(show mac-address-table notification change) CLI command on a D-Link DGS-1250 switch.
  - Displays MAC address notification configuration or history content.
  - Corresponds to CLI command described in chapter 28-10 of the DGS-1250 CLI Reference Guide.
version_added: "0.11.0"
author:
  - Jérôme Dumesnil
options:
  interface_id:
    description:
      - Optional interface ID to display notification information for.
    type: str
  history:
    description:
      - If C(true), display the MAC address notification change history.
    type: bool
    default: false
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Display global MAC notification configuration
  jaydee_io.dlink_dgs1250.show_mac_address_table_notification_change:
  register: result

- name: Display MAC notification configuration for all interfaces
  jaydee_io.dlink_dgs1250.show_mac_address_table_notification_change:
    interface_id: ""
  register: result

- name: Display MAC notification history
  jaydee_io.dlink_dgs1250.show_mac_address_table_notification_change:
    history: true
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


def _build_command(interface_id, history):
    cmd = "show mac-address-table notification change"
    if history:
        cmd += " history"
    elif interface_id is not None:
        cmd += " interface"
        if interface_id:
            cmd += " %s" % interface_id
    return cmd


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface_id=dict(type="str"),
            history=dict(type="bool", default=False),
        ),
        supports_check_mode=True,
    )
    command = _build_command(module.params["interface_id"], module.params["history"])
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
