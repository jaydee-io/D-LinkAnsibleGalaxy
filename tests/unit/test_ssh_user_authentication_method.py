"""Unit tests for ssh_user_authentication_method module command builder."""

from ssh_user_authentication_method import _build_commands


def test_password():
    assert _build_commands("tom", "password", None, None, None, "present") == [
        "ssh user tom authentication-method password",
    ]


def test_publickey():
    assert _build_commands("tom", "publickey", "c:/user1.pub", None, None, "present") == [
        "ssh user tom authentication-method publickey c:/user1.pub",
    ]


def test_hostbased():
    assert _build_commands("tom", "hostbased", "c:/host.pub", "myhost", None, "present") == [
        "ssh user tom authentication-method hostbased c:/host.pub host-name myhost",
    ]


def test_hostbased_with_ip():
    assert _build_commands("tom", "hostbased", "c:/host.pub", "myhost", "10.0.0.1", "present") == [
        "ssh user tom authentication-method hostbased c:/host.pub host-name myhost 10.0.0.1",
    ]


def test_revert():
    assert _build_commands("tom", None, None, None, None, "absent") == [
        "no ssh user tom authentication-method",
    ]
