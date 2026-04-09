#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: aaa_show
short_description: Display AAA status on a D-Link DGS-1250 switch
description:
  - Executes the C(show aaa) CLI command on a D-Link DGS-1250 switch.
  - Returns whether AAA is enabled or disabled.
  - Corresponds to CLI command described in chapter 8-26 of the DGS-1250 CLI Reference Guide.
version_added: "0.6.0"
author:
  - Jérôme Dumesnil
options: {}
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
"""

EXAMPLES = r"""
- name: Show AAA status
  jaydee_io.dlink_dgs1250.aaa_show:
  register: aaa_status
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
aaa:
  description: Parsed AAA status.
  returned: always
  type: dict
  contains:
    enabled:
      description: Whether AAA is enabled.
      type: bool
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

def _parse_aaa(output):
    """Parse show aaa output."""
    enabled = False
    for line in output.splitlines():
        m = re.search(r"AAA is (enabled|disabled)", line, re.IGNORECASE)
        if m:
            enabled = m.group(1).lower() == "enabled"
            break
    return {"enabled": enabled}


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(),
        supports_check_mode=True,
    )

    try:
        raw_output = run_command(module, "show aaa")
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    aaa = _parse_aaa(raw_output)
    module.exit_json(changed=False, raw_output=raw_output, aaa=aaa)


if __name__ == "__main__":
    main()
