#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: rmon_alarm
short_description: Configure an RMON alarm entry on a D-Link DGS-1250 switch
description:
  - Configures the C(rmon alarm) CLI command on a D-Link DGS-1250 switch.
  - Configures an alarm entry to monitor a variable via RMON.
  - Corresponds to CLI command described in chapter 55-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
author:
  - Jérôme Dumesnil
options:
  index:
    description:
      - Alarm index (1-65535).
    type: int
    required: true
  variable:
    description:
      - OID of the variable to sample. Required when C(state=present).
    type: str
  interval:
    description:
      - Sampling interval in seconds (1-2147483647). Required when C(state=present).
    type: int
  sample_type:
    description:
      - Sampling type.
    type: str
    choices: [delta, absolute]
  rising_threshold:
    description:
      - Rising threshold value (0-2147483647). Required when C(state=present).
    type: int
  rising_event:
    description:
      - Index of the event entry for rising threshold notification (1-65535).
    type: int
  falling_threshold:
    description:
      - Falling threshold value (0-2147483647). Required when C(state=present).
    type: int
  falling_event:
    description:
      - Index of the event entry for falling threshold notification (1-65535).
    type: int
  owner:
    description:
      - Owner string (max 127 characters).
    type: str
  state:
    description:
      - C(present) to configure the alarm, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Create RMON alarm
  jaydee_io.dlink_dgs1250.rmon_alarm:
    index: 783
    variable: "1.3.6.1.2.1.2.2.1.12.6"
    interval: 30
    sample_type: delta
    rising_threshold: 20
    rising_event: 1
    falling_threshold: 10
    falling_event: 1
    owner: Name

- name: Remove RMON alarm
  jaydee_io.dlink_dgs1250.rmon_alarm:
    index: 783
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


def _build_commands(index, variable, interval, sample_type, rising_threshold,
                    rising_event, falling_threshold, falling_event, owner, state):
    if state == "absent":
        return ["no rmon alarm %d" % index]
    cmd = "rmon alarm %d %s %d %s rising-threshold %d" % (
        index, variable, interval, sample_type, rising_threshold)
    if rising_event is not None:
        cmd += " %d" % rising_event
    cmd += " falling-threshold %d" % falling_threshold
    if falling_event is not None:
        cmd += " %d" % falling_event
    if owner:
        cmd += " owner %s" % owner
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            index=dict(type="int", required=True),
            variable=dict(type="str"),
            interval=dict(type="int"),
            sample_type=dict(type="str", choices=["delta", "absolute"]),
            rising_threshold=dict(type="int"),
            rising_event=dict(type="int"),
            falling_threshold=dict(type="int"),
            falling_event=dict(type="int"),
            owner=dict(type="str"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["variable", "interval", "sample_type",
                                   "rising_threshold", "falling_threshold"]),
        ],
        supports_check_mode=True,
    )
    p = module.params
    commands = _build_commands(
        p["index"], p["variable"], p["interval"], p["sample_type"],
        p["rising_threshold"], p["rising_event"],
        p["falling_threshold"], p["falling_event"],
        p["owner"], p["state"],
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
