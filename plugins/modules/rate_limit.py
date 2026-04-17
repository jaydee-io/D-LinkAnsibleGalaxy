#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: rate_limit
short_description: Configure the ingress or egress bandwidth limit on a D-Link DGS-1250 switch interface
description:
  - Configures the C(rate-limit input|output) CLI command on a D-Link DGS-1250 switch.
  - Sets the received or transmitted bandwidth limit for an interface.
  - Corresponds to CLI command described in chapter 54-13 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
author:
  - Jérôme Dumesnil
options:
  interface:
    description:
      - The interface to configure (e.g. C(eth1/0/5)).
    type: str
    required: true
  direction:
    description:
      - Direction to limit (C(input) or C(output)).
    type: str
    required: true
    choices: [input, output]
  kbps:
    description:
      - Bandwidth limit in kbps (mutually exclusive with C(percent)).
    type: int
  percent:
    description:
      - Bandwidth limit as a percentage (1-100) (mutually exclusive with C(kbps)).
    type: int
  burst_size:
    description:
      - Burst traffic limit in Kbytes.
    type: int
  state:
    description:
      - C(present) to set the limit, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Limit input to 2000 kbps, burst 30K on eth1/0/5
  jaydee_io.dlink_dgs1250.rate_limit:
    interface: eth1/0/5
    direction: input
    kbps: 2000
    burst_size: 30

- name: Limit output to 10 percent on eth1/0/5
  jaydee_io.dlink_dgs1250.rate_limit:
    interface: eth1/0/5
    direction: output
    percent: 10

- name: Remove input rate-limit
  jaydee_io.dlink_dgs1250.rate_limit:
    interface: eth1/0/5
    direction: input
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


def _build_commands(interface, direction, kbps, percent, burst_size, state):
    commands = ["interface %s" % interface]
    if state == "absent":
        commands.append("no rate-limit %s" % direction)
    else:
        if percent is not None:
            rate = "percent %d" % percent
        else:
            rate = "%d" % kbps
        cmd = "rate-limit %s %s" % (direction, rate)
        if burst_size is not None:
            cmd += " %d" % burst_size
        commands.append(cmd)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            direction=dict(type="str", required=True, choices=["input", "output"]),
            kbps=dict(type="int"),
            percent=dict(type="int"),
            burst_size=dict(type="int"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        mutually_exclusive=[("kbps", "percent")],
        supports_check_mode=True,
    )
    p = module.params
    if p["state"] == "present" and p["kbps"] is None and p["percent"] is None:
        module.fail_json(msg="Either kbps or percent is required when state=present")
    commands = _build_commands(
        p["interface"], p["direction"],
        p["kbps"], p["percent"], p["burst_size"],
        p["state"],
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
