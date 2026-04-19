#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: mgmt_show_users
short_description: Display active user sessions on a D-Link DGS-1250 switch
description:
  - Executes the C(show users) CLI command on a D-Link DGS-1250 switch.
  - Returns a list of active user sessions with their details.
  - Corresponds to CLI command described in chapter 5-17 of the DGS-1250 CLI Reference Guide.
version_added: "0.4.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options: {}
"""

EXAMPLES = r"""
- name: Show active user sessions
  jaydee_io.dlink_dgs1250.mgmt_show_users:
  register: result
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
users:
  description: List of active user sessions.
  returned: success
  type: list
  elements: dict
  contains:
    id:
      description: Session ID.
      type: int
    type:
      description: Connection type (console, telnet, ssh).
      type: str
    user_name:
      description: User name.
      type: str
    login_time:
      description: Login time.
      type: str
    ip:
      description: Source IP address.
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


def _parse_users(output):
    users = []
    for line in output.splitlines():
        m = re.match(r"^\s*(\d+)\s+(\S+)\s+(\S+)\s+(\S+\s+\S+)\s+(\S+)", line)
        if m:
            users.append({
                "id": int(m.group(1)),
                "type": m.group(2),
                "user_name": m.group(3),
                "login_time": m.group(4).strip(),
                "ip": m.group(5),
            })
    return users


def main():
    module = AnsibleModule(argument_spec=dict(), supports_check_mode=True)

    try:
        raw_output = run_command(module, "show users")
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    module.exit_json(changed=False, raw_output=raw_output, users=_parse_users(raw_output))


if __name__ == "__main__":
    main()
