"""Unit tests for crypto_pki_import_pem module command builder."""

from crypto_pki_import_pem import _build_commands


def test_import_both_with_password():
    assert _build_commands("TP1", "tftp://10.1.1.2/name/msca", "abcd1234", "both") == [
        "crypto pki import TP1 pem tftp://10.1.1.2/name/msca password abcd1234 both",
    ]


def test_import_ca_only():
    assert _build_commands("TP1", "flash:/cert", None, "ca") == [
        "crypto pki import TP1 pem flash:/cert ca",
    ]
