#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dot1x_max_req
short_description: Configure 802.1X maximum EAP request retransmissions on a D-Link DGS-1250 switch port
description:
  - Configures the C(dot1x max-req) CLI command on a D-Link DGS-1250 switch.
  - Sets the maximum number of times the switch retransmits an EAP request frame
    to the supplicant before restarting the authentication process.
  - Use C(state=absent) to revert to the default value (2).
  - Corresponds to CLI command described in chapter 3-7 of the DGS-1250 CLI Reference Guide.
version_added: "0.2.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Physical port interface to configure (e.g. C(eth1/0/1)).
    required: true
    type: str
  times:
    description:
      - Maximum number of EAP request retransmissions. Range is 1 to 10.
    type: int
  state:
    description:
      - Whether to set (C(present)) or reset to default (C(absent)) the max-req value.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Set max EAP retransmissions to 3 on port 1
  jaydee_io.dlink_dgs1250.dot1x_max_req:
    interface: eth1/0/1
    times: 3

- name: Reset to default (2) on port 1
  jaydee_io.dlink_dgs1250.dot1x_max_req:
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
        run_commands, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


# ---------------------------------------------------------------------------
# Command builder
# ---------------------------------------------------------------------------

def _build_commands(interface, state, times):
    """Build the CLI command list for interface configuration."""
    commands = ["interface %s" % interface]
    if state == "absent":
        commands.append("no dot1x max-req")
    else:
        commands.append("dot1x max-req %d" % times)
    return commands


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            times=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["times"]),
        ],
        supports_check_mode=True,
    )

    interface = module.params["interface"]
    state = module.params["state"]
    times = module.params["times"]

    if state == "present" and (times < 1 or times > 10):
        module.fail_json(msg="'times' must be between 1 and 10.")

    commands = _build_commands(interface, state, times)

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
