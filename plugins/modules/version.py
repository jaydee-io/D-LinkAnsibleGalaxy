#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: version
short_description: Display version information of a D-Link DGS-1250 switch
description:
  - Executes the C(show version) CLI command on a D-Link DGS-1250 switch.
  - Returns structured data for system MAC address, module name, hardware version, and runtime version.
  - Corresponds to CLI command described in chapter 2-13 of the DGS-1250 CLI Reference Guide.
version_added: "0.1.0"
author:
  - Jérôme Dumesnil
options: {}
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
"""

EXAMPLES = r"""
- name: Get version information
  jaydee_io.dlink_dgs1250.version:
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
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import run_command
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


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
        argument_spec=dict(),
        supports_check_mode=True,
    )

    try:
        raw_output = run_command(module, "show version")
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    parsed = _parse_version(raw_output)
    module.exit_json(changed=False, raw_output=raw_output, **parsed)


if __name__ == "__main__":
    main()
