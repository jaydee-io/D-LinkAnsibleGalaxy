#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: mgmt_show_ip_http_secure_server
short_description: Display HTTPS server status on a D-Link DGS-1250 switch
description:
  - Executes the C(show ip http secure-server) CLI command on a D-Link DGS-1250 switch.
  - Corresponds to CLI command described in chapter 5-16 of the DGS-1250 CLI Reference Guide.
version_added: "0.4.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options: {}
"""

EXAMPLES = r"""
- name: Show HTTPS server status
  jaydee_io.dlink_dgs1250.mgmt_show_ip_http_secure_server:
  register: result
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
server_state:
  description: Whether the HTTPS server is enabled.
  returned: success
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


def _parse_server_state(output):
    m = re.search(r"ip http secure-server state\s*:\s*(\S+)", output, re.IGNORECASE)
    if m:
        return m.group(1).strip().lower() == "enabled"
    return False


def main():
    module = AnsibleModule(argument_spec=dict(), supports_check_mode=True)

    try:
        raw_output = run_command(module, "show ip http secure-server")
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    module.exit_json(changed=False, raw_output=raw_output, server_state=_parse_server_state(raw_output))


if __name__ == "__main__":
    main()
