#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: mgmt_terminal_width
short_description: Set terminal width on a D-Link DGS-1250 switch
description:
  - Configures the C(terminal width) CLI command on a D-Link DGS-1250 switch.
  - Sets the number of columns displayed on the terminal for the current session or as default.
  - Corresponds to CLI command described in chapter 5-21 of the DGS-1250 CLI Reference Guide.
version_added: "0.4.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  width:
    description:
      - Number of columns to display.
    type: int
    required: true
  default:
    description:
      - If C(true), sets the default terminal width instead of the current session.
    type: bool
    default: false
"""

EXAMPLES = r"""
- name: Set terminal width to 132 for current session
  jaydee_io.dlink_dgs1250.mgmt_terminal_width:
    width: 132

- name: Set default terminal width to 80
  jaydee_io.dlink_dgs1250.mgmt_terminal_width:
    width: 80
    default: true
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


def _build_commands(width, is_default):
    if is_default:
        return ["terminal width default %d" % width]
    return ["terminal width %d" % width]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            width=dict(type="int", required=True),
            default=dict(type="bool", default=False),
        ),
        supports_check_mode=True,
    )

    commands = _build_commands(module.params["width"], module.params["default"])

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
