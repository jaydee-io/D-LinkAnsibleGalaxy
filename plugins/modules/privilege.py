#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: privilege
short_description: Display current privilege level on a D-Link DGS-1250 switch
description:
  - Executes the C(show privilege) CLI command on a D-Link DGS-1250 switch via SSH.
  - Returns the current privilege level of the session.
  - Corresponds to CLI command described in chapter 2-17 of the DGS-1250 CLI Reference Guide.
version_added: "0.1.0"
author:
  - Jérôme Dumesnil
options:
  host:
    description: IP address or hostname of the switch.
    required: true
    type: str
  username:
    description: SSH username.
    required: true
    type: str
  password:
    description: SSH password.
    required: true
    type: str
    no_log: true
  port:
    description: SSH port.
    type: int
    default: 22
  timeout:
    description: SSH connection timeout in seconds.
    type: int
    default: 30
notes:
  - Requires C(paramiko) on the Ansible controller (C(pip install paramiko)).
  - The switch must be reachable via SSH from the Ansible controller.
"""

EXAMPLES = r"""
- name: Get current privilege level
  dlink.dgs1250.privilege:
    host: 192.168.1.1
    username: admin
    password: admin
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
    from ansible_collections.dlink.dgs1250.plugins.module_utils.dgs1250 import (
        CONNECTION_ARGSPEC,
        HAS_PARAMIKO,
        connection_from_params,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import CONNECTION_ARGSPEC, HAS_PARAMIKO, connection_from_params


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
        argument_spec=dict(**CONNECTION_ARGSPEC),
        supports_check_mode=True,
    )

    if not HAS_PARAMIKO:
        module.fail_json(msg="paramiko is required: pip install paramiko")

    try:
        with connection_from_params(module.params) as conn:
            raw_output = conn.send_command("show privilege")
    except Exception as e:
        module.fail_json(msg="SSH connection or command failed: %s" % str(e))

    result = dict(
        changed=False,
        raw_output=raw_output,
        privilege_level=_parse_privilege(raw_output),
    )

    module.exit_json(**result)


if __name__ == "__main__":
    main()
