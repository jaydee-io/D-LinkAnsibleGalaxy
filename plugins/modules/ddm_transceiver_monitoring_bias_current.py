#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: ddm_transceiver_monitoring_bias_current
short_description: Configure transceiver monitoring bias-current thresholds on a D-Link DGS-1250 switch
description:
  - Configures the C(transceiver-monitoring bias-current) CLI command on a D-Link DGS-1250 switch.
  - Sets or removes the bias current threshold for a specified SFP/SFP+ port.
  - Corresponds to CLI command described in chapter 21-4 of the DGS-1250 CLI Reference Guide.
version_added: "0.10.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - The interface to configure (e.g. C(eth1/0/25)).
    type: str
    required: true
  threshold_level:
    description:
      - C(high) or C(low) threshold level.
    type: str
    choices: [high, low]
    required: true
  threshold_type:
    description:
      - C(alarm) or C(warning) threshold type.
    type: str
    choices: [alarm, warning]
    required: true
  value:
    description:
      - The threshold value in mA (0 to 131).
      - Required when state is C(present).
    type: float
  state:
    description:
      - C(present) to set, C(absent) to remove.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set bias-current high warning threshold
  jaydee_io.dlink_dgs1250.ddm_transceiver_monitoring_bias_current:
    interface: eth1/0/25
    threshold_level: high
    threshold_type: warning
    value: 10.237

- name: Remove bias-current high warning threshold
  jaydee_io.dlink_dgs1250.ddm_transceiver_monitoring_bias_current:
    interface: eth1/0/25
    threshold_level: high
    threshold_type: warning
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
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(interface, threshold_level, threshold_type, value, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["no transceiver-monitoring bias-current %s %s %s" % (
            interface, threshold_level, threshold_type)]
    else:
        return ["transceiver-monitoring bias-current %s %s %s %s" % (
            interface, threshold_level, threshold_type, value)]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            threshold_level=dict(type="str", choices=[
                                 "high", "low"], required=True),
            threshold_type=dict(type="str", choices=[
                                "alarm", "warning"], required=True),
            value=dict(type="float"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["value"])],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["interface"],
        module.params["threshold_level"],
        module.params["threshold_type"],
        module.params["value"],
        module.params["state"],
    )
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
