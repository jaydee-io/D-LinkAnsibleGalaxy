#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: snmp_server_enable_traps_errdisable
short_description: Enable SNMP notifications for error-disabled state on a D-Link DGS-1250 switch
description:
  - Enables or disables SNMP notifications for the error-disabled state using the
    C(snmp-server enable traps errdisable) CLI command.
  - Corresponds to CLI command described in chapter 26-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.11.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  asserted:
    description:
      - Control notifications when entering the error-disabled state.
    type: bool
  cleared:
    description:
      - Control notifications when exiting the error-disabled state.
    type: bool
  notification_rate:
    description:
      - Maximum number of traps per minute (0 to 1000). 0 means no limit.
    type: int
  state:
    description:
      - C(present) enables the SNMP notifications.
      - C(absent) disables the SNMP notifications.
    type: str
    default: present
    choices: [present, absent]
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable SNMP errdisable traps for asserted and cleared
  jaydee_io.dlink_dgs1250.snmp_server_enable_traps_errdisable:
    asserted: true
    cleared: true
    notification_rate: 3
    state: present

- name: Disable SNMP errdisable traps
  jaydee_io.dlink_dgs1250.snmp_server_enable_traps_errdisable:
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


def _build_commands(asserted, cleared, notification_rate, state):
    if state == "absent":
        cmd = "no snmp-server enable traps errdisable"
        parts = []
        if asserted:
            parts.append("asserted")
        if cleared:
            parts.append("cleared")
        if notification_rate is not None:
            parts.append("notification-rate")
        if parts:
            cmd += " " + " ".join(parts)
        return [cmd]
    cmd = "snmp-server enable traps errdisable"
    if asserted:
        cmd += " asserted"
    if cleared:
        cmd += " cleared"
    if notification_rate is not None:
        cmd += " notification-rate %d" % notification_rate
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            asserted=dict(type="bool"),
            cleared=dict(type="bool"),
            notification_rate=dict(type="int"),
            state=dict(type="str", default="present",
                       choices=["present", "absent"]),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["asserted"],
        module.params["cleared"],
        module.params["notification_rate"],
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
