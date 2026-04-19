#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dot1x_clear_counters
short_description: Clear 802.1X counters on a D-Link DGS-1250 switch
description:
  - Executes the C(clear dot1x counters) CLI command on a D-Link DGS-1250 switch.
  - Clears 802.1X diagnostics, statistics, and session statistics counters.
  - Corresponds to CLI command described in chapter 3-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.2.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interfaces:
    description:
      - List of physical port interfaces on which to clear counters.
      - Each entry can be a single port (e.g. C(eth1/0/1)) or a range (e.g. C(eth1/0/1-eth1/0/8)).
      - If omitted, counters are cleared on all interfaces.
    type: list
    elements: str
notes:
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Clear 802.1X counters on all interfaces
  jaydee_io.dlink_dgs1250.dot1x_clear_counters:

- name: Clear 802.1X counters on specific ports
  jaydee_io.dlink_dgs1250.dot1x_clear_counters:
    interfaces:
      - eth1/0/1
      - eth1/0/5

- name: Clear 802.1X counters on a range
  jaydee_io.dlink_dgs1250.dot1x_clear_counters:
    interfaces:
      - eth1/0/1-eth1/0/8
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
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_PRIVILEGED


# ---------------------------------------------------------------------------
# Command builder
# ---------------------------------------------------------------------------

def _build_commands(interfaces):
    """Build the CLI command list."""
    if not interfaces:
        return ["clear dot1x counters all"]

    commands = []
    for iface in interfaces:
        commands.append("clear dot1x counters interface %s" % iface)
    return commands


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            interfaces=dict(type="list", elements="str", default=None),
        ),
        supports_check_mode=True,
    )

    interfaces = module.params["interfaces"]
    commands = _build_commands(interfaces)

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
