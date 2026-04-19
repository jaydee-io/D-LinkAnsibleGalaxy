#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: ipv6_nd_ra_interval
short_description: Configure IPv6 ND router advertisement interval on an interface of a D-Link DGS-1250 switch
description:
  - Configures the C(ipv6 nd ra interval) CLI command on a D-Link DGS-1250 switch.
  - Sets or resets the interval between IPv6 router advertisement transmissions.
  - Corresponds to CLI command described in chapter 10-10 of the DGS-1250 CLI Reference Guide.
version_added: "0.7.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Interface on which to configure the RA interval (e.g. C(vlan1)).
    type: str
    required: true
  max_secs:
    description:
      - Maximum interval in seconds between RA transmissions (4-1800). Required when C(state=present).
    type: int
  min_secs:
    description:
      - Minimum interval in seconds between RA transmissions (3-1350). Optional.
    type: int
  state:
    description:
      - C(present) to set the interval, C(absent) to reset to default.
    type: str
    choices: [present, absent]
    default: present
notes:
"""

EXAMPLES = r"""
- name: Set RA interval to 600 seconds on vlan1
  jaydee_io.dlink_dgs1250.ipv6_nd_ra_interval:
    interface: vlan1
    max_secs: 600

- name: Set RA interval with min and max on vlan1
  jaydee_io.dlink_dgs1250.ipv6_nd_ra_interval:
    interface: vlan1
    max_secs: 600
    min_secs: 200

- name: Reset RA interval to default on vlan1
  jaydee_io.dlink_dgs1250.ipv6_nd_ra_interval:
    interface: vlan1
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


def _build_commands(interface, max_secs, min_secs, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["interface %s" % interface, "no ipv6 nd ra interval", "exit"]
    cmd = "ipv6 nd ra interval %d" % max_secs
    if min_secs is not None:
        cmd += " %d" % min_secs
    return ["interface %s" % interface, cmd, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            max_secs=dict(type="int"),
            min_secs=dict(type="int"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["max_secs"]),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["interface"],
        module.params["max_secs"],
        module.params["min_secs"],
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
