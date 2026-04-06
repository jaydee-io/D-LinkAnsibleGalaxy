"""Unit tests for module_utils/dgs1250.py mode detection and transitions."""

from unittest.mock import MagicMock

from dgs1250 import (
    _detect_mode,
    ensure_mode,
    MODE_USER,
    MODE_PRIVILEGED,
    MODE_GLOBAL_CONFIG,
)


def _mock_connection(prompt_bytes):
    """Return a mock Connection whose get_prompt returns prompt_bytes."""
    conn = MagicMock()
    conn.get_prompt.return_value = prompt_bytes
    return conn


# ---- _detect_mode ----------------------------------------------------------

def test_detect_user_mode():
    assert _detect_mode(_mock_connection(b"Switch>")) == MODE_USER


def test_detect_user_mode_with_space():
    assert _detect_mode(_mock_connection(b"Switch> ")) == MODE_USER


def test_detect_privileged_mode():
    assert _detect_mode(_mock_connection(b"Switch#")) == MODE_PRIVILEGED


def test_detect_privileged_mode_with_space():
    assert _detect_mode(_mock_connection(b"Switch# ")) == MODE_PRIVILEGED


def test_detect_global_config_mode():
    assert _detect_mode(_mock_connection(b"Switch(config)#")) == MODE_GLOBAL_CONFIG


def test_detect_config_if_mode():
    assert _detect_mode(_mock_connection(b"Switch(config-if)#")) == MODE_GLOBAL_CONFIG


def test_detect_config_line_mode():
    assert _detect_mode(_mock_connection(b"Switch(config-line)#")) == MODE_GLOBAL_CONFIG


def test_detect_config_vlan_mode():
    assert _detect_mode(_mock_connection(b"Switch(config-vlan)#")) == MODE_GLOBAL_CONFIG


def test_detect_config_with_trailing_space():
    assert _detect_mode(_mock_connection(b"Switch(config)# ")) == MODE_GLOBAL_CONFIG


def test_detect_custom_hostname():
    assert _detect_mode(_mock_connection(b"MySwitch-01#")) == MODE_PRIVILEGED


def test_detect_custom_hostname_user():
    assert _detect_mode(_mock_connection(b"MySwitch-01>")) == MODE_USER


# ---- ensure_mode: no-op when already in target mode ------------------------

def test_ensure_mode_noop_user():
    conn = _mock_connection(b"Switch>")
    ensure_mode(conn, MODE_USER)
    conn.get.assert_not_called()


def test_ensure_mode_noop_privileged():
    conn = _mock_connection(b"Switch#")
    ensure_mode(conn, MODE_PRIVILEGED)
    conn.get.assert_not_called()


def test_ensure_mode_noop_global_config():
    conn = _mock_connection(b"Switch(config)#")
    ensure_mode(conn, MODE_GLOBAL_CONFIG)
    conn.get.assert_not_called()


# ---- ensure_mode: escalation -----------------------------------------------

def test_escalate_user_to_privileged():
    conn = _mock_connection(b"Switch>")
    ensure_mode(conn, MODE_PRIVILEGED)
    conn.get.assert_called_once_with("enable")


def test_escalate_user_to_global_config():
    conn = _mock_connection(b"Switch>")
    ensure_mode(conn, MODE_GLOBAL_CONFIG)
    assert conn.get.call_count == 2
    conn.get.assert_any_call("enable")
    conn.get.assert_any_call("configure terminal")


def test_escalate_privileged_to_global_config():
    conn = _mock_connection(b"Switch#")
    ensure_mode(conn, MODE_GLOBAL_CONFIG)
    conn.get.assert_called_once_with("configure terminal")


# ---- ensure_mode: de-escalation --------------------------------------------

def test_deescalate_global_config_to_privileged():
    conn = _mock_connection(b"Switch(config)#")
    ensure_mode(conn, MODE_PRIVILEGED)
    conn.get.assert_called_once_with("end")


def test_deescalate_global_config_to_user():
    conn = _mock_connection(b"Switch(config)#")
    ensure_mode(conn, MODE_USER)
    assert conn.get.call_count == 2
    conn.get.assert_any_call("end")
    conn.get.assert_any_call("disable")


def test_deescalate_privileged_to_user():
    conn = _mock_connection(b"Switch#")
    ensure_mode(conn, MODE_USER)
    conn.get.assert_called_once_with("disable")


def test_deescalate_config_if_to_privileged():
    conn = _mock_connection(b"Switch(config-if)#")
    ensure_mode(conn, MODE_PRIVILEGED)
    conn.get.assert_called_once_with("end")
