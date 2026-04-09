#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: cable_diag_show
short_description: Display cable diagnostics results on a D-Link DGS-1250 switch
description:
  - Executes the C(show cable-diagnostics) CLI command on a D-Link DGS-1250 switch.
  - Returns cable diagnostics results for all or a specific interface.
  - Corresponds to CLI command described in chapter 11-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.7.0"
author:
  - Jérôme Dumesnil
options:
  interface:
    description:
      - Interface ID to display diagnostics for (e.g. C(eth1/0/1)).
      - If omitted, diagnostics for all interfaces are displayed.
    type: str
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
"""

EXAMPLES = r"""
- name: Show cable diagnostics for all interfaces
  jaydee_io.dlink_dgs1250.cable_diag_show:
  register: cable_diag

- name: Show cable diagnostics for a specific interface
  jaydee_io.dlink_dgs1250.cable_diag_show:
    interface: eth1/0/1
  register: cable_diag
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
"""

import re
from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import run_command
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


# ---------------------------------------------------------------------------
# Output parser
# ---------------------------------------------------------------------------

def _parse_cable_diag(output):
    """Parse show cable-diagnostics output.

    The table format is complex with multi-line test results per port,
    so we return the raw output only.
    """
    return {}


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str"),
        ),
        supports_check_mode=True,
    )

    cmd = "show cable-diagnostics"
    if module.params["interface"]:
        cmd += " interface %s" % module.params["interface"]

    try:
        raw_output = run_command(module, cmd)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    module.exit_json(changed=False, raw_output=raw_output)


if __name__ == "__main__":
    main()
