#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: sntp_server
short_description: Configure an SNTP server on a D-Link DGS-1250 switch
description:
  - Configures the C(sntp server) CLI command on a D-Link DGS-1250 switch.
  - Adds or removes an SNTP time server for clock synchronization.
  - Corresponds to CLI command described in chapter 67-6 of the DGS-1250 CLI Reference Guide.
version_added: "0.19.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  address:
    description:
      - IP or IPv6 address of the SNTP server.
    type: str
    required: true
  state:
    description:
      - C(present) to add, C(absent) to remove.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Add SNTP server
  jaydee_io.dlink_dgs1250.sntp_server:
    address: 192.168.22.44

- name: Remove SNTP server
  jaydee_io.dlink_dgs1250.sntp_server:
    address: 192.168.22.44
    state: absent
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
commands:
  description: List of CLI commands sent to the switch.
  returned: always
  type: list
  elements: str
"""

from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import (
        run_commands, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(address, state):
    if state == "absent":
        return ["no sntp server %s" % address]
    return ["sntp server %s" % address]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            address=dict(type="str", required=True),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["address"], module.params["state"])
    if module.check_mode:
        module.exit_json(changed=True, commands=commands, raw_output="")
        return
    try:
        raw_output = run_commands(module, commands, mode=MODE_GLOBAL_CONFIG)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    module.exit_json(changed=True, raw_output=raw_output, commands=commands)


if __name__ == "__main__":
    main()
