#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: speed
short_description: Configure port speed on a D-Link DGS-1250 switch interface
description:
  - Configures the C(speed) CLI command on a D-Link DGS-1250 switch interface.
  - Sets the port speed to 10, 100, 1000, 10giga, or auto.
  - Corresponds to CLI command described in chapter 64-4 of the DGS-1250 CLI Reference Guide.
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
  speed:
    description:
      - The speed to set. Use C(auto) for auto-negotiation.
    type: str
    choices: ["10", "100", "1000", "10giga", "auto"]
  master_slave:
    description:
      - For 1000BASE-T, set as master or slave. Only applicable with speed=1000.
    type: str
    choices: [master, slave]
  speed_list:
    description:
      - For auto mode, list of speeds to advertise (e.g. C(10,100)).
    type: str
  state:
    description:
      - C(present) to set the speed, C(absent) to revert to default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Set speed to auto on port 1
  jaydee_io.dlink_dgs1250.speed:
    interface: eth1/0/1
    speed: auto

- name: Set speed to auto with specific speeds
  jaydee_io.dlink_dgs1250.speed:
    interface: eth1/0/1
    speed: auto
    speed_list: "10,100"

- name: Set speed to 1000 master
  jaydee_io.dlink_dgs1250.speed:
    interface: eth1/0/1
    speed: "1000"
    master_slave: master

- name: Revert speed to default
  jaydee_io.dlink_dgs1250.speed:
    interface: eth1/0/1
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


def _build_commands(interface, speed, master_slave, speed_list, state):
    commands = ["interface %s" % interface]
    if state == "absent":
        commands.append("no speed")
    else:
        cmd = "speed %s" % speed
        if speed == "1000" and master_slave is not None:
            cmd += " %s" % master_slave
        if speed == "auto" and speed_list is not None:
            cmd += " %s" % speed_list
        commands.append(cmd)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            speed=dict(type="str", choices=[
                       "10", "100", "1000", "10giga", "auto"]),
            master_slave=dict(type="str", choices=["master", "slave"]),
            speed_list=dict(type="str"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["interface"], module.params["speed"],
                               module.params["master_slave"], module.params["speed_list"], module.params["state"])
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
