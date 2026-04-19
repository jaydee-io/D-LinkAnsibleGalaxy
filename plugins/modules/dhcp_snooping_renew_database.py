#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: dhcp_snooping_renew_database
short_description: Renew DHCP snooping binding database on a D-Link DGS-1250 switch
description:
  - Executes the C(renew ip dhcp snooping database) CLI command on a D-Link DGS-1250 switch.
  - Renews the DHCP snooping binding database from the specified URL.
  - Corresponds to CLI command described in chapter 17-6 of the DGS-1250 CLI Reference Guide.
version_added: "0.9.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  url:
    description:
      - URL from which to renew the binding database.
    type: str
    required: true
notes:
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Renew DHCP snooping binding database
  jaydee_io.dlink_dgs1250.dhcp_snooping_renew_database:
    url: tftp://192.168.1.1/snooping.db
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


def _build_commands(url):
    """Build the CLI command list."""
    return ["renew ip dhcp snooping database %s" % url]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            url=dict(type="str", required=True),
        ),
        supports_check_mode=True,
    )

    commands = _build_commands(module.params["url"])

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
