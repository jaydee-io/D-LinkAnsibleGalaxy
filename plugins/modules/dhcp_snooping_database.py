#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dhcp_snooping_database
short_description: Configure DHCP snooping binding database storage on a D-Link DGS-1250 switch
description:
  - Configures the C(ip dhcp snooping database) CLI command on a D-Link DGS-1250 switch.
  - Sets the URL for the binding database or the write-delay interval.
  - Use C(state=absent) to remove the database configuration or reset write-delay.
  - Corresponds to CLI command described in chapter 17-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.9.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  url:
    description:
      - URL for the binding database storage location.
      - Mutually exclusive with C(write_delay).
    type: str
  write_delay:
    description:
      - Write-delay interval in seconds for the binding database.
      - Mutually exclusive with C(url).
    type: int
  state:
    description:
      - Whether to set (C(present)) or remove (C(absent)) the database configuration.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set binding database URL
  jaydee_io.dlink_dgs1250.dhcp_snooping_database:
    url: tftp://192.168.1.1/snooping.db

- name: Set write-delay to 300 seconds
  jaydee_io.dlink_dgs1250.dhcp_snooping_database:
    write_delay: 300

- name: Remove binding database configuration
  jaydee_io.dlink_dgs1250.dhcp_snooping_database:
    state: absent

- name: Reset write-delay to default
  jaydee_io.dlink_dgs1250.dhcp_snooping_database:
    write_delay: 300
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


def _build_commands(state, url, write_delay):
    """Build the CLI command list."""
    if state == "absent":
        if write_delay is not None:
            return ["no ip dhcp snooping database write-delay"]
        return ["no ip dhcp snooping database"]
    if url is not None:
        return ["ip dhcp snooping database %s" % url]
    return ["ip dhcp snooping database write-delay %d" % write_delay]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            url=dict(type="str"),
            write_delay=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        mutually_exclusive=[
            ("url", "write_delay"),
        ],
        required_if=[
            ("state", "present", ("url", "write_delay"), True),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["state"],
        module.params["url"],
        module.params["write_delay"],
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
