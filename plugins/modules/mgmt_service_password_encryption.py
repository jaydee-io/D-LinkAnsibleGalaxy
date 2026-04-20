#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: mgmt_service_password_encryption
short_description: Enable or disable password encryption on a D-Link DGS-1250 switch
description:
  - Configures the C(service password-encryption) CLI command on a D-Link DGS-1250 switch.
  - When enabled, passwords are stored encrypted in the configuration file.
  - Corresponds to CLI command described in chapter 5-12 of the DGS-1250 CLI Reference Guide.
version_added: "0.4.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  state:
    description:
      - C(enabled) to enable password encryption, C(disabled) to disable it.
    type: str
    choices: [enabled, disabled]
    default: enabled
  encryption:
    description:
      - Encryption type. C(7) for SHA-1, C(15) for MD5.
      - If omitted, uses the switch default.
    type: int
    choices: [7, 15]
"""

EXAMPLES = r"""
- name: Enable password encryption
  jaydee_io.dlink_dgs1250.mgmt_service_password_encryption:

- name: Enable password encryption with MD5
  jaydee_io.dlink_dgs1250.mgmt_service_password_encryption:
    encryption: 15

- name: Disable password encryption
  jaydee_io.dlink_dgs1250.mgmt_service_password_encryption:
    state: disabled
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


def _build_commands(state, encryption):
    if state == "disabled":
        return ["no service password-encryption"]
    enc = " %d" % encryption if encryption is not None else ""
    return ["service password-encryption%s" % enc]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type="str", choices=[
                       "enabled", "disabled"], default="enabled"),
            encryption=dict(type="int", choices=[7, 15]),
        ),
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["state"], module.params["encryption"])

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
