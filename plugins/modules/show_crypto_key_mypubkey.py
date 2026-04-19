#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: show_crypto_key_mypubkey
short_description: Display RSA or DSA public key on a D-Link DGS-1250 switch
description:
  - Executes the C(show crypto key mypubkey) CLI command on a D-Link DGS-1250 switch.
  - Displays the RSA or DSA public key pairs.
  - Corresponds to CLI command described in chapter 58-6 of the DGS-1250 CLI Reference Guide.
version_added: "0.17.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  key_type:
    description:
      - The type of key to display.
    type: str
    required: true
    choices: [rsa, dsa]
notes:
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Show RSA public key
  jaydee_io.dlink_dgs1250.show_crypto_key_mypubkey:
    key_type: rsa
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
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


def _build_command(key_type):
    return "show crypto key mypubkey %s" % key_type



def main():
    module = AnsibleModule(
        argument_spec=dict(
            key_type=dict(type="str", required=True, choices=["rsa", "dsa"]),
        ),
        supports_check_mode=True,
    )
    command = _build_command(module.params["key_type"])
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
