"""
Common utilities for D-Link DGS-1250 Ansible modules.
Provides helpers for sending CLI commands via ansible.netcommon network_cli.
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import re

from ansible.module_utils.connection import Connection

# CLI mode constants
MODE_USER = "user"
MODE_PRIVILEGED = "privileged"
MODE_GLOBAL_CONFIG = "global_config"

# Mode hierarchy (lower index = less privileged)
_MODE_LEVELS = {
    MODE_USER: 0,
    MODE_PRIVILEGED: 1,
    MODE_GLOBAL_CONFIG: 2,
}

# Prompt patterns
_RE_CONFIG = re.compile(rb"\(config[^)]*\)#\s*$")
_RE_PRIVILEGED = re.compile(rb"[\w\-]+#\s*$")
_RE_USER = re.compile(rb"[\w\-]+>\s*$")


def get_connection(module):
    """Return a Connection object bound to the module's socket path."""
    return Connection(module._socket_path)


def _detect_mode(connection):
    """Detect the current CLI mode from the prompt."""
    prompt = connection.get_prompt()
    if isinstance(prompt, str):
        prompt = prompt.encode()
    if _RE_CONFIG.search(prompt):
        return MODE_GLOBAL_CONFIG
    if _RE_PRIVILEGED.search(prompt):
        return MODE_PRIVILEGED
    if _RE_USER.search(prompt):
        return MODE_USER
    return MODE_USER


def ensure_mode(connection, target_mode):
    """Transition to the target CLI mode if not already there."""
    current = _detect_mode(connection)
    current_level = _MODE_LEVELS[current]
    target_level = _MODE_LEVELS[target_mode]

    if current_level == target_level:
        return

    if current_level < target_level:
        # Escalate
        if current == MODE_USER:
            connection.get("enable")
            if target_mode == MODE_GLOBAL_CONFIG:
                connection.get("configure terminal")
        elif current == MODE_PRIVILEGED:
            connection.get("configure terminal")
    else:
        # De-escalate
        if current == MODE_GLOBAL_CONFIG:
            connection.get("end")
            if target_mode == MODE_USER:
                connection.get("disable")
        elif current == MODE_PRIVILEGED:
            connection.get("disable")


def run_command(module, command, mode=MODE_PRIVILEGED):
    """Send a single CLI command and return its output as a string."""
    connection = get_connection(module)
    ensure_mode(connection, mode)
    return connection.get(command)


def run_commands(module, commands, mode=MODE_PRIVILEGED):
    """Send multiple CLI commands and return their combined output."""
    connection = get_connection(module)
    ensure_mode(connection, mode)
    output = ""
    for cmd in commands:
        output += connection.get(cmd) + "\n"
    return output


def get_running_config(module):
    """Return the full running-config as a string."""
    connection = get_connection(module)
    ensure_mode(connection, MODE_PRIVILEGED)
    return connection.get("show running-config")


def get_running_config_section(module, regex_filter):
    """Return lines from running-config matching a regex filter.

    Uses 'show running-config' and filters lines locally.
    Returns a list of stripped, non-empty matching lines.
    """
    output = get_running_config(module)
    pattern = re.compile(regex_filter)
    return [line.strip() for line in output.splitlines()
            if line.strip() and pattern.search(line)]


_MODE_ENTRY_RE = re.compile(
    r"^(interface\s|line\s|router\s|spanning-tree mst configuration"
    r"|aaa server\s|ip dhcp pool\s|class-map\s|policy-map\s|ip access-list\s"
    r"|ipv6 access-list\s|mac access-list\s|vlan\s|time-range\s)",
    re.IGNORECASE,
)


def _config_commands(commands):
    """Extract the config-payload commands (skip mode-entry and exit lines)."""
    return [c for c in commands
            if c != "exit" and not _MODE_ENTRY_RE.match(c)]


# ---------------------------------------------------------------------------
# Range / list expansion helpers
# ---------------------------------------------------------------------------

