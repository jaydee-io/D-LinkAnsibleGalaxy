#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: config_diff
short_description: Compare running-config vs startup-config on a D-Link DGS-1250 switch
description:
  - Retrieves the running configuration and startup configuration from a
    D-Link DGS-1250 switch and computes a unified diff between the two.
  - Returns C(changed=True) when configurations differ, C(changed=False) when
    they are identical.
  - Useful for verifying unsaved changes before a reboot or in a CI pipeline.
version_added: "1.5.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
notes:
  - This command runs in Privileged EXEC Mode.
  - The diff is computed on the Ansible controller, not on the switch.
"""

EXAMPLES = r"""
- name: Check for unsaved changes
  jaydee_io.dlink_dgs1250.config_diff:
  register: result

- name: Fail if there are unsaved changes
  ansible.builtin.fail:
    msg: "Unsaved changes detected on {{ inventory_hostname }}"
  when: result.changed

- name: Show diff
  ansible.builtin.debug:
    msg: "{{ result.diff }}"
  when: result.changed
"""

RETURN = r"""
diff:
  description: Unified diff between startup-config and running-config. Empty when identical.
  returned: always
  type: str
changed:
  description: Whether the running-config differs from the startup-config.
  returned: always
  type: bool
commands:
  description: List of CLI commands sent to the switch.
  returned: always
  type: list
  elements: str
"""

import difflib
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


def _build_commands():
    """Return the two CLI commands needed for the diff."""
    return ["show running-config", "show startup-config"]


def _compute_diff(running, startup):
    """Return a unified diff string between startup and running configs."""
    startup_lines = startup.splitlines(keepends=True)
    running_lines = running.splitlines(keepends=True)
    diff = difflib.unified_diff(
        startup_lines,
        running_lines,
        fromfile="startup-config",
        tofile="running-config",
    )
    return "".join(diff)


def main():
    module = AnsibleModule(
        argument_spec=dict(),
        supports_check_mode=True,
    )

    commands = _build_commands()

    if module.check_mode:
        module.exit_json(changed=False, commands=commands, diff="")
        return

    try:
        running = run_command(module, commands[0])
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    try:
        startup = run_command(module, commands[1])
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    diff_text = _compute_diff(running, startup)
    has_diff = len(diff_text) > 0

    module.exit_json(changed=has_diff, diff=diff_text, commands=commands)


if __name__ == "__main__":
    main()
