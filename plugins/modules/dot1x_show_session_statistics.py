#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: dot1x_show_session_statistics
short_description: Display 802.1X session statistics on a D-Link DGS-1250 switch
description:
  - Executes the C(show dot1x session-statistics) CLI command on a D-Link DGS-1250 switch.
  - Returns session counters for all or specific interfaces.
  - Corresponds to CLI command described in chapter 3-15 of the DGS-1250 CLI Reference Guide.
version_added: "0.2.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Physical port interface to query (e.g. C(eth1/0/1)).
      - If omitted, session statistics for all interfaces are returned.
    type: str
notes:
"""

EXAMPLES = r"""
- name: Get 802.1X session statistics on port 1
  jaydee_io.dlink_dgs1250.dot1x_show_session_statistics:
    interface: eth1/0/1
  register: session

- name: Get 802.1X session statistics on all ports
  jaydee_io.dlink_dgs1250.dot1x_show_session_statistics:
  register: session_all
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
session_statistics:
  description: List of session statistics per interface.
  returned: success
  type: list
  elements: dict
  contains:
    interface:
      description: Interface name.
      type: str
      sample: "eth1/0/1"
    session_octets_rx:
      description: Session octets received.
      type: int
    session_octets_tx:
      description: Session octets transmitted.
      type: int
    session_frames_rx:
      description: Session frames received.
      type: int
    session_frames_tx:
      description: Session frames transmitted.
      type: int
    session_id:
      description: Session identifier.
      type: str
    session_authentication_method:
      description: Authentication method used.
      type: str
      sample: "Remote Authentication Server"
    session_time:
      description: Session time in seconds.
      type: int
    session_terminate_cause:
      description: Cause of session termination.
      type: str
      sample: "SupplicantLogoff"
    session_user_name:
      description: Session user name.
      type: str
"""

import re
from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import run_command
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


# ---------------------------------------------------------------------------
# Output parser
# ---------------------------------------------------------------------------

FIELD_MAP = {
    "SessionOctetsRX": ("session_octets_rx", int),
    "SessionOctetsTX": ("session_octets_tx", int),
    "SessionFramesRX": ("session_frames_rx", int),
    "SessionFramesTX": ("session_frames_tx", int),
    "SessionId": ("session_id", str),
    "SessionAuthenticationMethod": ("session_authentication_method", str),
    "SessionTime": ("session_time", int),
    "SessionTerminateCause": ("session_terminate_cause", str),
    "SessionUserName": ("session_user_name", str),
}


def _new_entry():
    """Return a fresh session statistics dict with default values."""
    result = {}
    for field_name, converter in FIELD_MAP.values():
        result[field_name] = 0 if converter is int else ""
    return result


def _parse_session_statistics(output):
    """
    Parse show dot1x session-statistics output.

    Handles single or multiple interface blocks. Each block starts with:
        Eth1/0/1 session statistic counters are following:
    """
    results = []
    current = None

    for line in output.splitlines():
        header = re.match(r"^\s*[Ee]th(\S+)\s+session statistic counters", line)
        if header:
            current = _new_entry()
            current["interface"] = "eth" + header.group(1)
            results.append(current)
            continue

        if current is None:
            continue

        m = re.match(r"^\s*(.+?)\s*:\s*(.*?)\s*$", line)
        if m:
            key = m.group(1).strip()
            value = m.group(2).strip()
            if key in FIELD_MAP:
                field_name, converter = FIELD_MAP[key]
                if converter is int:
                    current[field_name] = int(value) if value else 0
                else:
                    current[field_name] = value

    return results


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str"),
        ),
        supports_check_mode=True,
    )

    interface = module.params["interface"]

    command = "show dot1x session-statistics"
    if interface:
        command += " interface %s" % interface

    try:
        raw_output = run_command(module, command)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    result = dict(changed=False, raw_output=raw_output)
    result["session_statistics"] = _parse_session_statistics(raw_output)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