def _parse_numeric_list(spec):
    """Expand '1-10' or '10,15-18' into a list of individual numbers."""
    if '-' not in spec and ',' not in spec:
        return None
    numbers = []
    for part in spec.split(','):
        part = part.strip()
        if '-' in part:
            bounds = part.split('-', 1)
            try:
                start, end = int(bounds[0]), int(bounds[1])
                if start > end:
                    return None
                numbers.extend(range(start, end + 1))
            except (ValueError, IndexError):
                return None
        else:
            try:
                numbers.append(int(part))
            except ValueError:
                return None
    return numbers


def _expand_interface_spec(spec):
    """Expand 'eth1/0/1-8' or 'eth1/0/1,eth1/0/5' into individual interfaces."""
    if ',' in spec:
        parts = [p.strip() for p in spec.split(',')]
        result = []
        for part in parts:
            sub = _expand_interface_spec(part)
            if sub:
                result.extend(sub)
            else:
                result.append(part)
        return result if len(result) > 1 else None

    m = re.match(r'^(eth\d+/\d+/)(\d+)-(\d+)$', spec)
    if m:
        prefix, start, end = m.group(1), int(m.group(2)), int(m.group(3))
        if start > end:
            return None
        return ['%s%d' % (prefix, i) for i in range(start, end + 1)]

    return None


_IFACE_SPEC_RE = re.compile(r'interface\s+(eth\S+)')
_VLAN_NUMERIC_RE = re.compile(r'(\d+(?:[-,]\d+)+)')


def _expand_command(cmd):
    """Expand a command containing interface/VLAN ranges or lists.

    Returns a list of individual commands, or [cmd] if no expansion needed.
    """
    m = _IFACE_SPEC_RE.search(cmd)
    if m:
        expanded = _expand_interface_spec(m.group(1))
        if expanded:
            before = cmd[:m.start(1)]
            after = cmd[m.end(1):]
            return ['%s%s%s' % (before, iface, after) for iface in expanded]

    if 'vlan' in cmd.lower():
        m = _VLAN_NUMERIC_RE.search(cmd)
        if m:
            numbers = _parse_numeric_list(m.group(1))
            if numbers:
                before = cmd[:m.start(1)]
                after = cmd[m.end(1):]
                return ['%s%d%s' % (before, n, after) for n in numbers]

    return [cmd]


# ---------------------------------------------------------------------------
# Idempotency and diff
# ---------------------------------------------------------------------------

def is_config_present(module, commands):
    """Check whether every config-payload command already appears in running-config.

    Handles interface ranges (eth1/0/1-8), interface lists (eth1/0/1,eth1/0/5),
    and VLAN ranges/lists (1-10, 10,15-18) by expanding them into individual
    commands when the exact form is not found in running-config.
    """
    config = get_running_config(module)
    module._running_config = config
    config_lines = set(line.strip() for line in config.splitlines())
    payload = _config_commands(commands)
    if not payload:
        return True
    if all(cmd in config_lines for cmd in payload):
        return True
    expanded = []
    for cmd in payload:
        expanded.extend(_expand_command(cmd))
    if expanded != payload:
        return all(cmd in config_lines for cmd in expanded)
    return False


def build_config_diff(module, commands):
    """Build a diff dict for ansible-playbook --diff mode.

    Returns {'before': str, 'after': str} showing config changes.
    Uses cached running-config from is_config_present when available.
    Expands ranges/lists so the diff reflects individual entries.
    """
    config = getattr(module, '_running_config', None)
    if config is None:
        config = get_running_config(module)

    config_lines = set(line.strip() for line in config.splitlines())
    payload = _config_commands(commands)

    expanded = []
    for cmd in payload:
        expanded.extend(_expand_command(cmd))

    before_lines = []
    after_lines = []

    for cmd in expanded:
        if cmd.startswith("no "):
            positive = cmd[3:]
            if positive in config_lines:
                before_lines.append(positive)
        else:
            if cmd not in config_lines:
                after_lines.append(cmd)

    return {
        'before': '\n'.join(before_lines) + '\n' if before_lines else '',
        'after': '\n'.join(after_lines) + '\n' if after_lines else '',
    }
