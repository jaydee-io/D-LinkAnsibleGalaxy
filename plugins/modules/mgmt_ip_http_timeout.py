#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: mgmt_ip_http_timeout
short_description: Set the HTTP idle timeout on a D-Link DGS-1250 switch
description:
  - Configures the C(ip http timeout-policy idle) CLI command on a D-Link DGS-1250 switch.
  - Use C(state=absent) to revert to default (180 seconds).
  - Corresponds to CLI command described in chapter 5-8 of the DGS-1250 CLI Reference Guide.
version_added: "0.4.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  timeout:
    description:
      - Idle timeout in seconds (60-36000). Required when C(state=present).
    type: int
  state:
    description:
      - C(present) to set the timeout, C(absent) to revert to default.
    type: str
    choices: [present, absent]
    default: present
"""

EXAMPLES = r"""
- name: Set HTTP idle timeout to 100 seconds
  jaydee_io.dlink_dgs1250.mgmt_ip_http_timeout:
    timeout: 100

- name: Revert to default timeout
  jaydee_io.dlink_dgs1250.mgmt_ip_http_timeout:
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


def _build_commands(timeout, state):
    if state == "absent":
        return ["no ip http timeout-policy idle"]
    return ["ip http timeout-policy idle %d" % timeout]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            timeout=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["timeout"])],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["timeout"], module.params["state"])

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
