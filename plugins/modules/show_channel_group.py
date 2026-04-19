#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: show_channel_group
short_description: Display channel group information on a D-Link DGS-1250 switch
description:
  - Executes the C(show channel-group) CLI command on a D-Link DGS-1250 switch.
  - Displays channel group summary, detail, neighbor, load-balance, or sys-id information.
  - Corresponds to CLI command described in chapter 40-6 of the DGS-1250 CLI Reference Guide.
version_added: "0.13.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  view:
    description:
      - The type of information to display.
      - C(summary) shows the channel group summary (default).
      - C(detail) shows detailed channel group information.
      - C(neighbor) shows neighbor information.
      - C(load-balance) shows the load balance algorithm.
      - C(sys-id) shows the LACP system identifier.
    type: str
    choices: [summary, detail, neighbor, load-balance, sys-id]
    default: summary
  channel_no:
    description:
      - Optional channel group ID to display. Only used with C(detail) and C(neighbor) views.
    type: int
notes:
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Display channel group summary
  jaydee_io.dlink_dgs1250.show_channel_group:
  register: result

- name: Display detailed info for channel 3
  jaydee_io.dlink_dgs1250.show_channel_group:
    view: detail
    channel_no: 3
  register: result

- name: Display load balance information
  jaydee_io.dlink_dgs1250.show_channel_group:
    view: load-balance
  register: result
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
        run_command,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


def _build_command(view, channel_no):
    if view in ("detail", "neighbor"):
        if channel_no is not None:
            return "show channel-group channel %d %s" % (channel_no, view)
        return "show channel-group channel %s" % view
    if view == "load-balance":
        return "show channel-group load-balance"
    if view == "sys-id":
        return "show channel-group sys-id"
    return "show channel-group"


def main():
    module = AnsibleModule(
        argument_spec=dict(
            view=dict(type="str", choices=["summary", "detail", "neighbor", "load-balance", "sys-id"], default="summary"),
            channel_no=dict(type="int"),
        ),
        supports_check_mode=True,
    )
    command = _build_command(
        module.params["view"],
        module.params["channel_no"],
    )
    if module.check_mode:
        module.exit_json(changed=False, commands=[command], raw_output="")
        return
    try:
        raw_output = run_command(module, command)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    module.exit_json(changed=False, raw_output=raw_output, commands=[command])


if __name__ == "__main__":
    main()
