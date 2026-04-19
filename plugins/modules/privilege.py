#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: privilege
short_description: Display current privilege level on a D-Link DGS-1250 switch
description:
  - Executes the C(show privilege) CLI command on a D-Link DGS-1250 switch.
  - Returns the current privilege level of the session.
  - Corresponds to CLI command described in chapter 2-17 of the DGS-1250 CLI Reference Guide.
version_added: "0.1.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options: {}
"""

EXAMPLES = r"""
- name: Get current privilege level
  jaydee_io.dlink_dgs1250.privilege:
  register: priv_info

- name: Display privilege level
  ansible.builtin.debug:
    msg: "Privilege level: {{ priv_info.privilege_level }}"
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
privilege_level:
  description: The current privilege level name.
  returned: always
  type: str
  sample: "privilege level"
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
# Output parsers
# ---------------------------------------------------------------------------

def _parse_privilege(output):
    """
    Parse the show privilege output.

    Expected format:
        Current level is privilege level
    """
    for line in output.splitlines():
        m = re.match(r"^\s*Current level is\s+(.+?)\s*$", line)
        if m:
            return m.group(1).strip()
    return ""


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(),
        supports_check_mode=True,
    )

    try:
        raw_output = run_command(module, "show privilege")
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    module.exit_json(
        changed=False,
        raw_output=raw_output,
        privilege_level=_parse_privilege(raw_output),
    )


if __name__ == "__main__":
    main()
