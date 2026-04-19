#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dir
short_description: Display file system directory on a D-Link DGS-1250 switch
description:
  - Executes the C(dir) CLI command to display files or directory listing on the switch.
  - Corresponds to CLI command described in chapter 27-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.11.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  url:
    description:
      - Optional file or directory name to display.
      - If not specified, the current directory is listed.
    type: str
notes:
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Display root directory listing
  jaydee_io.dlink_dgs1250.dir:
  register: result

- name: Display specific file information
  jaydee_io.dlink_dgs1250.dir:
    url: Image1
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


def _build_command(url):
    if url:
        return "dir %s" % url
    return "dir"


def main():
    module = AnsibleModule(
        argument_spec=dict(
            url=dict(type="str"),
        ),
        supports_check_mode=True,
    )
    command = _build_command(module.params["url"])
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
