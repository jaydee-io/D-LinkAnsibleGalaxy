#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: aaa_clear_counters_servers
short_description: Clear AAA server counters on a D-Link DGS-1250 switch
description:
  - Executes the C(clear aaa counters servers) CLI command on a D-Link DGS-1250 switch.
  - Clears AAA server statistics counters for RADIUS, TACACS+, or server groups.
  - Corresponds to CLI command described in chapter 8-10 of the DGS-1250 CLI Reference Guide.
version_added: "0.6.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  target:
    description:
      - Type of server counters to clear.
      - C(all) clears all server counters.
      - C(radius) clears RADIUS server counters (use C(address) to specify which).
      - C(tacacs) clears TACACS+ server counters (use C(address) to specify which).
      - C(sg) clears server group counters (use C(address) to specify the group name).
    type: str
    required: true
    choices: [all, radius, tacacs, sg]
  address:
    description:
      - IP address, IPv6 address, C(all), or server group name depending on C(target).
      - Required when C(target) is C(radius), C(tacacs), or C(sg).
    type: str
notes:
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Clear all AAA server counters
  jaydee_io.dlink_dgs1250.aaa_clear_counters_servers:
    target: all

- name: Clear RADIUS server counters for specific IP
  jaydee_io.dlink_dgs1250.aaa_clear_counters_servers:
    target: radius
    address: 192.168.1.100

- name: Clear server group counters
  jaydee_io.dlink_dgs1250.aaa_clear_counters_servers:
    target: sg
    address: my_group
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
        run_commands, MODE_PRIVILEGED,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_PRIVILEGED


# ---------------------------------------------------------------------------
# Command builder
# ---------------------------------------------------------------------------

def _build_commands(target, address):
    """Build the CLI command list."""
    if target == "all":
        return ["clear aaa counters servers all"]
    return ["clear aaa counters servers %s %s" % (target, address)]


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            target=dict(type="str", required=True, choices=["all", "radius", "tacacs", "sg"]),
            address=dict(type="str"),
        ),
        required_if=[
            ("target", "radius", ["address"]),
            ("target", "tacacs", ["address"]),
            ("target", "sg", ["address"]),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(module.params["target"], module.params["address"])

    if module.check_mode:
        module.exit_json(changed=True, commands=commands, raw_output="")
        return

    try:
        raw_output = run_commands(module, commands, mode=MODE_PRIVILEGED)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    module.exit_json(changed=True, raw_output=raw_output, commands=commands)


if __name__ == "__main__":
    main()
