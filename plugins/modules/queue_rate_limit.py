#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: queue_rate_limit
short_description: Configure the bandwidth for a CoS queue on a D-Link DGS-1250 switch
description:
  - Configures the C(queue rate-limit) CLI command on a D-Link DGS-1250 switch.
  - Specifies the minimum and maximum bandwidth for a CoS queue on an interface.
  - Corresponds to CLI command described in chapter 54-12 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - The interface to configure (e.g. C(eth1/0/1)).
    type: str
    required: true
  queue_id:
    description:
      - Queue ID.
    type: int
    required: true
  min_bandwidth:
    description:
      - Minimal bandwidth in kbps. Required when C(state=present) and C(min_percent) is not set.
    type: int
  max_bandwidth:
    description:
      - Maximum bandwidth in kbps. Required when C(state=present) and C(max_percent) is not set.
    type: int
  min_percent:
    description:
      - Minimal bandwidth as a percentage (1-100).
    type: int
  max_percent:
    description:
      - Maximum bandwidth as a percentage (1-100).
    type: int
  state:
    description:
      - C(present) to set the rate-limit, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Queue 1 limited 100/2000 kbps on eth1/0/1
  jaydee_io.dlink_dgs1250.queue_rate_limit:
    interface: eth1/0/1
    queue_id: 1
    min_bandwidth: 100
    max_bandwidth: 2000

- name: Queue 2 limited 10%/50% on eth1/0/1
  jaydee_io.dlink_dgs1250.queue_rate_limit:
    interface: eth1/0/1
    queue_id: 2
    min_percent: 10
    max_percent: 50

- name: Remove rate limit on queue 1
  jaydee_io.dlink_dgs1250.queue_rate_limit:
    interface: eth1/0/1
    queue_id: 1
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


def _build_commands(interface, queue_id, min_bw, max_bw, min_pct, max_pct, state):
    commands = ["interface %s" % interface]
    if state == "absent":
        commands.append("no queue %d rate-limit" % queue_id)
    else:
        min_part = "percent %d" % min_pct if min_pct is not None else "%d" % min_bw
        max_part = "percent %d" % max_pct if max_pct is not None else "%d" % max_bw
        commands.append("queue %d rate-limit %s %s" %
                        (queue_id, min_part, max_part))
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            queue_id=dict(type="int", required=True),
            min_bandwidth=dict(type="int"),
            max_bandwidth=dict(type="int"),
            min_percent=dict(type="int"),
            max_percent=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    p = module.params
    if p["state"] == "present":
        if p["min_bandwidth"] is None and p["min_percent"] is None:
            module.fail_json(msg="min_bandwidth or min_percent is required")
        if p["max_bandwidth"] is None and p["max_percent"] is None:
            module.fail_json(msg="max_bandwidth or max_percent is required")
    commands = _build_commands(
        p["interface"], p["queue_id"],
        p["min_bandwidth"], p["max_bandwidth"],
        p["min_percent"], p["max_percent"],
        p["state"],
    )
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
