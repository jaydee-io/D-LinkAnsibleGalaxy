#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: crypto_key_generate
short_description: Generate RSA or DSA key pair on a D-Link DGS-1250 switch
description:
  - Executes the C(crypto key generate) CLI command on a D-Link DGS-1250 switch.
  - Generates the RSA or DSA key pair for SSH.
  - Corresponds to CLI command described in chapter 58-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.17.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  key_type:
    description:
      - The type of key pair to generate.
    type: str
    required: true
    choices: [rsa, dsa]
  modulus:
    description:
      - Number of bits in the modulus (RSA only). Valid values are 360, 512, 768, 1024, 2048.
    type: int
    choices: [360, 512, 768, 1024, 2048]
notes:
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Generate RSA key with 2048-bit modulus
  jaydee_io.dlink_dgs1250.crypto_key_generate:
    key_type: rsa
    modulus: 2048

- name: Generate DSA key
  jaydee_io.dlink_dgs1250.crypto_key_generate:
    key_type: dsa
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
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_PRIVILEGED


def _build_commands(key_type, modulus):
    cmd = "crypto key generate %s" % key_type
    if key_type == "rsa" and modulus is not None:
        cmd += " modulus %d" % modulus
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            key_type=dict(type="str", required=True, choices=["rsa", "dsa"]),
            modulus=dict(type="int", choices=[360, 512, 768, 1024, 2048]),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["key_type"], module.params["modulus"])
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
