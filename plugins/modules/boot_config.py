#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: boot_config
short_description: Configure boot configuration file on a D-Link DGS-1250 switch
description:
  - Configures the C(boot config) CLI command on a D-Link DGS-1250 switch.
  - Specifies the configuration file to use for the next boot.
  - Corresponds to CLI command described in chapter 65-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.18.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  config:
    description:
      - The configuration file to use.
    type: str
    required: true
    choices: [Config1, Config2]
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set boot config to Config2
  jaydee_io.dlink_dgs1250.boot_config:
    config: Config2
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


def _build_commands(config):
    return ["boot config %s" % config]




def main():
    module = AnsibleModule(
        argument_spec=dict(
            config=dict(type="str", required=True, choices=["Config1", "Config2"]),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["config"])
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
