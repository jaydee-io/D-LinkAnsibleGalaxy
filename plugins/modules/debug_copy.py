#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: debug_copy
short_description: Copy debug information to a destination on a D-Link DGS-1250 switch
description:
  - Executes the C(debug copy) CLI command on a D-Link DGS-1250 switch.
  - Copies debug information (error-log or tech-support) to a destination URL or TFTP server.
  - Corresponds to CLI command described in chapter 13-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.8.0"
author:
  - Jérôme Dumesnil
options:
  source:
    description:
      - Source of the debug information to copy.
    type: str
    choices: [error-log, tech-support]
    required: true
  destination:
    description:
      - Destination URL or TFTP path (e.g. C(tftp://10.90.90.99/abc.txt)).
    type: str
    required: true
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Copy tech-support to TFTP server
  jaydee_io.dlink_dgs1250.debug_copy:
    source: tech-support
    destination: "tftp://10.90.90.99/abc.txt"

- name: Copy error-log to TFTP server
  jaydee_io.dlink_dgs1250.debug_copy:
    source: error-log
    destination: "tftp://10.90.90.99/error.txt"
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


def _build_commands(source, destination):
    """Build the CLI command list."""
    return ["debug copy %s %s" % (source, destination)]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            source=dict(type="str", choices=["error-log", "tech-support"], required=True),
            destination=dict(type="str", required=True),
        ),
        supports_check_mode=True,
    )

    commands = _build_commands(module.params["source"], module.params["destination"])

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
