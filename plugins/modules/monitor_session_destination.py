#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jerome Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: monitor_session_destination
short_description: Configure port monitor session destination on a D-Link DGS-1250 switch
description:
  - Configures the C(monitor session destination interface) CLI command on a D-Link DGS-1250 switch.
  - Configures the destination interface for a port monitor session.
  - Corresponds to CLI command described in chapter 44-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.14.0"
author:
  - "Jérôme Dumesnil (@jaydee-io)"
options:
  session:
    description:
      - The session number. Valid value is 1.
    type: int
    required: true
  interface_id:
    description:
      - The destination interface ID (e.g. C(eth1/0/1)). Required when C(state=present).
    type: str
  state:
    description:
      - C(present) to set the destination, C(absent) to remove the session.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set port monitor session destination
  jaydee_io.dlink_dgs1250.monitor_session_destination:
    session: 1
    interface_id: eth1/0/1

- name: Remove port monitor session
  jaydee_io.dlink_dgs1250.monitor_session_destination:
    session: 1
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
        run_commands, is_config_present, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, is_config_present, MODE_GLOBAL_CONFIG


def _build_commands(session, interface_id, state):
    if state == "absent":
        return ["no monitor session %d" % session]
    return ["monitor session %d destination interface %s" % (session, interface_id)]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            session=dict(type="int", required=True),
            interface_id=dict(type="str"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["interface_id"]),
        ],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["session"], module.params["interface_id"], module.params["state"])
    if is_config_present(module, commands):
        module.exit_json(changed=False, commands=[], raw_output="")
        return
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
