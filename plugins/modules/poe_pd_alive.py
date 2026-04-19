#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: poe_pd_alive
short_description: Configure PoE PD alive check on an interface on a D-Link DGS-1250 switch
description:
  - Configures the C(poe pd alive) CLI command on a D-Link DGS-1250 switch.
  - Configures the PD alive check function (ping) for a PoE port.
  - Corresponds to CLI command described in chapter 51-11 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - The PoE interface to configure (e.g. C(eth1/0/1)).
    type: str
    required: true
  ip:
    description:
      - The IPv4 address of the target PD.
    type: str
  interval:
    description:
      - Interval in seconds between ping requests (10-300).
    type: int
  retry:
    description:
      - Retry count of ping requests (0-5).
    type: int
  waiting_time:
    description:
      - Waiting time in seconds for PD to recover from rebooting (30-300).
    type: int
  action:
    description:
      - Action when the PD does not respond.
    type: str
    choices: [reset, notify, both]
  state:
    description:
      - C(enabled) to enable the PD alive check, C(disabled) to disable.
      - When parameters (ip, interval, retry, waiting_time, action) are set, the matching sub-parameter is applied;
        when C(state=disabled) with a sub-parameter set, that sub-parameter is reverted to default.
    type: str
    choices: [enabled, disabled]
    default: enabled
notes:
  - This command runs in Interface Configuration Mode.
  - Only applies to DGS-1250-28XMP and DGS-1250-52XMP models.
"""

EXAMPLES = r"""
- name: Enable PoE PD alive check
  jaydee_io.dlink_dgs1250.poe_pd_alive:
    interface: eth1/0/1

- name: Configure target IP
  jaydee_io.dlink_dgs1250.poe_pd_alive:
    interface: eth1/0/1
    ip: 192.168.1.150

- name: Configure interval
  jaydee_io.dlink_dgs1250.poe_pd_alive:
    interface: eth1/0/1
    interval: 60

- name: Configure action
  jaydee_io.dlink_dgs1250.poe_pd_alive:
    interface: eth1/0/1
    action: reset

- name: Disable PoE PD alive check
  jaydee_io.dlink_dgs1250.poe_pd_alive:
    interface: eth1/0/1
    state: disabled
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


def _build_commands(interface, ip, interval, retry, waiting_time, action, state):
    commands = ["interface %s" % interface]
    prefix = "no " if state == "disabled" else ""
    if ip is not None:
        commands.append("%spoe pd alive ip %s" % (prefix, ip)
                        if state == "enabled" else "no poe pd alive ip")
    elif interval is not None:
        commands.append("poe pd alive interval %d" %
                        interval if state == "enabled" else "no poe pd alive interval")
    elif retry is not None:
        commands.append("poe pd alive retry %d" %
                        retry if state == "enabled" else "no poe pd alive retry")
    elif waiting_time is not None:
        commands.append("poe pd alive waiting-time %d" %
                        waiting_time if state == "enabled" else "no poe pd alive waiting-time")
    elif action is not None:
        commands.append("poe pd alive action %s" %
                        action if state == "enabled" else "no poe pd alive action")
    else:
        commands.append("poe pd alive" if state ==
                        "enabled" else "no poe pd alive")
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            ip=dict(type="str"),
            interval=dict(type="int"),
            retry=dict(type="int"),
            waiting_time=dict(type="int"),
            action=dict(type="str", choices=["reset", "notify", "both"]),
            state=dict(type="str", choices=[
                       "enabled", "disabled"], default="enabled"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["interface"],
        module.params["ip"],
        module.params["interval"],
        module.params["retry"],
        module.params["waiting_time"],
        module.params["action"],
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
