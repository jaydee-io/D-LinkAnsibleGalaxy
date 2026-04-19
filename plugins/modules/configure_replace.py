#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: configure_replace
short_description: Replace running configuration on a D-Link DGS-1250 switch
description:
  - Executes the C(configure replace) CLI command on a D-Link DGS-1250 switch.
  - Replaces the current running configuration with the specified configuration file.
  - Corresponds to CLI command described in chapter 65-5 of the DGS-1250 CLI Reference Guide.
version_added: "0.18.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  source:
    description:
      - The source type of the configuration file.
    type: str
    required: true
    choices: [tftp, flash]
  location:
    description:
      - The TFTP URL (e.g. C(//10.0.0.66/config.cfg)). Required when C(source=tftp).
    type: str
  config:
    description:
      - The flash config file. Required when C(source=flash).
    type: str
    choices: [Config1, Config2]
  force:
    description:
      - Execute immediately with no confirmation.
    type: bool
    default: false
notes:
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Replace config from TFTP
  jaydee_io.dlink_dgs1250.configure_replace:
    source: tftp
    location: "//10.0.0.66/config.cfg"

- name: Replace config from flash
  jaydee_io.dlink_dgs1250.configure_replace:
    source: flash
    config: Config1
    force: true
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
        run_commands, MODE_PRIVILEGED,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_PRIVILEGED


def _build_commands(source, location, config, force):
    if source == "tftp":
        cmd = "configure replace tftp: %s" % location
    else:
        cmd = "configure replace flash: %s" % config
    if force:
        cmd += " force"
    return [cmd]




def main():
    module = AnsibleModule(
        argument_spec=dict(
            source=dict(type="str", required=True, choices=["tftp", "flash"]),
            location=dict(type="str"),
            config=dict(type="str", choices=["Config1", "Config2"]),
            force=dict(type="bool", default=False),
        ),
        required_if=[("source", "tftp", ["location"]), ("source", "flash", ["config"])],
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["source"], module.params["location"], module.params["config"], module.params["force"])
    if module.check_mode:
        module.exit_json(changed=True, commands=commands, raw_output="")
        return
    try:
        raw_output = run_commands(module, commands, mode=MODE_PRIVILEGED)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    module.exit_json(changed=True, raw_output=raw_output, commands=commands)


if __name__ == "__main__":
    main()
