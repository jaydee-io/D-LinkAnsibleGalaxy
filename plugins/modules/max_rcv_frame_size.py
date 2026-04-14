#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: max_rcv_frame_size
short_description: Configure maximum receive frame size on a D-Link DGS-1250 switch interface
description:
  - Configures the C(max-rcv-frame-size) CLI command on a D-Link DGS-1250 switch.
  - Sets the maximum Ethernet frame size allowed on an interface.
  - Corresponds to CLI command described in chapter 39-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.13.0"
author:
  - Jérôme Dumesnil
options:
  interface:
    description:
      - The interface to configure (e.g. C(eth1/0/3)).
    type: str
    required: true
  size:
    description:
      - Maximum frame size in bytes (64 to 12288). Required when C(state=present).
    type: int
  state:
    description:
      - C(present) to set the frame size, C(absent) to revert to default (1536).
    type: str
    choices: [present, absent]
    default: present
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Set maximum receive frame size to 6000 bytes
  jaydee_io.dlink_dgs1250.max_rcv_frame_size:
    interface: eth1/0/3
    size: 6000

- name: Revert to default frame size
  jaydee_io.dlink_dgs1250.max_rcv_frame_size:
    interface: eth1/0/3
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


def _build_commands(interface, size, state):
    """Build the CLI command list."""
    commands = ["interface %s" % interface]
    if state == "absent":
        commands.append("no max-rcv-frame-size")
    else:
        commands.append("max-rcv-frame-size %d" % size)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            size=dict(type="int"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["size"]),
        ],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["interface"],
        module.params["size"],
        module.params["state"],
    )
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
