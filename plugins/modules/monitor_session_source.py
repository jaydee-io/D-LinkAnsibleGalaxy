#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jerome Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: monitor_session_source
short_description: Configure port monitor session source on a D-Link DGS-1250 switch
description:
  - Configures the C(monitor session source interface) CLI command on a D-Link DGS-1250 switch.
  - Configures the source interface(s) for a port monitor session.
  - Corresponds to CLI command described in chapter 44-2 of the DGS-1250 CLI Reference Guide.
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
      - The source interface ID (e.g. C(eth1/0/2-4)).
    type: str
    required: true
  direction:
    description:
      - The traffic direction to monitor.
      - If not specified, both TX and RX are monitored.
    type: str
    choices: [both, rx, tx]
  state:
    description:
      - C(present) to add the source, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Add source ports to monitor session
  jaydee_io.dlink_dgs1250.monitor_session_source:
    session: 1
    interface_id: eth1/0/2-4

- name: Add source port with RX direction only
  jaydee_io.dlink_dgs1250.monitor_session_source:
    session: 1
    interface_id: eth1/0/5
    direction: rx

- name: Remove source port from monitor session
  jaydee_io.dlink_dgs1250.monitor_session_source:
    session: 1
    interface_id: eth1/0/5
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


def _build_commands(session, interface_id, direction, state):
    if state == "absent":
        return ["no monitor session %d source interface %s" % (session, interface_id)]
    cmd = "monitor session %d source interface %s" % (session, interface_id)
    if direction:
        cmd += " %s" % direction
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            session=dict(type="int", required=True),
            interface_id=dict(type="str", required=True),
            direction=dict(type="str", choices=["both", "rx", "tx"]),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["session"], module.params["interface_id"], module.params["direction"], module.params["state"])
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
