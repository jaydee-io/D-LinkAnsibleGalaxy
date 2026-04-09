#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: debug_show_tech_support
short_description: Display technical support information on a D-Link DGS-1250 switch
description:
  - Executes the C(debug show tech-support) CLI command on a D-Link DGS-1250 switch.
  - Displays technical support information for troubleshooting.
  - Corresponds to CLI command described in chapter 13-5 of the DGS-1250 CLI Reference Guide.
version_added: "0.8.0"
author:
  - Jérôme Dumesnil
options: {}
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Display tech-support information
  jaydee_io.dlink_dgs1250.debug_show_tech_support:
  register: tech_support
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
        run_command, MODE_PRIVILEGED,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command, MODE_PRIVILEGED


def _build_command():
    """Build the CLI command."""
    return "debug show tech-support"


def main():
    module = AnsibleModule(
        argument_spec=dict(),
        supports_check_mode=True,
    )

    command = _build_command()

    if module.check_mode:
        module.exit_json(changed=False, commands=[command], raw_output="")
        return

    try:
        raw_output = run_command(module, command, mode=MODE_PRIVILEGED)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    module.exit_json(changed=False, raw_output=raw_output, commands=[command])


if __name__ == "__main__":
    main()
