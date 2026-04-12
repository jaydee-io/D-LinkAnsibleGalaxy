#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: mac_address_table_aging_time
short_description: Configure MAC address table aging time on a D-Link DGS-1250 switch
description:
  - Configures the MAC address table aging time using the C(mac-address-table aging-time) command.
  - Use C(state=absent) to revert to the default setting (C(no mac-address-table aging-time)).
  - Corresponds to CLI command described in chapter 28-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.11.0"
author:
  - Jérôme Dumesnil
options:
  seconds:
    description:
      - Aging time in seconds. Valid range is 0 or 10 to 1000000.
        Setting to 0 disables the aging-out function.
      - Required when C(state=present).
    type: int
  state:
    description:
      - C(present) sets the aging time.
      - C(absent) reverts to the default aging time.
    type: str
    default: present
    choices: [present, absent]
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Global Configuration Mode.
  - Default aging time is 300 seconds.
"""

EXAMPLES = r"""
- name: Set MAC address table aging time to 200 seconds
  jaydee_io.dlink_dgs1250.mac_address_table_aging_time:
    seconds: 200
    state: present

- name: Revert to default aging time
  jaydee_io.dlink_dgs1250.mac_address_table_aging_time:
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
    if state == "absent":
        return ["no mac-address-table aging-time"]
    return ["mac-address-table aging-time %d" % seconds]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            seconds=dict(type="int"),
            state=dict(type="str", default="present", choices=["present", "absent"]),
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
