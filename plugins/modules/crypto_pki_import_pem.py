#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: crypto_pki_import_pem
short_description: Import PEM certificates and keys to a trust point on a D-Link DGS-1250 switch
description:
  - Executes the C(crypto pki import pem) CLI command on a D-Link DGS-1250 switch.
  - Imports CA certificate, local certificate and/or keys to a trust-point from PEM-formatted files.
  - Corresponds to CLI command described in chapter 59-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.17.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  trustpoint:
    description:
      - Name of the trust-point to import to.
    type: str
    required: true
  source:
    description:
      - Source path (e.g. C(flash:/cert) or C(tftp://10.1.1.2/certs/name)).
    type: str
    required: true
  password:
    description:
      - Encrypted password phrase for the private key import (max 64 chars).
    type: str
  import_type:
    description:
      - What to import.
    type: str
    required: true
    choices: [ca, local, both]
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Import CA and local certificates via TFTP
  jaydee_io.dlink_dgs1250.crypto_pki_import_pem:
    trustpoint: TP1
    source: "tftp://10.1.1.2/name/msca"
    password: abcd1234
    import_type: both

- name: Import CA certificate only
  jaydee_io.dlink_dgs1250.crypto_pki_import_pem:
    trustpoint: TP1
    source: "flash:/cert"
    import_type: ca
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


def _build_commands(trustpoint, source, password, import_type):
    cmd = "crypto pki import %s pem %s" % (trustpoint, source)
    if password:
        cmd += " password %s" % password
    cmd += " %s" % import_type
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            trustpoint=dict(type="str", required=True),
            source=dict(type="str", required=True),
            password=dict(type="str", no_log=True),
            import_type=dict(type="str", required=True,
                             choices=["ca", "local", "both"]),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["trustpoint"], module.params["source"],
                               module.params["password"], module.params["import_type"])
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
