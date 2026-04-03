#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: cpu_utilization
short_description: Display CPU utilization of a D-Link DGS-1250 switch
description:
  - Executes the C(show cpu utilization) CLI command on a D-Link DGS-1250 switch via SSH.
  - Returns structured data for CPU utilization at 5-second, 1-minute, and 5-minute intervals.
  - Corresponds to CLI command described in chapter 2-12 of the DGS-1250 CLI Reference Guide.
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
- name: Get CPU utilization
  dlink.dgs1250.cpu_utilization:
    host: 192.168.1.1
    username: admin
    password: admin
  register: cpu_info

- name: Warn if CPU usage is high
  ansible.builtin.debug:
    msg: "High CPU: {{ cpu_info.five_seconds_percent }}%"
  when: cpu_info.five_seconds_percent > 80
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
five_seconds_percent:
  description: CPU utilization percentage over the last 5 seconds.
  returned: always
  type: int
  sample: 12
one_minute_percent:
  description: CPU utilization percentage over the last 1 minute.
  returned: always
  type: int
  sample: 12
five_minutes_percent:
  description: CPU utilization percentage over the last 5 minutes.
  returned: always
  type: int
  sample: 12
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

def _parse_cpu_utilization(output):
    """
    Parse the CPU utilization output.

    Expected format:
        CPU Utilization
        Five seconds -   12 %
        One minute -     12 %
        Five minutes -   12 %
    """
    result = {
        "five_seconds_percent": 0,
        "one_minute_percent": 0,
        "five_minutes_percent": 0,
    }

    for line in output.splitlines():
        m = re.match(r"^\s*Five seconds\s*-\s*(\d+)\s*%", line, re.IGNORECASE)
        if m:
            result["five_seconds_percent"] = int(m.group(1))
            continue
        m = re.match(r"^\s*One minute\s*-\s*(\d+)\s*%", line, re.IGNORECASE)
        if m:
            result["one_minute_percent"] = int(m.group(1))
            continue
        m = re.match(r"^\s*Five minutes\s*-\s*(\d+)\s*%", line, re.IGNORECASE)
        if m:
            result["five_minutes_percent"] = int(m.group(1))
            continue

    return result


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
            raw_output = conn.send_command("show cpu utilization")
    except Exception as e:
        module.fail_json(msg="SSH connection or command failed: %s" % str(e))

    parsed = _parse_cpu_utilization(raw_output)

    result = dict(
        changed=False,
        raw_output=raw_output,
        **parsed,
    )

    module.exit_json(**result)


if __name__ == "__main__":
    main()
