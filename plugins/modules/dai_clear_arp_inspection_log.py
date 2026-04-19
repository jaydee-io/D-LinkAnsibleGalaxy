#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dai_clear_arp_inspection_log
short_description: Clear ARP inspection log buffer on a D-Link DGS-1250 switch
description:
  - Executes the C(clear ip arp inspection log) CLI command on a D-Link DGS-1250 switch.
  - Clears the ARP inspection log buffer.
  - Corresponds to CLI command described in chapter 25-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.10.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options: {}
notes:
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Clear ARP inspection log buffer
  jaydee_io.dlink_dgs1250.dai_clear_arp_inspection_log:
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


def _build_commands():
    """Build the CLI command list."""
    return ["clear ip arp inspection log"]


def main():
    module = AnsibleModule(
        argument_spec=dict(),
        supports_check_mode=True,
    )
    commands = _build_commands()
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
