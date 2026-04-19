#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: acl_show_access_list
short_description: Display access list configuration on a D-Link DGS-1250 switch
description:
  - Executes the C(show access-list) CLI command on a D-Link DGS-1250 switch.
  - Returns configured access lists and their rules.
  - Can filter by type (ip, mac, ipv6, arp) and by name or number.
  - Corresponds to CLI command described in chapter 4-15 of the DGS-1250 CLI Reference Guide.
version_added: "0.3.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  acl_type:
    description:
      - Type of access list to display.
      - If omitted, a summary of all access lists is displayed.
    type: str
    choices: [ip, mac, ipv6, arp]
  name:
    description:
      - Name or number of a specific access list to display.
      - Only used when C(acl_type) is specified.
    type: str
"""

EXAMPLES = r"""
- name: Show summary of all access lists
  jaydee_io.dlink_dgs1250.acl_show_access_list:
  register: result

- name: Show IP access list 'Strict-Control'
  jaydee_io.dlink_dgs1250.acl_show_access_list:
    acl_type: ip
    name: Strict-Control
  register: result

- name: Show all MAC access lists
  jaydee_io.dlink_dgs1250.acl_show_access_list:
    acl_type: mac
  register: result
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
access_lists:
  description: >
    List of access lists parsed from the output.
    When no acl_type is specified, each entry has name and type fields (summary mode).
    When acl_type is specified, each entry has name, type, and a list of rules.
  returned: success
  type: list
  elements: dict
  contains:
    name:
      description: Access list name with ID.
      type: str
    type:
      description: Access list type (e.g. 'ip ext-acl', 'mac ext-acl').
      type: str
    rules:
      description: List of rule strings (only when acl_type is specified).
      type: list
      elements: str
"""

import re
from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import run_command
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


def _parse_summary(output):
    """
    Parse summary output (no acl_type specified).

    Expected format:
        Access-List-Name                                           Type
        -------------------------------------------              ---------------
        Strict-Control(ID: 3999)                                 ip ext-acl
        daily-profile(ID: 7999)                                  mac ext-acl
    """
    results = []
    for line in output.splitlines():
        if line.startswith("---") or line.startswith("Access-List-Name") or line.startswith("Total"):
            continue
        m = re.match(r"^\s*(\S+.*?\(ID:\s*\d+\))\s{2,}(\S.*?)\s*$", line)
        if m:
            results.append({"name": m.group(1).strip(), "type": m.group(2).strip()})
    return results


def _parse_detailed(output):
    """
    Parse detailed output (acl_type specified).

    Expected format:
        Extended IP access list Strict-Control(ID: 3999)
            10 permit any 10.20.0.0 0.0.255.255
            20 permit any host 10.100.1.2
    """
    results = []
    current = None

    for line in output.splitlines():
        header = re.match(r"^\s*(Extended\s+|Standard\s+)?(\S+)\s+access(?:\s+list)?\s+(.+)", line, re.IGNORECASE)
        if header:
            ext = (header.group(1) or "").strip().lower()
            acl_kind = header.group(2).strip().lower()
            acl_name = header.group(3).strip()
            acl_type = "%s %s" % (acl_kind, "ext-acl" if ext == "extended" else "std-acl") if ext else acl_kind
            current = {"name": acl_name, "type": acl_type, "rules": []}
            results.append(current)
            continue

        if current is not None:
            rule_match = re.match(r"^\s+(\d+\s+(?:permit|deny)\s+.+)", line)
            if rule_match:
                current["rules"].append(rule_match.group(1).strip())

    return results


def main():
    module = AnsibleModule(
        argument_spec=dict(
            acl_type=dict(type="str", choices=["ip", "mac", "ipv6", "arp"]),
            name=dict(type="str"),
        ),
        supports_check_mode=True,
    )

    acl_type = module.params["acl_type"]
    name = module.params["name"]

    command = "show access-list"
    if acl_type:
        command += " %s" % acl_type
        if name:
            command += " %s" % name

    try:
        raw_output = run_command(module, command)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    result = dict(changed=False, raw_output=raw_output)
    if acl_type:
        result["access_lists"] = _parse_detailed(raw_output)
    else:
        result["access_lists"] = _parse_summary(raw_output)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
