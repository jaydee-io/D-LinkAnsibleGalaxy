#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: logging_server
short_description: Configure a SYSLOG server on a D-Link DGS-1250 switch
description:
  - Configures the C(logging server) CLI command on a D-Link DGS-1250 switch.
  - Creates or removes a SYSLOG server host for logging system messages.
  - Corresponds to CLI command described in chapter 66-4 of the DGS-1250 CLI Reference Guide.
version_added: "0.19.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  address:
    description:
      - IP or IPv6 address of the SYSLOG server.
    type: str
    required: true
  severity:
    description:
      - Severity level name. Messages at this level or higher are logged.
    type: str
    choices: [emergencies, alerts, critical, errors, warnings, notifications, informational, debugging]
  facility:
    description:
      - Facility type as a decimal value from 0 to 23.
    type: int
  discriminator:
    description:
      - Name of the discriminator to filter messages.
    type: str
  port:
    description:
      - UDP port number (514 or 1024-65535).
    type: int
  state:
    description:
      - C(present) to create, C(absent) to remove.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Add SYSLOG server with warnings severity
  jaydee_io.dlink_dgs1250.logging_server:
    address: 20.3.3.3
    severity: warnings

- name: Remove SYSLOG server
  jaydee_io.dlink_dgs1250.logging_server:
    address: 20.3.3.3
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


def _build_commands(address, severity, facility, discriminator, port, state):
    if state == "absent":
        return ["no logging server %s" % address]
    cmd = "logging server %s" % address
    if severity is not None:
        cmd += " severity %s" % severity
    if facility is not None:
        cmd += " facility %d" % facility
    if discriminator is not None:
        cmd += " discriminator %s" % discriminator
    if port is not None:
        cmd += " port %d" % port
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            address=dict(type="str", required=True),
            severity=dict(type="str", choices=["emergencies", "alerts", "critical", "errors", "warnings", "notifications", "informational", "debugging"]),
            facility=dict(type="int"),
            discriminator=dict(type="str"),
            port=dict(type="int"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["address"], module.params["severity"], module.params["facility"], module.params["discriminator"], module.params["port"], module.params["state"])
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
