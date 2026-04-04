#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: version
short_description: Display version information of a D-Link DGS-1250 switch
description:
  - Executes the C(show version) CLI command on a D-Link DGS-1250 switch via SSH.
  - Returns structured data for system MAC address, module name, hardware version, and runtime version.
  - Corresponds to CLI command described in chapter 2-13 of the DGS-1250 CLI Reference Guide.
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
- name: Get version information
  dlink.dgs1250.version:
    host: 192.168.1.1
    username: admin
    password: admin
  register: version_info

- name: Display firmware version
  ansible.builtin.debug:
    msg: "Firmware: {{ version_info.runtime }}"
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
system_mac_address:
  description: System MAC address of the switch.
  returned: always
  type: str
  sample: "F0-7D-68-12-50-01"
module_name:
  description: Module/model name of the switch.
  returned: always
  type: str
  sample: "DGS-1250-28XMP"
hardware_version:
  description: Hardware revision of the switch.
  returned: always
  type: str
  sample: "A1"
runtime:
  description: Runtime firmware version.
  returned: always
  type: str
  sample: "2.04.P003"
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

def _parse_version(output):
    """
    Parse the show version output.

    Expected format:
        System MAC Address: F0-7D-68-12-50-01
        Module Name DGS-1250-28XMP
        H/W A1
        Runtime 2.04.P003
    """
    result = {
        "system_mac_address": "",
        "module_name": "",
        "hardware_version": "",
        "runtime": "",
    }

    for line in output.splitlines():
        m = re.match(r"^\s*System MAC Address:\s*(\S+)", line)
        if m:
            result["system_mac_address"] = m.group(1).strip()
            continue
        m = re.match(r"^\s*Module Name\s+(\S+)", line)
        if m:
            result["module_name"] = m.group(1).strip()
            continue
        m = re.match(r"^\s*H/W\s+(\S+)", line)
        if m:
            result["hardware_version"] = m.group(1).strip()
            continue
        m = re.match(r"^\s*Runtime\s+(\S+)", line)
        if m:
            result["runtime"] = m.group(1).strip()
            continue

    return result


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
            raw_output = conn.send_command("show version")
    except Exception as e:
        module.fail_json(msg="SSH connection or command failed: %s" % str(e))

    parsed = _parse_version(raw_output)

    result = dict(
        changed=False,
        raw_output=raw_output,
        **parsed,
    )

    module.exit_json(**result)


if __name__ == "__main__":
    main()
