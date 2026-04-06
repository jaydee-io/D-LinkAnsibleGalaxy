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
