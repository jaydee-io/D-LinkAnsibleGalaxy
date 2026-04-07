#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: dot1x_show_statistics
short_description: Display 802.1X statistics on a D-Link DGS-1250 switch
description:
  - Executes the C(show dot1x statistics) CLI command on a D-Link DGS-1250 switch.
  - Returns EAPOL frame counters for all or specific interfaces.
  - Corresponds to CLI command described in chapter 3-14 of the DGS-1250 CLI Reference Guide.
version_added: "0.2.0"
author:
  - Jérôme Dumesnil
options:
  interface:
    description:
      - Physical port interface to query (e.g. C(eth1/0/1)).
      - If omitted, statistics for all interfaces are returned.
    type: str
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
"""

EXAMPLES = r"""
- name: Get 802.1X statistics on port 1
  jaydee_io.dlink_dgs1250.dot1x_show_statistics:
    interface: eth1/0/1
  register: stats

- name: Get 802.1X statistics on all ports
  jaydee_io.dlink_dgs1250.dot1x_show_statistics:
  register: stats_all
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
statistics:
  description: List of statistics per interface.
  returned: success
  type: list
  elements: dict
  contains:
    interface:
      description: Interface name.
      type: str
      sample: "eth1/0/1"
    eapol_frames_rx:
      description: EAPOL frames received.
      type: int
    eapol_frames_tx:
      description: EAPOL frames transmitted.
      type: int
    eapol_start_frames_rx:
      description: EAPOL-Start frames received.
      type: int
    eapol_req_id_frames_tx:
      description: EAPOL-Req/Id frames transmitted.
      type: int
    eapol_logoff_frames_rx:
      description: EAPOL-Logoff frames received.
      type: int
    eapol_req_frames_tx:
      description: EAPOL-Req frames transmitted.
      type: int
    eapol_resp_id_frames_rx:
      description: EAPOL-Resp/Id frames received.
      type: int
    eapol_resp_frames_rx:
      description: EAPOL-Resp frames received.
      type: int
    invalid_eapol_frames_rx:
      description: Invalid EAPOL frames received.
      type: int
    eap_length_error_frames_rx:
      description: EAP-Length error frames received.
      type: int
    last_eapol_frame_version:
      description: Last EAPOL frame version.
      type: int
    last_eapol_frame_source:
      description: Last EAPOL frame source MAC address.
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
    "EAPOL Frames RX": ("eapol_frames_rx", int),
    "EAPOL Frames TX": ("eapol_frames_tx", int),
    "EAPOL-Start Frames RX": ("eapol_start_frames_rx", int),
    "EAPOL-Req/Id Frames TX": ("eapol_req_id_frames_tx", int),
    "EAPOL-Logoff Frames RX": ("eapol_logoff_frames_rx", int),
    "EAPOL-Req Frames TX": ("eapol_req_frames_tx", int),
    "EAPOL-Resp/Id Frames RX": ("eapol_resp_id_frames_rx", int),
    "EAPOL-Resp Frames RX": ("eapol_resp_frames_rx", int),
    "Invalid EAPOL Frames RX": ("invalid_eapol_frames_rx", int),
    "EAP-Length Error Frames RX": ("eap_length_error_frames_rx", int),
    "Last EAPOL Frame Version": ("last_eapol_frame_version", int),
    "Last EAPOL Frame Source": ("last_eapol_frame_source", str),
}


def _new_entry():
    """Return a fresh statistics dict with default values."""
    result = {}
    for field_name, converter in FIELD_MAP.values():
        result[field_name] = 0 if converter is int else ""
    return result


def _parse_statistics(output):
    """
    Parse show dot1x statistics output.

    Handles single or multiple interface blocks. Each block starts with:
        eth1/0/1 dot1x statistics information:
    """
    results = []
    current = None

    for line in output.splitlines():
        header = re.match(r"^\s*(eth\S+)\s+dot1x statistics information", line)
        if header:
            current = _new_entry()
            current["interface"] = header.group(1)
            results.append(current)
            continue

        if current is None:
            continue

        m = re.match(r"^\s*(.+?)\s*:\s*(.+?)\s*$", line)
        if m:
            key = m.group(1).strip()
            value = m.group(2).strip()
            if key in FIELD_MAP:
                field_name, converter = FIELD_MAP[key]
                current[field_name] = converter(value)

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

    command = "show dot1x statistics"
    if interface:
        command += " interface %s" % interface

    try:
        raw_output = run_command(module, command)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    result = dict(changed=False, raw_output=raw_output)
    result["statistics"] = _parse_statistics(raw_output)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
