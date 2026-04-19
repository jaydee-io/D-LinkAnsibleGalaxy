#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: dhcp_snooping_server_screen_log_buffer
short_description: Configure DHCP snooping server screen log buffer size on a D-Link DGS-1250 switch
description:
  - Configures the C(ip dhcp snooping server-screen log-buffer entries) CLI command on a D-Link DGS-1250 switch.
  - Corresponds to CLI command described in chapter 17-21 of the DGS-1250 CLI Reference Guide.
version_added: "0.9.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  entries:
    description:
      - The buffer entry number (max 1024). Required when C(state=present).
    type: int
  state:
    description:
      - C(present) to set, C(absent) to reset to default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set log buffer to 64 entries
  jaydee_io.dlink_dgs1250.dhcp_snooping_server_screen_log_buffer:
    entries: 64
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

def _build_commands(entries, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["no ip dhcp snooping server-screen log-buffer entries"]
    return ["ip dhcp snooping server-screen log-buffer entries %s" % entries]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            entries=dict(type="int"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["entries"])],
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["entries"], module.params["state"])
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
