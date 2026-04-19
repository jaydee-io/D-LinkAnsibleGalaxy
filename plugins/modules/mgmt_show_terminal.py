#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: mgmt_show_terminal
short_description: Display terminal settings on a D-Link DGS-1250 switch
description:
  - Executes the C(show terminal) CLI command on a D-Link DGS-1250 switch.
  - Returns terminal configuration parameters.
  - Corresponds to CLI command described in chapter 5-13 of the DGS-1250 CLI Reference Guide.
version_added: "0.4.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options: {}
"""

EXAMPLES = r"""
- name: Show terminal settings
  jaydee_io.dlink_dgs1250.mgmt_show_terminal:
  register: result
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
terminal:
  description: Parsed terminal settings.
  returned: success
  type: dict
  contains:
    length:
      description: Number of lines displayed.
      type: int
    width:
      description: Number of columns displayed.
      type: int
    default_length:
      description: Default number of lines.
      type: int
    default_width:
      description: Default number of columns.
      type: int
    baud_rate:
      description: Baud rate in bps.
      type: int
"""

import re
from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import run_command
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


def _parse_terminal(output):
    result = {
        "length": 0,
        "width": 0,
        "default_length": 0,
        "default_width": 0,
        "baud_rate": 0,
    }
    field_map = {
        "Length": "length",
        "width": "width",
        "Default Length": "default_length",
        "Default Width": "default_width",
        "Baud Rate": "baud_rate",
    }
    for line in output.splitlines():
        m = re.match(r"^\s*(.+?):\s*(\d+)", line)
        if m:
            key = m.group(1).strip()
            if key in field_map:
                result[field_map[key]] = int(m.group(2))
    return result


def main():
    module = AnsibleModule(argument_spec=dict(), supports_check_mode=True)

    try:
        raw_output = run_command(module, "show terminal")
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    result = dict(changed=False, raw_output=raw_output)
    result["terminal"] = _parse_terminal(raw_output)
    module.exit_json(**result)


if __name__ == "__main__":
    main()
