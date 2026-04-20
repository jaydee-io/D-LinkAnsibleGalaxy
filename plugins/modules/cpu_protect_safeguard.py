#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: cpu_protect_safeguard
short_description: Enable or configure the Safeguard Engine on a D-Link DGS-1250 switch
description:
  - Configures the C(cpu-protect safeguard) CLI command on a D-Link DGS-1250 switch.
  - Enables or disables the Safeguard Engine and optionally sets thresholds.
  - Corresponds to CLI command described in chapter 57-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.17.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  rising_threshold:
    description:
      - Rising CPU utilization threshold (20-100). Required together with C(falling_threshold).
    type: int
  falling_threshold:
    description:
      - Falling CPU utilization threshold (20-100). Required together with C(rising_threshold).
    type: int
  state:
    description:
      - C(enabled) to enable the Safeguard Engine, C(disabled) to disable it.
        C(threshold_absent) to revert thresholds to defaults.
    type: str
    choices: [enabled, disabled, threshold_absent]
    default: enabled
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable safeguard engine with thresholds
  jaydee_io.dlink_dgs1250.cpu_protect_safeguard:
    rising_threshold: 60
    falling_threshold: 40

- name: Enable safeguard engine with defaults
  jaydee_io.dlink_dgs1250.cpu_protect_safeguard:

- name: Disable safeguard engine
  jaydee_io.dlink_dgs1250.cpu_protect_safeguard:
    state: disabled

- name: Revert thresholds to defaults
  jaydee_io.dlink_dgs1250.cpu_protect_safeguard:
    state: threshold_absent
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


def _build_commands(rising_threshold, falling_threshold, state):
    if state == "disabled":
        return ["no cpu-protect safeguard"]
    if state == "threshold_absent":
        return ["no cpu-protect safeguard threshold"]
    cmd = "cpu-protect safeguard"
    if rising_threshold is not None and falling_threshold is not None:
        cmd += " threshold %d %d" % (rising_threshold, falling_threshold)
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            rising_threshold=dict(type="int"),
            falling_threshold=dict(type="int"),
            state=dict(type="str", choices=[
                       "enabled", "disabled", "threshold_absent"], default="enabled"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["rising_threshold"], module.params["falling_threshold"], module.params["state"])
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
