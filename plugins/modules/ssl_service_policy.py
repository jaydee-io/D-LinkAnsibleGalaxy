#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: ssl_service_policy
short_description: Configure an SSL service policy on a D-Link DGS-1250 switch
description:
  - Configures the C(ssl-service-policy) CLI command on a D-Link DGS-1250 switch.
  - Creates, configures, or removes an SSL service policy.
  - Corresponds to CLI command described in chapter 59-8 of the DGS-1250 CLI Reference Guide.
version_added: "0.17.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  name:
    description:
      - The SSL service policy name.
    type: str
    required: true
  version:
    description:
      - TLS version to configure.
    type: str
    choices: ["tls1.0", "tls1.1", "tls1.2"]
  ciphersuite:
    description:
      - Cipher suite to configure.
    type: str
    choices: [dhe-dss-3des-ede-cbc-sha, rsa-3des-ede-cbc-sha, rsa-rc4-128-sha,
              rsa-rc4-128-md5, rsa-export-rc4-40-md5, rsa-aes-128-cbc-sha,
              rsa-aes-256-cbc-sha, rsa-aes-128-cbc-sha256, rsa-aes-256-cbc-sha256,
              dhe-dss-aes-256-cbc-sha, dhe-rsa-aes-256-cbc-sha]
  secure_trustpoint:
    description:
      - Trust-point name to use in SSL handshake.
    type: str
  session_cache_timeout:
    description:
      - Session cache timeout in seconds (60-86400).
    type: int
  state:
    description:
      - C(present) to configure, C(absent) to remove.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Configure SSL policy with trustpoint
  jaydee_io.dlink_dgs1250.ssl_service_policy:
    name: ssl-server
    secure_trustpoint: TP1

- name: Remove SSL policy
  jaydee_io.dlink_dgs1250.ssl_service_policy:
    name: ssl-server
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
        run_commands, is_config_present, build_config_diff, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, is_config_present, build_config_diff, MODE_GLOBAL_CONFIG


def _build_commands(name, version, ciphersuite, secure_trustpoint, session_cache_timeout, state):
    prefix = "no " if state == "absent" else ""
    cmd = "%sssl-service-policy %s" % (prefix, name)
    parts = []
    if version:
        parts.append("version %s" % version)
    if ciphersuite:
        parts.append("ciphersuite %s" % ciphersuite)
    if secure_trustpoint:
        parts.append("secure-trustpoint %s" % secure_trustpoint)
    if session_cache_timeout is not None:
        parts.append("session-cache-timeout %d" % session_cache_timeout)
    if parts:
        cmd += " " + " ".join(parts)
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type="str", required=True),
            version=dict(type="str", choices=["tls1.0", "tls1.1", "tls1.2"]),
            ciphersuite=dict(type="str", choices=[
                "dhe-dss-3des-ede-cbc-sha", "rsa-3des-ede-cbc-sha", "rsa-rc4-128-sha",
                "rsa-rc4-128-md5", "rsa-export-rc4-40-md5", "rsa-aes-128-cbc-sha",
                "rsa-aes-256-cbc-sha", "rsa-aes-128-cbc-sha256", "rsa-aes-256-cbc-sha256",
                "dhe-dss-aes-256-cbc-sha", "dhe-rsa-aes-256-cbc-sha"]),
            secure_trustpoint=dict(type="str"),
            session_cache_timeout=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["name"], module.params["version"],
                               module.params["ciphersuite"], module.params["secure_trustpoint"],
                               module.params["session_cache_timeout"], module.params["state"])
    if is_config_present(module, commands):
        module.exit_json(changed=False, commands=[], raw_output="")
        return
    diff = build_config_diff(module, commands) if module._diff else None
    if module.check_mode:
        result = dict(changed=True, commands=commands, raw_output="")
        if diff:
            result['diff'] = diff
        module.exit_json(**result)
        return
    try:
        raw_output = run_commands(module, commands, mode=MODE_GLOBAL_CONFIG)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    result = dict(changed=True, raw_output=raw_output, commands=commands)
    if diff:
        result['diff'] = diff
    module.exit_json(**result)


if __name__ == "__main__":
    main()
