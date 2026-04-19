#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: dns_clear_host
short_description: Clear dynamically learned host entries on a D-Link DGS-1250 switch
description:
  - Executes the C(clear host) CLI command on a D-Link DGS-1250 switch.
  - Clears dynamically learned host entries from the DNS resolver or caching server.
  - Corresponds to CLI command described in chapter 23-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.10.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  host_name:
    description:
      - The host name to clear. If not specified, all host entries are cleared.
    type: str
notes:
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Clear all host entries
  jaydee_io.dlink_dgs1250.dns_clear_host:

- name: Clear specific host entry
  jaydee_io.dlink_dgs1250.dns_clear_host:
    host_name: www.abc.com
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


def _build_commands(host_name):
    """Build the CLI command list."""
    if host_name:
        return ["clear host %s" % host_name]
    else:
        return ["clear host all"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            host_name=dict(type="str"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["host_name"])
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
