#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: snmp_trap_mac_notification_change
short_description: Enable MAC address change notification trap on an interface on a D-Link DGS-1250 switch
description:
  - Enables or disables the MAC address change notification on a specific interface using the
    C(snmp trap mac-notification change) CLI command.
  - Corresponds to CLI command described in chapter 28-13 of the DGS-1250 CLI Reference Guide.
version_added: "0.11.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface_id:
    description:
      - The interface to configure (e.g. C(eth1/0/2)).
    type: str
    required: true
  added:
    description:
      - Enable notification when a MAC address is added on the interface.
    type: bool
  removed:
    description:
      - Enable notification when a MAC address is removed from the interface.
    type: bool
  state:
    description:
      - C(present) enables the notification trap.
      - C(absent) disables (reverts) the notification trap.
    type: str
    default: present
    choices: [present, absent]
notes:
  - This command runs in Interface Configuration Mode.
  - The C(mac-address-table notification change) command must be enabled globally for notifications
    to be sent.
"""

EXAMPLES = r"""
- name: Enable MAC added notification trap on port 2
  jaydee_io.dlink_dgs1250.snmp_trap_mac_notification_change:
    interface_id: eth1/0/2
    added: true
    state: present

- name: Enable MAC removed notification trap on port 2
  jaydee_io.dlink_dgs1250.snmp_trap_mac_notification_change:
    interface_id: eth1/0/2
    removed: true
    state: present
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


def _build_commands(interface_id, added, removed, state):
    cmds = ["interface %s" % interface_id]
    prefix = "no " if state == "absent" else ""
    if added:
        cmds.append("%ssnmp trap mac-notification change added" % prefix)
    if removed:
        cmds.append("%ssnmp trap mac-notification change removed" % prefix)
    if not added and not removed:
        cmds.append("%ssnmp trap mac-notification change" % prefix)
    cmds.append("exit")
    return cmds


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface_id=dict(type="str", required=True),
            added=dict(type="bool"),
            removed=dict(type="bool"),
            state=dict(type="str", default="present",
                       choices=["present", "absent"]),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["interface_id"],
        module.params["added"],
        module.params["removed"],
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
