#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: mac_address_table_notification_change
short_description: Configure MAC address notification on a D-Link DGS-1250 switch
description:
  - Enables or configures the MAC address notification function using the
    C(mac-address-table notification change) CLI command.
  - Use C(state=absent) to disable the function or revert optional settings to default.
  - Corresponds to CLI command described in chapter 28-4 of the DGS-1250 CLI Reference Guide.
version_added: "0.11.0"
author:
  - Jérôme Dumesnil
options:
  interval:
    description:
      - Interval in seconds for sending MAC address trap messages (1 to 2147483647).
    type: int
  history_size:
    description:
      - Maximum number of entries in the MAC history notification table (0 to 500).
    type: int
  trap_type:
    description:
      - Whether the trap information includes VLAN ID or not.
    type: str
    choices: [with-vlanid, without-vlanid]
  state:
    description:
      - C(present) enables the MAC address notification function.
      - C(absent) disables the function or reverts settings.
    type: str
    default: present
    choices: [present, absent]
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable MAC address change notification
  jaydee_io.dlink_dgs1250.mac_address_table_notification_change:
    state: present

- name: Configure MAC notification with interval and history size
  jaydee_io.dlink_dgs1250.mac_address_table_notification_change:
    interval: 10
    history_size: 500
    state: present

- name: Disable MAC address change notification
  jaydee_io.dlink_dgs1250.mac_address_table_notification_change:
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
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(interval, history_size, trap_type, state):
    cmds = []
    if state == "absent":
        cmd = "no mac-address-table notification change"
        parts = []
        if interval is not None:
            parts.append("interval")
        if history_size is not None:
            parts.append("history-size")
        if trap_type is not None:
            parts.append("trap-type")
        if parts:
            cmd += " " + " ".join(parts)
        return [cmd]
    cmds.append("mac-address-table notification change")
    if interval is not None:
        cmds.append("mac-address-table notification change interval %d" % interval)
    if history_size is not None:
        cmds.append("mac-address-table notification change history-size %d" % history_size)
    if trap_type is not None:
        cmds.append("mac-address-table notification change trap-type %s" % trap_type)
    return cmds


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interval=dict(type="int"),
            history_size=dict(type="int"),
            trap_type=dict(type="str", choices=["with-vlanid", "without-vlanid"]),
            state=dict(type="str", default="present", choices=["present", "absent"]),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["interval"],
        module.params["history_size"],
        module.params["trap_type"],
        module.params["state"],
    )
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
