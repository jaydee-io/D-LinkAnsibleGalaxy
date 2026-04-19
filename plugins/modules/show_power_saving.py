#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: show_power_saving
short_description: Display power saving configuration on a D-Link DGS-1250 switch
description:
  - Executes the C(show power-saving) CLI command on a D-Link DGS-1250 switch.
  - Displays power saving configuration information.
  - Corresponds to CLI command described in chapter 52-7 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  features:
    description:
      - Optional list of features to display
        (C(link-detection), C(length-detection), C(dim-led), C(port-shutdown), C(hibernation), C(eee)).
        If omitted, all information is shown.
    type: list
    elements: str
    choices: [link-detection, length-detection, dim-led, port-shutdown, hibernation, eee]
notes:
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Show all power saving information
  jaydee_io.dlink_dgs1250.show_power_saving:
  register: result

- name: Show only link detection and EEE
  jaydee_io.dlink_dgs1250.show_power_saving:
    features:
      - link-detection
      - eee
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
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


def _build_command(features):
    cmd = "show power-saving"
    if features:
        for f in features:
            cmd += " %s" % f
    return cmd


def main():
    module = AnsibleModule(
        argument_spec=dict(
            features=dict(type="list", elements="str",
                          choices=["link-detection", "length-detection", "dim-led",
                                   "port-shutdown", "hibernation", "eee"]),
        ),
        supports_check_mode=True,
    )
    command = _build_command(module.params["features"])
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
