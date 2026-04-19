#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: mgmt_clear_line
short_description: Clear a user session on a D-Link DGS-1250 switch
description:
  - Executes the C(clear line) CLI command on a D-Link DGS-1250 switch.
  - Disconnects a user session by its line ID.
  - Corresponds to CLI command described in chapter 5-24 of the DGS-1250 CLI Reference Guide.
version_added: "0.4.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  line_id:
    description:
      - The line ID to clear (session ID from C(show users) output).
    type: int
    required: true
"""

EXAMPLES = r"""
- name: Clear user session 2
  jaydee_io.dlink_dgs1250.mgmt_clear_line:
    line_id: 2
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


def _build_commands(line_id):
    return ["clear line %d" % line_id]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            line_id=dict(type="int", required=True),
        ),
        supports_check_mode=True,
    )

    commands = _build_commands(module.params["line_id"])

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
