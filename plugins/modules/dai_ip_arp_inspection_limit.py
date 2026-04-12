#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: dai_ip_arp_inspection_limit
short_description: Configure ARP inspection rate limit on a D-Link DGS-1250 switch interface
description:
  - Configures the C(ip arp inspection limit) CLI command on a D-Link DGS-1250 switch.
  - Limits the rate of incoming ARP requests and responses on an interface.
  - Corresponds to CLI command described in chapter 25-5 of the DGS-1250 CLI Reference Guide.
version_added: "0.10.0"
author:
  - Jérôme Dumesnil
options:
  interface:
    description:
      - The interface to configure (e.g. C(eth1/0/10)).
    type: str
    required: true
  rate:
    description:
      - The maximum number of ARP packets per second (1 to 150).
      - Mutually exclusive with C(no_limit).
    type: int
  burst_interval:
    description:
      - The burst duration in seconds (1 to 15). Default is 1.
    type: int
  no_limit:
    description:
      - If C(true), specifies no limit on the ARP packet rate.
    type: bool
    default: false
  state:
    description:
      - C(present) to configure, C(absent) to revert to default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Set ARP inspection rate limit on interface
  jaydee_io.dlink_dgs1250.dai_ip_arp_inspection_limit:
    interface: eth1/0/10
    rate: 30
    burst_interval: 5

- name: Set no ARP inspection rate limit
  jaydee_io.dlink_dgs1250.dai_ip_arp_inspection_limit:
    interface: eth1/0/10
    no_limit: true

- name: Revert to default ARP inspection rate limit
  jaydee_io.dlink_dgs1250.dai_ip_arp_inspection_limit:
    interface: eth1/0/10
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


def _build_commands(interface, rate, burst_interval, no_limit, state):
    """Build the CLI command list."""
    commands = ["interface %s" % interface]
    if state == "absent":
        commands.append("no ip arp inspection limit")
    elif no_limit:
        commands.append("ip arp inspection limit none")
    else:
        cmd = "ip arp inspection limit rate %d" % rate
        if burst_interval:
            cmd += " burst interval %d" % burst_interval
        commands.append(cmd)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            rate=dict(type="int"),
            burst_interval=dict(type="int"),
            no_limit=dict(type="bool", default=False),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        mutually_exclusive=[("rate", "no_limit")],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["interface"],
        module.params["rate"],
        module.params["burst_interval"],
        module.params["no_limit"],
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
