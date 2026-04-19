#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: cable_diag_clear
short_description: Clear cable diagnostics results on a D-Link DGS-1250 switch
description:
  - Executes the C(clear cable-diagnostics) CLI command on a D-Link DGS-1250 switch.
  - Clears cable diagnostics results for all interfaces or a specific interface.
  - Corresponds to CLI command described in chapter 11-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.7.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  target:
    description:
      - What to clear.
      - C(all) clears diagnostics results for all interfaces.
      - C(interface) clears diagnostics results for a specific interface (requires C(interface) parameter).
    type: str
    required: true
    choices: [all, interface]
  interface:
    description:
      - Interface ID to clear diagnostics for (e.g. C(eth1/0/1)).
      - Required when C(target) is C(interface).
    type: str
notes:
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Clear all cable diagnostics results
  jaydee_io.dlink_dgs1250.cable_diag_clear:
    target: all

- name: Clear cable diagnostics for a specific interface
  jaydee_io.dlink_dgs1250.cable_diag_clear:
    target: interface
    interface: eth1/0/1
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

def _build_commands(target, interface):
    """Build the CLI command list."""
    if target == "all":
        return ["clear cable-diagnostics all"]
    return ["clear cable-diagnostics interface %s" % interface]


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            target=dict(type="str", required=True,
                        choices=["all", "interface"]),
            interface=dict(type="str"),
        ),
        required_if=[
            ("target", "interface", ["interface"]),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["target"], module.params["interface"])

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
