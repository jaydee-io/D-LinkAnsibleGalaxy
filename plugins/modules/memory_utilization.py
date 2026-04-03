#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: memory_utilization
short_description: Display memory utilization of a D-Link DGS-1250 switch
description:
  - Executes the C(show memory utilization) CLI command on a D-Link DGS-1250 switch via SSH.
  - Returns structured data for DRAM and FLASH memory usage.
  - Corresponds to CLI command described in chapter 2-16 of the DGS-1250 CLI Reference Guide.
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
- name: Get memory utilization
  dlink.dgs1250.memory_utilization:
    host: 192.168.1.1
    username: admin
    password: admin
  register: mem_info

- name: Display DRAM usage
  ansible.builtin.debug:
    msg: "DRAM: {{ mem_info.memory[0].used_kb }}K / {{ mem_info.memory[0].total_kb }}K"
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
memory:
  description: Memory usage for DRAM and FLASH.
  returned: always
  type: list
  elements: dict
  contains:
    type:
      description: Memory type (DRAM or FLASH).
      type: str
      sample: "DRAM"
    total_kb:
      description: Total memory in kilobytes.
      type: int
      sample: 243268
    used_kb:
      description: Used memory in kilobytes.
      type: int
      sample: 125316
    free_kb:
      description: Free memory in kilobytes.
      type: int
      sample: 117952
"""

import re
from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.dlink.dgs1250.plugins.module_utils.dgs1250 import (
        DGS1250Connection,
        HAS_PARAMIKO,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import DGS1250Connection, HAS_PARAMIKO


# ---------------------------------------------------------------------------
# Output parsers
# ---------------------------------------------------------------------------

def _parse_memory_utilization(output):
    """
    Parse the memory utilization output.

    Expected format:
         Memory     Total       Used        Free
        --------  ----------  ----------  ----------
         DRAM      243268 K    125316 K    117952 K
         FLASH      45220 K     24968 K     20252 K
    """
    memory = []

    for line in output.splitlines():
        m = re.match(
            r"^\s*(DRAM|FLASH)\s+(\d+)\s*K\s+(\d+)\s*K\s+(\d+)\s*K\s*$",
            line
        )
        if m:
            memory.append({
                "type": m.group(1),
                "total_kb": int(m.group(2)),
                "used_kb": int(m.group(3)),
                "free_kb": int(m.group(4)),
            })

    return memory


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(type="str", required=True),
            username=dict(type="str", required=True),
            password=dict(type="str", required=True, no_log=True),
            port=dict(type="int", default=22),
            timeout=dict(type="int", default=30),
        ),
        supports_check_mode=True,
    )

    if not HAS_PARAMIKO:
        module.fail_json(msg="paramiko is required: pip install paramiko")

    host = module.params["host"]
    username = module.params["username"]
    password = module.params["password"]
    port = module.params["port"]
    timeout = module.params["timeout"]

    try:
        with DGS1250Connection(host, username, password, port, timeout) as conn:
            raw_output = conn.send_command("show memory utilization")
    except Exception as e:
        module.fail_json(msg="SSH connection or command failed: %s" % str(e))

    result = dict(
        changed=False,
        raw_output=raw_output,
        memory=_parse_memory_utilization(raw_output),
    )

    module.exit_json(**result)


if __name__ == "__main__":
    main()
