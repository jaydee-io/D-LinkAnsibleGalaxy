#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: environment_temperature_threshold
short_description: Configure environment temperature thresholds on a D-Link DGS-1250 switch
description:
  - Configures the C(environment temperature threshold thermal) command on a D-Link DGS-1250 switch.
  - Sets or resets high and low temperature thresholds for environment monitoring.
  - Corresponds to CLI command described in chapter 2-15 of the DGS-1250 CLI Reference Guide.
version_added: "0.1.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  state:
    description:
      - Whether to set (C(present)) or reset to default (C(absent)) the thresholds.
    type: str
    choices: [present, absent]
    default: present
  high:
    description:
      - High temperature threshold in Celsius.
      - Range is from -100 to 200.
      - Must be greater than C(low).
    type: int
  low:
    description:
      - Low temperature threshold in Celsius.
      - Range is from -100 to 200.
      - Must be smaller than C(high).
    type: int
notes:
  - This command requires Global Configuration Mode.
  - The low threshold must be smaller than the high threshold.
"""

EXAMPLES = r"""
- name: Set temperature thresholds
  jaydee_io.dlink_dgs1250.environment_temperature_threshold:
    high: 100
    low: 20

- name: Reset temperature thresholds to default
  jaydee_io.dlink_dgs1250.environment_temperature_threshold:
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


# ---------------------------------------------------------------------------
# Command builder
# ---------------------------------------------------------------------------

def _build_command(state, high, low):
    """Build the CLI command string."""
    if state == "absent":
        cmd = "no environment temperature threshold thermal"
        if high is not None:
            cmd += " high"
        if low is not None:
            cmd += " low"
        # If neither specified, reset both
        if high is None and low is None:
            cmd += " high low"
        return cmd

    cmd = "environment temperature threshold thermal"
    if high is not None:
        cmd += " high %d" % high
    if low is not None:
        cmd += " low %d" % low
    return cmd


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type="str", choices=["present", "absent"], default="present"),
            high=dict(type="int"),
            low=dict(type="int"),
        ),
        supports_check_mode=True,
    )

    state = module.params["state"]
    high = module.params["high"]
    low = module.params["low"]

    if state == "present" and high is None and low is None:
        module.fail_json(msg="At least one of 'high' or 'low' must be specified when state is 'present'.")

    if high is not None and (high < -100 or high > 200):
        module.fail_json(msg="'high' must be between -100 and 200.")

    if low is not None and (low < -100 or low > 200):
        module.fail_json(msg="'low' must be between -100 and 200.")

    if high is not None and low is not None and low >= high:
        module.fail_json(msg="'low' must be smaller than 'high'.")

    command = _build_command(state, high, low)
    commands = [command]

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
