"""Unit tests for mgmt_show_users module parser."""

from mgmt_show_users import _parse_users


def test_single_user():
    output = """\
ID   Type     User-Name  Login-Time           IP
----+--------+----------+--------------------+-----------------
1    console  admin      2024-01-15 10:30:00  0.0.0.0
"""
    users = _parse_users(output)
    assert len(users) == 1
    assert users[0]["id"] == 1
    assert users[0]["type"] == "console"
    assert users[0]["user_name"] == "admin"
    assert users[0]["login_time"] == "2024-01-15 10:30:00"
    assert users[0]["ip"] == "0.0.0.0"


def test_multiple_users():
    output = """\
ID   Type     User-Name  Login-Time           IP
----+--------+----------+--------------------+-----------------
1    console  admin      2024-01-15 10:30:00  0.0.0.0
2    telnet   operator   2024-01-15 11:00:00  192.168.1.100
3    ssh      monitor    2024-01-15 12:15:00  10.0.0.5
"""
    users = _parse_users(output)
    assert len(users) == 3
    assert users[1]["id"] == 2
    assert users[1]["type"] == "telnet"
    assert users[1]["user_name"] == "operator"
    assert users[1]["ip"] == "192.168.1.100"
    assert users[2]["type"] == "ssh"


def test_empty():
    assert _parse_users("") == []


def test_header_only():
    output = """\
ID   Type     User-Name  Login-Time           IP
----+--------+----------+--------------------+-----------------
"""
    assert _parse_users(output) == []
