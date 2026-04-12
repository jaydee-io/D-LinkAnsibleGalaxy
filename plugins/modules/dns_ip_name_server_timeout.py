#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: dns_ip_name_server_timeout
short_description: Configure DNS name server timeout on a D-Link DGS-1250 switch
description:
  - Configures the C(ip name-server timeout) CLI command on a D-Link DGS-1250 switch.
  - Sets or resets the maximum time to wait for a response from a DNS name server.
  - Corresponds to CLI command described in chapter 23-5 of the DGS-1250 CLI Reference Guide.
version_added: "0.10.0"
author:
  - Jérôme Dumesnil
options:
  seconds:
    description:
      - The timeout value in seconds (1 to 60). Default is 3.
      - Required when state is C(present).
    type: int
  state:
    description:
      - C(present) to configure, C(absent) to revert to default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set DNS timeout to 5 seconds
  jaydee_io.dlink_dgs1250.dns_ip_name_server_timeout:
    seconds: 5

- name: Revert DNS timeout to default
  jaydee_io.dlink_dgs1250.dns_ip_name_server_timeout:
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
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(seconds, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["no ip name-server timeout"]
    else:
        return ["ip name-server timeout %d" % seconds]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            seconds=dict(type="int"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["seconds"])],
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["seconds"], module.params["state"])
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
