"""
Common utilities for D-Link DGS-1250 Ansible modules.
SSH connection and command execution via Paramiko.
"""

import re
import socket
import time

try:
    import paramiko
    HAS_PARAMIKO = True
except ImportError:
    HAS_PARAMIKO = False


class DGS1250Connection:
    """SSH connection handler for D-Link DGS-1250 switches."""

    def __init__(self, host, username, password, port=22, timeout=30):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout
        self._client = None
        self._shell = None

    def connect(self):
        if not HAS_PARAMIKO:
            raise ImportError("paramiko is required: pip install paramiko")

        self._client = paramiko.SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._client.connect(
            hostname=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            timeout=self.timeout,
            look_for_keys=False,
            allow_agent=False,
        )
        self._shell = self._client.invoke_shell(width=200, height=200)
        self._read_until_prompt(timeout=10)

    def _read_until_prompt(self, timeout=10):
        """Read output until a Switch prompt is detected."""
        output = ""
        deadline = time.time() + timeout
        while time.time() < deadline:
            if self._shell.recv_ready():
                chunk = self._shell.recv(4096).decode("utf-8", errors="replace")
                output += chunk
                # DGS-1250 prompt ends with '#' or '>'
                if re.search(r"Switch[^#>]*[#>]\s*$", output):
                    break
            else:
                time.sleep(0.1)
        return output

    def send_command(self, command):
        """Send a command and return the output (without the command echo and prompt)."""
        self._shell.send(command + "\n")
        time.sleep(0.3)
        raw = self._read_until_prompt()

        # Strip the echoed command and trailing prompt line
        lines = raw.splitlines()
        # Remove first line (command echo) and last line (prompt)
        if lines and command.strip() in lines[0]:
            lines = lines[1:]
        if lines and re.search(r"Switch[^#>]*[#>]\s*$", lines[-1]):
            lines = lines[:-1]
        return "\n".join(lines).strip()

    def disconnect(self):
        if self._client:
            self._client.close()
            self._client = None
            self._shell = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


# ---------------------------------------------------------------------------
# Shared Ansible module helpers
# ---------------------------------------------------------------------------

CONNECTION_ARGSPEC = dict(
    host=dict(type="str", required=True),
    username=dict(type="str", required=True),
    password=dict(type="str", required=True, no_log=True),
    port=dict(type="int", default=22),
    timeout=dict(type="int", default=30),
)


def connection_from_params(params):
    """Create a DGS1250Connection from Ansible module params."""
    return DGS1250Connection(
        host=params["host"],
        username=params["username"],
        password=params["password"],
        port=params["port"],
        timeout=params["timeout"],
    )
