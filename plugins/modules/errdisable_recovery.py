#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: errdisable_recovery
short_description: Configure error recovery on a D-Link DGS-1250 switch
description:
  - Configures the error-disable auto-recovery for specified causes and optionally the recovery
    interval using the C(errdisable recovery cause) CLI command.
  - Use C(state=absent) to disable auto-recovery (C(no errdisable recovery cause)).
  - Corresponds to CLI command described in chapter 26-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.11.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  cause:
    description:
      - The cause for which auto-recovery is configured.
    type: str
    required: true
    choices: [all, psecure-violation, storm-control, arp-rate, dhcp-rate, loopback-detect]
  interval:
    description:
      - Recovery interval in seconds (5 to 86400). Default is 300.
      - Only used when C(state=present).
    type: int
  state:
    description:
      - C(present) enables auto-recovery for the cause.
      - C(absent) disables auto-recovery for the cause.
    type: str
    default: present
    choices: [present, absent]
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable auto-recovery for all causes
  jaydee_io.dlink_dgs1250.errdisable_recovery:
    cause: all
    state: present

- name: Enable auto-recovery for port security with 200s interval
  jaydee_io.dlink_dgs1250.errdisable_recovery:
    cause: psecure-violation
    interval: 200
    state: present

- name: Disable auto-recovery for storm-control
  jaydee_io.dlink_dgs1250.errdisable_recovery:
    cause: storm-control
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
        run_commands, is_config_present, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, is_config_present, MODE_GLOBAL_CONFIG


def _build_commands(cause, interval, state):
    if state == "absent":
        return ["no errdisable recovery cause %s" % cause]
    cmd = "errdisable recovery cause %s" % cause
    if interval is not None:
        cmd += " interval %d" % interval
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            cause=dict(type="str", required=True,
                       choices=["all", "psecure-violation", "storm-control",
                                "arp-rate", "dhcp-rate", "loopback-detect"]),
            interval=dict(type="int"),
            state=dict(type="str", default="present",
                       choices=["present", "absent"]),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["cause"],
        module.params["interval"],
        module.params["state"],
    )
    if is_config_present(module, commands):
        module.exit_json(changed=False, commands=[], raw_output="")
        return
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
