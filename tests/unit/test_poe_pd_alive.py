"""Unit tests for poe_pd_alive module command builder."""

from poe_pd_alive import _build_commands


def test_enable():
    assert _build_commands("eth1/0/1", None, None, None, None, None, "enabled") == [
        "interface eth1/0/1",
        "poe pd alive",
        "exit",
    ]


def test_set_ip():
    assert _build_commands("eth1/0/2", "192.168.1.150", None, None, None, None, "enabled") == [
        "interface eth1/0/2",
        "poe pd alive ip 192.168.1.150",
        "exit",
    ]


def test_set_interval():
    assert _build_commands("eth1/0/2", None, 60, None, None, None, "enabled") == [
        "interface eth1/0/2",
        "poe pd alive interval 60",
        "exit",
    ]


def test_set_retry():
    assert _build_commands("eth1/0/2", None, None, 4, None, None, "enabled") == [
        "interface eth1/0/2",
        "poe pd alive retry 4",
        "exit",
    ]


def test_set_waiting_time():
    assert _build_commands("eth1/0/2", None, None, None, 120, None, "enabled") == [
        "interface eth1/0/2",
        "poe pd alive waiting-time 120",
        "exit",
    ]


def test_set_action():
    assert _build_commands("eth1/0/2", None, None, None, None, "reset", "enabled") == [
        "interface eth1/0/2",
        "poe pd alive action reset",
        "exit",
    ]


def test_disable():
    assert _build_commands("eth1/0/1", None, None, None, None, None, "disabled") == [
        "interface eth1/0/1",
        "no poe pd alive",
        "exit",
    ]


def test_disable_ip():
    assert _build_commands("eth1/0/2", "192.168.1.150", None, None, None, None, "disabled") == [
        "interface eth1/0/2",
        "no poe pd alive ip",
        "exit",
    ]
