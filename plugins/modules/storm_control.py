#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: storm_control
short_description: Configure storm control on a D-Link DGS-1250 switch interface
description:
  - Configures the C(storm-control) CLI command on a D-Link DGS-1250 switch interface.
  - Sets broadcast, multicast, or unicast storm control thresholds and action.
  - Corresponds to CLI command described in chapter 62-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.18.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - The interface to configure (e.g. C(eth1/0/1)).
    type: str
    required: true
  traffic_type:
    description:
      - The traffic type to configure. Mutually exclusive with C(action).
    type: str
    choices: [broadcast, multicast, unicast]
  level_mode:
    description:
      - The level mode for the threshold. Required when C(traffic_type) is specified.
    type: str
    choices: [pps, kbps, percent]
  rise:
    description:
      - The rise threshold value. Required when C(traffic_type) is specified.
    type: int
  low:
    description:
      - The low threshold value. If not specified, defaults to 80%% of rise.
    type: int
  action:
    description:
      - The action to take when a storm is detected. Mutually exclusive with C(traffic_type).
    type: str
    choices: [shutdown, drop, none]
  state:
    description:
      - C(present) to set the configuration, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Set broadcast storm control to 500 pps on port 1
  jaydee_io.dlink_dgs1250.storm_control:
    interface: eth1/0/1
    traffic_type: broadcast
    level_mode: pps
    rise: 500

- name: Set broadcast storm control to 70%/60% on port 2
  jaydee_io.dlink_dgs1250.storm_control:
    interface: eth1/0/2
    traffic_type: broadcast
    level_mode: percent
    rise: 70
    low: 60

- name: Set storm control action to shutdown on port 1
  jaydee_io.dlink_dgs1250.storm_control:
    interface: eth1/0/1
    action: shutdown

- name: Remove broadcast storm control on port 1
  jaydee_io.dlink_dgs1250.storm_control:
    interface: eth1/0/1
    traffic_type: broadcast
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


def _build_commands(interface, traffic_type, level_mode, rise, low, action, state):
    commands = ["interface %s" % interface]
    if action is not None:
        if state == "absent":
            commands.append("no storm-control action")
        else:
            commands.append("storm-control action %s" % action)
    elif traffic_type is not None:
        if state == "absent":
            commands.append("no storm-control %s" % traffic_type)
        else:
            if level_mode == "pps":
                cmd = "storm-control %s level pps %d" % (traffic_type, rise)
            elif level_mode == "kbps":
                cmd = "storm-control %s level kbps %d" % (traffic_type, rise)
            else:
                cmd = "storm-control %s level %d" % (traffic_type, rise)
            if low is not None:
                cmd += " %d" % low
            commands.append(cmd)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            traffic_type=dict(type="str", choices=[
                              "broadcast", "multicast", "unicast"]),
            level_mode=dict(type="str", choices=["pps", "kbps", "percent"]),
            rise=dict(type="int"),
            low=dict(type="int"),
            action=dict(type="str", choices=["shutdown", "drop", "none"]),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["interface"], module.params["traffic_type"], module.params["level_mode"],
                               module.params["rise"], module.params["low"], module.params["action"], module.params["state"])
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
