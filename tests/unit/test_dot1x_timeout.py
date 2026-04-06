"""Unit tests for dot1x_timeout module command builder."""

from dot1x_timeout import _build_commands


def test_set_all_timers():
    cmds = _build_commands("eth1/0/1", "present", 15, 15, 10)
    assert cmds == [
        "interface eth1/0/1",
        "dot1x timeout server-timeout 15",
        "dot1x timeout supp-timeout 15",
        "dot1x timeout tx-period 10",
    ]


def test_set_server_timeout_only():
    cmds = _build_commands("eth1/0/1", "present", 20, None, None)
    assert cmds == ["interface eth1/0/1", "dot1x timeout server-timeout 20"]


def test_set_tx_period_only():
    cmds = _build_commands("eth1/0/1", "present", None, None, 5)
    assert cmds == ["interface eth1/0/1", "dot1x timeout tx-period 5"]


def test_reset_all_timers():
    cmds = _build_commands("eth1/0/1", "absent", None, None, None)
    assert cmds == [
        "interface eth1/0/1",
        "no dot1x timeout server-timeout",
        "no dot1x timeout supp-timeout",
        "no dot1x timeout tx-period",
    ]


def test_reset_specific_timer():
    cmds = _build_commands("eth1/0/1", "absent", None, 1, None)
    assert cmds == ["interface eth1/0/1", "no dot1x timeout supp-timeout"]


def test_reset_two_timers():
    cmds = _build_commands("eth1/0/1", "absent", 1, None, 1)
    assert cmds == [
        "interface eth1/0/1",
        "no dot1x timeout server-timeout",
        "no dot1x timeout tx-period",
    ]
